from bs4 import BeautifulSoup
import requests
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
from statistics import mean

import vars

from utils import (
    write_data,
    write_data_as_json
)


def get_data(url, sort, server):
    """extract data from website, return list of outcomes"""
    server_id = "&server=" + str(server['ID'])
    print(f"{url}{server['Region']}{server_id}{sort}")

    page = requests.get(f"{url}{server['Region']}{server_id}{sort}")

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


def update_servers(ddb=None):
    if not ddb:
        ddb = boto3.resource('dynamodb')

    servers = ddb.Table('Servers')

    server_list = get_server_list(vars.BASE_URL_)

    with servers.batch_writer() as batch:
        for key in server_list:
            if(server_list[key] == 'all'):
                continue

            region = "0"
            if "[EU]" in key:
                region = vars.EU_KEY
            elif "[US]" in key:
                region = vars.US_KEY
            else:
                region = vars.RU_KEY

            batch.put_item(
                Item={
                    'Server': key,
                    'ID': int(server_list[key]),
                    'Region': region,
                    'Faction': "Alliance" if "Alliance" in key else "Horde"
                })


def update_prices(ddb=None):
    if not ddb:
        ddb = boto3.resource('dynamodb')

    table = ddb.Table('Servers')

    scan_kwargs = {
        'FilterExpression': Key('ID').gt(0)
    }

    id_list = []
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        id_list.append(response.get('Items', []))
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None

    servers = id_list[0]

    for server in servers:
        iterations = zip([vars.RECOMMENDED, vars.CHEAPEST], [
            vars.RECOMMENDED_FILE, vars.CHEAPEST_FILE])

        for dataset, _ in iterations:
            now = datetime.now()
            dt_string = now.strftime("%B %d %Y %H:%M:%S")

            data = get_data(vars.BASE_URL_, dataset, server)

            if not data:
                continue

            price_tbl = ddb.Table('Pricepoints')
            response = price_tbl.put_item(
                Item={
                    'ID': str(server['ID']),
                    'Date': str(dt_string),
                    'Price': str(mean(data)),
                    'Sort': dataset.split('=')[-1]
                }
            )
