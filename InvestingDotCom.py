



investingfinancials = 'https://www.investing.com/equities/cancom-ag-ratios'
insoup = BeautifulSoup(URLHandler(investingfinancials), 'html.parser')
stable = insoup.find('table')
header = stable.findAll('th')
headers = [th.text for th in header]
print(headers)
for i in range(1,4):
    years.append(headers[i])
print(years)