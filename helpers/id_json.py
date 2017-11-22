import json

file = "helpers/ids.json"


def read(user, platform):
    with open(file) as data_file:
        data = json.load(data_file)
        try:
            return data[user][platform]
        except KeyError as e:
            print("ID Read KeyError: {}".format(e))
            return 0





