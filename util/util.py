import json
import dbus

CONFIG_FILE_PATH = "config.json"


def read_value(key):
    with open(CONFIG_FILE_PATH, 'rw') as f:
        data = json.load(f)
        res = data[key]

    if type(res) == int:
        return [dbus.Byte(res)]
    if type(res) == str:
        return string_to_byte_arr(res)

    return res


def write_value(key, new_value):
    with open(CONFIG_FILE_PATH, 'r') as f:
        data = json.load(f)

    data[key] = new_value
    with open(CONFIG_FILE_PATH, 'w') as f:
        f.write(json.dumps(data))

    return True


def string_to_byte_arr(string):
    res = []

    for char in string:
        res.append(dbus.Byte(char.encode()))

    return res
