import jsonpickle


def unpickle_json_from_file(filename):
    data = None
    try:
        json_data = open(filename).read()
        if json_data:
            data = jsonpickle.decode(json_data)
    finally:
        return data


def pickle_json_to_file(filename, data):
    # We do it this way in order to avoid getting a corrupt file if there's a serialization error.
    json_data = jsonpickle.encode(data)
    with open(filename, 'w') as outfile:
        outfile.write(json_data)
    return

