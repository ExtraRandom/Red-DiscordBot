import json
import bs4
import requests
import aiohttp
import asyncio

id_file = "helpers/steam_id.json"
pd2_file = "helpers/pd2_info.json"
unturned_file = "helpers/unturned.json"
csgo_file = "helpers/csgo.json"

"""
For reading and writing to steam_id.json
"""


def read(user):
    with open(id_file) as data_file:
        data = json.load(data_file)
        # TODO check user exists - if no stats exist then user doesnt own the game
        try:
            return data[user]
        except KeyError as e:
            print("KeyError: {}")
            return 0


def write(user_discord, user_steamid):
    """CURRENTLY THIS MESSES UP THE FILE WITH /'s N SHIT"""
    with open(id_file) as data_file:
        data = json.load(data_file)
        try:
            data[user_discord] = user_steamid
            print(data)
            with open(id_file, "w") as data_file2:
                jdata = json.dumps(data)
                json.dump(jdata, data_file2)
            return True
        except KeyError as e:
            print("ker err: {}".format(e))
            return False


async def check_profile(user_id):
    """Returns True if profile exists, false if not"""

    with aiohttp.ClientSession() as session:
        url = "http://steamcommunity.com/profiles/{}".format(user_id)
        async with session.get(url) as resp:
            try:
                data = await resp.text()
                doc = bs4.BeautifulSoup(data, "html.parser")
                error = doc.select('head title')[0].getText()
                if error == "Steam Community :: Error":
                    print("false exist")
                    return False
                else:
                    print("true exist")
                    return True
            except Exception as e:
                print("something went wrong: {}".format(e))


"""
For reading the .json containing stat info
"""


def steam_read(data, stat_name):
    jdata = json.loads(data)
    stats = len(jdata['playerstats']['stats'])

    for index in range(stats):
        if jdata['playerstats']['stats'][index]['name'] == stat_name:
            return jdata['playerstats']['stats'][index]['value']
    print("No result found for {}. Counting as zero.".format(stat_name))
    return 0


def csgo_info():

    with open(csgo_file) as out_file2:
        game_data = json.load(out_file2)

    return game_data  # game_data['Kills'], game_data['Maps']


def read_startswith(data, startswith, game):
    jdata = json.loads(data)

    game_data = 0

    result = []

    if game == "pd2":
        with open(pd2_file) as out_file2:
            game_data = json.load(out_file2)

    elif game == "unturned":
        with open(unturned_file) as out_file2:
            game_data = json.load(out_file2)

    elif game == "csgo":
        with open(csgo_file) as out_file2:
            game_data = json.load(out_file2)

    if game == "pd2":
        if startswith == "enemy_kills_":
            to_find = game_data['Kills']
            result = stat_loop(jdata, to_find, startswith)
        if startswith == "difficulty_":
            to_find = game_data['Difficulty']
            result = stat_loop(jdata, to_find, startswith)

    elif game == "unturned":
        if startswith == "Kills_":
            to_find = game_data['Kills']
            result = stat_loop(jdata, to_find, startswith)
        if startswith == "Found_":
            to_find = game_data['Found']
            result = stat_loop(jdata, to_find, startswith)
        if startswith == "Travel_":
            to_find = game_data['Travel']
            result = stat_loop(jdata, to_find, startswith)
        if startswith == "":
            to_find = game_data['WeaponUsage']
            result = stat_loop(jdata, to_find, startswith)

    elif game == "csgo":
        if startswith == "total_kills_":
            to_find = game_data['Kills']
            result = stat_loop(jdata, to_find, startswith)
        if startswith == "":
            to_find = game_data['General Stats']
            result = stat_loop(jdata, to_find, startswith)
        if startswith == "total_wins_map_":
            to_find = game_data['Maps']
            result = stat_loop(jdata, to_find, startswith)

    return result


def stat_loop(jdata, to_find, startswith):
    result = []
    loops = len(to_find)
    i_loops = len(jdata['playerstats']['stats'])
    for index in range(loops):
        for i_index in range(i_loops):
            if jdata['playerstats']['stats'][i_index]['name'] == "{}{}".format(startswith, to_find[index]):
                result.append(jdata['playerstats']['stats'][i_index]['value'])
                break
            if i_index == i_loops - 1:
                result.append(0)
    # print(result)
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
    try:
        if pd2_data['Weapons'][highest_gun]:
            highest_gun = pd2_data['Weapons'][highest_gun]
    except KeyError as e:
        highest_gun = ""

    if highest_gun == "" or highest_kills == 0:
        return "N/A", "N/A"
    else:
        return highest_gun, highest_kills


def armor_read(data):
    jdata = json.loads(data)

    with open(pd2_file) as out_file4:
        pd2_data = json.load(out_file4)

    stats = len(jdata['playerstats']['stats'])

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


