import requests
from bs4 import BeautifulSoup

HOST = 'https://www.ceramicspeed.com'
URL = 'https://www.ceramicspeed.com/en/cycling/support/wheel-kit-compatibility/road-wheel-kits/mavic-wheel-kits/'
HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,a',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}


def get_html(url, headers):
    return requests.get(url, headers=headers)


def get_content():
    soup = BeautifulSoup(get_html(URL, HEADERS).text, 'html.parser')

    data = []
    brand = soup.find('h1', {'class': 'intro-block__title'}).text.strip().split(' ')[0]

    for table in soup.find_all('tbody'):
        year = table.find('strong').text.split(' ')[0]

        for i, tr in enumerate(table.find_all('tr')):
            if(i > 0):
                next_td = tr.find_next('td')
                href = HOST + str(next_td.find_next('td').find('a')['href'])
                bs = BeautifulSoup(get_html(href, HEADERS).text, 'html.parser')
                image = bs.find('meta', {'property': 'og:image'})['content']
                data.append([year, brand, next_td.text, href, image])


    return data


with open('bearings.csv', 'w', encoding='UTF-8') as csv:
    for element in get_content():
        for i in range(0, (len(element))):
            print(element[i])
            csv.write(element[i])

            if(i != len(element) - 1):
                csv.write(';')
            else:
                csv.write('\n')
