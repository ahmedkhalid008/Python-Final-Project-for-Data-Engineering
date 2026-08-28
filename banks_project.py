# banks_project.py
# Code for ETL operations on Largest Banks data

from datetime import datetime
import sqlite3
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

# -------------------------------------------------------------------
# Configuration and Global Constants
# -------------------------------------------------------------------
URL = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
EXCHANGE_RATE_CSV = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv'
TABLE_ATTRIBS_EXTRACTION = ['Name', 'MC_USD_Billion']
FINAL_TABLE_ATTRIBS = [
    'Name',
    'MC_USD_Billion',
    'MC_GBP_Billion',
    'MC_EUR_Billion',
    'MC_INR_Billion',
]
OUTPUT_CSV_PATH = './Largest_banks_data.csv'
DB_NAME = 'Banks.db'
TABLE_NAME = 'Largest_banks'
LOG_FILE = 'code_log.txt'


# -------------------------------------------------------------------
# Task 1: Logging Function
# -------------------------------------------------------------------
def log_progress(message: str) -> None:
    """Logs the mentioned message of a given stage of code execution

    to a log file with timestamp syntax '<time_stamp> : <message>'.
    """
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(LOG_FILE, 'a') as f:
        f.write(f'{timestamp} : {message}\n')


# -------------------------------------------------------------------
# Task 2: Extraction Function
# -------------------------------------------------------------------
def extract(url: str, table_attribs: list) -> pd.DataFrame:
    """Extracts tabular data under 'By market capitalization' heading

    into a pandas DataFrame with columns 'Name' and 'MC_USD_Billion'.
    """
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)

    # In this archive snapshot, the first table contains market capitalization data
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            # col[1] contains the Bank name link/anchor tag
            # col[2] contains the market cap value with trailing newline
            bank_name = col[1].find_all('a')[-1].contents[0].strip()
            market_cap_str = col[2].contents[0].strip()

            # Clean and typecast market cap to float
            market_cap = float(market_cap_str)

            data_dict = {'Name': bank_name, 'MC_USD_Billion': market_cap}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)

    return df


# -------------------------------------------------------------------
# Task 3: Transformation Function
# -------------------------------------------------------------------
def transform(df: pd.DataFrame, csv_path: str) -> pd.DataFrame:
    """Reads exchange rate CSV into a dict and calculates market cap

    in GBP, EUR, and INR, rounded to 2 decimal places.
    """
    # Read the exchange rate CSV file into a pandas dataframe
    exchange_rate_df = pd.read_csv(csv_path)

    # Convert contents to dictionary: Currency -> Rate
    exchange_rate = exchange_rate_df.set_index('Currency').to_dict()['Rate']

    # Retrieve and cast exchange rates to float
    gbp_rate = float(exchange_rate['GBP'])
    eur_rate = float(exchange_rate['EUR'])
    inr_rate = float(exchange_rate['INR'])

    # Add transformed currency columns rounded to 2 decimal places
    df['MC_GBP_Billion'] = [
        np.round(x * gbp_rate, 2) for x in df['MC_USD_Billion']
    ]
    df['MC_EUR_Billion'] = [
        np.round(x * eur_rate, 2) for x in df['MC_USD_Billion']
    ]
    df['MC_INR_Billion'] = [
        np.round(x * inr_rate, 2) for x in df['MC_USD_Billion']
    ]

    return df


# -------------------------------------------------------------------
# Task 4: Loading to CSV
# -------------------------------------------------------------------
def load_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """Saves the final DataFrame as a CSV file to the provided path."""
    df.to_csv(output_path, index=False)


# -------------------------------------------------------------------
# Task 5: Loading to Database
# -------------------------------------------------------------------
def load_to_db(
    df: pd.DataFrame, sql_connection: sqlite3.Connection, table_name: str
) -> None:
    """Saves the final DataFrame to SQLite database table."""
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)


# -------------------------------------------------------------------
# Task 6: Running Database Queries
# -------------------------------------------------------------------
def run_query(
    query_statement: str, sql_connection: sqlite3.Connection
) -> None:
    """Runs the SQL query on the database table and prints output."""
    print(f'\nQuery: {query_statement}')
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)


# -------------------------------------------------------------------
# Main ETL Execution Pipeline
# -------------------------------------------------------------------
if __name__ == '__main__':
    # Initial Log Entry
    log_progress('Preliminaries complete. Initiating ETL process')

    # Task 2: Extraction
    df_extracted = extract(URL, TABLE_ATTRIBS_EXTRACTION)
    log_progress('Data extraction complete. Initiating Transformation process')

    # Task 3: Transformation
    df_transformed = transform(df_extracted, EXCHANGE_RATE_CSV)
    # Hint for quiz: Print 5th largest bank's EUR value
    # print("5th largest bank MC in EUR:", df_transformed['MC_EUR_Billion'][4])
    log_progress('Data transformation complete. Initiating Loading process')

    # Task 4: Load to CSV
    load_to_csv(df_transformed, OUTPUT_CSV_PATH)
    log_progress('Data saved to CSV file')

    # Task 5: SQL Connection and DB Load
    sql_connection = sqlite3.connect(DB_NAME)
    log_progress('SQL Connection initiated')

    load_to_db(df_transformed, sql_connection, TABLE_NAME)
    log_progress('Data loaded to Database as a table, Executing queries')

    # Task 6: Run Verification Queries
    query_1 = f'SELECT * FROM {TABLE_NAME}'
    query_2 = f'SELECT AVG(MC_GBP_Billion) FROM {TABLE_NAME}'
    query_3 = f'SELECT Name FROM {TABLE_NAME} LIMIT 5'

    run_query(query_1, sql_connection)
    run_query(query_2, sql_connection)
    run_query(query_3, sql_connection)

    log_progress('Process Complete')

    # Close SQLite Connection
    sql_connection.close()
    log_progress('Server Connection closed')