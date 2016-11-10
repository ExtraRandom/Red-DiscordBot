import json

file = "helpers/steam_id.json"
pd2_file = "helpers/pd2_weapons.json"

"""
For reading and writing to steam_id.json
"""


def read(user):
    with open(file) as data_file:
        data = json.load(data_file)
        # TODO check user exists
        return data[user]

"""
def write(user):

    return 0

    # todo get this code working

    data = read(user)

    with open(file) as out_file:
        data = json.dump(out_file)
"""

"""
For reading the .json containing stat info
"""


def steam_read(data, stat_name):
    jdata = json.loads(data)
    stats = len(jdata['playerstats']['stats'])

    # print(stats)

    for index in range(stats):
        if jdata['playerstats']['stats'][index]['name'] == stat_name:
            return jdata['playerstats']['stats'][index]['value']
    # TODO make log
    print("No result found for {}. Counting as zero.".format(stat_name))
    return 0


def weapon_read(data):
    # http://wiki.modworkshop.net/Payday_2/Weapon_IDs
    jdata = json.loads(data)

    with open(pd2_file) as out_file2:
        data = json.dump(out_file2)



    stats = len(jdata['playerstats']['stats'])

    highest_kills = 0
    highest_gun = ""

    # print(stats)

    for index in range(stats):
        if str(jdata['playerstats']['stats'][index]['name']).startswith('weapon_kills_'):
            if int(jdata['playerstats']['stats'][index]['value']) > highest_kills:
                highest_kills = int(jdata['playerstats']['stats'][index]['value'])
                highest_gun = str(jdata['playerstats']['stats'][index]['name'])

    if highest_gun == "" or highest_kills == 0:
        return "N/A", "N/A"
    else:
        return highest_gun, highest_kills


def test_json(data):

    jdata = json.loads(data)
    stats = len(jdata['playerstats']['stats'])

    count = 0

    for index in range(stats):
        if str(jdata['playerstats']['stats'][index]['name']).startswith('weapon_kills_'):
            count += 1
            # print(str(jdata['playerstats']['stats'][index]['name']))

    # print(count)
    return count



