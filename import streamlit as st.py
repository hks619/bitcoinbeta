import streamlit as st
import pandas as pd

# Load data (you need to provide the correct file paths)
bitfarms_data_path = '/Users/hks/Documents/intro_to_programming/bitcoinbeta/company_data/bitfarm_5yr.xlsx'  # Replace with the actual path
bitcoin_data_path = '/Users/hks/Documents/intro_to_programming/bitcoinbeta/bitcoin_5yr.xlsx'    # Replace with the actual path

# Function to load the data
def load_data(bitfarms_path, bitcoin_path):
    bitfarms_data = pd.read_csv(bitfarms_path)
    bitcoin_data = pd.read_csv(bitcoin_path)
    return bitfarms_data, bitcoin_data

# Function to calculate beta and correlation
def calculate_metrics(bitfarms_data, bitcoin_data):
    # Ensure the date columns are in datetime format
    bitfarms_data['Date'] = pd.to_datetime(bitfarms_data['Date'])
    bitcoin_data['Date'] = pd.to_datetime(bitcoin_data['Date'])
    
    # Merge data on date
    merged_data = pd.merge(bitfarms_data, bitcoin_data, on='Date')
    
    # Calculate daily returns
    merged_data['Bitfarms_Return'] = merged_data['Bitfarms_Price'].pct_change()
    merged_data['Bitcoin_Return'] = merged_data['Bitcoin_Price'].pct_change()
    
    # Drop NaN values
    merged_data = merged_data.dropna()
    
    # Calculate beta
    covariance = merged_data['Bitfarms_Return'].cov(merged_data['Bitcoin_Return'])
    variance = merged_data['Bitcoin_Return'].var()
    beta = covariance / variance
    
    # Calculate correlation
    correlation = merged_data['Revenue'].corr(merged_data['Bitcoin_Price'])
    
    return beta, correlation

# Load the data
bitfarms_data, bitcoin_data = load_data(bitfarms_data_path, bitcoin_data_path)

# Calculate metrics
beta, correlation = calculate_metrics(bitfarms_data, bitcoin_data)

# Streamlit App
st.title("Bitfarms Financial Analysis")

# Dropdown list
options = ['Bitfarms']
selected_option = st.selectbox('Select a company:', options)

if selected_option == 'Bitfarms':
    st.subheader('Financial Metrics for Bitfarms')
    
    st.write(f"**Beta:** {beta}")
    st.write(f"**Correlation of Revenue with Bitcoin's Price:** {correlation}")

# Run the app with: streamlit run bitfarms_analysis_app.py