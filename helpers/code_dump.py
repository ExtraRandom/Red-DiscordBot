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