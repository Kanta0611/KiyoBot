from discord import Option, OptionChoice, SlashCommandGroup, Embed
from os import getenv
from utils.classes.Player import Player
from utils.optionLists.statNames import statNames, statLongNames
from discord.ext import commands
from sqlite3 import connect

class Stats(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    stats = SlashCommandGroup("stats", "Commandes relatives aux statistiques")

    @stats.command(name="add", description="🧮 Permet de distribuer des points de statistiques")
    async def add(
        self,
        ctx: commands.Context,
        stat: Option(
            str,
            description="Stat à laquelle vous souhaitez ajouter des points",
            required=True,
            choices=statNames
        ),
        points: Option(
            int,
            description="Nombre de points à ajouter",
            required=True,
            min_value=1,
            max_value=100
        )
    ):

        db = connect("database/database.db")

        player = db.cursor().execute(f"SELECT * FROM player WHERE dsc_uid = \"{ctx.author.id}\"").fetchall()

        if len(player) == 0:
            await ctx.respond(embed = Embed(description="Vous n'avez pas encore de profil.", color=int(getenv("RED_COLOR"), 16)), ephemeral=True)
            return
        
        statName = ""
        for _statName in statNames:
            if _statName.value == stat:
                statName = _statName.name
                break

        player = Player(player[0])

        if player.freeStatPoints < points:
            await ctx.respond(embed = Embed(description=f"Vous n'avez pas assez de points de statistiques à distribuer.", color=int(getenv("RED_COLOR"), 16)), ephemeral=True)
            return

        realPoints = points

        if stat == "p_hp":
            realPoints *= 5
        elif stat == "p_mp" or stat == "p_ep":
            realPoints *= 3
        elif stat == "p_speed":
            realPoints *= 2

        db.cursor().execute(f"UPDATE player SET {stat} = {stat} + {realPoints}, p_statsFree = p_statsFree - {points} WHERE dsc_uid = \"{ctx.author.id}\"")

        if stat == "p_hp":
            db.cursor().execute(f"UPDATE player SET p_chp = p_chp + {realPoints} WHERE dsc_uid = \"{ctx.author.id}\"")
        elif stat == "p_mp":
            db.cursor().execute(f"UPDATE player SET p_cmp = p_cmp + {realPoints} WHERE dsc_uid = \"{ctx.author.id}\"")
        elif stat == "p_ep":
            db.cursor().execute(f"UPDATE player SET p_cep = p_cep + {realPoints} WHERE dsc_uid = \"{ctx.author.id}\"")    

        db.commit()

        await ctx.respond(embed = Embed(description=f"{ctx.author.mention} s'est ajouté {realPoints} {statName.lower()}.", color=int(getenv("GREEN_COLOR"), 16)))
        

def setup(bot:commands.Bot):
    bot.add_cog(Stats(bot))
    