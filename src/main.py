from discord import Activity, ActivityType, Bot, Intents
from dotenv import load_dotenv
from os import getenv, listdir
from os.path import isfile, join

load_dotenv()

bot = Bot(intents=Intents.all())
bot.activity = Activity(name="/help", type=ActivityType.listening)

@bot.event
async def on_ready():
    print(f'{bot.user} online')

for file in listdir("./src/cogs"):
    if isfile(join("./src/cogs", file)) and file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")
        print(f"Cog loaded: {file[:-3]}")  

bot.run(getenv("DISCORD_TOKEN"))