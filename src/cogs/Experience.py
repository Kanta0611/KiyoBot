import discord
from discord.ext import commands


class Experience(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        

def setup(bot:commands.Bot):
    bot.add_cog(Experience(bot))