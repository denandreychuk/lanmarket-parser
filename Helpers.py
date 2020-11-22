from urllib import request
from bs4 import BeautifulSoup

def openURL(url):
    response = request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup