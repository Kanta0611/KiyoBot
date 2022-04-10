from discord import Activity, ActivityType, Bot
from dotenv import load_dotenv
from os import getenv, listdir
from os.path import isfile, join

load_dotenv()

bot = Bot()
bot.activity = Activity(name="/help", type=ActivityType.listening)

@bot.event
async def on_ready():
    print(f'{bot.user} online')

# Prints every file name in cogs directory that ends with .py
for file in listdir("./src/cogs"):
    if isfile(join("./src/cogs", file)) and file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")
        print(f"Cog loaded: {file[:-3]}")  

bot.run(getenv("DISCORD_TOKEN"))