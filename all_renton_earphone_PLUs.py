import requests
from bs4 import BeautifulSoup as soup


# function returns a soup object of the current page being viewed
def getPage(num_page):
    resp = requests.get('https://www.frys.com/search?storeNo=30,&cat=-68978&pType=pDisplay&rows=20&fq=a%20Regular%20Items-100722%20Over__Ear-100722%20On__Ear-100722%20In__Ear&resultpage={}&start=0&rows=20'.format(num_page),
                        cookies={'J1_USER_ID': 'SAMNDEyNTMwNDE0NDpkYTI2ODRjOjE2OTM5YTJmZGQ1Oi00MjkyXjg4NDM4MjkyODE2NTEwNTA2MjM=|103- -Y-19521', '_ga': 'GA1.2.663394348.1551452841', 'BTgroup': 'B', 'HSC': 'Y', 'BVBRANDID': '02d7364e-0c04-4a29-8596-f839a92ed3e8', 'HZF': 'true', 'SD': '50', 'sl': '20', 'ID_KOT': '987123654', 'WS': 'PDCCADPXQPC', 'btpdb.gIgF3sY.dGZjLjQxNjY2MA': 'U0VTU0lPTg', 'btpdb.gIgF3sY.dGZjLjQyMzUyMTM': 'U0VTU0lPTg', 'btpdb.gIgF3sY.dGZjLjQ3MDYwMTg': 'U0VTU0lPTg', 'VW': 'L', 'ZCS': '95112', 'UPS': 'BQ', 'BVImplmain_site': '19182', 'FSERVERID': 'ssl111', '__utmc':
                                 '245170898', '__utmz': '245170898.1556172538.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)', '_gid': 'GA1.2.663671469.1556384523', 'spid': 'E5FAACD0-FE8C-4988-9B86-3FA24BCA414A', 'sp_ssid': '1556387058110', 'JSESSIONID': 'mf36Pjcgo88xudYWiEUqiQ__.node3', '__utma': '245170898.663394348.1551452841.1556172538.1556470605.2', '__utmb': '245170898.1.10.1556470605', 'FR_LD': '/template/index', 'LCP': '/template/index', 'UPFLCSZ': 'P-0_U-MC4zOTk3MTUzNzUxODU3MjUyXjcwNDk0OTIxNTVeMC4zMTc3OTMxMjA4OTY2MjU3', 'usr_med': '101', 'BVBRANDSID': '6af0dfe5-d4c8-4d2e-837b-61a1d2636d86', 'SC': 'BQ', '_gat': '1'}, headers={
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'})
    content = resp.text
    resp.close()

    return getSoupPage(content)

# function returns  soup object of the html text passed


def getSoupPage(content):
    return soup(content, "html.parser")

# function for getting the list of PLU numbers on the page

# function returns an array of the PLU #s found on the page


def getPLUs(soup_page):
    page_PLUs = soup_page.find_all('div', 'prodModel')
    plus = []
    for plu in page_PLUs:
        plus.append(plu.find('p').text.strip().strip('Frys #: '))
    return plus

# return a list of ints that are all the PLU #s from the searched url


def getAllPLUs(num_of_pages):
    all_plus = []
    i = 0
    while(i < num_of_pages):  # iterating through ll result pages
        print('CHECKING PAGE: ', i)
        soup_page = getPage(i)
        plu_nums = getPLUs(soup_page)
        all_plus = all_plus + plu_nums
        i += 1
    return all_plus


# write a csv file with the plu nums
def writeToFile(plu_nums):
    filename = "earphone_plus.csv"
    f = open(filename, "w")
    headers = "plu #\n"
    f.write(headers)
    for plu in plu_nums:
        f.write(plu + "\n")

    f.close()

# functions returns an int of the total number of pages to search


def getNumPages(soup_page):
    container = soup_page.find('select', id='jumpTo')
    string_num = container.find_next_sibling().text.strip('of ').strip()
    return int(string_num)


if __name__ == "__main__":
    soup_page = getPage(0)
    num_of_pages = getNumPages(soup_page)
    print("TOTAL PAGES: ", num_of_pages)
    all_plus = getAllPLUs(num_of_pages)
    writeToFile(all_plus)
