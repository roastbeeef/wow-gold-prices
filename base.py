from functions import get_data
from statistics import mean
from datetime import datetime

# globals
BASE_URL = 'https://www.g2g.com/wow-classic-tbc/gold-29076-29077?faction=41397&server=41092'
RECOMMENDED = '&sorting=recommended'
CHEAPEST = '&sorting=lowest_price'

now = datetime.now()
dt_string = now.strftime("%B %d %Y %H:%M:%S")

if __name__ == "__main__":
    rec = get_data(BASE_URL, RECOMMENDED)
    cheap = get_data(BASE_URL, CHEAPEST)

    r = open('data/datalog_recommended.txt', 'a')
    r.write(dt_string + "," + str(mean(rec)) + '\n')

    c = open('data/datalog_cheap.txt', 'a')
    c.write(dt_string + "," + str(mean(cheap)) + '\n')