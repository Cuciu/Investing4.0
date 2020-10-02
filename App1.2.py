from flask import Flask, render_template, request, redirect, url_for
from MarketWatch02 import MarketWatch_Value_Growth, MarketWatch_Cash_Factor, MarketWatch_Profile
from URLHandler import URLHandler
from bs4 import BeautifulSoup
import pandas as pd

def Read(url):
    stockname = url.replace('https://www.marketwatch.com/investing/stock/', '')
    string_financials = BeautifulSoup(URLHandler(str(url) + '/financials'), "html.parser")
    financials = string_financials.find_all('tr', attrs={'class': 'mainRow'})
    string_balancesheet = BeautifulSoup(URLHandler(str(url) + '/financials/balance-sheet'), 'html.parser')
    balancesheet = string_balancesheet.find_all('tr', attrs={'class': {'totalRow', 'mainRow', 'partialSum'}})
    string_profile = BeautifulSoup(URLHandler(str(url) + '/profile'), "html.parser")
    r = [stockname, financials, balancesheet, string_profile]
    return r

app = Flask(__name__)

@app.route('/')
def student():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        baseurl1 = request.form['Base_Link1']
        baseurl2 = request.form['Base_Link2']
        baseurl3 = request.form['Base_Link3']
        baseurl4 = request.form['Base_Link4']
        baseurl5 = request.form['Base_Link5']
        urls = [baseurl1, baseurl2, baseurl3, baseurl4, baseurl5]

        #Years = int(request.form['Years'])
        NBShares = int(request.form['Number_Shares'])
        RealDiscountRate = float(request.form['RealDiscountRate'])
        AverageInflation = float(request.form['AverageInflation'])
        NominalDiscountRate = float(RealDiscountRate + AverageInflation)
        strNominalDiscountRate = str("Nominal Discount Rate is {}%".format(NominalDiscountRate))
        t = [['Stock', 'Net Income Growth 5 years', 'Net Income Growth Average', 'EPS Growth 5 years', 'EPS Growth Average', 'Current Liabilities/Current Cash factor', 'Total Liabilities/Total Cash factor', 'Price/Earnings']]

        for item in urls:
            stockname = Read(item)[0]
            print(stockname)
            string_financials = Read(item)[1]
            string_balancesheet = Read(item)[2]
            string_profile = Read(item)[3]

            # Net Income Growth
            r1 = '{}%'.format(MarketWatch_Value_Growth(string_financials, 'Consolidated Net Income')[0])
            r2 = '{}%'.format(MarketWatch_Value_Growth(string_financials, 'Consolidated Net Income')[1])
            # EPS Growth
            r3 = '{}%'.format(MarketWatch_Value_Growth(string_financials, ' EPS (Diluted)')[0])
            r4 = '{}%'.format(MarketWatch_Value_Growth(string_financials, ' EPS (Diluted)')[1])
            #Current Liabilities/Current Cash factor
            r5 = '{}%'.format(MarketWatch_Cash_Factor(string_balancesheet, ' Total Current Liabilities', ' Cash & Short Term Investments'))
            #Total Liabilities/Total Assets
            r6 = '{}%'.format(MarketWatch_Cash_Factor(string_balancesheet, ' Total Liabilities', ' Total Assets'))
            #Price per ernings
            r7 = '{}'.format(MarketWatch_Profile(string_profile, 'P/E Current')[0]['data'])

            r = [stockname, r1, r2, r3, r4, r5, r6, r7]
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
