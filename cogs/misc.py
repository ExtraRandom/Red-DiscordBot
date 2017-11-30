from discord.ext import commands
import discord  # import requests # import json # import aiohttp
from datetime import datetime
from pytz import timezone
import time


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
    async def dltime(self, size_in_gigabytes: int):
        """See how long it'll take to download a given file size (in GB's)

        500 MegaBytes (MB) = 0.5 GigaBytes (GB)
        """

        speeds = {'1MB/s': 8, '2.5MB/s': 20, '3MB/s': 24, '4MB/s': 32}
        order = ['1MB/s', '2.5MB/s', '3MB/s', '4MB/s']

        embed = discord.Embed(title="Download Times for {} GigaBytes (GB)".format(size_in_gigabytes),
                              colour=discord.Colour.dark_green(),
                              description="Actual times taken will vary. Speeds are MegaBytes per second")
        for i in order:
            if i in speeds:
                value = (((1048576 * size_in_gigabytes) * 1024) * 8) / (speeds[i]*1000000)
                if 3599 < value < 7199:
                    fmt_value = time.strftime('%H hour %M minutes', time.gmtime(value))
                elif value > 7199:
                    fmt_value = time.strftime('%H hours %M minutes', time.gmtime(value))
                else:
                    fmt_value = time.strftime('%M minutes', time.gmtime(value))

                embed.add_field(name="{}".format(i),
                                value="{}".format(fmt_value))

        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))



