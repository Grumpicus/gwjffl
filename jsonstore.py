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
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
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

