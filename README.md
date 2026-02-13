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
1. Make sure [Python3](https://www.python.org) is installed
   ```sh
    python3 --version
    ```

2. Clone the repository (i.e. [`teiko-exam`](https://github.com/lynkos/teiko-exam)), then change directory to `teiko-exam`
   ```sh
   git clone https://github.com/lynkos/teiko-exam.git && cd teiko-exam
   ```

## Usage
Run the following command to set up the SQLite database and load the data from `cell-count.csv`

```sh
python3 load_data.py
```

> [!TIP]
> If `python3` doesn't work, try using `python` instead

## Database Schema

## Overview

## Dashboard

## Repository Structure
```plaintext
.
├── .gitignore
├── cell-count.csv
├── load_data.py
├── patients.db
└── README.md
```