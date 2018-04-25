import asyncio
import json
import requests
from datetime import datetime
import discord


class Main:
    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.chrono_gg())
        self.chrono_last_date_sent = datetime(2000, 1, 1)

    async def chrono_gg(self):
        def get_id_channel(bot, c_name):
            chans = []
            servers = bot.servers
            for server in servers:
                channels = server.channels

                for chan in channels:
                    # print(chan.name, chan.type, chan.id)
                    if chan.name == c_name:
                        # print(chan.name, "is the thing")
                        chans.append(chan)

            return chans

        # Wait for bot to finish starting before checking
        await asyncio.sleep(5)

        store_link = "https://www.chrono.gg/"
        channel_ids = get_id_channel(self.bot, "deals")

        while True:
            today = datetime.utcnow()
            # print(today)

            if today.hour == 16 and today.minute >= 20:
                # print("checking")

                if self.chrono_last_date_sent != datetime(today.year, today.month, today.day, 10, 00, 00, 00):
                    # print("Updating now")
                    self.chrono_last_date_sent = datetime(today.year, today.month, today.day, 10, 00, 00, 00)

                    name, discount, sale_price, normal_price, image, start_date, end_date, \
                        steam_link = await fetch_chrono_data()
                    # print(name, discount, sale_price, normal_price, image, start_date, end_date, steam_link)

                    end_time = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")  # print(end_time)

                    embed = discord.Embed(title="Chrono.gg Deal",
                                          colour=discord.Colour.dark_green(),
                                          description="Deal ends {} UTC".format(end_time)
                                          )

                    embed.set_thumbnail(url=image)

                    embed.add_field(name="Game: {}".format(name),
                                    value="Sale Price: ${} ~~${}~~\n"
                                          "Discount: {}\n"
                                          "".format(sale_price, normal_price, discount))

                    embed.add_field(name="Links",
                                    value="{}\n"
                                          "{}".format(store_link, steam_link))

                    for c_id in channel_ids:
                        await self.bot.send_message(c_id, embed=embed)

                else:
                    pass
                    # print("Already updated today")

            else:
                pass
                # print("not check time", today)

            await asyncio.sleep(5 * 60)


async def fetch_chrono_data():
    url = "https://api.chrono.gg/sale"     # print("fetching")
    resp = requests.get(url)  # print(resp.text)
    data = json.loads(resp.text)
    return data["name"], data["discount"], data["sale_price"], data["normal_price"],\
        data["og_image"], data["start_date"], data["end_date"], data["steam_url"]


def setup(bot):
    bot.add_cog(Main(bot))



