from discord.ext import commands
import discord  # import requests # import json # import aiohttp
from datetime import datetime
from pytz import timezone


class Misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def times(self):
        """Returns a list of Timezones and their current times"""

        # https://github.com/ExtraRandom/Discord-Bot/blob/96cae11c0a18d2015188d09fea2a1fdabe9c892f/cogs/general.py#L164
        # Taken from my old bot with some changes

        # Also useful
        # https://docs.python.org/3/library/datetime.html
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


def setup(bot):
    bot.add_cog(Misc(bot))



