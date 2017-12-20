    @commands.command(name="mc")
    async def minecraft_ip(self, ip: str):
        """Get Status of Minecraft Servers"""
        try:
            server = MinecraftServer.lookup(ip)
            status = server.status()
            data = status.raw
            # print(data)
            ver = data['version']['name']
            version = float(ver[2:])
            if version >= 9:
                s_desc = data['description']['text']
            else:
                s_desc = data['description']
            players = ""
            try:
                for player in data['players']['sample']:
                    players += "{}, ".format(player['name'])
                players = players[:-2]  # Remove final comma and the space after it
            except Exception:
                players = "None"

            msg = """ __*Status of {}*__

Version: {}
Online Players: {}
Description: {}
            """.format(ip, ver, players, s_desc)
            await self.bot.say(msg)

        except ValueError as e:
            await self.bot.say("Invalid IP")
            log.warn(e)

        except Exception as e:
            await self.bot.say("Server didn't return any info or an error occured.")
            log.warning("Exception in games.py - {}".format(e))






















            ############################################################

kills_cop = steam_json.steam_read(data, "enemy_kills_cop")
kills_fbi = steam_json.steam_read(data, "enemy_kills_fbi")
kills_fbi_swat = steam_json.steam_read(data, "enemy_kills_fbi_swat")
kills_fbi_heavy_swat = steam_json.steam_read(data, "enemy_kills_fbi_heavy_swat")
kills_swat = steam_json.steam_read(data, "enemy_kills_swat")
kills_heavy_swat = steam_json.steam_read(data, "enemy_kills_heavy_swat")
kills_city_swat = steam_json.steam_read(data, "enemy_kills_city_swat")
kills_security = steam_json.steam_read(data, "enemy_kills_security")
kills_gensec = steam_json.steam_read(data, "enemy_kills_gensec")
kills_gangster = steam_json.steam_read(data, "enemy_kills_gangster")
kills_sniper = steam_json.steam_read(data, "enemy_kills_sniper")
kills_shield = steam_json.steam_read(data, "enemy_kills_shield")
kills_cloaker = steam_json.steam_read(data, "enemy_kills_spooc")
kills_tank = steam_json.steam_read(data, "enemy_kills_tank")
kills_taser = steam_json.steam_read(data, "enemy_kills_taser")
kills_mobster = steam_json.steam_read(data, "enemy_kills_mobster")
kills_mobster_boss = steam_json.steam_read(data, "enemy_kills_mobster_boss")
kills_civilian = steam_json.steam_read(data, "enemy_kills_civilian")
kills_civilian_female = steam_json.steam_read(data, "enemy_kills_civilian")
kills_tank_hw = steam_json.steam_read(data, "enemy_kills_tank_hw")
kills_hector_boss = steam_json.steam_read(data, "enemy_kills_hector_boss")
kills_hector_boss_no_armor = steam_json.steam_read(data, "enemy_kills_hector_boss_no_armor")
kills_tank_green = steam_json.steam_read(data, "enemy_kills_tank_green")
kills_tank_black = steam_json.steam_read(data, "enemy_kills_tank_black")
kills_tank_skull = steam_json.steam_read(data, "enemy_kills_tank_skull")
kills_hostage_rescue = steam_json.steam_read(data, "enemy_kills_hostage_rescue")
kills_murkywater = steam_json.steam_read(data, "enemy_kills_murkywater")
kills_winters_minion = steam_json.steam_read(data, "enemy_kills_phalanx_minion")
kills_biker_boss = steam_json.steam_read(data, "enemy_kills_biker_boss")
kills_cop_female = steam_json.steam_read(data, "enemy_kills_cop_female")
kills_medic = steam_json.steam_read(data, "enemy_kills_medic")
kills_chavez_boss = steam_json.steam_read(data, "enemy_kills_chavez_boss")

total_kills = kills_cop + kills_fbi + kills_fbi_swat + kills_fbi_heavy_swat + kills_swat + \
              kills_heavy_swat + kills_city_swat + kills_security + kills_gensec + kills_gangster + \
              kills_sniper + kills_shield + kills_cloaker + kills_tank + kills_taser + kills_mobster + \
              kills_mobster_boss + kills_civilian + kills_civilian_female + kills_tank_hw + \
              kills_hector_boss + kills_hector_boss_no_armor + kills_tank_green + kills_tank_black + \
              kills_tank_skull + kills_hostage_rescue + kills_murkywater + kills_winters_minion + \
              kills_biker_boss + kills_cop_female + kills_medic + kills_chavez_boss

