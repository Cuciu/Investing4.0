import re
from URLHandler import URLHandler
from bs4 import BeautifulSoup

years = []

#html_string = BeautifulSoup(URLHandler('https://www.marketwatch.com/investing/stock/goog/financials'), "html.parser")

def Average(lst):
    return sum(lst) / len(lst)

def Format(string):
    lst = []
    formated_lst = []
    for div in string.find_all('div', {'class': 'miniGraph'}):
        lst.append(div)
    for x in lst:
        b = re.findall(r'\[(.*)\]', str(x))
        b2 = (str(b).replace("['", '').replace("']", '')).split(sep=',')
        formated_lst.append(b2)
    return formated_lst
#print(Format(html_string))

def MarketWatch_Financials(html_string):
    data = Format(html_string)
    #Net Income
    l_netincome = [float(x) for x in data[36]]
    netincome_growth_5years = "%.2f" % round(100*(int(l_netincome[4]) - l_netincome[0])/l_netincome[0], 2)
    netincome_growth_average = "%.2f" % round(Average([100*(int(l_netincome[i+1]) - l_netincome[i])/l_netincome[i] for i in range(0,4)]),2)
    #EPS
    l_eps = [float(x) for x in data[48]]
    eps_growth_5years = "%.2f" % round(100*(int(l_eps[4]) - l_eps[0])/l_eps[0], 2)
    eps_growth_average = "%.2f" % round(Average([100 * (int(l_eps[i + 1]) - l_eps[i]) / l_eps[i] for i in range(0, 4)]), 2)
    r = [netincome_growth_5years, netincome_growth_average, eps_growth_5years, eps_growth_average, l_eps[4]]
    return r

def MarketWatch_BalanceSheet(html_string2):
    data = Format(html_string2)
    #Current Liabilities / Current Cash Factor
    l_cash = [float(x) for x in data[0]]  #Total Current Assets
    l_current_liabilities = [float(x) for x in data[47]] # Total Current Liabilities
    f_current_liabilites_cash = "%.2f" % round(100*l_current_liabilities[4]/l_cash[4])
    #Total Liabilities / Total Assets Factor
    l_total_assets = [float(x) for x in data[35]]    #Total Assets
    l_total_liabilities = [float(x) for x in data[60]] #Total Liabilities
    f_toatl_liabilities_assets = "%.2f" % round(100*l_total_liabilities[4]/l_total_assets[4])
    r = [f_current_liabilites_cash, f_toatl_liabilities_assets]
    return r

def CurrentPrice(string):
    CurrentPrice_str = string.find_all('p', {'class': 'data bgLast'})
    CurrentPrice0 = re.findall('<p class="data bgLast">(.*)</p>]', str(CurrentPrice_str))
    CurrentPrice = float(str(CurrentPrice0).replace("['", '').replace("']", '').replace(',', ''))
    return CurrentPrice

def MarketWatch_PricePerEarnings(string):
    PricePerEarnings = "%.2f" % round(CurrentPrice(string)/MarketWatch_Financials(string)[4])
    return PricePerEarnings
#print(PricePerEarnings(html_string))

def Years(string):
    stable = string.find('table')
    header = stable.findAll('th')
    headers = [th.text for th in header]
    for i in range(1,6):
        years.append(headers[i])
    return years

#print(Years(html_string))
