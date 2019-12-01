from lxml import html
from bs4 import BeautifulSoup
import requests

def get_indiaexpress_data(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'xml')
    links = []
    for link in soup.find_all('title'):
        links.append(link.text)

    return links


# print(get_indiaexpress_data('https://indianexpress.com/section/india/feed/'))


def get_toi_data(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'xml')
    links = []
    for link in soup.find_all('title'):
        links.append(link.text)

    return links

print(get_toi_data('https://timesofindia.indiatimes.com/rssfeedstopstories.cms'))

