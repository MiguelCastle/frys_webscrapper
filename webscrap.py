from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import sys

current_plu = 0
template_website_url = 'https://www.frys.com/product/%d?site=sr:SEARCH:MAIN_RSLT_PG'
target_url = ""

for arg in sys.argv:
    try:
        current_plu = int(arg, 10)
    except ValueError:
        print('Cant read PLU: #', arg)
        continue
    else:
        target_url = template_website_url % (current_plu)
        print("SEARCHING...")
        uClient = uReq(target_url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")

        product_name = page_soup.find_all(
            'h3', 'product-title')[0].text.strip()
        product_label = page_soup.find_all('span', 'product-label-value')
        plu_num = product_label[0].text.strip()
        model_num = product_label[1].text.strip()

        product_price = page_soup.find('span', 'net-total-price').text.strip()
        s_descr = page_soup.find('div', 'shortDescrDiv').text.strip()
        short_descr = s_descr.replace(',', '-')

        features_container = page_soup.find('div', 'onecol')
        features_list = features_container.find_all('li')
        list_of_features = []

        for feature in features_list:
            list_of_features.append(feature.text.strip())

        table_specs = page_soup.find('table', 'specifications')
        specs_table_headers = table_specs.find_all('thead')
        spec_table_body_container = table_specs.find_all('tbody')

        body_index = -1
        specification_list = []

        for body in spec_table_body_container:
            body_index += 1
            table_body_trs = body.find_all('tr')
            temp_spec_list = []

            for tr in table_body_trs:
                if len(tr.find_all('td')) < 2:
                    current_label = tr.find_all('td')[0].text.strip()
                    current_details = ""
                else:
                    current_label = tr.find_all('td')[0].text.strip()
                    current_details = tr.find_all('td')[1].text.strip()

                temp_spec_list.append([current_label, current_details])

            if len(specs_table_headers) == 0:
                specification_list.append(["", temp_spec_list])
            else:
                specification_list.append(
                    [specs_table_headers[body_index], temp_spec_list])

        print('PRODUCT RESULTS')
        print('Product Name: ' + product_name)
        print('PLU: #' + plu_num)
        print('Model: ' + model_num)
        print("Price: " + product_price)
        print('Short Description: \n' + short_descr+"\n")
        print('List of Features')
        for i in list_of_features:
            print(i)
        print()
        print('Specifications: ')
        for spec in specification_list:
            print(spec[0])
            for spec_item in spec[1]:
                print(spec_item[0] + ":" + spec_item[1])
