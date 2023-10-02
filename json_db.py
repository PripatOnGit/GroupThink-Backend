import json


def read_all_rows() -> list:
    with open('data.json', 'r') as f:
        data_lst = json.loads(f.read())
        return data_lst


def write_row(data_row):
    data_lst = read_all_rows()
    data_lst.append(data_row)
    with open('data.json', 'w') as json_file:
        json.dump(data_lst, json_file, indent=4)


def update_row(data_row):
    data_lst = read_all_rows()
    for row in data_lst:
        if data_row["username"] == data_row["username"]:
            row.update(data_row)
    with open('data.json', 'w') as json_file:
        json.dump(data_lst, json_file, indent=4)