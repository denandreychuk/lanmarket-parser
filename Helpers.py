import urllib
from bs4 import BeautifulSoup

def openURL(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup