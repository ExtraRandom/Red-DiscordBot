from discord.ext import commands
import discord
from datetime import datetime  # , date, timedelta
from pytz import timezone
import time
from cogs.utils import checks
import platform
import os

import subprocess


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

    @commands.command(hidden=True, aliases=["who_where", "ww", "who", "where"])
    @checks.is_owner()
    async def where_who(self):
        """Admin Only Command"""
        servers = self.bot.servers

        embed = discord.Embed(title="List of servers I am in and people in them",
                              colour=discord.Colour.darker_grey(),
                              description="Hello")

        for server in servers:
            name = server.name

            users = server.members
            user_msg = ""

            for user in users:
                user_msg += "{}\n".format(user.name)

            embed.add_field(name="{}".format(name),
                            value="{}".format(user_msg))

        await self.bot.say(embed=embed)

    @commands.command(hidden=True, aliases=["chans", "chan", "channel"])
    @checks.is_owner()
    async def channels(self):
        """Admin Only Command"""
        servers = self.bot.servers

        embed = discord.Embed(title="Channels that I am in",
                              colour=discord.Colour.darker_grey(),
                              description="Channels")

        for server in servers:
            name = "{} - {}".format(server.name, server.id)

            channels = server.channels
            chan_msg = ""

            for chan in channels:
                chan_msg += "{} - {} - {}\n".format(chan.name, chan.type, chan.id)

            embed.add_field(name="{}".format(name),
                            value="{}".format(chan_msg))

        await self.bot.say(embed=embed)

    @commands.command(hidden=True, aliases=["tlog", "t_log", "log"])
    @checks.is_owner()
    async def text_log(self, channel: str, limit=10):
        """Admin Only Command"""
        # TODO add better link detection so they don't embed

        try:
            ignore_list = ["181177004085739520", "378608361727328267"]
            msgs = ""
            i = 0
            async for msg in self.bot.logs_from(self.bot.get_channel(channel), limit):
                i += 1
                if msg.author.id in ignore_list:
                    msgs += "{} - Ignored Author\n".format(i)
                else:
                    msg_content = msg.clean_content
                    msg_content = msg_content.replace("https://", "").replace("http://", "")  # link detect. to replace
                    msgs += "{} - {} - {} - {}\n".format(i, msg_content, msg.author,
                                                         str(msg.timestamp).split(".")[0])

                if i % 20 == 0:
                    await self.bot.say(msgs)
                    msgs = ""

            if msgs != "":
                await self.bot.say(msgs)
        except Exception as e:
            await self.bot.say("Error [{}]: {}".format(type(e), e))

    @commands.command(hidden=True)
    @checks.is_owner()
    async def system(self):
        """Get System Temp and Up time if  running on RPi"""
        os_name = platform.system()

        if os_name == "Linux":
            res = os.popen('vcgencmd measure_temp').readline()
            temp = res.replace("temp=", "").replace("'C\n", "")

            uptime = os.popen('uptime').readline()
        elif os_name == "Windows":
            temp = "Bot running on Windows - System Temperature N/A"
            uptime = "Bot running on Windows - System Uptime N/A"
        else:
            temp = "Error retrieving temperature."
            uptime = "Error retrieving uptime"

        embed = discord.Embed(title="System Status",
                              colour=discord.Colour.green())

        embed.add_field(name="Temperature",
                        value=temp)
        embed.add_field(name="Uptime",
                        value=uptime)

        await self.bot.say(embed=embed)

    @commands.command(hidden=True)
    @checks.is_owner()
    async def update(self):
        subprocess.call(["./surs"])


def secs_to_days(seconds):
    return str(seconds / 86400).split(".")[0]


def setup(bot):
    bot.add_cog(Misc(bot))
