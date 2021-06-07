import json
from statistics import mean


def write_data(directory, file, data, date_string):
    """write data to text file"""
    file = open(f"{directory}/{file}", "a")
    file.write(date_string + "," + str(mean(data)) + "\n")


def write_data_as_json(directory, file, data):
    """write dict to json file"""
    with open(f"{directory}/{file}", 'w') as fp:
        json.dump(data, fp)
