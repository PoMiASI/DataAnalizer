# PoMiASI Project – HTTP Log Analyzer (Jupyter)

This repository contains a Jupyter notebook that analyzes HTTP request/response logs exported to CSV format.  
Each record represents a single HTTP request and its corresponding response.

---

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

### Dependencies
```bash
pip install pandas matplotlib seaborn
All required libraries are preinstalled in Google Colab.

Input Data
The notebook expects a CSV file containing the following columns:



Usage
Option 1 – Run in Google Colab
Go to Google Colab

Click File → Upload Notebook and select data_analizer_final.ipynb
Run all cells sequentially (Runtime → Run all)

Option 2 – Run locally
jupyter notebook data_analizer_final.ipynb
Then open the notebook in your browser and run the cells step-by-step.

Notebook Structure
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


