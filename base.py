from bs4 import BeautifulSoup
import requests
from statistics import mean
from datetime import datetime

base_url = 'https://www.g2g.com/wow-classic-tbc/gold-29076-29077?faction=41397&server=41092'
recommended = '&sorting=recommended'
cheapest = '&sorting=lowest_price'

now = datetime.now()
dt_string = now.strftime("%B %d %Y %H:%M:%S")

def get_data(url, sort):
    page = requests.get(url+sort)

    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.findAll('li', class_='products__list-item')

    datapoints = []

    for li in content:
        datapoints.append(float(li.div.find('div', class_="products__statistic").find(
            'span', class_='products__exch-rate').span.text.strip()))

    return datapoints


rec = get_data(base_url, recommended)
cheap = get_data(base_url, cheapest)

r = open('data/datalog_recommended.txt', 'a')
r.write(dt_string + "," + str(mean(rec)) + '\n')

c = open('data/datalog_cheap.txt', 'a')
c.write(dt_string + "," + str(mean(cheap)) + '\n')