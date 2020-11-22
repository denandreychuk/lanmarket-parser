import Constants as c
import Helpers as h

def getNumberOfPages(soup):
    pagination = soup.find('ul', {'class': 'c_pagination_list'})
    lists = pagination.find_all('li')
    numberOfPages = int(lists[-2].text)
    return numberOfPages

def getProductLinks(soup):
    products = soup.find_all('div', {'class': 'prdct_i bx_catalog_item_container aaa typeCatalog'})
    return list(map(lambda product: c.baseURL + product.find('div', {'class': 'name-wrap'}).a.get('href'), products))

if __name__ == '__main__':
    categorySoup = h.openURL(c.categoryURL)
    numberOfPages = getNumberOfPages(categorySoup)

    print(f'Found {numberOfPages} pages in category: {c.categoryURL}')

    products = []

    for pageNumber in range(1, numberOfPages):
        pageLink = c.categoryURL + f'?PAGEN_1={pageNumber}'
        print(f'Parsing page: {pageLink}')
        pageSoup = h.openURL(pageLink)
        productLinks = getProductLinks(pageSoup)
        print(productLinks)
