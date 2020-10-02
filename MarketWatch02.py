import re
import requests
from URLHandler import URLHandler
from bs4 import BeautifulSoup

#html_string = BeautifulSoup(URLHandler('https://www.marketwatch.com/investing/stock/goog/financials'), "html.parser")
#html_string2 = BeautifulSoup(URLHandler('https://www.marketwatch.com/investing/stock/khc/profile'), 'html.parser')
#html_string2 = BeautifulSoup(URLHandler('https://www.marketwatch.com/investing/stock/goog/financials/balance-sheet'), 'html.parser')
#string_balancesheet = html_string2.find_all('tr', attrs={'class': {'totalRow', 'mainRow', 'partialSum'}})
#string = BeautifulSoup(URLHandler('https://www.marketwatch.com/investing/stock/goog/profile'), "html.parser")

def Average(lst):
    return sum(lst) / len(lst)

def MarKetWatch_Financials(string, valuename):
    all_data = []
    for a in string:
        value = {}
        value['name'] = a.td.text
        if value['name'] == valuename:
            value['data'] = str(re.findall(r"\[.*\]", str(a.td.findNext('td', attrs='miniGraphCell'))))
            for item in {'\[\'\[', '\]\'\]'}:
                value['data'] = re.sub(item, '', value['data'])
            value['data'] = value['data'].split(',')
            all_data.append(value)
    return all_data

def MarketWatch_Value_Growth(string, value):
    data = MarKetWatch_Financials(string, value)
    Value_Growth = "%.2f" % round(100*(float(data[0]['data'][4]) - float(data[0]['data'][0]))/float(data[0]['data'][0]))
    Value_Growth_average = "%.2f" % round(Average([100*((float(data[0]['data'][i+1]) - float(data[0]['data'][i]))/float(data[0]['data'][i])) for i in range(0, 4)]), 2)
    r = [Value_Growth, Value_Growth_average]
    return r

def MarketWatch_Cash_Factor(string, value1, value2):
    cash = MarKetWatch_Financials(string, value2)
    liabilities = MarKetWatch_Financials(string, value1)
    factor = "%.2f" % round(100*(float(liabilities[0]['data'][4])/float(cash[0]['data'][4])))
    return factor

#MarketWatch Profile
def MarketWatch_Profile(string, value):
    base = string.find('div', attrs={'class': 'sixwide addgutter'})
    section = base.findAll('div', attrs={'class': 'section'})
    all_data = []
    for item in section:
        data = {}
        data['name'] = item.p.text
        data['data'] = item.p.findNext('p').text
        if data['name'] == value:
            all_data.append(data)
    return all_data
