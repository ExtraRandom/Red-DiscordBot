import asyncio
import logging
from datetime import datetime, timedelta

from helpers import tokens as t, steam_json, time_calculations as tc

import aiohttp
from discord.ext import commands
import discord

# from cogs.utils import checks
# import json

from mcstatus import MinecraftServer


loop = asyncio.get_event_loop()
log = logging.getLogger(__name__)


class Games:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mc")
    async def minecraft_ip(self, ip: str):
        """Get Status of Minecraft Servers"""
        # TODO remove '§' from text and format the embed better
        try:
            server = MinecraftServer.lookup(ip)
            status = server.status()
            data = status.raw
            # print(data)
            ver = data['version']['name']
            s_desc = "n/a"
            try:
                s_desc = data['description']['text']
            except TypeError:
                s_desc = data['description']

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

                    embed.add_field(name="Steam", value="Client: {}\n"
                                                        "Community: {}, {}\n"
                                                        "Store: {}, {}\n"
                                                        "User: {}, {}\n".format(client, community, community_error,
                                                                                store, store_error, user, user_error))

                    embed.add_field(name="Team Fortress 2", value="Items: {}, {}\n"
                                                                  "Games: {}, {}".format(items_440, items_440_error,
                                                                                         games_440, games_440_error))

                    embed.add_field(name="Dota 2", value="Items: {}, {}\n"
                                                         "Games: {}, {}\n"
                                                         "Players Searching: {}".format(items_570, items_570_error,
                                                                                        games_570, games_570_error,
                                                                                        games_570_searching))
                    try:
                        embed.add_field(name="CS:GO", value="Items: {}, {}\n"
                                                            "Games: {}, {}\n"
                                                            "Players Online: {}\n"
                                                            "Players Searching: {}\n"
                                                            "Ongoing Matches: {}\n"
                                                            "Average Wait: {}".format(items_730, items_730_error,
                                                                                      games_730, games_730_error,
                                                                                      games_730_players,
                                                                                      games_730_searching,
                                                                                      games_730_matches,
                                                                                      games_730_wait))
                    except Exception as e:
                        embed.add_field(name="CS:GO", value="Items: {}, {}\n"
                                                            "Games: {}, {}\n"
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
        """Get Payday 2 Stats"""
        run = True
        user = str(ctx.message.author)
        inp = ctx.message.content

        if inp.replace(" ", "") != "!pd2":
            entered_name = inp.split()[1:]
            entered_name = ' '.join(entered_name).replace("@", "")
            # print(entered_name)

            try:
                user_id = steam_json.read(entered_name)
                user = entered_name
            except KeyError as e:
                await self.bot.say("Error: User with name '{}' not found on list.".format(entered_name))
                return
        else:
            try:
                user_id = steam_json.read(user)
            except KeyError as e:
                await self.bot.say("Error: User {} has no Steam ID associated to them.".format(user))
                return

        if not t.web_api == "" and run:
            try:
                link = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=218620&key={}" \
                       "&steamid={}&format=json" \
                       "".format(t.web_api, user_id)

                with aiohttp.ClientSession() as session:
                    async with session.get(link)as resp:
                        data = await resp.text()  # resp.json()

                        heist_s = steam_json.steam_read(data, "heist_success")
                        heist_f = steam_json.steam_read(data, "heist_failed")

                        kills = steam_json.read_startswith(data, "enemy_kills_", "pd2")
                        diffs = steam_json.read_startswith(data, "difficulty_", "pd2")

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

                        most_used_gun, most_used_kills = steam_json.weapon_read(data)

                        most_used_gadget, most_used_gadget_uses = steam_json.gadget_read(data)
                        most_used_armor, most_used_armor_uses = steam_json.armor_read(data)

                        embed = discord.Embed(title="PD2 Stats for " + user,
                                              colour=discord.Colour.blue(),
                                              url="http://pd2stats.com/profiles/" + user_id)

                        embed.add_field(name="Heists", value="{} Completed"
                                                             "\n{} Failed"
                                                             "".format(heist_s, heist_f))

                        embed.add_field(name="Difficulty", value="{} Normal\n"
                                                                 "{} Hard\n"
                                                                 "{} Very Hard\n"
                                                                 "{} Overkill\n"
                                                                 "{} Mayhem\n"
                                                                 "{} Deathwish\n"
                                                                 "{} One Down"
                                                                 "".format(diffs[0], diffs[1], diffs[2], diffs[3]
                                                                           , diffs[5], diffs[4], diffs[6]))

                        embed.add_field(name="Kills", value="{} FBI\n"
                                                            "{} Cops/SWAT\n"
                                                            "{} Shield\n"
                                                            "{} Sniper\n"
                                                            "{} Cloaker\n"
                                                            "{} Bulldozer\n"
                                                            "{} Gang/Mob\n"
                                                            "{} Civilian\n"
                                                            "{} Other"
                                                            "".format(fbi, cop_swat, kills_shield, kills_sniper,
                                                                      kills_cloaker, tank_kills, gang_mob_kills,
                                                                      civ_kills, other_kills))
                        embed.add_field(name="Favourite Gun",
                                        value="{}\n{} kills".format(most_used_gun, most_used_kills))
                        embed.add_field(name="Favourite Gadget",
                                        value="{}\n{} uses".format(most_used_gadget, most_used_gadget_uses))
                        embed.add_field(name="Favourite Armor",
                                        value="{}\n{} uses".format(most_used_armor, most_used_armor_uses))

                        embed.set_footer(text="As of {} UTC".format(datetime.utcnow()))

                        try:
                            await self.bot.say(embed=embed)
                        except discord.HTTPException:
                            await self.bot.say("I need the `Embed links` permission "
                                               "to send this")

            except KeyError as e:
                log.warn("KeyError: {}".format(e))
                await self.bot.say("Error: User {} has no Steam ID associated to them or an error occurred fetching "
                                   "stats.")
        else:
            await self.bot.say("This command is disabled currently. Ask the bot owner to add a Steam WebAPI key in "
                               "tokens.py for it to be enabled")

    @commands.command(pass_context=True)
    async def csgo(self, ctx):
        """Get CS:GO Stats"""
        user = str(ctx.message.author)
        user_id = steam_json.read(user)
        if user_id == 0:
            await self.bot.say("Error: User {} has no Steam ID associated to them.".format(user))
            return

        if not t.web_api == "":
            try:
                link = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={}" \
                       "&steamid={}&format=json" \
                       "".format(t.web_api, user_id)

                with aiohttp.ClientSession() as session:
                    async with session.get(link)as resp:
                        data = await resp.text()  # resp.json()

                        kills = steam_json.read_startswith(data, "total_kills_", "csgo")
                        general = steam_json.read_startswith(data, "", "csgo")
                        mapwins = steam_json.read_startswith(data, "total_wins_map_", "csgo")
                        # accuracy = steam_json.read_startswith(data, "")
                        kd_ratio = general[0] / general[1]
                        kd_ratio = str(kd_ratio)[:4]

                        top_guns = get_top5(kills)
                        top_maps = get_top5(mapwins)

                        gdata = steam_json.csgo_info()

                        embed = discord.Embed(title="CS:GO Stats for {}".format(user),
                                              colour=discord.Colour.dark_green())

                        embed.add_field(name="General", value="Total Kills: {}\n"
                                                              "Total Deaths: {}\n"
                                                              "K/D Ratio: {}\n"
                                                              "Bombs Planted: {}\n"
                                                              "Bombs Defused: {}\n"
                                                              "Hostages Rescued: {}"
                                                              "".format(general[0], general[1], kd_ratio,
                                                                        general[2], general[3], general[4]))

                        embed.add_field(name="Top Guns", value="1: {} - {} kills\n"
                                                               "2: {} - {} kills\n"
                                                               "3: {} - {} kills\n"
                                                               "4: {} - {} kills\n"
                                                               "5: {} - {} kills\n"
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

                        embed.add_field(name="Top Maps", value="1: {} - {} wins\n"
                                                               "2: {} - {} wins\n"
                                                               "3: {} - {} wins\n"
                                                               "4: {} - {} wins\n"
                                                               "5: {} - {} wins\n"
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
                        embed.add_field(name="Accuracy", value="Shots Hit: {}\n"
                                                               "Shots Fired: {}\n"
                                                               "Accuracy Percent: {}%"
                                                               "".format(general[5], general[6],
                                                                         str(percent).split(".")[0]))

                        embed.set_footer(text="As of {} UTC".format(datetime.utcnow()))

                        try:
                            await self.bot.say(embed=embed)
                        except discord.HTTPException:
                            await self.bot.say("I need the `Embed links` permission "
                                               "to send this")
            except KeyError as e:
                self.bot.say("Error finding stat - {}".format(e))

    @commands.command(pass_context=True)
    async def unturned(self, ctx):
        """Get Unturned Stats"""

        user = str(ctx.message.author)
        user_id = steam_json.read(user)
        if user_id == 0:
            await self.bot.say("Error: User {} has no Steam ID associated to them.".format(user))
            return

        if not t.web_api == "":
            # try:
                link = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=304930&key={}" \
                       "&steamid={}&format=json" \
                       "".format(t.web_api, user_id)

                with aiohttp.ClientSession() as session:
                    async with session.get(link)as resp:
                        data = await resp.text()

                        kills = steam_json.read_startswith(data, "Kills_", "unturned")
                        founds = steam_json.read_startswith(data, "Found_", "unturned")
                        travel = steam_json.read_startswith(data, "Travel_", "unturned")
                        acc = steam_json.read_startswith(data, "", "unturned")
                        a_wins = steam_json.steam_read(data, "Arena_Wins")

                        embed = discord.Embed(title="Unturned Stats for " + user,
                                              colour=discord.Colour.green())

                        embed.add_field(name="Kills", value="Players: {}\n"
                                                            "Zombies: {}\n"
                                                            "Mega Zombies: {}\n"
                                                            "Animals: {}".format(kills[0], kills[1], kills[2],
                                                                                  kills[3]))
                        embed.add_field(name="General", value="Items Crafted: {}\n"
                                                              "Resources Harvested: {}\n"
                                                              "Experience Gained: {}\n"
                                                              "Items Crafted: {}\n"
                                                              "Fish Caught: {}\n"
                                                              "Plants Grown: {}\n"
                                                              "Objects Built: {}\n"
                                                              "Projectiles Thrown: {}"
                                                              "".format(founds[0], founds[1], founds[2], founds[3],
                                                                        founds[4], founds[5], founds[6], founds[7]))

                        embed.add_field(name="Traveled", value="By Foot: {}m\n"
                                                               "By Vehicle: {}m".format(travel[0], travel[1]))

                        embed.add_field(name="Weapon Usage", value="Shots: {}\n"
                                                                   "Hits: {}\n"
                                                                   "Headshots: {}"
                                                                   "".format(acc[0], acc[1], acc[2]))

                        embed.add_field(name="Arena", value="Wins: {}".format(a_wins))

                        embed.set_footer(text="As of {} UTC".format(datetime.utcnow()))

                        try:
                            await self.bot.say(embed=embed)
                        except discord.HTTPException:
                            await self.bot.say("I need the `Embed links` permission "
                                               "to send this")

            # except Exception as e:
                # print("oh no")

    @commands.command()
    async def overwatch(self, region: str, battletag: str):
        """Get Overwatch Stats - Regions are 'eu', 'us' and 'kr'"""

        # Updated to use https://github.com/SunDwarf/OWAPI/blob/master/api.md
        # https://owapi.net/api/v3/u/ExtraRandom-2501/blob?format=json_pretty

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
            link = "https://owapi.net/api/v3/u/{}/stats?format=json_pretty".format(user)

            with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(link)as resp:
                    data = await resp.json()

                    stats = data[reg]['stats']['quickplay']

                    time_played = stats['game_stats']['time_played']
                    level = stats['overall_stats']['level']
                    wins = stats['overall_stats']['wins']
                    avatar = stats['overall_stats']['avatar']

                    # used to be ['average_stats']
                    death_avg = int(stats['game_stats']['deaths'])  #_avg']
                    elims_avg = int(stats['game_stats']['eliminations'])  #_avg']
                    heals_avg = int(stats['game_stats']['healing_done'])  #_avg']
                    objks_avg = int(stats['game_stats']['objective_kills'])  #_avg']

                    md_total = int(stats['game_stats']['medals'])
                    md_gold = int(stats['game_stats']['medals_gold'])
                    md_silver = int(stats['game_stats']['medals_silver'])
                    md_bronze = int(stats['game_stats']['medals_bronze'])

                    embed = discord.Embed(title="Overwatch Stats for {}".format(battletag),
                                          colour=discord.Colour.orange())
                    embed.set_thumbnail(url=avatar)

                    embed.add_field(name="General", value="Time Played: {}\n"
                                                          "Level: {}\n"
                                                          "Wins: {}"
                                                          "".format(time_played, level, wins))

                    embed.add_field(name="Totals", value="Eliminations: {}\n"
                                                          "Deaths: {}\n"
                                                          "Healing Done: {}\n"
                                                          "Objective Kills: {}"
                                                          "".format(elims_avg, death_avg, heals_avg, objks_avg))

                    embed.add_field(name="Medals", value="Total: {}\n"
                                                         "Gold: {}\n"
                                                         "Silver: {}\n"
                                                         "Bronze: {}\n"
                                                         "".format(md_total, md_gold, md_silver, md_bronze))

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
        else:
            await self.bot.say("Error: Couldn't fetch stats, check spelling and try again. Check Overwatch server"
                               "status if issue persists.")

# TODO use twitter api to get info from PUBG twitter


def get_top5(data):
    """Get top 5 stats from given data"""
    gdata = data
    result = sorted(range(len(gdata)), key=lambda i: gdata[i], reverse=True)

    return result


def setup(bot):
    bot.add_cog(Games(bot))
