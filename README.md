# bitcoinbeta
small project to get beta of bitcoin mining companies against the bitcoin price

# Bitcoin Mining company: Financial analyses using python

The rise in Bitcoin and cryptocurrency has led many companies and governments to start mining Bitcoin using their computers. This project looks at how much Bitcoin mining companies depend on the price of Bitcoin especially regarding the recent halving. A split in rewards for new Bitcoin blocks mined that takes place every four years.

The project has three main goals:

- To see how changes in Bitcoin's price affect the stock prices of the ten largest bitcoin mining companies by market cap
- To see how much the quarterly revenue of bitcoin mining companies correlates with price fluctuations
- To visualize the data on streamlit: https://bitcoinbeta.streamlit.app/

We collect data on the stock prices of ten leading Bitcoin mining companies and historical Bitcoin prices from a GitHub repository. We also gather information about each company, like their stock ticker symbol, market cap, and a short description. The data is cleaned and prepared for analysis, making sure dates are in the correct format and revenue data is aligned.

We calculate the beta of each company's stock price against Bitcoin's price to measure how much the company's stock price moves compared to Bitcoin. We also calculate the correlation between Bitcoin's price and the company's quarterly revenue. The results are visualized using Matplotlib, showing stock prices alongside Bitcoin prices on two y-axes.

An interactive Streamlit web app allows users to choose from ten different companies and time periods within last 5 years for analysis. The app displays each company’s market cap, beta, and revenue correlation with Bitcoin’s price, along with plots comparing stock prices to Bitcoin prices over the chosen period.

This project gives useful insights into how Bitcoin mining companies perform financially in relation to Bitcoin's price. The Streamlit app helps users explore these relationships, aiding in better understanding the cryptocurrency market. The project uses Python programming and statistical tools like Pandas, Matplotlib, and NumPy to provide detailed insights into the dependency of these companies on the Bitcoin prices.

Future improvements to this project include: If we had access to plugins that allow us to retrieve financial data, an improvement would be automating the gathering of financial data instead of manually handling downloaded data. Another improvement would be enabling calculation of beta and correlation with revenue for data beyond the 5 year limit that we currently have. 

disclaimer: chatgpt was consulted for this project

This project was completed by:

- Benjamin Bolliger - BB
- Joaquim Graber - topG
- Hari Krishnan Suresh - hks619 

23/05/2024
