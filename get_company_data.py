import json
from time import sleep
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from pprint import pprint
import re

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
        print("couldn't find file: "+file, '\nreturning empty dict.')
        return {}

def get_info(url,options):
    data = {}
    driver = webdriver.Chrome('/Volumes/EMTECC450/CodingProjects/AlgoTrading/macdriver/chromedriver', options=options)
    driver.get(url) #in this case the URL is a morningstar page of a stock
    sleep(8) #allow time for page to load all data.
    html = driver.execute_script('return document.body.innerHTML;')
    driver.close()
    soup = BeautifulSoup(html, "lxml")
    info=soup.find_all("div", {"class": "dp-pair"}) #all data we need is within a dp-pair class.
    info = [re.sub("  +", " ", re.sub("\n", "", data.text)).strip() for data in info] #replace all \n characters with "" and then replace all multi spaces with a single space.
    pprint(info)
    #the info list has the form ["Sector xxx", "Industry xxx", "Investment Style xxx", ...]
    data["sector"] = [item.split("Sector ")[1] for item in info if "Sector " in item][0] 
    data["style"] = [item.split("Investment Style ")[1] for item in info if "Investment Style " in item][0]
    return data

def get_industry_info():
    options = webdriver.ChromeOptions() #standard chome options
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    #open all the data we already have so we can check
    information = open_JSON('/Volumes/EMTECC450/CodingProjects/AlgoTrading/IndustryRegression/stock_info.json')
    exchange = open_JSON('/Volumes/EMTECC450/CodingProjects/AlgoTrading/IndustryRegression/testexchange_info.json')

    for symbol in symbols:
        if symbol not in information.keys(): #skip if we already have stocks information
            information[symbol] = {}
            if symbol in exchange.keys():
                url='https://www.morningstar.com/stocks/{}/{}/quote'.format(exchange[symbol],symbol.lower())
                information[symbol] = get_info(url,options)
            else: #if we don't yet know whether the stock is listed on the NASDAQ or the NYSE, we need to try both URLs to see which one works, and then save the info for future use.
                try:
                    url='https://www.morningstar.com/stocks/xnys/{}/quote'.format(symbol.lower())
                    information[symbol] = get_info(url,options)
                    exchange[symbol] = 'xnys'
                except:
                    try:
                        url='https://www.morningstar.com/stocks/xnas/{}/quote'.format(symbol.lower())
                        information[symbol] = get_info(url,options)
                        exchange[symbol] = 'xnas'
                    except Exception as e:
                        print('ERROR: {}'.format(e))
            pprint(information[symbol])
    #once everything is downloaded we can save the info to json files.
    save_dict_as_JSON(exchange,'/Volumes/EMTECC450/CodingProjects/AlgoTrading/IndustryRegression/','testexchange_info')
    save_dict_as_JSON(information,'/Volumes/EMTECC450/CodingProjects/AlgoTrading/IndustryRegression/','stock_info')




if __name__ == "__main__":
    #list of symbols in the S&P500 that I scraped in a previous project
    symbols = ['MMM', 'AOS', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADBE', 'AAP', 'AMD', 'AES', 'AFL', 'A', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALXN', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'ANTM', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'BKR', 'BLL', 'BAC', 'BAX', 'BDX', 'BBY', 'BIO', 'BIIB', 'BLK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'CHRW', 'COG', 'CDNS', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CAT', 'CBRE', 'CE', 'CNP', 'CF', 'CHTR', 'CMG', 'CHD', 'CINF', 'CSCO', 'CFG', 'CME', 'KO', 'CL', 'CMA', 'COP', 'STZ', 'GLW', 'COST', 'CSX', 'CVS', 'DHR', 'DVA', 'DAL', 'DVN', 'FANG', 'DFS', 'DISCK', 'DG', 'D', 'DOV', 'DTE', 'DRE', 'DXC', 'ETN', 'ECL', 'EW', 'EMR', 'ETR', 'EFX', 'EQR', 'EL', 'RE', 'ES', 'EXPE', 'EXR', 'FFIV', 'FAST', 'FDX', 'FITB', 'FE', 'FLT', 'FLS', 'F', 'FTV', 'FOXA', 'BEN', 'GPS', 'IT', 'GE', 'GM', 'GILD', 'GL', 'GWW', 'HBI', 'HAS', 'PEAK', 'HES', 'HLT', 'HOLX', 'HON', 'HST', 'HPQ', 'HBAN', 'IEX', 'INFO', 'ILMN', 'IR', 'ICE', 'IFF', 'IPG', 'ISRG', 'IPGP', 'IRM', 'JKHY', 'SJM', 'JCI', 'JNPR', 'K', 'KEYS', 'KIM', 'KLAC', 'KR', 'LHX', 'LRCX', 'LVS', 'LDOS', 'LLY', 'LIN', 'LKQ', 'L', 'LUMN', 'MTB', 'MPC', 'MAR', 'MLM', 'MA', 'MKC', 'MCK', 'MRK', 'MTD', 'MCHP', 'MSFT', 'MHK', 'MDLZ', 'MCO', 'MSI', 'NDAQ', 'NFLX', 'NEM', 'NWS', 'NLSN', 'NI', 'NTRS', 'NLOK', 'NOV', 'NUE', 'NVR', 'OXY', 'OMC', 'ORCL', 'PCAR', 'PH', 'PAYC', 'PNR', 'PEP', 'PRGO', 'PM', 'PNW', 'PNC', 'PPG', 'PFG', 'PGR', 'PRU', 'PSA', 'PVH', 'QCOM', 'DGX', 'RJF', 'O', 'REGN', 'RSG', 'RHI', 'ROL', 'ROST', 'SPGI', 'SBAC', 'STX', 'SRE', 
    'SHW', 'SWKS', 'SNA', 'LUV', 'SBUX', 'STE', 'SIVB', 'SNPS', 'TMUS', 'TTWO', 'TGT', 'FTI', 'TFX', 'TSLA', 'TXT', 'CLX', 'HSY', 'TRV', 'TMO', 'TSCO', 'TDG', 'TFC', 'TYL', 'USB', 'ULTA', 'UA', 'UAL', 'URI', 'UHS', 'VLO', 'VTR', 'VRSK', 'VRTX', 'VIAC', 'V', 'VNO', 'VMC', 'WRB', 'WBA', 'WMT', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WU', 'WAB', 'WRK', 'WY', 'WHR', 'WMB', 'WLTW', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']
    get_industry_info()