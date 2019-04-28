from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import sys
# Working PLUs 8998303, 9283099, 9765014, 8789491, 9104358, 9849625, 9849505, 9065017, 8033484, 9722824, 9039867, 8998243, 8789671, 9126778, 8839092, 8838982, 8454128, 8839132, 8839142, 8981763, 8353877, 9126758, 8789701, 8964283
# PLUs to investigate 8353877 9126758 8789701 8964283
washer_plus = [8789491]
# 9104358, 9849505, 9065017, 8033484, 9039867,8998243, 8789671, 9126778, 8839092, 8838982, 8454128, 8839132, 8839142, 8981763, 8789701, 8964283
template_website_url = 'https://www.frys.com/product/%d?site=sr:SEARCH:MAIN_RSLT_PG'
target_url = ""
index = -1


class product(object):
    def __init__(self, name, plu, model, price, descr, specs):
        self.name = name
        self.plu = plu
        self.model = model
        self.price = price
        self.descr = descr
        self.specs = specs


def getSoup(target_url):
    uClient = uReq(target_url)  # open connection with url
    page_html = uClient.read()  # read in the raw html
    uClient.close()  # close the connection
    return soup(page_html, "html.parser")  # instaniate a soup object


def getItemInformation(page_soup):
    # get product name
    non_working_plus = []
    list_of_specs = []  # list of specifcations. [[spec_name, spec_detail],[...], ...]
    product_name = page_soup.find_all('h3', 'product-title')[0].text.strip()
    # get PLU and Model Number, class 'product-label-value' holds info
    product_label = page_soup.find_all('span', 'product-label-value')
    plu_num = product_label[0].text.strip()
    model_num = product_label[1].text.strip()
    # find the price of the object
    product_price = page_soup.find('span', 'net-total-price')
    # some products dont have the price in the 'span' with class 'net-total-price'
    if product_price is None:
        # we need to find the 'span' 'productPrice'
        product_price = page_soup.find('span', 'productPrice').text.strip()
    else:
        product_price = product_price.text.strip()

    # find the short desciption of the product
    s_descr = page_soup.find('div', 'shortDescrDiv').text.strip()
    short_descr = s_descr.replace(',', '-')

    # Grabbing the table that holds the specifications
    # attempt to find <tbody class=specifications />
    table_specs_container = page_soup.find('table', 'specifications')
    if table_specs_container != None:
        table_body = table_specs_container.find_all('tbody')
        for body in table_body:
            all_td = body.find_all('td')
            temp_list = []
            index = 1
            for td in all_td:
                temp_list.append(td.text.strip())
                if index % 2 == 0:
                    list_of_specs.append(temp_list)
                    temp_list = []
                index += 1
        return product(product_name, plu_num, model_num, product_price, short_descr, list_of_specs)
    else:
        print(table_specs_container)
    print(page_soup)
    table_specs_container = page_soup.find('ul', 'wc-rich-features')
    print(table_specs_container)
    if table_specs_container != None:
        print('HERE')
        features_li = table_specs_container.find_all(
            'li', 'wc-rich-feature-item')
        temp_list = []
        for li in features_li:
            info_container = li.find('div', 'wc-text-wrap')
            spec_title = li.find('h3', 'wc-rich-content-header').text.strip()
            spec_info = li.find(
                'div', 'wc-rich-content-description').text.strip()
            temp_list.append(spec_title)
            temp_list.append(spec_info)
            list_of_specs.append(temp_list)
            temp_list = []
        return product(product_name, plu_num, model_num, product_price, short_descr, list_of_specs)

    # else:
    #     non_working_plus.append(plu_num)
    #     print("SKIPPING PLU: ", plu_num)
    #     return None
    # print('Non working PLUs')
    # for plu in non_working_plus:
    #     print('-', plu)


for arg in washer_plus:
    target_url = template_website_url % (arg)
    print(target_url)
    page_soup = getSoup(target_url)
    print(page_soup.get_text())
    # print("SEARCHING... [ ", arg, " ]")
    # current_product = getItemInformation(page_soup)
    # if current_product != None:
    #     print("PRODUCT OBJECT CREATED : ", current_product.name)
