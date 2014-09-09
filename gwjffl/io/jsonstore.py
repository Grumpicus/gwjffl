import json

import jsonpickle


def read_json_from_file(filename):
    data = None
    try:
        json_data = open(filename).read()
        if json_data:
            data = json.loads(json_data)
    finally:
        return data


def write_json_to_file(filename, data):
    # We do it this way because json.dump can corrupt the file if there's a serialization error.
    json_data = json.dumps(data)
    with open(filename, 'w') as outfile:
        outfile.write(json_data)
    return


def unpickle_json_from_file(filename):
    data = None
    try:
        json_data = open(filename).read()
        if json_data:
            data = jsonpickle.decode(json_data)
    finally:
        return data


def pickle_json_to_file(filename, data):
    with open(filename, 'w') as outfile:
        outfile.write(jsonpickle.encode(data))
    return

