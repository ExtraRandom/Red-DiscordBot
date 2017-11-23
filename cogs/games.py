import asyncio
import logging
from datetime import datetime

from helpers import tokens as t, id_json, games_json

import aiohttp
from discord.ext import commands
import discord

from mcstatus import MinecraftServer

import requests
import json

from re import sub
import pydest


loop = asyncio.get_event_loop()
log = logging.getLogger(__name__)


class Games:
    def __init__(self, bot):
        self.bot = bot
        # self.url_base = "https://www.bungie.net/Platform"
        self.img_base = "https://www.bungie.net"
        self.er_id = "<@92562410493202432>"
        self.s = "Steam"
        self.b = "BattleNet"

    @commands.command(name="mc")
    async def minecraft_ip(self, ip: str):
        """Get Status of Minecraft Servers"""
        try:
            server = MinecraftServer.lookup(ip)
            status = server.status()
            data = status.raw  # print(data)
            ver = data['version']['name']
            s_desc = "N/A"
            try:
                s_desc = data['description']['text']
            except TypeError:
                s_desc = data['description']

            desc_filter = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "k", "l",
                           "m", "n", "o", "r"]

            for item in desc_filter:
                s_desc = str(s_desc).replace("§{}".format(item), "")

            s_desc = sub(' +', ' ', s_desc)  # not sure if this is actually needed

            player_count = int(data['players']['online'])
            player_limit = int(data['players']['max'])

            if player_count > 1000:
                try_players = False
            else:
                try_players = True

            players = ""

            if try_players:
                try:
                    for player in data['players']['sample']:
                        players += "{}, ".format(player['name'])
                    players = players[:-2]  # Remove final comma and the space after it
                except Exception:
                    players = "None"
            else:
                players = "N/A"

            embed = discord.Embed(title="Status of {}".format(ip),
                                  colour=discord.Colour.green())

            embed.add_field(name="Info", value="Version Info: {}\n\n"
                                               "Player Count/Limit: **{}**/**{}**\n"
                                               "Player Sample: {}\n\n"
                                               "Description: {}".format(ver, player_count, player_limit, players,
                                                                        s_desc))

            await self.bot.say(embed=embed)

        except ValueError as e:
            await self.bot.say("Error Occured - Check IP is correct - Value Error")
            log.warn(e)

        except ConnectionRefusedError as e:
            await self.bot.say("Error Occured - Target Refused Connection")
            log.warn(e)

        except Exception as e:
            await self.bot.say("Error Occured - Server didn't respond")
            log.warn(e)

    @commands.command()
    async def status(self):
        """Get Status of Steam and CS:GO servers"""
        try:

            embed = discord.Embed(title="Status of Steam", description="Also includes TF2, Dota 2 and CSGO Status",
                                  url="https://steamstat.us/", colour=discord.Colour.red())

            url = 'https://steamgaug.es/api/v2'

            with aiohttp.ClientSession() as session:
                async with session.get(url)as resp:
                    data = await resp.json()

                    client = data["ISteamClient"]["online"]

                    community = data["SteamCommunity"]["online"]
                    community_error = data["SteamCommunity"]["error"]

                    store = data["SteamStore"]["online"]
                    store_error = data["SteamStore"]["error"]

                    user = data["ISteamUser"]["online"]
                    user_error = data["ISteamUser"]["error"]

                    items_440 = data["IEconItems"]["440"]["online"]
                    items_440_error = data["IEconItems"]["440"]["error"]

                    items_570 = data["IEconItems"]["570"]["online"]
                    items_570_error = data["IEconItems"]["570"]["error"]

                    items_730 = data["IEconItems"]["570"]["online"]
                    items_730_error = data["IEconItems"]["570"]["error"]

                    games_440 = data["ISteamGameCoordinator"]["440"]["online"]
                    games_440_error = data["ISteamGameCoordinator"]["440"]["error"]
                    games_570 = data["ISteamGameCoordinator"]["570"]["online"]
                    games_570_error = data["ISteamGameCoordinator"]["570"]["error"]
                    games_570_searching = data["ISteamGameCoordinator"]["570"]["stats"]["players_searching"]
                    games_730 = data["ISteamGameCoordinator"]["730"]["online"]
                    games_730_error = data["ISteamGameCoordinator"]["730"]["error"]

                    # TODO change this so it's if statements instead of this mess

                    try:
                        games_440_error_code = data["ISteamGameCoordinator"]["440"]["error"]["code"]
                        # games_440_error_connect = data["ISteamGameCoordinator"]["440"]["error"]["connect"]
                        games_440_error = "Error: {}".format(games_440_error_code)

                        games_570_error_code = data["ISteamGameCoordinator"]["570"]["error"]["code"]
                        # games_570_error_connect = data["ISteamGameCoordinator"]["570"]["error"]["connect"]
                        games_570_error = "Error: {}".format(games_570_error_code)

                        games_730_error_code = data["ISteamGameCoordinator"]["730"]["error"]["code"]
                        # games_730_error_connect = data["ISteamGameCoordinator"]["730"]["error"]["connect"]
                        games_730_error = "Error: {}".format(games_730_error_code)

                    except Exception as e:
                        pass

                    try:
                        games_730_searching = data["ISteamGameCoordinator"]["730"]["stats"]["players_searching"]
                        games_730_wait = data["ISteamGameCoordinator"]["730"]["stats"]["average_wait"]
                        games_730_matches = data["ISteamGameCoordinator"]["730"]["stats"]["ongoing_matches"]
                        games_730_players = data["ISteamGameCoordinator"]["730"]["stats"]["players_online"]
                    except Exception as e:
                        pass

                    if client == 1: client = "Online"
                    else: client = "Down"

                    if community == 1: community = "Online"
                    else: community = "Down"

                    if store == 1: store = "Online"
                    else: store = "Down"

                    if user == 1: user = "Online"
                    else: user = "Down"

                    if items_440 == 1: items_440 = "Online"
                    else: items_440 = "Down"

                    if items_570 == 1: items_570 = "Online"
                    else: items_570 = "Down"

                    if items_730 == 1: items_730 = "Online"
                    else: items_730 = "Down"

                    if games_440 == 1: games_440 = "Online"
                    else: games_440 = "Down"

                    if games_570 == 1: games_570 = "Online"
                    else: games_570 = "Down"

                    if games_730 == 1: games_730 = "Online"
                    else: games_730 = "Down"

                    embed.add_field(name="Steam", value="**Client:** {}\n"
                                                        "**Community:** {}, {}\n"
                                                        "**Store:** {}, {}\n"
                                                        "**User:** {}, {}\n".format(client, community, community_error,
                                                                                store, store_error, user, user_error))

                    embed.add_field(name="Team Fortress 2", value="**Items:** {}, {}\n"
                                                                  "**Games:** {}, {}".format(items_440, items_440_error,
                                                                                         games_440, games_440_error))

                    embed.add_field(name="Dota 2", value="**Items:** {}, {}\n"
                                                         "**Games:** {}, {}\n"
                                                         "**Players Searching:** {}".format(items_570, items_570_error,
                                                                                        games_570, games_570_error,
                                                                                        games_570_searching))
                    try:
                        embed.add_field(name="CS:GO", value="**Items:** {}, {}\n"
                                                            "**Games:** {}, {}\n"
                                                            "**Players Online:** {}\n"
                                                            "**Players Searching:** {}\n"
                                                            "**Ongoing Matches:** {}\n"
                                                            "**Average Wait:** {}".format(items_730, items_730_error,
                                                                                      games_730, games_730_error,
                                                                                      games_730_players,
                                                                                      games_730_searching,
                                                                                      games_730_matches,
                                                                                      games_730_wait))
                    except Exception as e:
                        embed.add_field(name="CS:GO", value="**Items:** {}, {}\n"
                                                            "**Games:** {}, {}\n"
                                                            "".format(items_730, items_730_error, games_730,
                                                                      games_730_error))

                    embed.set_footer(text="As of {} UTC".format(datetime.utcnow()))

                    try:
                        await self.bot.say(embed=embed)
                    except discord.HTTPException as e:
                        await self.bot.say("I need the `Embed links` permission to send this")

        except Exception as e:
            await self.bot.say("Error occurred whilst getting Steam Status, try again in a few minutes.")
            log.warn(e)
            print(e)

    @commands.command(pass_context=True)
    async def pd2(self, ctx):
        """Get Payday 2 Stats, Mention someone to get their stats
        E.g. "?pd2" for personal stats, "?pd2 @SomeUser" for SomeUser's stats
        """
        run = True
        user_id = parse_user(ctx.message)
        steam_id = id_json.read(user_id, self.s)
        username = await steam_from_id(steam_id)

        if user_id is not None:
            user = "<@" + user_id + ">"
        else:
            await self.bot.say("Error: '{}' is not a user. Try mentioning the desired user to get their stats"
                               ", or only type the command without anything following it you get your own stats."
                               "".format(" ".join(ctx.message.content.split(" ")[1:])))
            return

        if steam_id == 0:
            await self.bot.say("Error: User {} has no Steam ID associated to them. {} plz fix!".format(user,
                                                                                                       self.er_id))
            return

        if not t.web_api == "" and run:
            try:
                link = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=218620&key={}" \
                       "&steamid={}&format=json" \
                       "".format(t.web_api, steam_id)
                # print("link ", link)

                with aiohttp.ClientSession() as session:
                    async with session.get(link)as resp:
                        data = await resp.text()  # resp.json()

                        stats = json.loads(data)['playerstats']['stats']

                        try:
                            heist_s = games_json.find_stat("heist_success", stats)
                        except KeyError:
                            await self.bot.say("Error: User {} ({} on Steam) does not own Payday 2".format(user,
                                                                                                           username))
                            return

                        if heist_s == -1:
                            await self.bot.say("Error occurred whilst reading PD2 stats. (Code 1)")
                            print("PD2ERROR")
                            return

                        heist_f = games_json.find_stat("heist_failed", stats)
                        kills = games_json.get_stats("pd2", "kills", stats)
                        diffs = games_json.get_stats("pd2", "diffs", stats)

                        most_used_gun, most_used_kills, most_used_gadget, most_used_gadget_uses,\
                            most_used_armor, most_used_armor_uses = games_json.item_stats(stats)

                        fbi = kills[1] + kills[2] + kills[3]
                        cop_swat = kills[0] + kills[29] + kills[7] + kills[6] + kills[5]
                        tank_kills = kills[13] + kills[23] + kills[24] + kills[22] + kills[19]
                        gang_mob_kills = kills[16] + kills[15] + kills[9]
                        civ_kills = kills[18] + kills[17]
                        kills_shield = kills[11]
                        kills_sniper = kills[10]
                        kills_cloaker = kills[12]

                        total_kills = 0
                        for i in range(0, len(kills)):
                            total_kills = total_kills + kills[i]

                        other_kills = total_kills - (fbi + cop_swat + tank_kills + gang_mob_kills + civ_kills +
                                                     kills_cloaker + kills_shield + kills_sniper)

                        embed = discord.Embed(title="PD2 Stats for " + username,
                                              colour=discord.Colour.blue())
                        # ,url="http://pd2stats.com/profiles/" + user_id)
                        # That website no longer seems to work :/

                        embed.add_field(name="Heists", value="**Completed:** {}\n"
                                                             "**Failed:** {}"
                                                             "".format(heist_s, heist_f))

                        embed.add_field(name="Difficulty", value="**Normal:** {}\n"
                                                                 "**Hard:** {}\n"
                                                                 "**Very Hard:** {}\n"
                                                                 "**Overkill:** {}\n"
                                                                 "**Mayhem:** {}\n"
                                                                 "**Deathwish:** {}\n"
                                                                 "**One Down:** {}"
                                                                 "".format(diffs[0], diffs[1], diffs[2], diffs[3]
                                                                           , diffs[5], diffs[4], diffs[6]))

                        embed.add_field(name="Kills", value="**FBI:** {}\n"
                                                            "**Cops/SWAT:** {}\n"
                                                            "**Shield:** {}\n"
                                                            "**Sniper:** {}\n"
                                                            "**Cloaker:** {}\n"
                                                            "**Bulldozer:** {}\n"
                                                            "**Gang/Mob:** {}\n"
                                                            "**Civilian:** {}\n"
                                                            "**Other:** {}"
                                                            "".format(fbi, cop_swat, kills_shield, kills_sniper,
                                                                      kills_cloaker, tank_kills, gang_mob_kills,
                                                                      civ_kills, other_kills))
                        embed.add_field(name="Favourite Gun",
                                        value="**{}**\n{} kills".format(most_used_gun, most_used_kills))
                        embed.add_field(name="Favourite Gadget",
                                        value="**{}**\n{} uses".format(most_used_gadget, most_used_gadget_uses))
                        embed.add_field(name="Favourite Armor",
                                        value="**{}**\n{} uses".format(most_used_armor, most_used_armor_uses))

                        embed.set_footer(text="As of {} UTC".format(datetime.utcnow()))

                        try:
                            await self.bot.say(embed=embed)
                        except discord.HTTPException:
                            await self.bot.say("I need the `Embed links` permission "
                                               "to send this")

            except KeyError as e:
                log.warn("KeyError: {}".format(e))
                await self.bot.say("Error: User {} has no Steam ID associated to them or an error occurred fetching "
                                   "stats.".format(user))
        else:
            await self.bot.say("This command is disabled currently. Ask the bot owner to add a Steam WebAPI key in "
                               "tokens.py for it to be enabled")

    @commands.command(pass_context=True)
    async def csgo(self, ctx):
        """Get CS:GO Stats, Mention someone to get their stats
        E.g. "?csgo" for personal stats, "?csgo @SomeUser" for SomeUser's stats
        """
        user_id = parse_user(ctx.message)
        steam_id = id_json.read(user_id, self.s)
        username = await steam_from_id(steam_id)
        if user_id is not None:
            user = "<@" + user_id + ">"
        else:
            await self.bot.say("Error: '{}' is not a user. Try mentioning the desired user to get their stats"
                               ", or only type the command without anything following it you get your own stats."
                               "".format(" ".join(ctx.message.content.split(" ")[1:])))
            return

        if steam_id == 0:
            await self.bot.say("Error: User {} has no Steam ID associated to them.".format(user))
            return

        if not t.web_api == "":
            try:
                link = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={}" \
                       "&steamid={}&format=json" \
                       "".format(t.web_api, steam_id)

                with aiohttp.ClientSession() as session:
                    async with session.get(link)as resp:
                        data = await resp.text()  # resp.json()
                        # print(link)
                        stats = json.loads(data)['playerstats']['stats']

                        kills = games_json.get_stats("csgo", "kills", stats)
                        mapwins = games_json.get_stats("csgo", "maps", stats)
                        general = games_json.get_stats("csgo", "general", stats)
                        headshots = games_json.find_stat("total_kills_headshot", stats)

                        gdata = games_json.read_json_for_game("CSGO")

                        kd_ratio = general[0] / general[1]
                        kd_ratio = str(kd_ratio)[:4]

                        top_guns = get_top5(kills)
                        top_maps = get_top5(mapwins)

                        embed = discord.Embed(title="CS:GO Stats for {}".format(username),
                                              colour=discord.Colour.dark_green())

                        embed.add_field(name="General", value="**Total Kills:** {}\n"
                                                              "**Total Deaths:** {}\n"
                                                              "**K/D Ratio:** {}\n"
                                                              "**Bombs Planted:** {}\n"
                                                              "**Bombs Defused:** {}\n"
                                                              "**Hostages Rescued:** {}"
                                                              "".format(general[0], general[1], kd_ratio,
                                                                        general[2], general[3], general[4]))

                        embed.add_field(name="Top Guns", value="**1:** {} - {} kills\n"
                                                               "**2:** {} - {} kills\n"
                                                               "**3:** {} - {} kills\n"
                                                               "**4:** {} - {} kills\n"
                                                               "**5:** {} - {} kills\n"
                                                               "".format(str(gdata['Kills'][top_guns[0]]).upper(),
                                                                         kills[top_guns[0]],
                                                                         str(gdata['Kills'][top_guns[1]]).upper(),
                                                                         kills[top_guns[1]],
                                                                         str(gdata['Kills'][top_guns[2]]).upper(),
                                                                         kills[top_guns[2]],
                                                                         str(gdata['Kills'][top_guns[3]]).upper(),
                                                                         kills[top_guns[3]],
                                                                         str(gdata['Kills'][top_guns[4]]).upper(),
                                                                         kills[top_guns[4]]
                                                                         ))

                        embed.add_field(name="Top Maps", value="**1:** {} - {} wins\n"
                                                               "**2:** {} - {} wins\n"
                                                               "**3:** {} - {} wins\n"
                                                               "**4:** {} - {} wins\n"
                                                               "**5:** {} - {} wins\n"
                                                               "".format(str(gdata['Maps'][top_maps[0]]).split("_")[1]
                                                                         .capitalize(), mapwins[top_maps[0]],
                                                                         str(gdata['Maps'][top_maps[1]]).split("_")[1]
                                                                         .capitalize(), mapwins[top_maps[1]],
                                                                         str(gdata['Maps'][top_maps[2]]).split("_")[1]
                                                                         .capitalize(), mapwins[top_maps[2]],
                                                                         str(gdata['Maps'][top_maps[3]]).split("_")[1]
                                                                         .capitalize(), mapwins[top_maps[3]],
                                                                         str(gdata['Maps'][top_maps[4]]).split("_")[1]
                                                                         .capitalize(), mapwins[top_maps[4]]))

                        percent = (general[5] / general[6]) * 100
                        embed.add_field(name="Accuracy", value="**Shots Hit:** {}\n"
                                                               "**Shots Fired:** {}\n"
                                                               "**Accuracy Percent:** {}%\n"
                                                               "**Headshots:** {}"
                                                               "".format(general[5], general[6],
                                                                         str(percent).split(".")[0], headshots))

                        embed.set_footer(text="As of {} UTC".format(datetime.utcnow()))

                        try:
                            await self.bot.say(embed=embed)
                        except discord.HTTPException:
                            await self.bot.say("I need the `Embed links` permission "
                                               "to send this")
            except KeyError as e:
                await self.bot.say("Error: User {} ({} on Steam) does not own CS:GO.".format(user,
                                                                                             username))
                log.warn("Key Error: {}".format(e))

    @commands.command(pass_context=True)
    async def overwatch(self, ctx, battletag_or_discord="myself", region="eu"):
        """Get Overwatch Stats

        Defaults to yourself if no one else is specified (this'll require your battletag to be on the list)
        Default Region is EU - Other Regions are 'eu', 'us' and 'kr'"""

        # Uses https://github.com/SunDwarf/OWAPI/blob/master/api.md
        # https://owapi.net/api/v3/u/ExtraRandom-2501/blob?format=json_pretty

        if battletag_or_discord == "myself":
            battletag_or_discord = ctx.message.author.id

        battletag = battle_net_parse_user(battletag_or_discord)
        if battletag == 0:
            await self.bot.say("'{}' is not a BattleTag or Discord Mention.".format(battletag_or_discord))
            return
        elif battletag == 1:
            await self.bot.say("User '{}' has no associated BattleTag. Tell {} to add it to the list! Until it is added"
                               " type their battletag instead. (i.e. ?overwatch ExtraRandom#2501)."
                               "".format(battletag_or_discord, self.er_id))
            return

        msg = await self.bot.say("Fetching Stats for {}".format(battletag))

        user = battletag.replace("#", "-")

        reg_eu = ["eu", "euro", "europe", "italy", "it", "fr", "france", "sp", "spain", "en", "england", "uk", "gb"]
        reg_us = ["australia", "aussie", "aus", "us", "usa", "na", "america", "au"]
        reg_kr = ["asia", "korea", "kr", "as", "china", "japan"]

        if region.lower() in reg_eu:
            reg = "eu"
        elif region.lower() in reg_us:
            reg = "us"
        elif region.lower() in reg_kr:
            reg = "kr"
        else:
            self.bot.edit_message(msg, "Unknown region: {}".format(region))
            return

        try:
            headers = {
                'User-Agent': 'DiscordBot'
            }
            link = "https://owapi.net/api/v3/u/{}/stats?format=json_pretty".format(user)  # print(link)

            with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(link)as resp:
                    data = await resp.json()

                    try:
                        error = data['error']
                        await self.bot.edit_message(msg, "User '{}' does not own Overwatch. If this is incorrect, "
                                                         "please check your spelling.".format(battletag_or_discord))
                        return
                    except KeyError:
                        pass

                    stats = data[reg]['stats']['quickplay']
                    comp_stats = data[reg]['stats']['competitive']

                    qp_time = int(stats['game_stats']['time_played'])
                    comp_time = int(comp_stats['game_stats']['time_played'])
                    time_played = qp_time + comp_time

                    level = stats['overall_stats']['level']
                    prestige = stats['overall_stats']['prestige']
                    avatar = stats['overall_stats']['avatar']

                    qp_wins = stats['overall_stats']['wins']
                    comp_wins = comp_stats['overall_stats']['wins']
                    comp_played = comp_stats['overall_stats']['games']
                    comp_tier = str(comp_stats['overall_stats']['tier']).capitalize()

                    qp_death = int(stats['game_stats']['deaths'])
                    qp_elims = int(stats['game_stats']['eliminations'])
                    qp_heals = int(stats['game_stats']['healing_done'])
                    qp_objks = int(stats['game_stats']['objective_kills'])

                    comp_death = int(comp_stats['game_stats']['deaths'])
                    comp_elims = int(comp_stats['game_stats']['eliminations'])
                    comp_heals = int(comp_stats['game_stats']['healing_done'])
                    comp_objks = int(comp_stats['game_stats']['objective_kills'])

                    qp_md_total = int(stats['game_stats']['medals'])
                    qp_md_gold = int(stats['game_stats']['medals_gold'])
                    qp_md_silver = int(stats['game_stats']['medals_silver'])
                    qp_md_bronze = int(stats['game_stats']['medals_bronze'])

                    comp_md_total = int(comp_stats['game_stats']['medals'])
                    comp_md_gold = int(comp_stats['game_stats']['medals_gold'])
                    comp_md_silver = int(comp_stats['game_stats']['medals_silver'])
                    comp_md_bronze = int(comp_stats['game_stats']['medals_bronze'])

                    if prestige >= 1:
                        level_final = str(prestige) + "-" + str(level)
                    else:
                        level_final = level

                    embed = discord.Embed(title="Overwatch Stats for {}".format(battletag),
                                          colour=discord.Colour.orange(),
                                          description="Does NOT include Arcade Stats (QP + Comp only)")
                    embed.set_thumbnail(url=avatar)

                    embed.add_field(name="General", value="**Time Played:** {} hours\n"
                                                          "**Level:** {}\n"
                                                          "**Quick Play Wins:** {}\n"
                                                          "**Competitive Wins:** {}\n"
                                                          "**Competitive Tier:** {}"
                                                          "".format(time_played, level_final, qp_wins, comp_wins,
                                                                    comp_tier))

                    embed.add_field(name="Quick Play Totals", value="**Eliminations:** {}\n"
                                                                    "**Deaths:** {}\n"
                                                                    "**Healing Done:** {}\n"
                                                                    "**Objective Kills:** {}"
                                                                    "".format(qp_elims, qp_death,
                                                                              qp_heals, qp_objks))

                    embed.add_field(name="Quick Play Medals", value="**Total:** {}\n"
                                                                    "**Gold:** {}\n"
                                                                    "**Silver:** {}\n"
                                                                    "**Bronze:** {}\n"
                                                                    "".format(qp_md_total, qp_md_gold,
                                                                              qp_md_silver, qp_md_bronze))

                    embed.add_field(name="Competitive Totals", value="**Eliminations:** {}\n"
                                                                     "**Deaths:** {}\n"
                                                                     "**Healing Done:** {}\n"
                                                                     "**Objective Kills:** {}"
                                                                     "".format(comp_elims, comp_death,
                                                                               comp_heals, comp_objks))

                    embed.add_field(name="Competitive Medals", value="**Total:** {}\n"
                                                                     "**Gold:** {}\n"
                                                                     "**Silver:** {}\n"
                                                                     "**Bronze:** {}\n"
                                                                     "".format(comp_md_total, comp_md_gold,
                                                                               comp_md_silver, comp_md_bronze))

                    embed.set_footer(text="As of {} UTC".format(datetime.utcnow()))

        except KeyError as e:
            print("KeyError in Overwatch command: {}".format(e))

        await self.bot.delete_message(msg)
        if 'embed' in locals():
            try:
                await self.bot.say(embed=embed)
            except discord.HTTPException:
                await self.bot.say("I need the `Embed links` permission "
                                   "to send this")
                # TODO repeat this on other commands
        else:
            await self.bot.say("Error: Couldn't fetch Overwatch stats, check spelling and try again.")

    @commands.command()
    async def pubg(self, bg_name: str, region="eu"):
        """Get PUBG Stats (Use in-game name)

        Region is Optional Argument, Defaults to EU

        Regions: AS, NA, SEA, EU, OC, SA, All
        """

        # TODO redo formatting maybe remove some stats that just make it messy
        # TODO error catch - if user enters a name that doesnt exist

        msg = await self.bot.say("Fetching PUBG Stats for {}".format(bg_name))

        region = region.lower()

        key = t.pubg_api
        url_base = "https://pubgtracker.com/api/profile/pc/"
        url = "{}{}".format(url_base, bg_name)
        headers = {
            'content-type': "application/json",
            'trn-api-key': key,
        }

        response = requests.request("GET", url, headers=headers)

        # print(response.text)
        data = json.loads(response.text)
        # print(data)

        working = True
        reason = ""

        try:
            if data['message']:
                working = False
                reason = data['message']
        except KeyError:
            pass

        try:
            if data['error']:
                working = False
                reason = data['error']
        except KeyError:
            pass

        if working:
            season = data['seasonDisplay']
            avatar = data['Avatar']
            properName = data['PlayerName']
            update_time = str(data['LastUpdated'])
            last_updated = update_time.split(".")[0].replace("T", " ")
            site_link = "https://pubgtracker.com/profile/pc/{}?region={}".format(properName, region)

            solo_n = pubg_find("solo", region, data)
            duo_n = pubg_find("duo", region, data)
            squad_n = pubg_find("squad", region, data)

            embed = discord.Embed(title="{} PUBG Stats for {}".format(region.upper(), properName),
                                  description=season,
                                  colour=discord.Colour.gold(),
                                  url=site_link)

            if solo_n is not None:
                solo_data = pubg_filter(data, solo_n)
                embed.add_field(name="Solo",
                                value="Kill Death Ratio: {}\n"
                                      "Kills: {}\n"
                                      "Played: {}\n"
                                      "Wins: {}\n"
                                      "Rank: {}\n"
                                      "Rank %: Top {}%\n"
                                      "Top 10's: {}"
                                      "".format(solo_data[0], solo_data[1], solo_data[2], solo_data[3], solo_data[4],
                                                solo_data[5], solo_data[6]))
            else:
                embed.add_field(name="Solo", value="No Data for Solo Matches")

            if duo_n is not None:
                duo_data = pubg_filter(data, duo_n)
                embed.add_field(name="Duo",
                                value="Kill Death Ratio: {}\n"
                                      "Kills: {}\n"
                                      "Played: {}\n"
                                      "Wins: {}\n"
                                      "Rank: {}\n"
                                      "Rank %: Top {}%\n"
                                      "Top 10's: {}"
                                      "".format(duo_data[0], duo_data[1], duo_data[2], duo_data[3], duo_data[4],
                                                duo_data[5], duo_data[6]))
            else:
                embed.add_field(name="Duo", value="No Data for Duo Matches")

            if squad_n is not None:
                squad_data = pubg_filter(data, squad_n)

                embed.add_field(name="Squad",
                                value="Kill Death Ratio: {}\n"
                                      "Kills: {}\n"
                                      "Played: {}\n"
                                      "Wins: {}\n"
                                      "Rank: {}\n"
                                      "Rank %: Top {}%\n"
                                      "Top 10's: {}"
                                      "".format(squad_data[0], squad_data[1], squad_data[2], squad_data[3],
                                                squad_data[4], squad_data[5], squad_data[6]))
            else:
                embed.add_field(name="Squad", value="No Data for Squad Matches")

            embed.set_thumbnail(url=avatar)
            embed.set_footer(text="Stats Last Updated: {}".format(last_updated))

            await self.bot.delete_message(msg)
            await self.bot.say(embed=embed)

        else:  # if not working
            await self.bot.edit_message(msg, "Error occurred whilst getting data. Try again later.\nReason from Server:"
                                             " {}".format(reason))

    @commands.command(pass_context=True)
    async def d2(self, ctx, battletag_or_discord="myself", character=1):
        """
        Get Destiny 2 Stats and Equipped Items

        Defaults to yourself if no one else is specified (this'll require your battletag to be on the list)
        Defaults to character 1 if no character is specified
        """
        # Some code from https://github.com/jgayfer/spirit/blob/master/cogs/destiny.py

        # TODO allow for something like "?d2 2" (will think you're changing battletag atm)

        if battletag_or_discord == "myself":
            battletag_or_discord = ctx.message.author.id

        bnet = battle_net_parse_user(battletag_or_discord)
        if bnet == 0:
            await self.bot.say("'{}' is not a BattleTag or Discord Mention.".format(battletag_or_discord))
            return
        elif bnet == 1:
            await self.bot.say("User '{}' has no associated BattleTag. Tell {} to add it to the list! Until it is added"
                               " type their battletag instead. (i.e. ?d2 ExtraRandom#2501)."
                               "".format(battletag_or_discord, self.er_id))
            return

        destiny = pydest.Pydest(t.d2_api)
        pre_data = await destiny.api.search_destiny_player(4, bnet)  # print(pre_data)
        try:
            user_id = pre_data['Response'][0]['membershipId']  # print("user id: {}".format(user_id))
        except IndexError:
            await self.bot.say("User '{}' does not own Destiny 2.".format(bnet))
            return

        try:
            profile_data = await destiny.api.get_profile(4, user_id, ['characters', 'characterEquipment', 'profiles'])
        except pydest.PydestException as e:
            await self.bot.say("Error getting Guardian Stats (Code: 1)")
            return

        if profile_data['ErrorCode'] != 1:
            await self.bot.say("Error getting Guardian Stats (Code: 2)")
            return

        chars = len(profile_data['Response']['characters']['data'])
        if character > chars or character < 1:
            await self.bot.say("No chatacter #{} found, defaulting to character #1 instead".format(character))
            character = 1

        char = character - 1
        char_id = 0

        try:
            char_id = profile_data['Response']['profile']['data']['characterIds'][char]
        except Exception as e:
            await self.bot.say("Error getting Guardian Stats (Code: 3)")
            return

        try:
            char_data = profile_data['Response']['characters']['data'][char_id]

            role_dict = await destiny.decode_hash(char_data['classHash'], 'DestinyClassDefinition')
            role = role_dict['displayProperties']['name']

            gender_dict = await destiny.decode_hash(char_data['genderHash'], 'DestinyGenderDefinition')
            gender = gender_dict['displayProperties']['name']

            race_dict = await destiny.decode_hash(char_data['raceHash'], 'DestinyRaceDefinition')
            race = race_dict['displayProperties']['name']

            level = char_data['levelProgression']['level']
            light = char_data['light']

            avatar = self.img_base + char_data['emblemPath']

            mins_played = int(char_data['minutesPlayedTotal'])
            time_played = mins_played / 60

            equipped = profile_data['Response']['characterEquipment']['data'][char_id]['items']

            weapon_i = 0
            armour_i = 0

            weapons = []
            armours = []

            for item in equipped:

                item_dict = await destiny.decode_hash(item['itemHash'], 'DestinyInventoryItemDefinition')
                item_name = item_dict['displayProperties']['name']

                if weapon_i < 3:
                    weapons.append(item_name)
                    weapon_i += 1

                elif armour_i < 5:
                    armours.append(item_name)
                    armour_i += 1

            stat_hashs = char_data['stats']

            s_recovery = -1
            s_resilience = -1
            s_mobility = -1

            for stat in stat_hashs:
                stat_dict = await destiny.decode_hash(stat, 'DestinyStatDefinition')  # print(stat, stat_dict)
                try:
                    if stat_dict['displayProperties']['name'] == "Recovery":
                        s_recovery = stat_hashs[stat]
                    elif stat_dict['displayProperties']['name'] == "Mobility":
                        s_mobility = stat_hashs[stat]
                    elif stat_dict['displayProperties']['name'] == "Resilience":
                        s_resilience = stat_hashs[stat]

                    if s_mobility > -1 and s_recovery > -1 and s_resilience > -1:
                        break

                except KeyError:
                    pass

            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_author(name=bnet.replace("%23", "#"), icon_url="https://i.imgur.com/NF5PVtL.png")
            embed.set_thumbnail(url=avatar)
            embed.description = "Level {} {} {} {} |" \
                                ":small_blue_diamond:{}\n" \
                                "{} Mobility - {} Resilience - {} Recovery" \
                                "".format(level, race, gender, role, light,
                                          s_mobility, s_resilience, s_recovery)
            embed.add_field(name="Weapons", value="**Kinetic:** {}\n"
                                                  "**Energy:** {}\n"
                                                  "**Power:** {}"
                                                  "".format(weapons[0], weapons[1], weapons[2]))
            embed.add_field(name="Armour", value="**Helmet:** {}\n"
                                                 "**Gauntlets:** {}\n"
                                                 "**Chest:** {}\n"
                                                 "**Legs:** {}\n"
                                                 "**Class Item:** {}"
                                                 "".format(armours[0], armours[1], armours[2], armours[3], armours[4]))
            embed.add_field(name="Other Stats", value="**Time Played:** {} hours"
                                                      "".format(round(time_played, 2)))

            await self.bot.say(embed=embed)
        except Exception as e:
            log.warn("D2 command Error: ", e)
            await self.bot.say("Error getting Guardian Stats (Code: 4)")

        destiny.close()

    @commands.command(pass_context=True, hidden=True)
    async def check_id(self, ctx, user="self"):
        if user == "self":
            user = ctx.message.author.id
        tag = user
        user = user.replace("<@", "").replace("!", "").replace(">", "")
        await self.bot.say("{} Associated ID's are:\n**Steam** - {}  -  **BattleNet** - {}"
                           "\n*(A value of '0' means there is no ID's associated)*".format(tag,
                                                                                           id_json.read(
                                                                                              user, "Steam"),
                                                                                           id_json.read(
                                                                                              user, "BattleNet")
                                                                                           )
                           )


