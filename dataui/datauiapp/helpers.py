import csv
import os
from collections import namedtuple


def get_file_path(kwargs_dict):
    return os.path.join('/Users/Spyro/Developer/graphql_ui',
                        '{}.csv'.format(kwargs_dict.get('file_name')))


def get_csv_tuples(file_path):
    header_cols = [a for a in csv.reader(open(file_path, "r"))][0]
    return namedtuple('CSVRow', header_cols)


def get_csv_rows(file_path):
    CSVRow = get_csv_tuples(file_path)
    return [CSVRow._make(a) for a in csv.reader(open(file_path, "r"))][1:]


def attach_client_info(client_id, client_mapping, client_file_path):
    csv_rows = get_csv_rows(client_file_path)
    client_row = None
    for row in csv_rows:
        row_id = getattr(row, client_mapping.get('id'))
        if row_id == client_id:
            client_row = row

    if client_row:
        new_dict = {}
        for key, val in client_mapping.items():
            if getattr(client_row, val, None):
                new_dict.update({key: getattr(client_row, val)})
        new_dict.pop('id')
        return new_dict
