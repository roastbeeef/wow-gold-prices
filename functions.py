from bs4 import BeautifulSoup
import requests
import boto3
from datetime import datetime

import vars

from utils import (
    write_data,
    write_data_as_json
)


def get_data(url, sort, server_id):
    """extract data from website, return list of outcomes"""
    page = requests.get(f"{url}{sort}{server_id}")
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
        server_list[option.get_text()] = option.get('value')

    return server_list


def update_servers():
    ddb = boto3.resource('dynamodb')
    servers = ddb.Table('Servers')

    server_list = get_server_list(vars.BASE_URL_)

    with servers.batch_writer() as batch:
        for key in server_list:
            if(server_list[key] == 'all'):
                continue

            batch.put_item(
                Item={
                    'Server': key,
                    'ID': int(server_list[key])
                })


def update_prices():
    now = datetime.now()
    dt_string = now.strftime("%B %d %Y %H:%M:%S")

    iterations = zip([vars.RECOMMENDED, vars.CHEAPEST], [
        vars.RECOMMENDED_FILE, vars.CHEAPEST_FILE])

    for dataset, write_file in iterations:
        _ = get_data(vars.BASE_URL, dataset, vars.TEMP_SERVER_NAME)
        write_data(vars.DATA_DIRECTORY, write_file, _, dt_string)
