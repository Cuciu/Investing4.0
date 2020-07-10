from flask import Flask, render_template, request, redirect, url_for
from MarketWatch import Years, MarketWatch_Financials, MarketWatch_BalanceSheet
from URLHandler import URLHandler
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def student():
   return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
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

      string_financials= BeautifulSoup(URLHandler(baseurl + '/financials'),'html.parser')
      string_balancesheet = BeautifulSoup(URLHandler(baseurl + '/financials/balance-sheet'), 'html.parser')

      r1 = MarketWatch_Financials(string_financials)
      r2 = MarketWatch_BalanceSheet(string_balancesheet)
      #listyears = Years(string_financials)

      r = ['{}'.format(r1), '{}'.format(r2)]
      return render_template("result.html", result=r)

if __name__ == '__main__':
   app.run(debug = True)




#cells = []
#rows = stable.findAll('tr')
#for tr in rows:
    # Process the body of the table
    #td = tr.findAll('td')
    #for t in td:
        #a = re.findall('>(.*)<', str(t))
        #b = a[0]
        #cells.append(b)
