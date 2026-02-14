<div align="center">
    <h1>Teiko Technical Exam</h1>
    <img alt="Python" src="https://img.shields.io/static/v1?label=Language&style=flat&message=Python+3.14.3&logo=python&color=c7a228&labelColor=393939&logoColor=4f97d1">
    <img alt="SQLite" src="https://img.shields.io/static/v1?label=Libraries&style=flat&message=SQLite&logo=sqlite&color=003B57&labelColor=393939&logoColor=003B57">
    <img alt="Shell" src="https://img.shields.io/static/v1?label=Shell&style=flat&message=Bash&logo=gnu+bash&color=4EAA25&labelColor=393939&logoColor=4EAA25">
    <br>
    <img alt="Last Commit" src="https://img.shields.io/github/last-commit/lynkos/teiko-exam?style=flat&label=Last+Commit&labelColor=393939&color=be0000">
    <img alt="Repo Size" src="https://img.shields.io/github/repo-size/lynkos/teiko-exam?style=flat&label=Repo+Size&labelColor=393939&color=ff62b1">
</div>

## Requirements
- [x] [Python 3](https://www.python.org/downloads)

## Installation
1. Make sure [Python 3](https://www.python.org) is installed
   ```sh
   python3 --version
   ```

2. Clone the repository (i.e. [`teiko-exam`](https://github.com/lynkos/teiko-exam)), then change directory to `teiko-exam`
   ```sh
   git clone https://github.com/lynkos/teiko-exam.git && cd teiko-exam
   ```

3. Create a virtual environment and activate it
   - Unix:
     ```sh
     python3 -m venv .venv
     ```
   - Windows:
     ```sh
     py -m venv .venv
     ```

4. Activate virtual environment
   - Unix:
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
   python3 load_data.py
   ```

### Part 2: Initial Analysis - Data Overview
Run the data analysis script to generate insights and visualizations
   ```sh
   python3 data_analysis.py
   ```

### Part 3: Statistical Analysis

### Part 4: Data Subset Analysis

## Database Schema

## Overview

## Dashboard

## Repository Structure
```plaintext
.
├── .gitignore
├── cell-count.csv
├── data_analysis.py
├── load_data.py
├── README.md
└── subjects.db
```