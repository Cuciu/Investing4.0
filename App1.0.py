from flask import Flask, render_template, request, redirect, url_for
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

        r1 = 'Finalncials {}%'.format(MarketWatch_Financials(string_financials))
        r2 = 'Balance-sheet {}%'.format(MarketWatch_BalanceSheet(string_balancesheet))
        # listyears = Years(string_financials)

        r = [r1, r2]
        print(r)
        return render_template("result.html", result=r, graphdata=0, labels='a', values='10')


if __name__ == '__main__':
    app.run(debug=True)
