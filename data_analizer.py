"""
Data Analizer for PoMiASI Project
---------------------------------
Analyzes HTTP request/response logs exported to CSV.

Features:
- Calculates total and average load times.
- Plots download times of individual objects.
- Visualizes concurrency over time.
- Detects time gaps within single TCP connections.
- Generates a Gantt chart for file downloads.
- Exports all visualizations into a single PDF report.

Usage:
    python data_analizer.py C:\path\to\output.csv
"""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader


def analyze(csv_path: str):
    # --- Paths and preparation ---
    out_dir = os.path.join(os.path.dirname(csv_path), "wyniki_analizy")
    os.makedirs(out_dir, exist_ok=True)

    # --- Load data ---
    df = pd.read_csv(csv_path)
    df['first_timestamp'] = pd.to_datetime(df['first_timestamp_ms'], unit='ms', utc=True)
    df['last_timestamp'] = pd.to_datetime(df['last_timestamp_ms'], unit='ms', utc=True)
    df['duration_ms'] = df['duration_ms'].astype(float)

    # --- Stats ---
    total_time_ms = (df['last_timestamp'].max() - df['first_timestamp'].min()).total_seconds() * 1000
    avg_duration_ms = df['duration_ms'].mean()
    total_bytes_sum = df['total_bytes'].sum()

    print(f'Całkowity czas ładowania strony: {total_time_ms:.1f} ms')
    print(f'Średni czas pobierania obiektu: {avg_duration_ms:.1f} ms')
    print(f'Łączna ilość danych: {total_bytes_sum/1024/1024:.2f} MB')

    # --- Plot 1: per-object download time ---
    fig1 = plt.figure(figsize=(10, 6))
    plt.barh(df['request_uri'], df['duration_ms'])
    plt.xlabel('Download time [ms]')
    plt.ylabel('Object (URI)')
    plt.title('Download time per object')
    plt.tight_layout()
    fig1_path = os.path.join(out_dir, 'wykres_czasy_obiektow.png')
    fig1.savefig(fig1_path, dpi=150, bbox_inches='tight')
    plt.close(fig1)

    # --- Plot 2: concurrency ---
    ts_all = pd.date_range(df['first_timestamp'].min(), df['last_timestamp'].max(), freq='10ms')
    active_counts = []
    for t in ts_all:
        count = ((df['first_timestamp'] <= t) & (df['last_timestamp'] >= t)).sum()
        active_counts.append(count)

    fig2 = plt.figure(figsize=(10, 5))
    plt.plot(ts_all, active_counts)
    plt.title('Concurrency of downloads over time')
    plt.xlabel('Time')
    plt.ylabel('Active downloads')
    plt.tight_layout()
    fig2_path = os.path.join(out_dir, 'wykres_rownoleglosc.png')
    fig2.savefig(fig2_path, dpi=150, bbox_inches='tight')
    plt.close(fig2)

    # --- Plot 3: gaps within connections ---
    gaps = []
    for port, group in df.sort_values('first_timestamp').groupby('client_port'):
        ends = group['last_timestamp'].shift(1)
        starts = group['first_timestamp']
        gap = (starts - ends).dt.total_seconds() * 1000
        gaps += list(gap[gap > 0].dropna())

    fig3 = plt.figure(figsize=(8, 5))
    plt.hist(gaps, bins=50)
    plt.title('Time gaps between downloads (same connection)')
    plt.xlabel('Gap length [ms]')
    plt.ylabel('Occurrences')
    plt.tight_layout()
    fig3_path = os.path.join(out_dir, 'wykres_przerwy.png')
    fig3.savefig(fig3_path, dpi=150, bbox_inches='tight')
    plt.close(fig3)

    # --- Plot 4: Gantt chart ---
    gantt_df = df[['request_uri', 'first_timestamp', 'last_timestamp']].copy()
    gantt_df = gantt_df.sort_values('first_timestamp').reset_index(drop=True)

    fig4 = plt.figure(figsize=(12, max(4, len(gantt_df) * 0.15)))
    ax = plt.gca()
    for i, row in gantt_df.iterrows():
        ax.hlines(y=i, xmin=row['first_timestamp'], xmax=row['last_timestamp'])
    ax.set_yticks(range(len(gantt_df)))
    ax.set_yticklabels(gantt_df['request_uri'])
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S.%f"))
    plt.title('Gantt: file downloads over time')
    plt.xlabel('Time')
    plt.ylabel('Object (URI)')
    plt.tight_layout()
    fig4_path = os.path.join(out_dir, 'wykres_gantt.png')
    fig4.savefig(fig4_path, dpi=150, bbox_inches='tight')
    plt.close(fig4)

    # --- PDF report ---
    raport_path = os.path.join(out_dir, 'raport_analizy.pdf')
    width, height = A4
    c = canvas.Canvas(raport_path, pagesize=A4)
    c.setTitle("HTTP Analysis Report")

    # Page 1: stats
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2.5 * cm, "HTTP Analysis Report")
    c.setFont("Helvetica", 11)
    y = height - 3.5 * cm
    lines = [
        f"Total page load time: {total_time_ms:.1f} ms",
        f"Average object download time: {avg_duration_ms:.1f} ms",
        f"Total data transferred: {total_bytes_sum/1024/1024:.2f} MB",
        f"Objects analyzed: {len(df)}",
    ]
    for line in lines:
        c.drawString(2 * cm, y, line)
        y -= 0.7 * cm
    c.showPage()

    def add_chart_to_pdf(c, title, path):
        img = ImageReader(path)
        img_w, img_h = img.getSize()
        scale = min((width - 3 * cm) / img_w, (height - 4 * cm) / img_h)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2 * cm, height - 2 * cm, title)
        c.drawImage(img, 1.5 * cm, 2 * cm, img_w * scale, img_h * scale)
        c.showPage()

    add_chart_to_pdf(c, "Per-object download times", fig1_path)
    add_chart_to_pdf(c, "Download concurrency over time", fig2_path)
    add_chart_to_pdf(c, "Gaps within single connections", fig3_path)
    add_chart_to_pdf(c, "Gantt chart of downloads", fig4_path)

    c.save()
    print(f"\nReport generated successfully: {raport_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python data_analizer.py <path_to_csv>")
        sys.exit(1)

    csv_input = sys.argv[1]
    if not os.path.exists(csv_input):
        print(f"Error: file {csv_input} not found.")
        sys.exit(1)

    analyze(csv_input)
