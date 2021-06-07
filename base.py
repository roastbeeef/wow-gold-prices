from datetime import datetime

from functions import (
    get_data,
    get_server_list
)

from utils import (
    write_data,
    write_data_as_json
)

import vars

now = datetime.now()
dt_string = now.strftime("%B %d %Y %H:%M:%S")

if __name__ == "__main__":
    server_list = get_server_list(vars.BASE_URL_)
    write_data_as_json(vars.DATA_DIRECTORY, vars.SERVER_LIST_FILE, server_list)

    iterations = zip([vars.RECOMMENDED, vars.CHEAPEST], [vars.RECOMMENDED_FILE, vars.CHEAPEST_FILE])
    for dataset, write_file in iterations:
        _ = get_data(vars.BASE_URL, dataset, vars.TEMP_SERVER_NAME)
        write_data(vars.DATA_DIRECTORY, write_file, _, dt_string)
