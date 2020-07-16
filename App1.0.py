rom flask import Flask, render_template, request, redirect, url_for
from MarketWatch import Years, MarketWatch_Financials, MarketWatch_BalanceSheet
from URLHandler import URLHandler
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def student():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        baseurl = request.form['Base_Link']
        Years = int(request.form['Years'])
        NBShares = int(request.form['Number_Shares'])
        RealDiscountRate = float(request.form['RealDiscountRate'])
        AverageInflation = float(request.form['AverageInflation'])
        NominalDiscountRate = float(RealDiscountRate + AverageInflation)
        strNominalDiscountRate = str("Nominal Discount Rate is {}%".format(NominalDiscountRate))

        string_financials = BeautifulSoup(URLHandler(baseurl + '/financials'), "html.parser")
        string_balancesheet = BeautifulSoup(URLHandler(baseurl + '/financials/balance-sheet'), 'html.parser')

        r1 = 'Net Income Growth 5 years: {}%'.format(MarketWatch_Financials(string_financials)[0])
        r2 = 'Net Income Growth Average: {}%'.format(MarketWatch_Financials(string_financials)[1])
        r3 = 'EPS Growth 5 years: {}%'.format(MarketWatch_Financials(string_financials)[2])
        r4 = 'EPS Growth Average: {}%'.format(MarketWatch_Financials(string_financials)[1])
        r5 = 'Current Liabilities/Current Cash factor: {}%'.format(MarketWatch_BalanceSheet(string_balancesheet)[0])
        r6 = 'Total Liabilities/Total Cash factor: {}%'.format(MarketWatch_BalanceSheet(string_balancesheet)[1])
        # listyears = Years(string_financials)

        r = [r1, r2, r3, r4, r5, r6]
        print(r)
        return render_template("result.html", result=r, graphdata=0, labels='a', values='10')


if __name__ == '__main__':
    app.run(debug=True)

