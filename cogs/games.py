import asyncio
import logging
from datetime import datetime

from helpers import tokens as t, steam_json

import aiohttp
from discord.ext import commands
import discord
from cogs.utils import checks

import json

# from mcstatus import MinecraftServer


loop = asyncio.get_event_loop()
log = logging.getLogger(__name__)


class Games:
    def __init__(self, bot):
        self.bot = bot

    # TODO fix and re-add minecraft ip command (see code_dump.py)

    @commands.command()
    async def status(self):
        """Get Status of Steam and CS:GO servers"""
        # TODO add a fallback if something fails
        login, community, economy = await status_steam()
        scheduler, servers, players, searching, search_time = await status_csgo()

        embed = discord.Embed(title="Status of Steam", description="Also includes CSGO Status",
                              url="https://steamstat.us/", colour=discord.Colour.red())
        embed.add_field(name="Steam", value="Login: {}\n"
                                            "Community: {}\n"
                                            "Economy: {}"
                                            "".format(login, community, economy))
        embed.add_field(name="CS:GO", value="Scheduler: {}\n"
                                            "Online Servers: {}\n"
                                            "Online Players: {} ({} searching)\n"
                                            "Average Search Time: {} seconds"
                                            "".format(scheduler.capitalize(), servers, players, searching, search_time))
        embed.set_footer(text="As of {} UTC".format(datetime.utcnow()))
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def pd2(self, ctx):
        """Get Payday 2 Stats"""
        run = True
        user = str(ctx.message.author)
        inp = ctx.message.content

        # print(inp)
        # print(user)

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

                        # TODO add possible error catching

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

                        await self.bot.say(embed=embed)

            except KeyError as e:
                log.warn("KeyError: {}".format(e))
                await self.bot.say("Error: User {} has no Steam ID associated to them or an error occurred fetching "
                                   "stats.")
        else:
            await self.bot.say("This command is disabled currently. Ask the bot owner to add a Steam WebAPI key in "
                               "tokens.py for it to be enabled")

    @commands.command(pass_context=True)
    async def csgo(self, ctx):
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

                        await self.bot.say(embed=embed)

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
            #try:
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

                        await self.bot.say(embed=embed)

            #except Exception as e:
                #print("oh no")

    @commands.command()
    async def overwatch(self, region: str, battletag: str):
        """Get Overwatch Stats - Regions are 'eu', 'us' and 'kr'"""

        # TODO update to use https://github.com/SunDwarf/OWAPI/blob/master/api.md
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
                'User-Agent': 'Ravioli'
            }
            link = "https://owapi.net/api/v3/u/{}/stats?format=json_pretty".format(user)

            with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(link)as resp:
                    data = await resp.json()

                    stats = data['eu']['stats']['quickplay']

                    time_played = stats['game_stats']['time_played']
                    level = stats['overall_stats']['level']
                    wins = stats['overall_stats']['wins']
                    avatar = stats['overall_stats']['avatar']

                    death_avg = stats['average_stats']['deaths_avg']
                    elims_avg = stats['average_stats']['eliminations_avg']
                    heals_avg = stats['average_stats']['healing_done_avg']
                    objks_avg = stats['average_stats']['objective_kills_avg']

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

                    embed.add_field(name="Average", value="Eliminations: {}\n"
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
            await self.bot.say(embed=embed)
        else:
            await self.bot.say("Error: Couldn't fetch stats, check spelling and try again. Check Overwatch server"
                               "status if issue persists.")

    @commands.command(hidden=True)
    @checks.is_owner()
    async def addsteam(self, user: str, steamid: str):
        """Owner only command -- WIP"""
        print(user, " - ", steamid)
        exists = await steam_json.check_profile(steamid)
        exists = False # disables command as i need to finish it
        if exists:
            write_json = steam_json.write(user, steamid)
            print(write_json)
            pass

    @commands.command()
    async def pewds(self):
        """Temporary - Find out if PewDiePie has hit 50m subs yet"""
        if not t.yt_api == "":
            try:
                link = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC-lHJZR3Gqxm24_Vd_AJ5Yw&k" \
                       "ey={}".format(t.yt_api)

                with aiohttp.ClientSession() as session:
                    async with session.get(link)as resp:
                        data = await resp.text()
                        #print(data)#.replace("'",'\\"'))
                        tdata = json.loads(data)
                        #print(tdata)
                        subs = int(tdata['items'][0]['statistics']['subscriberCount'])
                        to_go = 50000000 - subs
                        to_go_count = "{:,}".format(to_go)
                        sub_count = "{:,}".format(subs)
                        await self.bot.say("PewDiePie Currently has {} subs, {} until 50m.".format(sub_count,
                                                                                                   to_go_count))

            except KeyError as e:
                await self.bot.say("Error Getting Subs - KeyError {} - Channel may have already been deleted. "
                                   "Try this link: <https://www.youtube.com/user/PewDiePie>".format(e))
            except Exception as e:
                await self.bot.say("An Error occurred. Error: {} - Channel may have already been deleted. "
                                   "Try this link: <https://www.youtube.com/user/PewDiePie>".format(e))
        else:
            await self.bot.say("No YT API Key. Add one in helpers/tokens.py")


def get_top5(data):
    """Get top 5 stats from given data - should probably rename this somewhen"""
    gdata = data
    result = sorted(range(len(gdata)), key=lambda i: gdata[i], reverse=True)

    return result

async def status_steam():
    url = 'http://is.steam.rip/api/v1/?request=SteamStatus'
    try:
        with aiohttp.ClientSession() as session:
            async with session.get(url)as resp:
                data = await resp.json()
                if str(data["result"]["success"]) == "True":
                    login = (data["result"]["SteamStatus"]["services"]["SessionsLogon"]).capitalize()
                    community = (data["result"]["SteamStatus"]["services"]["SteamCommunity"]).capitalize()
                    economy = (data["result"]["SteamStatus"]["services"]["IEconItems"]).capitalize()
                else:
                    login = "N/A"
                    community = "N/A"
                    economy = "N/A"
    except Exception as e:
        login = "Error"
        community = "Error"
        economy = "Error"
        log.info("Error getting steam status: {}".format(e))
    return login, community, economy


async def status_csgo():

    scheduler = "N/A"
    servers = "N/A"
    players = "N/A"
    searching = "N/A"
    search_time = "N/A"

    if not t.web_api == "":
        try:
            link = "https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key={}&format=json" \
                   "".format(t.web_api)

            with aiohttp.ClientSession() as session:
                async with session.get(link)as resp:
                    data = await resp.json()

                    scheduler = data['result']['matchmaking']['scheduler']
                    servers = data['result']['matchmaking']['online_servers']
                    players = data['result']['matchmaking']['online_players']
                    searching = data['result']['matchmaking']['searching_players']
                    search_time = data['result']['matchmaking']['search_seconds_avg']
        except Exception as e:
            print("Error: {}".format(e))

    return scheduler, servers, players, searching, search_time


def setup(bot):
    bot.add_cog(Games(bot))
