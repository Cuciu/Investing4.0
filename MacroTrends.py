def Convert(string):
    li = list(string.split(","))
    return li

def MacroTrends_RORE(StringEPS, StringDividends):

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

    r = [RORE1, RORE5years]
    return r
