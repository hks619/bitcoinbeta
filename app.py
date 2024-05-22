import streamlit as st
import pandas as pd
import requests
import io

# Define the base URL for the GitHub repository
base_url = "https://raw.githubusercontent.com/hks619/bitcoinbeta/main/company_data/"
bitcoin_data_url = "https://raw.githubusercontent.com/hks619/bitcoinbeta/main/bitcoin_5yr.xlsx"
bitcoin_logo_url = "https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg"  # Example URL for Bitcoin logo

# Dictionary to map company names to their ticker symbols
company_tickers = {
    "bitdeer": "NASDAQ:BTDR",
    "bitfarms": "NASDAQ:BITF",
    "cipher": "NASDAQ:CIFR",
    "cleanspark": "NASDAQ:CLSK",
    "core": "NASDAQ:CORZ",
    "hut": "NASDAQ:HUT",
    "iris": "NASDAQ:IREN",
    "marathon": "NASDAQ:MARA",
    "riot": "NASDAQ:RIOT",
    "terawulf": "NASDAQ:WULF"
}

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
    company_data_url = base_url + f'{company_name}_5yr.xlsx'
    revenue_data_url = base_url + f'IS_{company_name}_qusd.xlsx'
    
    company_data = load_data_from_github(company_data_url)
    bitcoin_data = load_data_from_github(bitcoin_data_url)
    income_statement = load_data_from_github(revenue_data_url)
    
    if company_data is None or bitcoin_data is None or income_statement is None:
        return None, None, None

    # Extract the header row containing the dates, excluding non-date columns
    header_row = income_statement.columns[1:]

    # Manually clean the date strings by removing non-breaking spaces and other anomalies
    cleaned_dates = header_row.str.replace('\u00a0', '').str.strip()
    cleaned_dates = pd.to_datetime(cleaned_dates, format='%d-%b-%Y', errors='coerce')

    # Remove any columns that could not be parsed as dates
    valid_columns = cleaned_dates.notna()

    # Filter out invalid dates
    cleaned_dates = cleaned_dates[valid_columns]
    revenue_series = income_statement.iloc[1, 1:][valid_columns]

    # Create a new DataFrame with cleaned dates as the index and revenue data
    revenue_df = pd.DataFrame(revenue_series.values, index=cleaned_dates, columns=['Revenue'])
    revenue_df['Revenue'] = pd.to_numeric(revenue_df['Revenue'], errors='coerce')
    revenue_df.dropna(inplace=True)
    return company_data, bitcoin_data, revenue_df

# Function to calculate beta and correlation
def calculate_metrics(company_data, bitcoin_data, revenue_df):
    # Ensure the date columns are in datetime format
    company_data['Exchange Date'] = pd.to_datetime(company_data['Exchange Date'])
    bitcoin_data['Exchange Date'] = pd.to_datetime(bitcoin_data['Exchange Date'])
    
    # Merge data on date
    merged_data = pd.merge(bitcoin_data[['Exchange Date', 'Open']],
                           company_data[['Exchange Date', 'Open']],
                           on='Exchange Date',
                           suffixes=('_btc', '_bf'))
    merged_data.set_index('Exchange Date', inplace=True)
    
    merged_data['Return_btc'] = merged_data['Open_btc'].pct_change()
    merged_data['Return_bf'] = merged_data['Open_bf'].pct_change()

    # Remove the NaN values that result from the pct_change calculation
    merged_data = merged_data.dropna()
    
    # Calculate beta
    covariance = merged_data['Return_bf'].cov(merged_data['Return_btc'])
    variance = merged_data['Return_btc'].var()
    beta = covariance / variance
    
    # Calculate correlation
    merged_data_quarterly = merged_data.resample('Q').mean()
    final_merged_df = revenue_df.merge(merged_data_quarterly, left_index=True, right_index=True)
    correlation_btc = final_merged_df.corr().loc['Revenue', 'Open_btc']
    return beta, correlation_btc

# Get the list of companies from the data folder on GitHub
company_files = [
    "bitdeer_5yr.xlsx", "bitfarms_5yr.xlsx", "cipher_5yr.xlsx", 
    "cleanspark_5yr.xlsx", "core_5yr.xlsx", "hut_5yr.xlsx", 
    "iris_5yr.xlsx", "marathon_5yr.xlsx", "riot_5yr.xlsx", 
    "terawulf_5yr.xlsx"
]
company_names = [f.split('_')[0] for f in company_files]

# Streamlit App
st.image(bitcoin_logo_url, width=100)  # Add Bitcoin logo to main page
st.title("Bitcoin Mining Companies Financial Analysis")

# Create a list of display names for the dropdown
display_names = [f"{name.upper()} ({company_tickers[name]})" for name in company_names]

# Dropdown list for selecting a company
selected_display_name = st.selectbox('Select a company:', display_names)

if selected_display_name:
    # Extract the company name from the display name
    selected_company = selected_display_name.split()[0].lower()
    company_data, bitcoin_data, revenue_df = load_company_data(selected_company)
    if company_data is not None and bitcoin_data is not None and revenue_df is not None:
        beta, correlation_btc = calculate_metrics(company_data, bitcoin_data, revenue_df)
        
        st.subheader(f'Financial Metrics for {selected_display_name}')
        st.write(f"**Beta against Bitcoin:** {beta:.5f}")
        st.write(f"**Correlation of Revenue with Bitcoin's Price:** {correlation_btc:.5f}")
    else:
        st.error("Failed to load data for the selected company")

# Run the app with: streamlit run app.py
