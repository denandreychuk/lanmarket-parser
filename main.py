import Constants as c
import Helpers as h
import csv
import re

# Determines number of pages for specific category
def getNumberOfPages(soup):
    pagination = soup.find('ul', {'class': 'c_pagination_list'})
    lists = pagination.find_all('li')
    numberOfPages = int(lists[-2].text)
    return numberOfPages

# Parses product links for specific category
def getProductLinks(soup):
    products = soup.find_all('div', {'class': re.compile('prdct_i bx_catalog_item_container aaa typeCatalog')})
    return list(map(lambda product: c.baseURL + product.find('div', {'class': 'name-wrap'}).a.get('href'), products))

# Formats characteristic
#
# - Discussion
#
# Lanmarket uses a simple HTML table to display product characteristics.
# It has two parts: type and value.
#
# | type |: | value |
#
# The value must undergo additional processing because it may contain
# special characters like newlines, tabs, etc. Also, we have corner cases
# like multi-line values, which we handle with simple reg exp and split
# it with space.
def formatCharacteristic(characteristic):
    type = characteristic.find('td', {'class': 'product_card__product_characters_type'}).text.split(':')[0].strip()
    rawValue = characteristic.find('td', {'class': 'product_card__product_characters_val'}).text.strip()
    value = re.sub('\s+', ' ', rawValue)
    return f'{type}: {value}'

# Extracts payload from product page. This includes: name, price, vendor,
# short description, description, chars, photo links.
def parseProductData(productURL):
    soup = h.openURL(productURL)

    # name

    name = soup.find('h1', {'class': 'product_card__title'}).text.strip()

    # price

    try:
        price = float(soup.find('span', {'class': 'js-doll-price'}).text.strip())
    except AttributeError:
        price = "0.0"

    # vendor

    try:
        vendor = soup.find('div', {'class': 'prod-art1'}).find_all('span')[1].text.strip()
    except AttributeError:
        vendor = ''

    # short description

    try:
        shortDescription = soup.find('span', {'itemprop': 'description'}).text.strip()
    except AttributeError:
        shortDescription = ''

    # description

    try:
        rawDescription = soup.find('div', {'id': 'product_description'}).find_all('p')
        description = ''.join(list(map(lambda p: p.text.strip(), rawDescription)))
    except AttributeError:
        description = ''

    # characteristics

    try:
        rawCharacteristics = soup.find('div', {'id': 'product_characteristics'}).find_all('tr', {
            'class': 'product_card__product_characters_item clearfix'})
        characteristics = ', '.join(list(map(formatCharacteristic, rawCharacteristics)))
    except AttributeError:
        characteristics = ''

    # photos

    try:
        photos = ', '.join(
            list(map(lambda photo: 'https:' + photo.get('href'), soup.find_all('a', {'class': 'vert_centred'})))
        )
    except AttributeError:
        photos = ''

    return {
        'name': name,
        'price': price,
        'vendor': vendor,
        'short_description': shortDescription,
        'description': description,
        'characteristics': characteristics,
        'photos': photos
    }

# Saves list to csv file. One item per row.
def save(products, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Название', 'Цена', 'Артикуль', 'Краткое описание', 'Полное описание', 'Характеристики', 'Фото'))
        for product in products:
            writer.writerow((
                product['name'],
                product['price'],
                product['vendor'],
                product['short_description'],
                product['description'],
                product['characteristics'],
                product['photos']
            ))

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

        for productLink in productLinks:
            print(f'Parsing product: {productLink}')
            product = parseProductData(productLink)
            products.append(product)

    save(products, 'result.csv')