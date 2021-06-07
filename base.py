from functions import get_data, write_data
from datetime import datetime

# globals
BASE_URL = 'https://www.g2g.com/wow-classic-tbc/gold-29076-29077?faction=41397&server=41092'
RECOMMENDED = '&sorting=recommended'
CHEAPEST = '&sorting=lowest_price'
DATA_DIRECTORY = 'data'
RECOMMENDED_FILE = 'datalog_recommended.txt'
CHEAPEST_FILE = 'datalog_cheap.txt'


now = datetime.now()
dt_string = now.strftime("%B %d %Y %H:%M:%S")

if __name__ == "__main__":
    iterations = zip([RECOMMENDED, CHEAPEST], [RECOMMENDED_FILE, CHEAPEST_FILE])
    for dataset, write_file in iterations:
        _ = get_data(BASE_URL, dataset)
        write_data(DATA_DIRECTORY, write_file, _, dt_string)
