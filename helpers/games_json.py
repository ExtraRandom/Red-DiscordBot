import json

file = "helpers/games.json"


def find_stat(stat, data):
    """
    For finding a single stat from the given data

    :param stat: The stat to find
    :param data: The data to find the stat in
    :return: The value of the stat or -1 if it wasn't found
    """
    # print("finding stat ", stat)
    try:
        loops = len(data)

        for i in range(loops):
            # print("i is ", i, " and loops is ", loops)
            if data[i]['name'] == stat:
                return data[i]['value']

        return 0
    except Exception as e:
        print("Error in games_json find_stat command. Error is: ", e)
        return -1


def get_stats(game, stat, data):
    """
    Get an array of stats of a similar type (i.e. if they all start with "total_kills_" within the data

    :param game: The game to get stats from
    :param stat: The stat type to find (this is the catergory in games.json (i.e. 'Kills' under the CSGO part
    :param data: Data to find the stats within
    :return: The stats
    """
    with open(file, "r") as out_file:
        jdata = json.load(out_file)

    if game == "pd2":
        stats = jdata["PD2"]

        if stat == "kills":
            stats = stats['Kills']
            stuff = stat_looper(data, stats, "enemy_kills_")
            return stuff

        elif stat == "diffs":
            stats = stats['Difficulty']
            stuff = stat_looper(data, stats, "difficulty_")
            return stuff

    elif game == "csgo":
        stats = jdata['CSGO']

        if stat == "kills":
            stats = stats['Kills']
            stuff = stat_looper(data, stats, "total_kills_")
            return stuff

        elif stat == "maps":
            stats = stats['Maps']
            stuff = stat_looper(data, stats, "total_wins_map_")
            return stuff

        elif stat == "general":
            stats = stats['General Stats']
            stuff = stat_looper(data, stats, "")
            return stuff


def stat_looper(data, stats, starts_with):
    """
    Loops through the data to find stats based on input

    :param data: The Data
    :param stats: See below
    :param starts_with: What do all the stats start with (will be combined with each entry in stats
    :return: The stats
    """
    result = []
    loops = len(stats)
    i_loops = len(data)
    for index in range(loops):
        for i_index in range(i_loops):
            if data[i_index]['name'] == "{}{}".format(starts_with, stats[index]):
                result.append(data[i_index]['value'])
                break
            if i_index == i_loops -1:
                result.append(0)
    return result


def read_json_for_game(game):
    """
    Read in the json and filter to a certain game and then return

    :param game: Must be the same as spelling/caps as it is in games.json
    :return: The json as a string
    """
    with open(file, "r") as out_file:
        jdata = json.load(out_file)

    try:
        r_json = jdata[game]
    except KeyError as e:
        print("Key error for read_json_for_game: {}".format(e))
        return None

    return r_json


def item_stats(data):
    """
    Specifically meant for the PD2 command to retrieve the most used gun, armour and gadgets and they ammount
    of kills/uses they have

    :param data: The data to search within
    :return:
    """

    gun_name = ""
    gun_kills = 0

    armour_name = ""
    armour_uses = 0

    gadget_name = ""
    gadget_uses = 0

    for index in range(3):
        if index == 0:
            look_for = "weapon_kills_"
        elif index == 1:
            look_for = "armor_used_level_"
        elif index == 2:
            look_for = "gadget_used_"

        for l_index in range(len(data)):
            if str(data[l_index]['name']).startswith(look_for):
                # print(data[l_index]['name'])
                # print(data[l_index]['value'])

                if look_for == "weapon_kills_":
                    if int(data[l_index]['value']) > gun_kills:
                        gun_kills = int(data[l_index]['value'])
                        gun_name = data[l_index]['name']

                if look_for == "armor_used_level_":
                    if int(data[l_index]['value']) > armour_uses:
                        armour_uses = int(data[l_index]['value'])
                        armour_name = data[l_index]['name']

                if look_for == "gadget_used_":
                    if int(data[l_index]['value']) > gadget_uses:
                        gadget_uses = int(data[l_index]['value'])
                        gadget_name = data[l_index]['name']

    with open(file) as names_file:
        load = json.load(names_file)
        names = load['PD2']

        gun_name = names['Weapons'][gun_name]
        gadget_name = names['Gadget'][gadget_name]
        armour_name = names['Armor'][armour_name]

    return gun_name, gun_kills, gadget_name, gadget_uses, armour_name, armour_uses
