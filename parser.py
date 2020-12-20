import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


HOST = 'https://www.ceramicspeed.com'
URL = 'https://www.ceramicspeed.com/en/cycling/support/wheel-kit-compatibility/road-wheel-kits/mavic-wheel-kits/'
HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,a',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

PATH = 'C:\Program Files (x86)\chromedriver.exe' # change path as needed
CHROME = Chrome(executable_path=PATH)

br = ["5/32''", '626', '628/8', '608', '609', '61800', '6000', '61801', '61901', '6001', '61902', '61903', '61805', '61906','R6']
urls = ['https://www.ceramicspeed.com/en/cycling/support/wheel-kit-compatibility/mtb-wheel-kits/mavic-wheel-kits/',
        'https://www.ceramicspeed.com/en/cycling/support/wheel-kit-compatibility/road-wheel-kits/shimano-road-wheel-kits/',
        'https://www.ceramicspeed.com/en/cycling/support/wheel-kit-compatibility/mtb-wheel-kits/shimano-mtb-wheel-kits/',
        'https://www.ceramicspeed.com/en/cycling/support/wheel-kit-compatibility/road-wheel-kits/lightweight-wheel-kits/']
# 'https://www.ceramicspeed.com/en/cycling/support/wheel-kit-compatibility/road-wheel-kits/'


def get_html(url, headers):
    return requests.get(url, headers=headers)


def filter(bearings):
    data = []
    for i in range(0, len(br)):
        data.append('')

    for b in bearings:
        l = b.text.split(' ')
        if len(l) > 2:
            s = l[2]
            if s in br:
                i = br.index(s)
                data.pop(i)
                data.insert(i, l[0])
    return data


def get_content(url, headers, data):
    soup = BeautifulSoup(get_html(url, headers).text, 'html.parser')
    brand = soup.find('h1', {'class': 'intro-block__title'}).text.strip().split(' ')[0]
    tables = (str(t) for t in soup.find_all('tbody'))
    mb = {}

    for table in tables:
        soup = BeautifulSoup(table, 'html.parser')
        year = soup.find('strong').text.split(' ')[0]

        for i, tr in enumerate(soup.find_all('tr')):
            if i > 0:
                next = tr.find_next('td')
                name = next.text
                next = next.find_next('td').find('a')
                href = HOST + str(next['href'])
                kit = next.text

                if kit not in mb.keys():
                    print(kit, href)
                    CHROME.get(href)
                    try:
                        wait = WebDriverWait(CHROME, 5).until(EC.presence_of_element_located((By.ID, 'tab_1')))
                    except TimeoutException:
                        print('load is failed')
                    # print(CHROME.page_source)
                    # body = CHROME.find_element_by_id('tab_1').get_attribute('innerHTML')
                    body = CHROME.page_source
                    # CHROME.quit()
                    bs = BeautifulSoup(body, 'html.parser')
                    image = bs.find('meta', {'property': 'og:image'})['content']
                    bearings = bs.find_all('li')
                    buff = filter(bearings)
                    mb.update({kit: buff})
                data.append([year, brand, name, kit, href, image, mb.get(kit)])
    return data


def get_all_content():
    data = []
    for url in urls:
        data = get_content(url, HEADERS, data)
    return data



with open('bearings.csv', 'w', encoding='UTF-8') as csv:
    csv.write("YEAR;BRAND;NAME;KIT;URL;IMAGE;5/32'';626;688;608;609;61800;6000;61801;61901;6001;61902;61903;61805;61906;R6\n")
    for element in get_all_content():
        for i in range(0, (len(element)) - 1):
            print(element[i])
            csv.write(element[i])
            csv.write(';')

        buff = element[len(element) - 1]
        for i, e in enumerate(buff):
            csv.write(e)
            if (i != len(buff) - 1):
                csv.write(';')
            else:
                csv.write('\n')
CHROME.quit()

# print(BeautifulSoup(get_html('https://www.ceramicspeed.com/en/cycling/shop/wheel-kits/mavic-23/', HEADERS).text, 'html.parser').find_all('div', {'class': 'product__information-block'}))

# print(body)

