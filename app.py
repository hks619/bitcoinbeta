import streamlit as st
import pandas as pd

# Load data (you need to provide the correct file paths)
bitfarms_data_path = '/Users/hks/Documents/intro_to_programming/bitcoinbeta/company_data/bitfarm_5yr.xlsx'  # Replace with the actual path
bitcoin_data_path = '/Users/hks/Documents/intro_to_programming/bitcoinbeta/bitcoin_5yr.xlsx'    # Replace with the actual path
file_path = '/Users/hks/Documents/intro_to_programming/bitcoinbeta/company_data/IS_bitfarms_qusd.xlsx'

# Function to load the data
def load_data(bitfarms_path, bitcoin_path, file_path):
    bitfarms_data = pd.read_excel(bitfarms_path)
    bitcoin_data = pd.read_excel(bitcoin_path)
    income_statement = pd.read_excel(file_path)
    
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
    return bitfarms_data, bitcoin_data, revenue_df

# Function to calculate beta and correlation
def calculate_metrics(bitfarms_data, bitcoin_data, revenue_df):
    # Ensure the date columns are in datetime format
    bitfarms_data['Exchange Date'] = pd.to_datetime(bitfarms_data['Exchange Date'])
    bitcoin_data['Exchange Date'] = pd.to_datetime(bitcoin_data['Exchange Date'])
    
    # Merge data on date
    merged_data = pd.merge(bitcoin_data[['Exchange Date', 'Open']],
                           bitfarms_data[['Exchange Date', 'Open']],
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

# Load the data
bitfarms_data, bitcoin_data, revenue_df = load_data(bitfarms_data_path, bitcoin_data_path, file_path)

# Calculate metrics
beta, correlation_btc = calculate_metrics(bitfarms_data, bitcoin_data, revenue_df)

# Streamlit App
st.title("Bitfarms Financial Analysis")

# Dropdown list
options = ['Bitfarms']
selected_option = st.selectbox('Select a company:', options)

if selected_option == 'Bitfarms':
    st.subheader('Financial Metrics for Bitfarms')
    
    st.write(f"**Beta:** {beta}")
    st.write(f"**Correlation of Revenue with Bitcoin's Price:** {correlation_btc}")

# Run the app with: streamlit run bitfarms_analysis_app.py