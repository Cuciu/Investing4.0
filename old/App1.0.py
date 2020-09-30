from flask import Flask, render_template, request, redirect, url_for
from MarketWatch import Years, MarketWatch_Financials, MarketWatch_BalanceSheet, MarketWatch_PricePerEarnings
from URLHandler import URLHandler
from bs4 import BeautifulSoup
import pandas as pd

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
        baseurl = [baseurl1, baseurl2, baseurl3, baseurl4, baseurl5]

        Years = int(request.form['Years'])
        NBShares = int(request.form['Number_Shares'])
        RealDiscountRate = float(request.form['RealDiscountRate'])
        AverageInflation = float(request.form['AverageInflation'])
        NominalDiscountRate = float(RealDiscountRate + AverageInflation)
        strNominalDiscountRate = str("Nominal Discount Rate is {}%".format(NominalDiscountRate))
        t = [['Stock', 'Net Income Growth 5 years', 'Net Income Growth Average', 'EPS Growth 5 years', 'EPS Growth Average', 'Current Liabilities/Current Cash factor', 'Total Liabilities/Total Cash factor', 'Price/Earnings']]
        for item in baseurl:
            stockname = item.replace('https://www.marketwatch.com/investing/stock/','')
            string_financials = BeautifulSoup(URLHandler(item + '/financials'), "html.parser")
            string_balancesheet = BeautifulSoup(URLHandler(item + '/financials/balance-sheet'), 'html.parser')

            r1 = '{}%'.format(MarketWatch_Financials(string_financials)[0]) #Net Income Growth 5 years
            r2 = '{}%'.format(MarketWatch_Financials(string_financials)[1]) #Net Income Growth Average
            r3 = '{}%'.format(MarketWatch_Financials(string_financials)[2]) #EPS Growth 5 years
            r4 = '{}%'.format(MarketWatch_Financials(string_financials)[1]) #EPS Growth Average
            r5 = '{}%'.format(MarketWatch_BalanceSheet(string_balancesheet)[0]) #Current Liabilities/Current Cash factor
            r6 = '{}%'.format(MarketWatch_BalanceSheet(string_balancesheet)[1]) #Total Liabilities/Total Cash factor
            r7 = '{}'.format(MarketWatch_PricePerEarnings(string_financials)) #Price per ernings

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
