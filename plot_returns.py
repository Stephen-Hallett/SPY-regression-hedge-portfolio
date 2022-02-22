import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import symbols

def plot_returns(symbols,size):
    #initialise empty dataframes for predicted daily returns and actual daily returns
    predicted_returns_df = pd.DataFrame()
    returns_df = pd.DataFrame()

    #for each stock add its returns and prediction data to 
    for symbol in symbols:
        filename = '/Volumes/EMTECC450/CodingProjects/AlgoTrading/IndustryRegression/symbolCSVs/{}_df.csv'.format(symbol)
        if os.path.isfile(filename):
            data = pd.read_csv(filename)
            returns_df[symbol] = data['returns']
            predicted_returns_df[symbol] = data['predicted returns']

    positions_array = np.zeros(predicted_returns_df.shape) #initialise positions array where 0 means no action, 1 means long and -1 means short
    predicted_returns_array = predicted_returns_df.to_numpy() #convert df to array so we can  easily iterate over rows

    for i in range(predicted_returns_array.shape[0]): #for i in range(num rows)
        row = list(predicted_returns_array[i,])

        tup_list = [tup[::-1] for tup in enumerate(row)] #create list of tuples of form (return, index) for each stock in the row
        sorted_tups = sorted(tup_list) #sort tuples by returns, from lowest to highest
        
        #we want to long and short the same amount of stocks to have a hedge portfolio, the amount of each is the size parameter.
        #we want to short the first size stocks and long the last size stocks in sorted tups.
        for j in range(size):
            short = sorted_tups[j][1] #take the index of the stock with lowest returns
            long = sorted_tups[-(j+1)][1] #take index of the stock with lowest returns
            positions_array[i,short] = -1 #set the short index to -1
            positions_array[i,long] = 1 #set long index to 1

    returns_array = returns_df.to_numpy()
    profit = returns_array*positions_array #multiply returns with positions element-wise

    #now create daily profit array by taking the average profit across all 2*size positions, and adding 1 so daily returns can be compounded
    daily_profit = np.array([(sum(profit[i,])/(size*2))+1 for i in range(profit.shape[0])])
    compounding_profit = np.cumprod(daily_profit)

    plt.plot(list(range(compounding_profit.shape[0])), list(compounding_profit))
    plt.show()



symbols = ['MMM', 'AOS', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADBE', 'AAP', 'AMD', 'AES', 'AFL', 'A', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALXN', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'ANTM', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'BKR', 'BLL', 'BAC', 'BAX', 'BDX', 'BBY', 'BIO', 'BIIB', 'BLK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'CHRW', 'COG', 'CDNS', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CAT', 'CBRE', 'CE', 'CNP', 'CF', 'CHTR', 'CMG', 'CHD', 'CINF', 'CSCO', 'CFG', 'CME', 'KO', 'CL', 'CMA', 'COP', 'STZ', 'GLW', 'COST', 'CSX', 'CVS', 'DHR', 'DVA', 'DAL', 'DVN', 'FANG', 'DFS', 'DISCK', 'DG', 'D', 'DOV', 'DTE', 'DRE', 'DXC', 'ETN', 'ECL', 'EW', 'EMR', 'ETR', 'EFX', 'EQR', 'EL', 'RE', 'ES', 'EXPE', 'EXR', 'FFIV', 'FAST', 'FDX', 'FITB', 'FE', 'FLT', 'FLS', 'F', 'FTV', 'FOXA', 'BEN', 'GPS', 'IT', 'GE', 'GM', 'GILD', 'GL', 'GWW', 'HBI', 'HAS', 'PEAK', 'HES', 'HLT', 'HOLX', 'HON', 'HST', 'HPQ', 'HBAN', 'IEX', 'INFO', 'ILMN', 'IR', 'ICE', 'IFF', 'IPG', 'ISRG', 'IPGP', 'IRM', 'JKHY', 'SJM', 'JCI', 'JNPR', 'K', 'KEYS', 'KIM', 'KLAC', 'KR', 'LHX', 'LRCX', 'LVS', 'LDOS', 'LLY', 'LIN', 'LKQ', 'L', 'LUMN', 'MTB', 'MPC', 'MAR', 'MLM', 'MA', 'MKC', 'MCK', 'MRK', 'MTD', 'MCHP', 'MSFT', 'MHK', 'MDLZ', 'MCO', 'MSI', 'NDAQ', 'NFLX', 'NEM', 'NWS', 'NLSN', 'NI', 'NTRS', 'NLOK', 'NOV', 'NUE', 'NVR', 'OXY', 'OMC', 'ORCL', 'PCAR', 'PH', 'PAYC', 'PNR', 'PEP', 'PRGO', 'PM', 'PNW', 'PNC', 'PPG', 'PFG', 'PGR', 'PRU', 'PSA', 'PVH', 'QCOM', 'DGX', 'RJF', 'O', 'REGN', 'RSG', 'RHI', 'ROL', 'ROST', 'SPGI', 'SBAC', 'STX', 'SRE', 
'SHW', 'SWKS', 'SNA', 'LUV', 'SBUX', 'STE', 'SIVB', 'SNPS', 'TMUS', 'TTWO', 'TGT', 'FTI', 'TFX', 'TSLA', 'TXT', 'CLX', 'HSY', 'TRV', 'TMO', 'TSCO', 'TDG', 'TFC', 'TYL', 'USB', 'ULTA', 'UA', 'UAL', 'URI', 'UHS', 'VLO', 'VTR', 'VRSK', 'VRTX', 'VIAC', 'V', 'VNO', 'VMC', 'WRB', 'WBA', 'WMT', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WU', 'WAB', 'WRK', 'WY', 'WHR', 'WMB', 'WLTW', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']


if __name__ == "__main__":
    plot_returns(symbols, size=5)