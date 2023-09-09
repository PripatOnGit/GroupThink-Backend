import json


def read() -> list:
    with open('data.json', 'r') as f:
        data_lst = json.load(f)
        return data_lst


def write(data_row):
    data_lst = read()
    data_lst.append(data_row)
    with open('data.json', 'w') as json_file:
        json.dump(data_lst, json_file)