from bs4 import BeautifulSoup
import requests
from statistics import mean
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%B %d %Y %H:%M:%S")

url = 'https://www.g2g.com/wow-classic-tbc/gold-29076-29077?faction=41397&server=41092&sorting=recommended'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
content = soup.findAll('li', class_='products__list-item')

datapoints = []

for li in content:
    datapoints.append(float(li.div.find('div', class_="products__statistic").find(
        'span', class_='products__exch-rate').span.text.strip()))


f = open('data/datalog.txt', 'a')
f.write(dt_string + "," + str(mean(datapoints)) + '\n')