def battle_net_parse_user(name):
    if name.startswith("<@") is True:
        # So its a Discord tag
        name = name.replace("<@", "").replace(">", "").replace("!","")
        bnet = id_json.read(name, "BattleNet")
        if bnet == 0:
            return 1

    elif len(name.split("#")) == 2:
        # It be a battle tag
        bnet = name
    else:
        # Check its not an already formatted id (i.e. if myself was used on d2 command)
        check_list = id_json.read(name, "BattleNet")
        if check_list != 0:
            return check_list
        return 0
    return bnet


def parse_user(msg):
    user = str(msg.author.id)
    inp = msg.content
    check_other = inp.split(" ")  # print("CHECK OTHER IS: ", check_other)
    try:
        user_id = check_other[1]
        if user_id.startswith("<@"):
            user_id = user_id.replace("<", "").replace("@", "").replace(">", "").replace("!", "")
        else:
            user_id = None
    except IndexError:
        user_id = user

    return user_id


async def steam_from_id(s_id: int):
    try:
        url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={}&format=json&steamids={}" \
              "".format(t.web_api, s_id)
        res = requests.request("GET", url)
        if res.status_code == 200:
            data = json.loads(res.text)
            steam_name = data['response']['players'][0]['personaname']
            return steam_name
        else:
            return None
    except Exception as e:
        # log.warn("Error getting steam name from id: {}".format(e))
        return None


