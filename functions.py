from bs4 import BeautifulSoup
from statistics import mean
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


def write_data(directory, file, data, date_string):
    """write data to text file"""
    file = open(f"{directory}/{file}", "a")
    file.write(date_string + "," + str(mean(data)) + "\n")
