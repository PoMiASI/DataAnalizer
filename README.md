# Data Analyzer — PoMiASI Project

`data_analyzer.py` is a standalone data processing tool developed for the **PoMiASI** project.  
It analyzes HTTP request and response logs exported as CSV files and generates visual reports that describe the behavior of browsers during page loading.

---

##  Overview

The analyzer helps visualize and quantify browser performance by examining how files are downloaded over time.  
It produces multiple plots and a detailed PDF report that make it easy to compare how Chrome, Firefox, Opera, and Safari handle network requests.

---

##  Features

-  **Total and average load time** calculation  
-  **Per-object download time** visualization  
-  **Concurrency analysis** – number of simultaneous downloads over time  
-  **Connection gap detection** – time gaps within a single TCP port session (`client_port`)  
-  **Gantt chart** – timeline of all downloads  //additional summary
-  **Automatic PDF report generation** including all visualizations  // additional snapshot of captured data

---

##  Requirements

Python **3.9+** is recommended.  
Install required libraries before running:

```bash
pip install pandas matplotlib reportlab

 -------------Expected CSV Structure------------------------

The input CSV should contain at least the following columns:

Column name	Description
first_timestamp_ms	Request start timestamp (in ms)
last_timestamp_ms	Response end timestamp (in ms)
duration_ms	Download duration
request_uri	Requested resource path
client_port	Client TCP port
total_bytes	Total bytes transferred
request_user_agent	User-Agent string (browser identifier)


---------------How to use---------------------

Run the script directly from the command line:

python data_analyzer.py C:\path\to\output.csv


The analyzer will automatically:

Create a results folder next to your CSV file

Generate all required visualizations

Export a combined PDF report

----- Output Files Tree ---------------

After running, a new folder will appear:

C:\path\to\wyniki_analizy\
 ├── wykres_czasy_obiektow.png       # Object download times
 ├── wykres_rownoleglosc.png         # Concurrency over time
 ├── wykres_przerwy.png              # Gaps between downloads per connection
 ├── wykres_gantt.png                # Gantt chart of downloads
 └── raport_analizy.pdf              # Combined PDF report
