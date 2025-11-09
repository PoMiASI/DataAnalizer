# PoMiASI Project – HTTP Data Analyzer (Jupyter)

This repository contains a Jupyter notebook that analyzes HTTP request/response logs exported to CSV format.  
Each record represents a single HTTP request and its corresponding response.

-------------------------------------------------------------------------------------------------------------
### Changelog V2
- Added trimming of the two shortest downloads per browser × attempt.
- Added detailed download time statistics (mean, median, min, max).
- Added percentage distribution of concurrent downloads.
- Added full statistics for time gaps (mean, median, min, max).
- Added "Active downloads over time" chart (=1st packet, up to 25 s).
- Reworked Gantt chart: grouped by client_port, showing execution order.
- Added cross-browser comparison summary.
- Introduced support for multiple attempts (runs) via `attempt` column.
- Removed Seaborn — all plots now use clean Matplotlib.
- Notebook organized into clear, logical cells and formatted for Colab.

## Features

The notebook performs a complete analysis of network request timing and data transfer patterns.  
It includes:

- Total page load time – calculated based on the earliest request start and the latest response end  
- Average object download time  
- Total amount of transferred data  
- Concurrency visualization – number of simultaneous downloads over time  
- Time gaps – delays between consecutive downloads within a single TCP connection (`client_port`)  
- Gantt chart – visual timeline of all object downloads  
- Browser comparison (optional) – automatic detection and comparison of Chrome, Firefox, and Opera based on `request_user_agent`

---

## Requirements

The notebook runs in Google Colab or any local Jupyter env.

---

### Obligatory Input Data
The notebook expects a CSV file containing the following columns:

first_timestamp_ms
last_timestamp_ms
duration_ms
total_bytes
request_uri
client_port
request_user_agent	

---

### Usage
Option 1 – Run in Google Colab
Go to Google Colab

Click File → Upload Notebook and select data_analizer_final.ipynb
Run all cells sequentially (Runtime → Run all)

Option 2 – Run locally
jupyter notebook data_analizer_final.ipynb
Then open the notebook in your browser and run the cells step-by-step.

### Notebook Structure
Section	Description
1	Project description
2	Imports
3	Data loading
4	Browser detection and comparison
5	Basic statistics
6	Per-object download times
7	Download concurrency
8	Time gaps between downloads
9	Gantt chart

---


## Docker Compose

Builds the project's Docker image and runs Jupyter Lab inside the conda environment defined in `environment.yml`.

Run (Docker Compose v2):

```bash
docker compose up --build
```

Or if you have Docker Compose v1 (with hyphen):

```bash
docker-compose up --build
```

After the container starts, open http://localhost:8888 in your browser. Jupyter is started without a token for local convenience; if you want a token, remove the `--NotebookApp.token=''` flag in `docker-compose.yml`.

To stop and remove containers:

```bash
docker compose down
# or for v1:
docker-compose down
```

