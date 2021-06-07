from bs4 import BeautifulSoup
import requests

def get_data(url, sort):
    page = requests.get(url+sort)

    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.findAll('li', class_='products__list-item')

    datapoints = []

    for li in content:
        datapoints.append(float(li.div.find('div', class_="products__statistic").find(
            'span', class_='products__exch-rate').span.text.strip()))

    return datapoints