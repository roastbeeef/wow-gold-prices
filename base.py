import argparse


from functions import (
    get_data,
    get_server_list,
    update_prices,
    update_servers
)


import vars

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--action", help="Update server list or get latest prices", type=str, choices=['prices', 'servers'])

    args = parser.parse_args()

    if(args.action == "prices"):
        update_prices()
    if(args.action == "servers"):
        update_servers()
