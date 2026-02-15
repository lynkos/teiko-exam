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
> [!IMPORTANT]
> Regarding the scripts in [**Part 2: Initial Analysis - Data Overview**](#part-2-initial-analysis---data-overview), [**Part 3: Statistical Analysis**](#part-3-statistical-analysis), and [**Part 4: Data Subset Analysis**](#part-4-data-subset-analysis):
> * The output data for each of those scripts is displayed in the [web dashboard](https://be97c6b7-cf30-4e8b-958d-837de4ee4a72.plotly.app) (see [**Dashboard**](#dashboard) section for more details).
> * Therefore, running the scripts may not be necessary since it's already visualized in the [web dashboard](https://be97c6b7-cf30-4e8b-958d-837de4ee4a72.plotly.app).
> * Alternatively, if you want to see the output in the terminal, you can run the scripts.

### Part 1: Data Management
Set up the SQLite database `subjects.db` and load the data from [`cell-count.csv`](cell-count.csv) into `samples` and `subjects` tables
   ```sh
   python load_data.py
   ```

### Part 2: Initial Analysis - Data Overview
Generate the summary table and add to `subjects.db` as `summary_table` table
   ```sh
   python data_analysis.py
   ```

### Part 3: Statistical Analysis
Run the stats analysis script for insights and visualizations
   ```sh
   python stats_analysis.py
   ```

### Part 4: Data Subset Analysis
Run the subset analysis
   ```sh
   python subset_analysis.py
   ```

## Database Schema
<div align="center">
    <img alt="SQLite database schema" src="db_schema.svg">
</div>

My database [`subjects.db`](subjects.db) contains 3 tables:
   * `samples`: Contains information about each sample; generated in [`load_data.py`](load_data.py)
   * `subjects`: Contains information about each subject; generated in [`load_data.py`](load_data.py)
   * `summary_table`: Contains summary statistics for each sample; generated in [`data_analysis.py`](data_analysis.py)

Initially I considered making a `project` table, but I decided against it because there are only 3 unique projects (i.e. `proj1`, `proj2`, `proj3`) in the dataset. However, if there were hundreds of projects or more, I'd have created a `project` table and link it to the `subjects` table (instead of the `project` column in the `subjects` table).

## Overview

## Dashboard
<div align="center"><span style="font-size: 1.5em; font-weight: bold; text-decoration: underline;"><a href="https://be97c6b7-cf30-4e8b-958d-837de4ee4a72.plotly.app" target="_blank" title="Interactive dashboard hosted by Plotly">Interactive dashboard for Teiko Exam</a></span></div>

> [!NOTE]
> This dashboard has been generated with the [`app.py`](app.py) script and uploaded to [Plotly Cloud](https://plotly.com/cloud). You can click the link above to view the dashboard, which includes visualizations for all parts of the exam (except [**Part 1: Data Management**](#part-1-data-management)).
> 
> To run the dashboard locally:
> ```sh
> python app.py
> ```

## Assumptions
* An empty `response` does **NOT** imply a value of `no`. In other words, I did **NOT** interpret any sample with an empty `response` as a non-responder (i.e. `response=NULL` is **NOT** interpreted as `response=no`).
* Data is **NOT** normally distributed, so I used **Mann–Whitney U test** for the statistical analysis.
* For [**Part 3: Statistical Analysis**](#part-3-statistical-analysis):
  * I was unsure of these instructions:
     > Visualize the population relative frequencies comparing responders versus non-responders using a boxplot of for each immune cell population.
     > 
     > Report which cell populations have a significant difference in relative frequencies between responders and non-responders. Statistics are needed to support any conclusion to convince Yah of Bob's findings.
   * I didn't know if the visualization and report should be for "`melanoma` patients receiving `miraclib` who respond (`responders`) versus those who do not (`non-responders`)", as specified in the 1st bullet of that section, or if the visualization should be for all samples
   * As a result, I decided to play it safe by including visualizations and reports for both:
     * **ALL** samples (i.e. includes non-`melanoma` patients, non-`miraclib`, etc.)
     * **ONLY** `melanoma` patients receiving `miraclib` who are `responders` or `non-responders`
   * Each one has been labeled accordingly in the dashboard.

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