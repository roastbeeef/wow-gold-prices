from bs4 import BeautifulSoup
import requests


def get_data(url, sort):
    """extract data from website, return list of outcomes"""
    page = requests.get(url+sort)
    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.findAll('li', class_='products__list-item')

    datapoints = []

    for li in content:
        datapoints.append(float(li.div.find('div', class_="products__statistic").find(
            'span', class_='products__exch-rate').span.text.strip()))

    return datapoints


def get_server_list(url):
    """get list of g2g server availability"""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.findAll('option')

    server_list = {}

    for option in content:
        server_list[option.get('value')] = option.get_text()

    return server_list
