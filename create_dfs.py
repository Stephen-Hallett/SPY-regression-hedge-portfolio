import numpy as np
import os
import json
import yfinance as yf
import pandas as pd
import statsmodels.api as sm


def save_dict_as_JSON(dictionary, path, name):
    jsondict = json.dumps(dictionary)
    file = os.path.join(path, name+".json")
    with open(file, 'w') as f:
        print('writing information to ' + name + '.json')
        f.write(jsondict)
        f.close()

def open_JSON(file):
    if os.path.isfile(file):
        with open(file) as jsonfile:
            print('opening '+file)
            data = json.load(jsonfile)
        jsonfile.close()
        return data
    else:
        print("couldn't find file: "+file)

def save_regression_to_CSV(symbols):
    #get stock info of the form: {"SBUX": {"sector": "Consumer Cyclical", "industry": "Restaurants", "style": "Large Growth"}
    stock_info = open_JSON('/Volumes/EMTECC450/CodingProjects/AlgoTrading/IndustryRegression/stock_info.json')
    
    #get dictionaries with etfs corresponding to style and sector, i.e. "Large Growth": "VUG", "Large Value": "VTV" etc.
    sector_etfs = open_JSON('/Volumes/EMTECC450/CodingProjects/AlgoTrading/IndustryRegression/sector_etfs.json')
    style_etfs = open_JSON('/Volumes/EMTECC450/CodingProjects/AlgoTrading/IndustryRegression/style_etfs.json')
    
    for symbol in symbols:
        #only get new data if csv doesn't already exist
        if not os.path.isfile('/Volumes/EMTECC450/CodingProjects/AlgoTrading/IndustryRegression/symbolCSVs/{}_df.csv'.format(symbol)):
            try:
                df = pd.DataFrame()
                #save stocks sector and style etfs as their own variables
                sector_etf = sector_etfs[stock_info[symbol]["sector"]]
                style_etf = style_etfs[stock_info[symbol]["style"]]

                #for sector, style, price and S&P500, download price data for the last 5 years,
                #and calculate returns and lagged returns

                df['sector prices'] = yf.download(sector_etf, period='5y', interval='1d')['Adj Close']
                df['sector lagged prices'] = df['sector prices'].shift(1)
                df['sector returns'] = df['sector prices']/df['sector lagged prices'] -1
                df['sector lagged returns'] = df['sector returns'].shift(1)

                df['prices'] = yf.download(symbol, period='5y', interval='1d')['Adj Close']
                df['lagged prices'] = df['prices'].shift(1)
                df['returns'] = df['prices']/df['lagged prices'] -1
                df['lagged returns'] = df['returns'].shift(1)

                df['spy prices'] = yf.download('SPY', period='5y', interval='1d')['Adj Close']
                df['spy lagged prices'] = df['spy prices'].shift(1)
                df['spy returns'] = df['spy prices']/df['spy lagged prices'] -1
                df['spy lagged returns'] = df['spy returns'].shift(1)

                df['style prices'] = yf.download(style_etf, period='5y', interval='1d')['Adj Close']
                df['style lagged prices'] = df['style prices'].shift(1)
                df['style returns'] = df['style prices']/df['style lagged prices'] -1
                df['style lagged returns'] = df['style returns'].shift(1)
                
                df['intercept'] = np.ones(df['returns'].shape)

                df = df.dropna() #delete first couple of rows with NA values due to calculating lagged returns
                
                #initialise empty columns for predictions and coefficients
                df['prediction'] = np.full(df['returns'].shape, None)
                df['price coef'] = np.full(df['returns'].shape, None)
                df['sector coef'] = np.full(df['returns'].shape, None)
                df['spy coef'] = np.full(df['returns'].shape, None)
                df['style coef'] = np.full(df['returns'].shape, None)

                for i,index in enumerate(df.index): #index is a datetime object, this is the row name for each row of the df
                    if i > 251: #generate new coefficients and prediction based on a years data, only start once i > 251
                        x = df[['lagged prices', 'sector lagged returns', 'style lagged returns', 'spy lagged returns', 'intercept']][i-252:i]
                        y = df['prices'][i-252:i]
                        regr = sm.OLS(y,x) #x and y data is everything in a 252 day period up to but not including i so there is no bias.
                        results = regr.fit() #fit OLS regression
                        coefs = [coef for coef in results.params]
                        df.loc[index,['price coef','sector coef','style coef', 'spy coef','intercept']] = coefs
                        df.loc[index,'prediction'] = sum(np.array(coefs)*np.array(df.loc[index,['lagged prices','sector lagged returns', 'style lagged returns', 'spy lagged returns', 'intercept']])) #prediction calculated by multiplying coefficients wit data values at current day

                df['diff'] = df['prediction'] - df['lagged prices'] 
                df['diff %'] = df['diff']/df['lagged prices'] #diff is positive if regression predicts a gain the next day
                
                #save dataframe to csv of form 'symbol_df.csv'
                filename = '/Volumes/EMTECC450/CodingProjects/AlgoTrading/IndustryRegression/symbolCSVs/{}_df.csv'.format(symbol)
                print('saving {} data to filename {}'.format(symbol,filename))
                df.to_csv(filename)
            except Exception as e:
                print('-'*26)
                print("ERROR: {}".format(e))
                print('-'*26)
        else:
            print('{}_df is already saved!'.format(symbol))


