# 🧮 Data Analizer — PoMiASI Project

`data_analizer.py` is a standalone Python tool developed for the **PoMiASI** project.  
It analyzes HTTP request and response logs exported as CSV files and generates visual and statistical reports that describe browser behavior during page loading.

---

## 🚀 Overview

The analyzer provides detailed insights into how browsers fetch resources.  
It calculates page load metrics, visualizes parallel downloads, identifies idle periods in connections, and exports everything into a single PDF report.

---

## 📊 Features

- ⏱️ **Total and average load time** calculation  
- 📁 **Per-object download duration** visualization  
- 🔁 **Concurrency analysis** – number of simultaneous downloads over time  
- 🔌 **TCP gap detection** – idle gaps between file downloads within a single connection (`client_port`)  
- 📅 **Gantt chart** – timeline of all object downloads  // additional summary gathered data
- 🧾 **Automatic PDF report** containing all plots and key statistics  // additional snapshot of session to file

---

## ⚙️ Requirements

Python **3.9+** is recommended.  
Install dependencies before running:

```bash
pip install pandas matplotlib reportlab

----------🧠 Expected CSV Format-----------------
The input CSV should contain the following columns:

Column name	Description
first_timestamp_ms	Start time of request (in ms)
last_timestamp_ms	End time of response (in ms)
duration_ms	Download duration
request_uri	Requested file path
client_port	Client TCP port
total_bytes	Total bytes transferred
request_user_agent	User-Agent header (browser identifier)

-------------🖥️ Usage---------------------

Run the analyzer directly from the console:

python data_analizer.py C:\path\to\output.csv

The script will automatically:

Create a folder named wyniki_analizy next to your CSV file

Generate all visualizations (PNG images)

Save a combined PDF report with charts and metrics

------------📁 Output Files Tree-----------------
After execution, you’ll find the following files:

makefile
Skopiuj kod
C:\path\to\wyniki_analizy\
 ├── wykres_czasy_obiektow.png       # Object download times
 ├── wykres_rownoleglosc.png         # Concurrency over time
 ├── wykres_przerwy.png              # Time gaps between downloads
 ├── wykres_gantt.png                # Gantt chart of download activity
 └── raport_analizy.pdf              # Complete PDF report


📚 License
This module is part of the PoMiASI research and development project.
Usage and modification are allowed within the project’s context.

✍️ Authors
Developed by the PoMiASI Team
