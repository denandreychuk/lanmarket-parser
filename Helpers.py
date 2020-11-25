from urllib import request
from bs4 import BeautifulSoup

# Performs simple GET request to endpoint.
# Constructs object using bs4 lib.
def openURL(url):
    response = request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup