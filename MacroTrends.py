import re
import numpy as np

def Convert(string):
    li = list(string.split(","))
    return li

def MacroTrends_RORE(StringEPS, StringDividends, StringCurrentPrice, StringPrice,  NBShares, RealDiscountRate, AverageInflation):

    Years = 5
    #EPS
    EPS = str(StringEPS.group(1).replace('"', ''))
    a1 = EPS.count(':')
    b1 = Convert(EPS)
    listofEPS = []
    listofEPSGrowth = []
    for i in range(0, a1):
        var = b1[i]
        c1 = list(var.split(":"))
        e1, f1 = [c1[j] for j in (0, 1)]
        listofEPS.append(f"{round(float(f1), 2):.2f}")

    #Dividends
    Dividends = str(StringDividends.group(1).replace('"', ''))
    a1 = Dividends.count(':')
    b1 = Convert(Dividends)
    if b1[0] == '': del b1[0]
    listDividends = []
    for i in range(0, a1):
        var = b1[i]
        c1 = list(var.split(":"))
        e1, f1 = [c1[j] for j in (0, 1)]
        if f1 == '':
            listDividends.append(0)
        else:
            listDividends.append(f"{round(float(f1), 2):.2f}")

    print(listofEPS)
    print(listDividends)

    RORE1 = "%.2f" % round(100 * (float(listofEPS[0]) - float(listofEPS[1])) / (float(listofEPS[0]) + float(listofEPS[1]) - float(listDividends[0]) - float(listDividends[1])), 2)
    print(RORE1)
    RORE2 = "%.2f" % round(100 * (float(listofEPS[1]) - float(listofEPS[2])) / (float(listofEPS[1]) + float(listofEPS[2]) - float(listDividends[1]) - float(listDividends[2])), 2)
    RORE3 = "%.2f" % round(100 * (float(listofEPS[2]) - float(listofEPS[3])) / (float(listofEPS[2]) + float(listofEPS[3]) - float(listDividends[2]) - float(listDividends[3])), 2)
    RORE4 = "%.2f" % round(100 * (float(listofEPS[3]) - float(listofEPS[4])) / (float(listofEPS[3]) + float(listofEPS[4]) - float(listDividends[3]) - float(listDividends[4])), 2)
    RORE5 = "%.2f" % round(100 * (float(listofEPS[4]) - float(listofEPS[5])) / (float(listofEPS[4]) + float(listofEPS[5]) - float(listDividends[4]) - float(listDividends[5])), 2)

    RORE5years = "%.2f" % round(((float(RORE1) + float(RORE2) + float(RORE3) + float(RORE4) + float(RORE5)) / 5), 2)
    print(RORE5years)

    # Overpriced
    CurrentPrice = re.findall("\d+\.\d+", StringCurrentPrice)
    PriceNow = float(CurrentPrice[0])
    PriceNow0 = str("Current Price is {}".format(PriceNow))

    # Price 5 years ago

    header = StringPrice.findAll('th')
    headers = [th.text for th in header]
    cells = []
    rows = StringPrice.findAll('tr')
    for tr in rows:
        # Process the body of the table
        td = tr.findAll('td')
        for t in td:
            a = re.findall('>(.*)<', str(t))
            b = a[0]
            cells.append(b)
    Price5Years = float(cells[36])
    cellsyears = [int(i) for i in cells[0::7]]
    pricecells = [float(i) for i in cells[1::7]]

    RetainedErnings = []
    for i in range(0, Years):
        a = NBShares * (float(listofEPS[i]) - float(listDividends[i]))
        RetainedErnings.append(f"{round(float(a), 2):.2f}")
    RetainedErnings = [float(i) for i in RetainedErnings]
    NominalDiscountRate = RealDiscountRate + AverageInflation
    NetPresentValue = np.npv(NominalDiscountRate, RetainedErnings)
    NETPRESENT = str("Net present Value {}".format(NetPresentValue))
    # EstimatedPrice
    TotalValueYears = "%.2f" % round(
        np.fv(-AverageInflation, Years, 0, -NetPresentValue) + np.fv(-AverageInflation, Years, 0,
                                                                     -(NBShares * Price5Years)), 2)
    TOTALVALUE = str("Total Value Years {}".format(TotalValueYears))
    EstimatedPrice = "%.2f" % round((float(TotalValueYears) / float(NBShares)), 2)

    Overpriced = "%.2f" % round(100 * (PriceNow / float(EstimatedPrice) - 1), 2)

    r = [RORE1, RORE5years, Overpriced]
    return r
