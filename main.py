import Constants as c
import Helpers as h

def getNumberOfPages(soup):
    pagination = soup.find('ul', {'class': 'c_pagination_list'})
    lists = pagination.find_all('li')
    numberOfPages = int(lists[-2].text)
    return numberOfPages

if __name__ == '__main__':
    categorySoup = h.openURL(c.categoryURL)
    print(getNumberOfPages(categorySoup))
