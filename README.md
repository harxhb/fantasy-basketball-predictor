# 🏀 NBA Fantasy Basketball Predictor

**Course:** CS 210: Data Management for Data Science
**Team:** Harsh Borkhetaria, Aryan Sehgal

## 📌 Project Overview
The **NBA Fantasy Basketball Predictor** is a unified Data Management System designed to solve the "data fragmentation" problem in fantasy sports. By ingesting raw player statistics into a normalized SQLite database and analyzing them through a custom scoring engine, this tool identifies undervalued players and provides strategic insights for fantasy managers.

## 🚀 Features
* **Unified Data Pipeline:** An ETL process that cleans, normalizes, and stores disparate player stats into a persistent `fantasy.db` SQL database.
* **Advanced SQL Analysis:**
    * **True Value Calculator:** Ranks players based on total efficiency (accounting for turnovers and defensive stats).
    * **Sleeper Finder:** Identifies bench players with elite "Fantasy Points Per Minute" production.
    * **Scarcity Analysis:** Quantifies positional depth to guide draft strategy.
* **Interactive Dashboard:** A **Streamlit** web application that allows users to search for players and perform head-to-head comparisons with algorithmic decision support.

## 📂 File Structure
* `fantasy_app.py`: The main application code containing the ETL pipeline, SQL schema definitions, and Streamlit frontend.
* `fantasy.db`: The pre-built SQLite database containing normalized `Players` and `Player_Stats` tables.
* `nbastats.csv`: The raw source dataset used for ingestion.
* `Fantasy Basketball Predictor Final Report.pdf`: Comprehensive documentation of the project methodology and findings.
* `Final Project Slides.pdf`: Presentation slides summarizing the system architecture and results.

## 🛠️ Installation & Usage
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/fantasy-basketball-predictor.git](https://github.com/YOUR_USERNAME/fantasy-basketball-predictor.git)
    cd fantasy-basketball-predictor
    ```

2.  **Install requirements:**
    ```bash
    pip install streamlit pandas
    ```

3.  **Run the Dashboard:**
    ```bash
    streamlit run fantasy_app.py
    ```
