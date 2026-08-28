# World's Largest Banks ETL Pipeline

An automated Python ETL (Extract, Transform, Load) system designed to scrape, process, convert, and store market capitalization data for the world's top 10 largest banks.

---

## ?? Project Scenario
You have been hired as a **Data Engineer** by a research organization. Your task is to build an automated pipeline that compiles the list of the top 10 largest banks globally, ranked by market capitalization in billion USD. 

The pipeline transforms and converts the financial data into GBP, EUR, and INR based on dynamic exchange rate information, saving the structured results locally as a CSV file and inside an SQLite database table for quarterly financial reporting.

---

## ?? Data Sources & URLs
* **Web Data Source:** [Wikipedia - List of largest banks (Web Archive)](https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks)
* **Exchange Rates CSV:** [Exchange Rate Data (IBM Cloud Storage)](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv)

---

## ?? ETL Architecture & Tasks

1. **Extract:** Scrapes bank names and market capitalization from Wikipedia using BeautifulSoup and requests.
2. **Transform:** Reads exchange rate data, converts USD valuations to GBP, EUR, and INR, and rounds all numerical metrics to 2 decimal places.
3. **Load:** 
   - Exports the processed dataset to Largest_banks_data.csv.
   - Ingests records into the Largest_banks table within the Banks.db SQLite database.
4. **Query & Audit:** 
   - Runs verification SQL queries on the database.
   - Logs timestamped execution milestones to code_log.txt.

---

## ?? How to Run

1. **Install Dependencies:**
   pip install requests beautifulsoup4 pandas numpy lxml

2. **Execute Script:**
   python banks_project.py
