import json

file = "helpers/steam_id.json"
pd2_file = "helpers/pd2_info.json"

"""
For reading and writing to steam_id.json
"""


def read(user):
    with open(file) as data_file:
        data = json.load(data_file)
        # TODO check user exists - if no stats exist then user doesnt own the game
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

    for index in range(stats):
        if jdata['playerstats']['stats'][index]['name'] == stat_name:
            return jdata['playerstats']['stats'][index]['value']
    # TODO make log
    print("No result found for {}. Counting as zero.".format(stat_name))
    return 0


def read_startswith(data, startswith):
    jdata = json.loads(data)

    with open(pd2_file) as out_file2:
        pd2_data = json.load(out_file2)

    stats = len(jdata['playerstats']['stats'])

    result = []

    for index in range(stats):
        index_str = str(jdata['playerstats']['stats'][index]['name'])
        if index_str.startswith(startswith):

            if startswith == "enemy_kills_":
                for word in range(len(pd2_data['Kills'])):
                    if index_str == ("enemy_kills_" + pd2_data['Kills'][word]):
                        result.append(jdata['playerstats']['stats'][index]['value'])

            if startswith == "difficulty_":
                for word in range(len(pd2_data['Difficulty'])):
                    if index_str.endswith(pd2_data['Difficulty'][word]):
                        result.append(jdata['playerstats']['stats'][index]['value'])

    return result


def weapon_read(data):
    # http://wiki.modworkshop.net/Payday_2/Weapon_IDs
    jdata = json.loads(data)

    with open(pd2_file) as out_file3:
        pd2_data = json.load(out_file3)

    stats = len(jdata['playerstats']['stats'])
    # achievements = len(jdata['playerstats']['achievements'])
    # weapons = len(pd2_data)

    highest_kills = 0
    highest_gun = ""

    for index in range(stats):
        if str(jdata['playerstats']['stats'][index]['name']).startswith('weapon_kills_'):
            if int(jdata['playerstats']['stats'][index]['value']) > highest_kills:
                highest_kills = int(jdata['playerstats']['stats'][index]['value'])
                highest_gun = str(jdata['playerstats']['stats'][index]['name'])

    if pd2_data['Weapons'][highest_gun]:
        highest_gun = pd2_data['Weapons'][highest_gun]

    if highest_gun == "" or highest_kills == 0:
        return "N/A", "N/A"
    else:
        return highest_gun, highest_kills


def armor_read(data):
    jdata = json.loads(data)

    with open(pd2_file) as out_file4:
        pd2_data = json.load(out_file4)

    stats = len(jdata['playerstats']['stats'])

    # TODO better variable names

    highest = 0
    highest_armor = ""

    for index in range(stats):
        # print("arm: {}, use: {}".format(highest_armor, highest))
        if str(jdata['playerstats']['stats'][index]['name']).startswith('armor_used_level_'):
            if int(jdata['playerstats']['stats'][index]['value']) > highest:
                highest = int(jdata['playerstats']['stats'][index]['value'])
                highest_armor = str(jdata['playerstats']['stats'][index]['name'])

    if pd2_data['Armor'][highest_armor]:
        highest_armor = pd2_data['Armor'][highest_armor]

    if highest_armor == "" or highest == 0:
        return "N/A", "N/A"
    else:
        return highest_armor, highest


def gadget_read(data):
    jdata = json.loads(data)

    with open(pd2_file) as out_file5:
        pd2_data = json.load(out_file5)

    stats = len(jdata['playerstats']['stats'])

    # TODO better variable names

    highest = 0
    highest_gadget = ""

    for index in range(stats):
        # print("arm: {}, use: {}".format(highest_gadget, highest))
        if str(jdata['playerstats']['stats'][index]['name']).startswith('gadget_used_'):
            if int(jdata['playerstats']['stats'][index]['value']) > highest:
                highest = int(jdata['playerstats']['stats'][index]['value'])
                highest_gadget = str(jdata['playerstats']['stats'][index]['name'])

    if pd2_data['Gadget'][highest_gadget]:
        highest_gadget = pd2_data['Gadget'][highest_gadget]

    if highest_gadget == "" or highest == 0:
        return "N/A", "N/A"
    else:
        return highest_gadget, highest


