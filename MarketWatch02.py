import re
import requests
from URLHandler import URLHandler
from bs4 import BeautifulSoup

#html_string = BeautifulSoup(URLHandler('https://www.marketwatch.com/investing/stock/goog/financials'), "lxml")
#financials = html_string.find_all('tr', attrs={'class': 'table__row'})
#test = html_string.find_all('div', attrs={'class': 'cell__content fixed--cell'})

def Average(lst):
    return sum(lst) / len(lst)

def MarKetWatch_Financials(string, valuename):
    all_data = []
    for a in string:
        value = {}
        value['name'] = a.text
        if value['name'] == valuename:
            try:
                value['data'] = a.find_next('div', attrs={'class': 'chart--financials js-financial-chart'})['data-chart-data']
                value['data'] = value['data'].split(',')
                print(value['data'])
            except:
                value['data'] = 0
            all_data.append(value)
    return all_data
#print(MarKetWatch_Financials(test, 'Consolidated Net Income'))

def MarketWatch_Value_Growth(string, value):
    data = MarKetWatch_Financials(string, value)
    try:
        Value_Growth = "%.2f" % round(100*(float(data[0]['data'][4]) - float(data[0]['data'][0]))/float(data[0]['data'][0]))
        Value_Growth_average = "%.2f" % round(Average([100*((float(data[0]['data'][i+1]) - float(data[0]['data'][i]))/float(data[0]['data'][i])) for i in range(0, 4)]), 2)
    except:
        Value_Growth = 0
        Value_Growth_average = 0
    r = [Value_Growth, Value_Growth_average]
    return r

def MarketWatch_Cash_Factor(string, value1, value2):
    cash = MarKetWatch_Financials(string, value2)
    liabilities = MarKetWatch_Financials(string, value1)
    factor = "%.2f" % round(100*(float(liabilities[0]['data'][4])/float(cash[0]['data'][4])))
    return factor

def MarketWatch_Dividends(string, valuename):
    dividend = MarKetWatch_Financials(string, valuename)
    print(dividend)
    return dividend[0]['data'][0]

#MarketWatch Profile
def MarketWatch_Profile(string, value):
    base = string.find('div', attrs={'class': 'element element--table'})
    section = base.findAll('tr', attrs={'class': 'table__row'})
    all_data = []
    for item in section:
        data = {}
        try:
            data['name'] = item.find('td', attrs={'class': 'table__cell w75'}).text
            data['data'] = item.find('td', attrs={'class': 'table__cell w25'}).text
        except AttributeError:
            data['name'] = 0
            data['data'] = 0
        if data['name'] == value:
            all_data.append(data)
    return all_data

#RORE Last Year
#RORE Last 5 years

#NPV 5 years
#Overpriced formula