tank_kills = kills_tank + kills_tank_skull + kills_tank_green + kills_tank_hw + kills_tank_black
civ_kills = kills_civilian + kills_civilian_female
gang_mob_kills = kills_gangster + kills_mobster_boss + kills_mobster

cop_swat = kills_cop + kills_cop_female + kills_city_swat + kills_heavy_swat + kills_swat
fbi = kills_fbi + kills_fbi_heavy_swat + kills_fbi_swat

shield_sniper_cloaker = kills_sniper + kills_shield + kills_cloaker
other_kills = total_kills - (tank_kills + gang_mob_kills + civ_kills + shield_sniper_cloaker +
                             cop_swat + fbi)




# norm_vh_diff = diff_norm + diff_h + diff_vh
# ovk_may_diff = diff_ovk + diff_my
# dw_od_diff = diff_dw + diff_od









#########################################################################



    @commands.group(pass_context=True, description=desc.steam_status, brief=desc.steam_status)
    async def steam(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say(await get_status("short"))

    @steam.command(name="status", description=desc.steam_status, brief=desc.steam_status)
    async def _status(self):
        await self.bot.say(await get_status("long"))

    @steam.command(name="bestsellers", description=desc.steam_bs, brief=desc.steam_bs)
    async def _bs(self):
        future = loop.run_in_executor(None, requests.get,
                                      "http://store.steampowered.com/search/?filter=topsellers&os=win")
        res = await future

        try:
            res.raise_for_status()
        except Exception as e:
            await self.bot.say("**Error with request.\nError: {}".format(str(e)))
            log.exception("Error with request (games.py)")
            return

        doc = bs4.BeautifulSoup(res.text, "html.parser")
        title = doc.select('span[class="title"]')

        msg = """**Best Selling Steam Games**

 1) {}
2) {}
4) {}
3) {}
5) {}
""".format(title[0].getText(), title[1].getText(), title[2].getText(), title[3].getText(), title[4].getText())

        await self.bot.say(msg)





async def get_status(fmt):
    steam_api = 'http://is.steam.rip/api/v1/?request=SteamStatus'
    with aiohttp.ClientSession() as session:
        async with session.get(steam_api)as resp:
            data = await resp.json()
            if str(data["result"]["success"]) == "True":
                login = (data["result"]["SteamStatus"]["services"]["SessionsLogon"]).capitalize()
                community = (data["result"]["SteamStatus"]["services"]["SteamCommunity"]).capitalize()
                economy = (data["result"]["SteamStatus"]["services"]["IEconItems"]).capitalize()
                # leaderboards = (data["result"]["SteamStatus"]["services"]["LeaderBoards"]).capitalize()
                if fmt == "long":
                    reply = """**Steam Server Status**
    ```xl
    Login          {}
    Community      {}
    Economy        {}```""".format(login, community, economy)
                elif fmt == "short":
                    if str(login) != "Normal" and str(community) != "Normal" and str(economy) != "Normal":
                        reply = "Steam might be having some issues, use `!steam status! for more info."
                    # elif login is "normal" and community is "normal" and economy is "normal":
                    #    reply = "Steam is running fine - no issues detected, use `!steam status! for more info."
                    else:
                        reply = "Steam appears to be running fine."
                else:  # if wrong format
                    log.error("Wrong format given for get_status().")
                    reply = "This error has occurred because you entered an incorrect format for get_status()."

            else:
                reply = "Failed to connect to API - Error: {}".format(data["result"]["error"])

    return reply




#########################################################################




def read_startswith(data, startswith, game):
    jdata = json.loads(data)

    if game == "pd2":
        with open(pd2_file) as out_file2:
            game_data = json.load(out_file2)
    elif game == "unturned":
        with open(unturned_file) as out_file2:
            game_data = json.load(out_file2)

    stats = len(jdata['playerstats']['stats'])

    result = []

    for index in range(stats):
        index_str = str(jdata['playerstats']['stats'][index]['name'])
        print("index string:  ", index_str)
        if index_str.startswith(startswith):
            if game == "pd2":
                if startswith == "enemy_kills_":
                    for word in range(len(game_data['Kills'])):
                        if index_str == ("enemy_kills_" + game_data['Kills'][word]):
                            result.append(jdata['playerstats']['stats'][index]['value'])
                        else:
                            result.append(0)

                if startswith == "difficulty_":
                    for word in range(len(game_data['Difficulty'])):
                        if index_str.endswith(game_data['Difficulty'][word]):
                            result.append(jdata['playerstats']['stats'][index]['value'])
                        else:
                            result.append(0)

            elif game == "unturned":
                if startswith == "Kills_":
                    test = "fuck"
                    for word in range(len(game_data['Kills'])):
                        print("word: ", word, "             ,", index_str)
                        if index_str.endswith(game_data['Kills'][word]):
                            test = jdata['playerstats']['stats'][index]['value']
                            # result.append(jdata['playerstats']['stats'][index]['value'])
                            # break
                        print("test: ", test)

                    print("test is ", test, " and is about to be appended")
                    result.append(test)


                if startswith == "Found_":
                    for word in range(len(game_data['Found'])):
                        if index_str.endswith(game_data['Found'][word]):
                            result.append(jdata['playerstats']['stats'][index]['value'])
                        else:
                            result.append(0)

    print(result)

    return result

############################################################################

    @commands.command(hidden=True)
    async def pewds(self):
        """Temporary - Find out if PewDiePie has hit 50m subs yet"""
        if not t.yt_api == "":
            try:
                link = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC-lHJZR3Gqxm24_Vd_AJ5Yw&k" \
                       "ey={}".format(t.yt_api)

                with aiohttp.ClientSession() as session:
                    async with session.get(link)as resp:
                        data = await resp.text()
                        tdata = json.loads(data)
                        #print(tdata)
                        subs = int(tdata['items'][0]['statistics']['subscriberCount'])
                        to_go = 50000000 - subs
                        to_go_count = "{:,}".format(to_go)
                        sub_count = "{:,}".format(subs)
                        await self.bot.say("PewDiePie currently has {} subs, {} until 50m.".format(sub_count,
                                                                                                   to_go_count))

            except KeyError as e:
                await self.bot.say("Error Getting Subs - KeyError {} - Channel may have already been deleted. "
                                   "Try this link: <https://www.youtube.com/user/PewDiePie>".format(e))
            except Exception as e:
                await self.bot.say("An Error occurred. Error: {} - Channel may have already been deleted. "
                                   "Try this link: <https://www.youtube.com/user/PewDiePie>".format(e))
        else:
            await self.bot.say("No YT API Key. Add one in helpers/tokens.py")


######################################




    @commands.command()
    async def cod(self):
        """Get time until COD:WW2 reveal"""
        now = datetime.utcnow()
        bst = now + timedelta(hours=1)

        then = datetime(2017, 4, 26, 18, 00, 00, 0)
        # days, hrs, mins = tc.calc_until(then)
        days, hrs, mins = tc.calc_from_until(bst, then)

        if days == "0 days":
            # Less than a day left

            if hrs == "0":
                # Less than Hour Left

                if mins == "0":
                    # Trailer is (probably) out
                    msg = "**Reveal Livestream should be live now.** Check these links:\n" \
                          "<https://www.callofduty.com/uk/en/wwii>\n" \
                          "<https://www.youtube.com/user/CALLOFDUTY>\n" \
                          "<https://www.twitch.tv/callofduty>"
                else:
                    msg = "Time until Call of Duty: WW2 Reveal Livestream:\n" \
                          "**Only** **{}** **minutes**\n\n" \
                          "Links: \n" \
                          "<https://www.callofduty.com/uk/en/wwii>\n" \
                          "<https://www.youtube.com/user/CALLOFDUTY>\n" \
                          "<https://www.twitch.tv/callofduty>".format(mins)
            else:
                msg = "Time until Call of Duty: WW2 Reveal Livestream:\n" \
                      "     **{}** **hours** and **{}** **minutes**.".format(hrs, mins)
        else:
            if "-" in days:
                msg = "**Reveal Livestream should be live now.** Check these links for the trailer:\n" \
                      "<https://www.callofduty.com/uk/en/wwii>\n" \
                      "<https://www.youtube.com/user/CALLOFDUTY>\n" \
                      "<https://www.twitch.tv/callofduty>"
            else:
                msg = "Time until Call of Duty: WW2 Reveal Livestream:\n" \
                      "     **{}**, **{}** **hours** and **{}** **minutes**" \
                      "".format(days, hrs, mins)

        await self.bot.say(msg)



        ##################################################################################################################

        @commands.command(hidden=True)
        @checks.is_owner()
        async def addsteam(self, user: str, steamid: str):
            """Owner only command -- WIP"""
            print(user, " - ", steamid)
            exists = await steam_json.check_profile(steamid)
            exists = False  # disables command as i need to finish it
            if exists:
                write_json = steam_json.write(user, steamid)
                print(write_json)
                pass



            ####################################################


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











            #############################





                @commands.command()
                async def d2mu(self):
                    msg = await self.bot.say("Checking for Destiny 2 Manifest Update")
                    v_current = d2_mani_get_version(self.d2_mv_file)
                    v_latest = await d2_main_get_latest(self.url_base, self.headers)
                    if v_current != v_latest:
                        print("Update Required")

                    else:
                        print("No Update Required")

            def d2_mani_get_version(file):
                if os.path.exists(file):
                    with open(file, "r") as version_file:
                        return version_file.readline()
                else:
                    return 0

            async def d2_main_get_latest(url_base, headers):
                get_manifest = requests.request("GET", (url_base + "/Destiny2/Manifest"), headers=headers)
                manifest = json.loads(get_manifest.text)
                version = manifest['Response']['version']

                return version


            ##########################################



            @commands.command()
            async def d2(self, bnet: str, character=1):

                start = time.time()

                # https://bungie-net.github.io/multi/
                # Doc's

                # https://github.com/jgayfer/spirit/blob/master/cogs/destiny.py
                # Very useful for figuring out how to get this working

                msg_contents = "Getting Destiny 2 Stats for {}, this may take a while!".format(bnet)
                msg = await self.bot.say(msg_contents)

                if t.d2_api == "":
                    await self.bot.edit_message(msg, "Error: No Destiny 2 API key stated in tokens.py!")
                    return

                headers = {
                    'X-API-Key': t.d2_api,
                }

                bnet = bnet.replace("#", "%23")
                char = character - 1

                search = self.url_base + "/Destiny2/SearchDestinyPlayer/4/" + bnet
                user_info_r = requests.request("GET", search, headers=headers)
                user_info = json.loads(user_info_r.text)  # print(user_info_r.text)

                user_id = user_info['Response'][0]['membershipId']

                user_search = self.url_base + "/Destiny2/4/Profile/" \
                                              "" + user_id + "?components=100,200,205"

                get_user = requests.request("GET", user_search, headers=headers)  # print(get_user.text)

                data = json.loads(get_user.text)

                chars = data['Response']['profile']['data']['characterIds']
                char_id = 0

                if (char + 1) > len(chars):
                    # char the user wants doesnt exist, default to 1
                    msg_contents += "\n{} only has {} character(s). No #{} character exists, getting stats from " \
                                    "character #1 instead.".format(bnet.replace("%23", "#"), len(chars), character)
                    await self.bot.edit_message(msg, msg_contents)
                    char_id = chars[0]
                else:
                    char_id = chars[char]

                if char_id == 0:
                    await self.bot.edit_message(msg, "An error occurred whilst getting stats. (char_id wasn't changed "
                                                     "for some reason, Thomas plz fix)")
                    return

                """GET GENERAL STATS"""

                msg_contents += "\n\nFetching General Stats... "
                await self.bot.edit_message(msg, msg_contents)

                char_data = data['Response']['characters']['data'][char_id]
                t_race = char_data['raceType']
                race_r = "N/A"
                if t_race == 0:
                    race_r = "Human"
                elif t_race == 1:
                    race_r = "Awoken"
                elif t_race == 2:
                    race_r = "Evo"

                t_class = char_data['classType']
                class_r = "N/A"
                if t_class == 0:
                    class_r = "Titan"
                elif t_class == 1:
                    class_r = "Hunter"
                elif t_class == 2:
                    class_r = "Warlock"

                t_gender = char_data['genderType']
                gender_r = "N/A"
                if t_gender == 0:
                    gender_r = "Male"
                elif t_gender == 1:
                    gender_r = "Female"

                icon = char_data['emblemPath']
                avatar = self.img_base + icon

                level = char_data['levelProgression']['level']
                light = char_data['light']

                # print(class_r, race_r, gender_r)

                msg_contents += " Done!\nFetching Weapon/Armour Stats... "
                await self.bot.edit_message(msg, msg_contents)

                """GET ITEMS"""

                s_recovery = -1
                s_resilience = -1
                s_mobility = -1
                s_power = -1

                for stat in char_data['stats']:
                    stat_req = self.url_base + "/Destiny2/Manifest/DestinyStatDefinition/" + str(stat)
                    stat_resp = requests.request("GET", stat_req, headers=headers)  # print(stat_resp.text)
                    stat_data = json.loads(stat_resp.text)
                    try:
                        stat_name = stat_data['Response']['displayProperties']['name']
                        if stat_name == "Recovery":
                            s_recovery = char_data['stats'][stat]
                        elif stat_name == "Resilience":
                            s_resilience = char_data['stats'][stat]
                        elif stat_name == "Mobility":
                            s_mobility = char_data['stats'][stat]
                        elif stat_name == "Power":
                            s_power = char_data['stats'][stat]

                        # print(stat_data['Response']['displayProperties']['name'] + ": " + str(char_data['stats'][stat]))
                    except Exception as e:
                        pass

                weapon_index = 0
                armour_index = 0

                weapons = []
                armours = []

                mins_played = int(char_data['minutesPlayedTotal'])
                time_played = mins_played / 60

                for item in data['Response']['characterEquipment']['data'][char_id]['items']:
                    item_hash = item['itemHash']
                    item_req = self.url_base + "/Destiny2/Manifest/DestinyInventoryItemDefinition/" + str(item_hash)
                    get_item_decode = requests.request("GET", item_req, headers=headers)
                    # print(get_item_decode.text)
                    idata = json.loads(get_item_decode.text)
                    name = idata['Response']['displayProperties']['name']

                    if weapon_index < 3:
                        # weapons[weapon_index] = name
                        weapons.append(name)
                        weapon_index += 1

                    elif armour_index < 5:
                        # armours[armour_index] = name
                        armours.append(name)
                        armour_index += 1

                msg_contents += " Done!\nFormatting Data!"
                await self.bot.edit_message(msg, msg_contents)

                embed = discord.Embed(colour=discord.Colour.blue())
                embed.set_author(name=bnet.replace("%23", "#"), icon_url="https://i.imgur.com/NF5PVtL.png")
                embed.set_thumbnail(url=avatar)
                embed.description = "Level {} {} {} {} |" \
                                    ":small_blue_diamond:{}\n" \
                                    "{} Mobility - {} Resilience - {} Recovery" \
                                    "".format(level, race_r, gender_r, class_r,
                                              s_power,
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
                                                     "".format(armours[0], armours[1], armours[2], armours[3],
                                                               armours[4]))
                embed.add_field(name="Other Stats", value="**Time Played:** {} hours"
                                                          "".format(round(time_played, 2)))
                await self.bot.delete_message(msg)
                await self.bot.say(embed=embed)

                end = time.time()

                await self.bot.say("That took {}".format(str(end - start)))















                ############################





                @commands.command(hidden=True)
                @checks.is_owner()
                async def test(self, user: str, id: int):
                    print("heck")

                    print(user)
                    print(id)

                    id_file = "helpers/steam_id.json"
                    with open(id_file) as id_file:
                        data = json.load(id_file)
                        print(data)

                        finished = json.dumps(data)
                        print(finished)













"""
For reading and writing to steam_id.json
"""

"""
def read(user):
    with open(id_file) as data_file:
        data = json.load(data_file)
        # TODO see if checking whether the user has the game or not can/should be done here
        try:
            # print("read user '", user, "' for info :", data[user])
            return data[user]
        except KeyError as e:
            print("Steam - KeyError: {}".format(e))
            return 0
"""
# Move to code dump some when
"""
def write(user_discord, user_steamid):
    ""CURRENTLY THIS MESSES UP THE FILE WITH /'s""
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
    ""Returns True if profile exists, false if not""

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





















@commands.command(pass_context=True)
    async def unturned(self, ctx):
        """Get Unturned Stats, Mention someone to get their stats
        E.g. "?unturned" for personal stats, "?unturned @SomeUser" for SomeUser's stats
        """
        print(ctx.message.content)
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
                link = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=304930&key={}" \
                       "&steamid={}&format=json" \
                       "".format(t.web_api, steam_id)

                with aiohttp.ClientSession() as session:
                    async with session.get(link)as resp:
                        data = await resp.text()

                        try:
                            kills = steam_json.read_startswith(data, "Kills_", "unturned")
                        except Exception as e:
                            await self.bot.say("Error: User {} ({} on Steam) does not own Unturned.".format(user,
                                                                                                            username))
                            return
                        founds = steam_json.read_startswith(data, "Found_", "unturned")
                        travel = steam_json.read_startswith(data, "Travel_", "unturned")
                        acc = steam_json.read_startswith(data, "", "unturned")
                        a_wins = steam_json.steam_read(data, "Arena_Wins")

                        embed = discord.Embed(title="Unturned Stats for " + username,
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

            except Exception as e:
                log.warn("Error in unturned command: ", e)
                await self.bot.say("Error: Issue occurred whilst getting Unturned Stats")


    "Unturned":
    {
        "Kills": [
            "Zombies_Normal", "Players", "Zombies_Mega", "Animals"
        ]
        ,
        "Found": [
            "Items", "Resources", "Experience", "Crafts", "Fishes", "Plants",
            "Buildables", "Throwables"
        ],
        "Travel": [
            "Foot", "Vehicle"
        ],
        "WeaponUsage": [
            "Accuracy_Shot", "Accuracy_Hit", "Headshots"
        ],
        "#Sources": ["https://steamdb.info/app/304930/stats/"]
    },





import json  # import bs4  # import requests # import aiohttp  # import asyncio

# id_file = "helpers/steam_id.json"
pd2_file = "helpers/pd2_info.json"
unturned_file = "helpers/unturned.json"
csgo_file = "helpers/csgo.json"

file = "helpers/games.json"

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
    with open(file) as out_file2:
        data = json.load(out_file2)
        game_data = data["CSGO"]

    return game_data  # game_data['Kills'], game_data['Maps']


def read_startswith(data, startswith, game):
    jdata = json.loads(data)

    game_data = jdata

    result = []

    """
    if game == "pd2":
        with open(pd2_file) as out_file2:
            game_data = json.load(out_file2)

    elif game == "unturned":
        with open(unturned_file) as out_file2:
            game_data = json.load(out_file2)

    elif game == "csgo":
        with open(csgo_file) as out_file2:
            game_data = json.load(out_file2)
    """

    if game == "pd2":
        if startswith == "enemy_kills_":
            to_find = game_data['PD2']['Kills']
            result = stat_loop(jdata, to_find, startswith)
        if startswith == "difficulty_":
            to_find = game_data['PD2']['Difficulty']
            result = stat_loop(jdata, to_find, startswith)

    elif game == "unturned":
        if startswith == "Kills_":
            to_find = game_data['Unturned']['Kills']
            result = stat_loop(jdata, to_find, startswith)
        if startswith == "Found_":
            to_find = game_data['Unturned']['Found']
            result = stat_loop(jdata, to_find, startswith)
        if startswith == "Travel_":
            to_find = game_data['Unturned']['Travel']
            result = stat_loop(jdata, to_find, startswith)
        if startswith == "":
            to_find = game_data['Unturned']['WeaponUsage']
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


---------------------------------------


    @commands.command(aliases=["hb", "yogshb"], hidden=True)
    async def yogs(self):
        # TODO remove once this bundle ends
        try:
            url = "https://www.humblebundle.com/yogscast-jingle-jam-2017"
            res = requests.get(url)

            res.raise_for_status()

            html = bs4.BeautifulSoup(res.text, "html.parser")
            games = html.select('em')

            msg = "**GAMES:**"

            for game in games:
                msg += "\n  " \
                       "{}".format(game.getText())

            await self.bot.say(msg)

        except Exception as e:
            print("Error in yogs command: {}".format(e))
            await self.bot.say("Error getting data.")
            return