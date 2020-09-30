import re
import requests
from URLHandler import URLHandler
from bs4 import BeautifulSoup

#html_string = BeautifulSoup(URLHandler('https://www.marketwatch.com/investing/stock/goog/financials'), "html.parser")
#html_string2 = BeautifulSoup(URLHandler('https://www.marketwatch.com/investing/stock/khc/profile'), 'html.parser')
#string = html_string.find_all('tr', attrs={'class': 'mainRow'})

def Average(lst):
    return sum(lst) / len(lst)

def MarKetWatch_Financials(string, valuename):
    all_data = []
    for a in string:
        netincome = {}
        netincome['name'] = a.td.text
        if netincome['name'] == valuename:
            netincome['data'] = str(re.findall(r"\[.*\]", str(a.td.findNext('td', attrs='miniGraphCell'))))
            for item in {'\[\'\[', '\]\'\]'}:
                netincome['data'] = re.sub(item, '', netincome['data'])
            netincome['data'] = netincome['data'].split(',')
            all_data.append(netincome)
    return all_data

def MarketWatch_NetIncome_Growth(string):
    data = MarKetWatch_Financials(string, 'Consolidated Net Income')
    NetIncome_Growth = "%.2f" % round(100*(int(data[0]['data'][4]) - int(data[0]['data'][0]))/int(data[0]['data'][0]))
    NetIncome_Growth_average = "%.2f" % round(Average([100*((int(data[0]['data'][i+1]) - int(data[0]['data'][i]))/int(data[0]['data'][i])) for i in range(0, 3)]), 2)
    r = [NetIncome_Growth, NetIncome_Growth_average]
    return r

#MarketWatch Profile
def Test2(string):
    base = string.find('div', attrs={'class': 'sixwide addgutter'})
    section = base.findAll('div', attrs={'class': 'section'})
    all_data = []
    for item in section:
        data = {}
        data['name'] = item.p.text
        data['value'] = item.p.findNext('p').text
        if data['name'] == 'P/E Current':
            all_data.append(data)
    return all_data
#print(Test2(html_string2)[0]['value'])
