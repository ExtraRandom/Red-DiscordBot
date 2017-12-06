from discord.ext import commands
import discord  # import requests # import json # import aiohttp
from datetime import datetime
from pytz import timezone
import time

# TODO remove when no longer needed
import requests, bs4


class Misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def times(self):
        """Returns a list of Timezones and their current times"""

        # https://github.com/ExtraRandom/Discord-Bot/blob/96cae11c0a18d2015188d09fea2a1fdabe9c892f/cogs/general.py#L164
        # Taken from my old bot with some changes

        # Also useful
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        # https://stackoverflow.com/questions/13866926/python-pytz-list-of-timezones

        zones = {'US Pacific': 'US/Pacific', 'US Central': 'US/Central', 'US Eastern': 'US/Eastern',
                 'United Kingdom': 'Europe/London', 'Moscow': 'Europe/Moscow', 'Japan': 'Asia/Tokyo'}

        now_utc = datetime.now(timezone('UTC'))

        embed = discord.Embed(title="Current Times in Other Timezones",
                              colour=discord.Colour.red())

        order = ['US Pacific', 'US Central', 'US Eastern', 'United Kingdom', 'Moscow', 'Japan']
        # Thank you Japan for insisting on being first on the list for no reason

        for i in order:
            if i in zones:
                time = now_utc.astimezone(timezone(zones[i]))
                fmttime = time.strftime('%a %H:%M')
                tz_from_time = time.strftime('%Z')
                embed.add_field(name="{} ({})".format(i, tz_from_time),
                                value="{}".format(fmttime))

        await self.bot.say(embed=embed)

    @commands.command()
    async def dltime(self, size_in_gigabytes: float):
        """See how long it'll take to download a given file size (in GB's)

        500 MegaBytes (MB) = 0.5 GigaBytes (GB)
        """
        # size_in_gigabytes = float(size_in_gigabytes)
        speeds = {'1MB/s': 8, '2MB/s': 16, '3MB/s': 24, '4MB/s': 32}
        order = ['1MB/s', '2MB/s', '3MB/s', '4MB/s']

        embed = discord.Embed(title="Download Times for {} GigaBytes (GB)".format(size_in_gigabytes),
                              colour=discord.Colour.dark_green(),
                              description="Actual times taken will vary. Speeds are MegaBytes per second")
        for i in order:
            if i in speeds:
                value = (((1048576 * size_in_gigabytes) * 1024) * 8) / (speeds[i]*1000000)
                if 3599 < value < 7199:
                    fmt_value = time.strftime('%H hour, %M minutes', time.gmtime(value))
                elif 7199 < value < 86399:
                    fmt_value = time.strftime('%H hours, %M minutes', time.gmtime(value))
                elif 86399 < value:
                    fmt_value = time.strftime('{} Day(s), %H hours, %M minutes'.format(secs_to_days(value)),
                                              time.gmtime(value))
                    embed.set_footer(text="What on earth are you downloading?")
                else:
                    fmt_value = time.strftime('%M minutes', time.gmtime(value))

                embed.add_field(name="{}".format(i),
                                value="{}".format(fmt_value))

        await self.bot.say(embed=embed)

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


def secs_to_days(seconds):
    return str(seconds / 86400).split(".")[0]


def setup(bot):
    bot.add_cog(Misc(bot))