symbols = ['MMM', 'AOS', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADBE', 'AAP', 'AMD', 'AES', 'AFL', 'A', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALXN', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'ANTM', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'BKR', 'BLL', 'BAC', 'BAX', 'BDX', 'BBY', 'BIO', 'BIIB', 'BLK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'CHRW', 'COG', 'CDNS', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CAT', 'CBRE', 'CE', 'CNP', 'CF', 'CHTR', 'CMG', 'CHD', 'CINF', 'CSCO', 'CFG', 'CME', 'KO', 'CL', 'CMA', 'COP', 'STZ', 'GLW', 'COST', 'CSX', 'CVS', 'DHR', 'DVA', 'DAL', 'DVN', 'FANG', 'DFS', 'DISCK', 'DG', 'D', 'DOV', 'DTE', 'DRE', 'DXC', 'ETN', 'ECL', 'EW', 'EMR', 'ETR', 'EFX', 'EQR', 'EL', 'RE', 'ES', 'EXPE', 'EXR', 'FFIV', 'FAST', 'FDX', 'FITB', 'FE', 'FLT', 'FLS', 'F', 'FTV', 'FOXA', 'BEN', 'GPS', 'IT', 'GE', 'GM', 'GILD', 'GL', 'GWW', 'HBI', 'HAS', 'PEAK', 'HES', 'HLT', 'HOLX', 'HON', 'HST', 'HPQ', 'HBAN', 'IEX', 'INFO', 'ILMN', 'IR', 'ICE', 'IFF', 'IPG', 'ISRG', 'IPGP', 'IRM', 'JKHY', 'SJM', 'JCI', 'JNPR', 'K', 'KEYS', 'KIM', 'KLAC', 'KR', 'LHX', 'LRCX', 'LVS', 'LDOS', 'LLY', 'LIN', 'LKQ', 'L', 'LUMN', 'MTB', 'MPC', 'MAR', 'MLM', 'MA', 'MKC', 'MCK', 'MRK', 'MTD', 'MCHP', 'MSFT', 'MHK', 'MDLZ', 'MCO', 'MSI', 'NDAQ', 'NFLX', 'NEM', 'NWS', 'NLSN', 'NI', 'NTRS', 'NLOK', 'NOV', 'NUE', 'NVR', 'OXY', 'OMC', 'ORCL', 'PCAR', 'PH', 'PAYC', 'PNR', 'PEP', 'PRGO', 'PM', 'PNW', 'PNC', 'PPG', 'PFG', 'PGR', 'PRU', 'PSA', 'PVH', 'QCOM', 'DGX', 'RJF', 'O', 'REGN', 'RSG', 'RHI', 'ROL', 'ROST', 'SPGI', 'SBAC', 'STX', 'SRE', 
'SHW', 'SWKS', 'SNA', 'LUV', 'SBUX', 'STE', 'SIVB', 'SNPS', 'TMUS', 'TTWO', 'TGT', 'FTI', 'TFX', 'TSLA', 'TXT', 'CLX', 'HSY', 'TRV', 'TMO', 'TSCO', 'TDG', 'TFC', 'TYL', 'USB', 'ULTA', 'UA', 'UAL', 'URI', 'UHS', 'VLO', 'VTR', 'VRSK', 'VRTX', 'VIAC', 'V', 'VNO', 'VMC', 'WRB', 'WBA', 'WMT', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WU', 'WAB', 'WRK', 'WY', 'WHR', 'WMB', 'WLTW', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']

if __name__ == '__main__':
    save_regression_to_CSV(symbols)