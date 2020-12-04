from flask import Flask, render_template, request, redirect, url_for
from URLHandler import URLHandler
from MarketWatch02 import MarketWatch_Value_Growth, MarketWatch_Cash_Factor, MarketWatch_Dividends, MarketWatch_Profile
from MacroTrends import MacroTrends_RORE
from bs4 import BeautifulSoup
import pandas as pd
import re

# MarketWatch
def Read(url):
    stockname = url.replace('https://www.marketwatch.com/investing/stock/', '')
    string_financials = BeautifulSoup(URLHandler(str(url) + '/financials'), "html.parser")
    financials = string_financials.find_all('div', attrs={'class': 'cell__content fixed--cell'})
    string_balancesheet = BeautifulSoup(URLHandler(str(url) + '/financials/balance-sheet'), 'html.parser')
    balancesheet = string_balancesheet.find_all('div', attrs={'class': 'cell__content fixed--cell'})
    string_cashflow = BeautifulSoup(URLHandler(url + '/financials/cash-flow'), "html.parser")
    cashflow = string_cashflow.find_all('div', attrs={'class': 'cell__content fixed--cell'})
    string_profile = BeautifulSoup(URLHandler(str(url) + '/profile'), "html.parser")
    r = [stockname, financials, balancesheet, cashflow, string_profile]
    return r

#MacroTrends
def Read_MacroTrends(url):
    url_financial = url + 'financial-statements'
    url_cashflow = url + 'cash-flow-statement'
    #StringEPS0 = BeautifulSoup(URLHandler(url + 'financial-statements'), "html.parser")
    #StringEPS = StringEPS0.find_all('div', attrs={'id': 'row21jqxgrid'})
    #print(StringEPS)
    StringEPS0 = re.search('eps-earnings-per-share-diluted(.*)}];', URLHandler(url + 'financial-statements'))
    StringEPS = re.search('div>",(.*)}];', StringEPS0.group(0))

    if 'common-stock-dividends-paid' in URLHandler(url + 'cash-flow-statement'):
        StringDividends0 = re.search('common-stock-dividends-paid(.*)}];', URLHandler(url + 'cash-flow-statement'))
        StringDividends = re.search('/div>"(.*)}', StringDividends0.group(0))
    else:
        StringDividends0 = re.search('Common Stock Dividends Paid(.*)}];', URLHandler(url + 'cash-flow-statement'))
        StringDividends = re.search('popup_icon(.*)}', StringDividends0.group(0))
    r = [StringEPS, StringDividends]
    return r

app = Flask(__name__)

@app.route('/')
def student():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        listofurls = []
        for i in range(4):
            if request.form[f'Base_Link{i+1}'] != '':
                baseurl = request.form[f'Base_Link{i+1}']
                baseurl2 = request.form[f'MacroTrends_Link{i+1}']
                urls = [baseurl, baseurl2]
                print(urls)
                listofurls.append(urls)
        print(listofurls)

        #Years = int(request.form['Years'])
        NBShares = int(request.form['Number_Shares'])
        RealDiscountRate = float(request.form['RealDiscountRate'])
        AverageInflation = float(request.form['AverageInflation'])
        NominalDiscountRate = float(RealDiscountRate + AverageInflation)
        strNominalDiscountRate = str("Nominal Discount Rate is {}%".format(NominalDiscountRate))
        t = [['Stock', 'Net Income Growth 5 years', 'Net Income Growth Average', 'EPS Growth 5 years', 'EPS Growth Average', 'Current Liabilities/Current Cash factor', 'Total Liabilities/Total Cash factor', 'Price/Earnings', 'Total paid dividends', 'RORE last Year']]

        for item in listofurls:
            stockname = Read(item[0])[0]
            print(stockname)
            string_financials = Read(item[0])[1]
            string_balancesheet = Read(item[0])[2]
            string_cashflow = Read(item[0])[3]
            string_profile = Read(item[0])[4]

            # Net Income Growth
            try:
                r1 = '{}%'.format(MarketWatch_Value_Growth(string_financials, 'Consolidated Net Income')[0])
                r2 = '{}%'.format(MarketWatch_Value_Growth(string_financials, 'Consolidated Net Income')[1])
            except:
                r1 = 0
                r2 = 0
            # EPS Growth
            try:
                r3 = '{}%'.format(MarketWatch_Value_Growth(string_financials, 'EPS (Diluted)')[0])
                r4 = '{}%'.format(MarketWatch_Value_Growth(string_financials, 'EPS (Diluted)')[1])
            except:
                r3 = 0
                r4 = 0
            #Current Liabilities/Current Cash factor
            # Total Liabilities/Total Assets
            try:
                r5 = '{}%'.format(MarketWatch_Cash_Factor(string_balancesheet, 'Total Current Liabilities', 'Cash & Short Term Investments'))
                r6 = '{}%'.format(MarketWatch_Cash_Factor(string_balancesheet, 'Total Liabilities', 'Total Assets'))
            except:
                r5 = 0
                r6 = 0
            #Price per ernings
            try:
                r7 = '{}'.format(MarketWatch_Profile(string_profile, 'P/E Current')[0]['data'])
            except:
                   r7 = 0
            try:
                r8 = '{}'.format(MarketWatch_Dividends(string_cashflow, 'Cash Dividends Paid - Total'))
                print(r8)
            except:
                r8 = 0

            string_eps = Read_MacroTrends(item[1])[0]
            string_dividends = Read_MacroTrends(item[1])[1]

            try:
                r9 = '{}'.format(MacroTrends_RORE(string_eps, string_dividends)[0])
            except:
                r9 = 0

            r = [stockname, r1, r2, r3, r4, r5, r6, r7, r8, r9]
            t.append(r)

        # listyears = Years(string_financials)

        #format table data
        t = [x for x in t if str(x) != 'nan']
        df = pd.DataFrame(t, columns=t.pop(0))
        temp = df.to_dict('records')
        columnNames = df.columns.values

        return render_template("result.html", records=temp, colnames=columnNames, graphdata=0, labels='a', values='10')

if __name__ == '__main__':
    app.run(debug=True)
