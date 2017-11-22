import json

file = "helpers/bnet_id.json"


def read(user):
    with open(file) as bnet_file:
        data = json.load(bnet_file)
        try:
            return data[user]
        except KeyError as e:
            print("BNet - KeyError: {}".format(e))
            return 0














