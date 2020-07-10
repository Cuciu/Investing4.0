import requests
from bs4 import BeautifulSoup

def URLHandler(url0):
    res = requests.get(url0, headers={'User-Agent': 'Mozilla/5.0'})
    html_string = BeautifulSoup(res.content, 'html.parser')
    html_string = str(html_string)
    return html_string
    sleep(1)
