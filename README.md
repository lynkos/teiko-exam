<div align="center">
    <h1>Teiko Technical Exam</h1>
    <img alt="Python" src="https://img.shields.io/static/v1?label=Language&style=flat&message=Python+3.14.0&logo=python&color=c7a228&labelColor=393939&logoColor=4f97d1">
    <img alt="SQLite" src="https://img.shields.io/static/v1?label=Libraries&style=flat&message=SQLite&logo=sqlite&color=003B57&labelColor=393939&logoColor=003B57">
    <img alt="pandas" src="https://img.shields.io/static/v1?label=Libraries&style=flat&message=pandas&logo=pandas&color=150458&labelColor=393939&logoColor=150458">
    <img alt="SciPy" src="https://img.shields.io/static/v1?label=Libraries&style=flat&message=SciPy&logo=scipy&color=8CAAE6&labelColor=393939&logoColor=8CAAE6">
    <img alt="Plotly" src="https://img.shields.io/static/v1?label=Libraries&style=flat&message=Plotly&logo=plotly&color=7A76FF&labelColor=393939&logoColor=7A76FF">
    <img alt="Shell" src="https://img.shields.io/static/v1?label=Shell&style=flat&message=Bash&logo=gnu+bash&color=4EAA25&labelColor=393939&logoColor=4EAA25">
    <br>
    <img alt="Last Commit" src="https://img.shields.io/github/last-commit/lynkos/teiko-exam?style=flat&label=Last+Commit&labelColor=393939&color=be0000">
    <img alt="Repo Size" src="https://img.shields.io/github/repo-size/lynkos/teiko-exam?style=flat&label=Repo+Size&labelColor=393939&color=ff62b1">
</div>

> [!IMPORTANT]
> Even though I submitted my solution before the deadline, I continue to make changes (even after the deadline has passed).
> 
> If you see this message, it means that my solution is still being updated. Please check back later for the final version (i.e. once I remove this message), which will ideally be by Monday.

## Requirements
- [x] [Python 3](https://www.python.org/downloads)

## Installation
1. Confirm [Python 3](https://www.python.org) is installed
   ```sh
   python3 --version
   ```

2. Clone the repository (i.e. [`teiko-exam`](https://github.com/lynkos/teiko-exam)), then change directory to `teiko-exam`
   ```sh
   git clone https://github.com/lynkos/teiko-exam.git && cd teiko-exam
   ```

3. Create virtual environment
   - UNIX:
     ```sh
     python3 -m venv .venv
     ```
   - Windows:
     ```sh
     py -m venv .venv
     ```

4. Activate virtual environment
   - UNIX:
     ```sh
     source .venv/bin/activate
     ```
   - Windows:
     ```sh
     .venv\Scripts\activate
     ```

5. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```

## Usage
### Part 1: Data Management
Set up the SQLite database `subjects.db` and load the data from [`cell-count.csv`](cell-count.csv)
   ```sh
   python load_data.py
   ```

### Part 2: Initial Analysis - Data Overview
Generate and print the summary table
   ```sh
   python data_analysis.py
   ```

### Part 3: Statistical Analysis
Run the stats analysis script to generate insights and visualizations
   ```sh
   python stats_analysis.py
   ```

### Part 4: Data Subset Analysis
Run `app.py` for data subset analysis (i.e. visualizes data from [`subset_analysis.py`](subset_analysis.py))
   ```sh
   python app.py
   ```

## Database Schema
<div align="center">
    <img alt="SQLite database schema" src="db_schema.svg">
</div>

## Overview

## Dashboard
<span style="font-size: 1.5em; font-weight: bold;"><a href="https://be97c6b7-cf30-4e8b-958d-837de4ee4a72.plotly.app" target="_blank" title="">Interactive dashboard for Teiko Exam</a></span>

## Repository Structure
```plaintext
.
├── .gitignore
├── app.py
├── cell-count.csv
├── data_analysis.py
├── db_schema.svg
├── load_data.py
├── README.md
├── requirements.txt
├── stats_analysis.py
├── subjects.db
└── subset_analysis.py
```

| Filename | Description |
|:--------:|:-----------:|
| `.gitignore` | Files and directories to be ignored by Git |
| `app.py` | Creates a web dashboard using Plotly |
| `cell-count.csv` | Original dataset |
| `data_analysis.py` | Generate and print the summary table for "Part 2". Data will be displayed in the web dashboard. |
| `db_schema.svg` | Image displaying schema of `subjects.db` |
| `load_data.py` | Set up the SQLite database `subjects.db` and load the data from `cell-count.csv` for "Part 1" |
| `README.md` | This file |
| `requirements.txt` | Dependencies |
| `stats_analysis.py` | Statistical analysis of data in `subjects.db` for "Part 3". Data will be displayed in the web dashboard. |
| `subjects.db` | SQLite database containing samples, subjects, and summary tables |
| `subset_analysis.py` | Filters and analyzes data from `subjects.db` for "Part 4". Data will be displayed in the web dashboard. |

## Assumptions
* An empty `response` does NOT imply a value of `no`. In other words, I excluded any sample with an empty `response` from the analysis.
* In Part 3, the visualization does not exclude non-`melanoma` patients, non-`PBMC` samples, or non-`miraclib` treatments.
* Data is **NOT** normally distributed, so I used Mann–Whitney U test for Part 3.