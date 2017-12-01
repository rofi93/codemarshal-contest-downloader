import os
import shutil
import requests
from pdfkit import from_url
from bs4 import BeautifulSoup

NUM = 1
PAGE = 'page'
CONTESTS = 'contests'
STANDINGS = 'standings'
CODEMARSHAL_URL = 'https://algo.codemarshal.org'

while True:
    URL = CODEMARSHAL_URL + '/' + CONTESTS + '/?' + PAGE + '=' + str(NUM)
    html = requests.get(URL)
    soup = BeautifulSoup(html.text, 'lxml')
    list_groups = soup.find_all('div', {'class': 'list-group'})[1]

    if len(list_groups) == 0:
        break

    for list_group in list_groups:
        title = list_group.find('h4').get_text()
        standing_url = CODEMARSHAL_URL + list_group['href'] + '/' + STANDINGS

        title = '_'.join(str(title).split())

        if os.path.exists(title):
            shutil.rmtree(title)

        os.makedirs(title)
        path = os.path.realpath(title)

        page_num = 1
        while True:
            url = standing_url + '?' + PAGE + '=' + str(page_num)
            html = requests.get(url)
            table = BeautifulSoup(html.text, 'lxml').find('tbody')

            if len(table) == 0:
                break

            from_url(url, path + '/' + 'standing-' + str(page_num) + '.pdf')

            page_num = page_num + 1

    NUM = NUM + 1
