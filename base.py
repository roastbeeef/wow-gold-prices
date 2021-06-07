from datetime import datetime

from functions import (
    get_data,
    get_server_list
)

from utils import (
    write_data,
    write_data_as_json
)

from vars import (
    BASE_URL_,
    BASE_URL,
    RECOMMENDED,
    CHEAPEST,
    DATA_DIRECTORY,
    RECOMMENDED_FILE,
    CHEAPEST_FILE,
    SERVER_LIST_FILE
)

now = datetime.now()
dt_string = now.strftime("%B %d %Y %H:%M:%S")

if __name__ == "__main__":
    server_list = get_server_list(BASE_URL_)
    write_data_as_json(DATA_DIRECTORY, SERVER_LIST_FILE, server_list)

    iterations = zip([RECOMMENDED, CHEAPEST], [RECOMMENDED_FILE, CHEAPEST_FILE])
    for dataset, write_file in iterations:
        _ = get_data(BASE_URL, dataset)
        write_data(DATA_DIRECTORY, write_file, _, dt_string)
