import requests
from bs4 import BeautifulSoup as soup

# Quick Note abbreviations:
# bsts = 'better safe than sorry'


class product(object):
    def __init__(self, name, plu, model, price, specs_list, short_descr, feats_list):
        self.name = name
        self.plu = plu
        self.model = model
        self.price = price
        self.specs = specs_list
        self.descr = short_descr
        self.feats = feats_list


def getAllPluNums():
    all_plus = []
    file = open('earphone_plus.csv', 'r')
    file.readline()  # consume the header
    f1 = file.readlines()
    for x in f1:
        all_plus.append(x)
    file.close()
    all_plus = list(dict.fromkeys(all_plus))
    return all_plus


def getPrice(page):
    results = page.find('span', 'net-total-price')
    if results != None:
        return results.text.strip().strip('$')
    results = page.find('li', id='did_price4textdiv')
    if results != None:
        return results.text.strip().strip('$')
    results = page.find('span', id='did_price4textdiv')
    if results != None:
        return results.text.strip().strip('$')
    results = page.find('span', id='did_price1valuediv')
    if results != None:
        return results.text.strip().strip('$')
    else:
        return '0.00'

# function returns the specifications listed on the Frys website
# returns dict


def getSpecs(page):
    specs_dict = {}
    table_container = page.find('table', 'table-specifications')
    if table_container != None:
        table_body = table_container.find_all('tr')
        for tr in table_body:
            tds = tr.find_all('td')
            spec_title = tds[0].text.strip()
            spec_details = tds[1].text.strip()
            specs_dict[spec_title] = spec_details
    else:
        specs_dict = {'no': 'specs'}
    return specs_dict


def getShortDescr(page):
    # container appears aftering clicking 'Features and Specs' collapsing menu
    container = page.find('div', id='collapseFrysManufacturerTab')
    # each div 'body-panel' composed of two inner 'div's:
    #            div[0] contains shortDescrDiv
    #            div[1] contains 'manufacturer-detail-container'
    container_div = container.find('div', 'panel-body')
    short_descr = container_div.find('div', 'shortDescrDiv')
    # check if item has a short description
    if short_descr != None:
        d = short_descr.text.strip()
        temp = d.replace('\n', ' ').replace('\r', ' ')
        temp = temp.split()
        d = ",".join(temp)
        d = d.replace(",", " ")
        return d
    else:
        return 'N/A'  # assign N/A so we can still create an object later


def getFeatures(page):
    features_dic = {}
    # container appears aftering clicking 'Features and Specs' collapsing menu
    container = page.find('div', id='collapseFrysManufacturerTab')
    # each div 'body-panel' composed of two inner 'div's:
    #            div[0] contains shortDescrDiv
    #            div[1] contains 'manufacturer-detail-container'
    container_div = container.find('div', 'panel-body')
    # every item should have a manufactorer-detail-container
    manufacturer_detail_container = container_div.find(
        'div', 'manufacturer-detail-container')

    # every item should have a 'div' with a class 'mdc-product-info'. Some will be empty
    manufacturer_product_info = manufacturer_detail_container.find(
        'div', 'mdc-product-info')
    if len(manufacturer_product_info) > 1:
        # features_container will be nested with 'div's. must iterate through each
        features_container = manufacturer_product_info.find(
            'div', id='features')
        if features_container != None:
            feature_divs = features_container.find_all(
                'div', 'onecol')  # list of nested divs
            for div in feature_divs:
                feature_header = div.find('div', 'header')
                if feature_header != None:
                    header = feature_header.get_text().strip()
                    header.replace('\n', '').replace('\r', '')
                    list = header.split()
                    header = ",".join(list)
                    header = header.replace(",", " ")
                else:
                    header = 'N/A'
                div_text = div.find('div', 'text')
                if div_text != None:
                    div_text = div_text.text.strip()
                    feats = div_text.split('\n')
                else:
                    feats = []
                if features_dic.get(header) == None:
                    features_dic[header] = feats
    return features_dic


def getProduct(plu):
    url = 'https://www.frys.com/product/{}?site=sr:SEARCH:MAIN_RSLT_PG'.format(
        plu)
    plu = plu.strip()
    resp = requests.get(url)
    content = resp.text
    resp.close()
    page_soup = getSoupPage(content)
    # extracting the data
    name = page_soup.find('h3', 'product-title').text.strip()
    name = name.replace(',', '-')
    labels = page_soup.find_all('span', 'product-label-value')
    model = labels[1].text.strip()
    price = getPrice(page_soup)
    specs_list = getSpecs(page_soup)  # dict
    short_descr = getShortDescr(page_soup)  # string
    features_list = getFeatures(page_soup)  # dict
    return product(name, plu, model, price, specs_list, short_descr, features_list)

# function returns  soup object of the html text passed


def getSoupPage(content):
    return soup(content, "html.parser")

# write a csv file with the plu nums


def writeToFile(products):
    filename = "products.csv"
    f = open(filename, "w")
    headers = "plu, name, model, price, description, specifications, features \n"
    f.write(headers)
    for p in products:
        f.write(str(p.plu) + "," + str(p.name) + "," + str(p.model) +
                "," + str(p.price) + "," + str(p.descr) + ",")
        for key, val in (p.specs).items():
            temp_str = str(key) + " : " + str(val) + " | "
            f.write(temp_str)
        f.write(",")
        for key, val in (p.feats).items():
            temp_str = str(key) + " : " + str(val).replace(",", "-") + " | "
            f.write(temp_str)
        f.write("\n")

    f.close()


if __name__ == "__main__":
    plu_list = getAllPluNums()
    product_list = []
    for plu in plu_list:
        p = getProduct(plu)
        product_list.append(p)
        print(p.plu + " | " + p.name)
    print("WRITING to file")
    writeToFile(product_list)