def pubg_filter(data, number):
    """
    All Stats: KillDeathRatio, WinRatio, TimeSurvived, RoundsPlayed, Wins, WinTop10Ratio, Top10s, Top10Ratio,
    Losses, Rating, BestRating, BestRank, DamagePg, HeadshotKillsPg, HealsPg, KillsPg, MoveDistancePg, RevivesPg,
    RoadKillsPg, TeamKillsPg, TimeSurvivedPg, Top10sPg, Kills, Assists, Suicides, TeamKills, HeadshotKills,
    HeadshotKillRatio, VehicleDestroys, RoadKills, DailyKills, WeeklyKills, RoundMostKills, MaxKillStreaks,
    WeaponsAcquired, Days, LongestTimeSurvived, MostSurvivalTime, AvgSurvivalTime, WinPoints, WalkDistance,
    RideDistance, MoveDistance, AvgWalkDistance, AvgRideDistance, LongestKill, Heals, Revives, Boosts, DamageDealt,
    DBNOs,
    """
    s_filter = ["KillDeathRatio", "Wins", "RoundsPlayed", "Kills", "Rating", "Top10s"]
    # results = []

    KDR = None
    Kills = None
    Rounds = None
    Wins = None
    Rating = None
    RatingPercent = None
    Top10s = None

    loops = len(data['Stats'][number]['Stats'])

    for i in range(0, loops - 1):
        item = str(data['Stats'][number]['Stats'][i]['field'])
        if item in s_filter:
            if item == "KillDeathRatio":
                KDR = data['Stats'][number]['Stats'][i]['value']
            elif item == "Wins":
                Wins = data['Stats'][number]['Stats'][i]['value']
            elif item == "RoundsPlayed":
                Rounds = data['Stats'][number]['Stats'][i]['value']
            elif item == "Kills":
                Kills = data['Stats'][number]['Stats'][i]['value']
            elif item == "Top10s":
                Top10s = data['Stats'][number]['Stats'][i]['value']
            elif item == "Rating":
                Rating = data['Stats'][number]['Stats'][i]['rank']
                RatingPercent = data['Stats'][number]['Stats'][i]['percentile']

    return [KDR, Kills, Rounds, Wins, Rating, RatingPercent, Top10s]


def pubg_find(mode, region, data):
    """
    :param mode: solo, duo or squad
    :param region: eu, na, as, sa, sea, oc, agg
    :param data: the data to find the stuff from
    :return:
    """
    # modes = ["solo", "duo", "squad"]
    # print("ok so now it do a filter on {} and {}".format(mode, region))

    loops = len(data['Stats'])

    result = None

    for i in range(0, loops):
        if data['Stats'][i]['Region'] == region:
            if data['Stats'][i]['Match'] == mode:
                result = i
                break
    return result


def get_top5(data):
    """Get top 5 stats from given data"""
    gdata = data
    result = sorted(range(len(gdata)), key=lambda i: gdata[i], reverse=True)

    return result


def setup(bot):
    bot.add_cog(Games(bot))
