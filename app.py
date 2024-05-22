import streamlit as st
import pandas as pd
import os
import requests
import io

# Define the path to the data folder and the bitcoin data
data_folder_path = '/Users/hks/Documents/intro_to_programming/bitcoinbeta/company_data/'
bitcoin_data_path = '/Users/hks/Documents/intro_to_programming/bitcoinbeta/bitcoin_5yr.xlsx'
# Define the base URL for the GitHub repository
base_url = "https://raw.githubusercontent.com/hks619/bitcoinbeta/main/company_data/"
bitcoin_data_url = "https://raw.githubusercontent.com/hks619/bitcoinbeta/main/bitcoin_5yr.xlsx"

# Function to load data from GitHub
def load_data_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_excel(io.BytesIO(response.content))
    else:
        st.error("Error loading data from GitHub")
        return None

# Function to load the data for a specific company
def load_company_data(company_name):
    bitfarms_data_path = os.path.join(data_folder_path, f'{company_name}_5yr.xlsx')
    revenue_data_path = os.path.join(data_folder_path, f'IS_{company_name}_qusd.xlsx')
    company_data_url = base_url + f'{company_name}_5yr.xlsx'
    revenue_data_url = base_url + f'IS_{company_name}_qusd.xlsx'

    bitfarms_data = pd.read_excel(bitfarms_data_path)
    bitcoin_data = pd.read_excel(bitcoin_data_path)
    income_statement = pd.read_excel(revenue_data_path)
    company_data = load_data_from_github(company_data_url)
    bitcoin_data = load_data_from_github(bitcoin_data_url)
    income_statement = load_data_from_github(revenue_data_url)

    if company_data is None or bitcoin_data is None or income_statement is None:
        return None, None, None

    # Extract the header row containing the dates, excluding non-date columns
    header_row = income_statement.columns[1:]

@@ -33,17 +46,17 @@ def load_company_data(company_name):
    revenue_df = pd.DataFrame(revenue_series.values, index=cleaned_dates, columns=['Revenue'])
    revenue_df['Revenue'] = pd.to_numeric(revenue_df['Revenue'], errors='coerce')
    revenue_df.dropna(inplace=True)
    return bitfarms_data, bitcoin_data, revenue_df
    return company_data, bitcoin_data, revenue_df

# Function to calculate beta and correlation
def calculate_metrics(bitfarms_data, bitcoin_data, revenue_df):
def calculate_metrics(company_data, bitcoin_data, revenue_df):
    # Ensure the date columns are in datetime format
    bitfarms_data['Exchange Date'] = pd.to_datetime(bitfarms_data['Exchange Date'])
    company_data['Exchange Date'] = pd.to_datetime(company_data['Exchange Date'])
    bitcoin_data['Exchange Date'] = pd.to_datetime(bitcoin_data['Exchange Date'])

    # Merge data on date
    merged_data = pd.merge(bitcoin_data[['Exchange Date', 'Open']],
                           bitfarms_data[['Exchange Date', 'Open']],
                           company_data[['Exchange Date', 'Open']],
                           on='Exchange Date',
                           suffixes=('_btc', '_bf'))
    merged_data.set_index('Exchange Date', inplace=True)
@@ -65,8 +78,13 @@ def calculate_metrics(bitfarms_data, bitcoin_data, revenue_df):
    correlation_btc = final_merged_df.corr().loc['Revenue', 'Open_btc']
    return beta, correlation_btc

# Get the list of companies from the data folder
company_files = [f for f in os.listdir(data_folder_path) if f.endswith('_5yr.xlsx')]
# Get the list of companies from the data folder on GitHub
company_files = [
    "bitdeer_5yr.xlsx", "bitfarms_5yr.xlsx", "cipher_5yr.xlsx", 
    "cleanspark_5yr.xlsx", "core_5yr.xlsx", "hut_5yr.xlsx", 
    "iris_5yr.xlsx", "marathon_5yr.xlsx", "riot_5yr.xlsx", 
    "terawulf_5yr.xlsx"
]
company_names = [f.split('_')[0] for f in company_files]

# Streamlit App
@@ -76,11 +94,14 @@ def calculate_metrics(bitfarms_data, bitcoin_data, revenue_df):
selected_company = st.selectbox('Select a company:', company_names)

if selected_company:
    bitfarms_data, bitcoin_data, revenue_df = load_company_data(selected_company)
    beta, correlation_btc = calculate_metrics(bitfarms_data, bitcoin_data, revenue_df)

    st.subheader(f'Financial Metrics for {selected_company.capitalize()}')
    st.write(f"**Beta:** {beta}")
    st.write(f"**Correlation of Revenue with Bitcoin's Price:** {correlation_btc}")
    company_data, bitcoin_data, revenue_df = load_company_data(selected_company)
    if company_data is not None and bitcoin_data is not None and revenue_df is not None:
        beta, correlation_btc = calculate_metrics(company_data, bitcoin_data, revenue_df)

        st.subheader(f'Financial Metrics for {selected_company.capitalize()}')
        st.write(f"**Beta:** {beta}")
        st.write(f"**Correlation of Revenue with Bitcoin's Price:** {correlation_btc}")
    else:
        st.error("Failed to load data for the selected company")

# Run the app with: streamlit run bitfarms_analysis_app.py
# Run the app with: streamlit run bitfarms_analysis_app.py
