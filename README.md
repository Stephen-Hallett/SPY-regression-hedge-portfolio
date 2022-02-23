# SPY-regression-hedge-portfolio
Analysis of S&amp;P500 hedge portfolio trading strategy based on a regression of company sector, size and style.

The aim of this project is to see if next day price can be predicted from todays price, sector returns, spy returns and investment style returns


We start by scraping the info on a list of companies in the S&P500 from the Morningstar website:

The data was scraped using pythons selenium package to open a chrome browser to open the Morningstar website corresponding to a specific stock, with the link “https://www.morningstar.com/stocks/{EXCHANGE}/{TICKER}/quote” where {EXCHANGE} is ‘xnys’ if the company is listed in the New York Stock Exchange and ‘xnas’ if the company is listed in the NASDAQ exchange. The website looks like so:
<img width="1046" alt="Tesla Inc TSLA" src="https://user-images.githubusercontent.com/87107274/155244890-d929852c-0848-483e-bc79-1c5db58a0db9.png">

From this table, the only data we need is the sector, and investment style
<img width="472" alt="Screen Shot 2022-02-23 at 1 05 32 PM" src="https://user-images.githubusercontent.com/87107274/155245134-03e4ab8a-c21a-43c8-8564-ea5bb45b5e03.png">
The HTML for this table was an unordered list, where each cell of the table was a <li> element containing a div with class=‘dp pair’. At this point I used BeautifulSoup to extract all elements with that div and class, and then isolated the sector and investment style data and saved it to a dictionary of form {’TSLA’ : {style: ‘Large Growth’, sector: ‘Consumer Cyclical’}}. This process is repeated for every ticker in the list and then it is all saved to stock_info.json

![Uploading 'AAP' ('sector' 'Consumer Cyclical', 'style' 'Mid Core'},.png…]()

creating a dataframe of prices returns, regression coefficients and predictions:
Using the information gathered in the first step, for each stock we download price information for the last 5 years, for both the stock, the S&P500 tracking index SPY, and the ETFs which correspond to the companies investment style and sector, then we feed this data into an ordinary least squares	regression model of the form:

_Prices =  B0*lagged prices + B1*SPY returns + B2*sector returns + B3*style returns + B4_

