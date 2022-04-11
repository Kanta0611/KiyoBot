from math import ceil
from random import randint
from sqlite3 import connect
from discord import Embed, Member, Message, Option, Permissions, SlashCommandGroup
from discord.ext import commands
from cogs.Profile import Player
from os import getenv

class Experience(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    exp = SlashCommandGroup("exp", "Commandes relatives à l'expérience")
    
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        print("Euh : " + message.content)
        if message.content.startswith("(") or message.content.endswith(")") or len(message.content) < 40:
            return

        if message.author.bot:
            return

        if message.guild is None:
            return
        
        db = connect("database/database.db")
        checkplayer = db.cursor().execute(f"SELECT dsc_uid FROM player WHERE dsc_uid = \"{message.author.id}\"").fetchall()

        if len(checkplayer) == 0:
            return

        rpchans = db.cursor().execute(f"SELECT dsc_cid FROM localisation WHERE dsc_cid = {message.channel.id} OR dsc_cid = {message.channel.category.id}").fetchall()

        # if rpchans is a length of 0, then the channel is not a RP channel
        if len(rpchans) == 0:
            return

        bonus = randint(1, 100)

        if bonus > 95:
            bonus = 3
        elif bonus > 50:
            bonus = 2
        else:
            bonus = 1

        db.cursor().execute(f"UPDATE player SET p_xp = p_xp + {bonus * ceil(len(message.content) / 100)} WHERE dsc_uid = {message.author.id}")
        db.commit()

        player = Player(db.cursor().execute(f"SELECT * FROM player WHERE dsc_uid = {message.author.id}").fetchall()[0])

        levelChannel = self.bot.get_channel(int(getenv("LEVEL_CHANNEL")))
        while player.xp >= ceil(100 * (1.15 ** player.level)):
            db.cursor().execute(f"UPDATE player SET p_lvl = p_lvl + 1, p_xp = p_xp - {ceil(100 * 1.15 ** player.level)}, p_statsfree = p_statsfree + {5 * ceil(player.level/10)} WHERE dsc_uid = {message.author.id}")
            db.commit()

            player = Player(db.cursor().execute(f"SELECT * FROM player WHERE dsc_uid = {message.author.id}").fetchall()[0])
            
            await levelChannel.send(embed=Embed(description=f"{message.author.mention} a atteint le niveau {player.level} !\nIl a {player.freeStatPoints} points à attribuer à ses stats.", color=int(getenv("GREEN_COLOR"), 16)))

    @exp.command(name="add", description="✨ Ajoute de l'expérience à un joueur")
    async def add(
        self,
        ctx: commands.Context,
        exp: Option(
            int,
            description="L'expérience à ajouter à un joueur",
            min_value=1,
            required=True
        ),
        member: Option(
            Member,
            description="La personne à qui ajouter de l'expérience",
            required=False
        )
    ):
        canDo = False
        for role in ctx.author.roles:
            if role.permissions.moderate_members:
                canDo = True
                break

        if not canDo:
            await ctx.respond(embed=Embed(description="Vous n'avez pas la permission d'utiliser cette commande.", color=int(getenv("RED_COLOR"), 16)), ephemeral=True)
            return    
        
        if member is None:
            member = ctx.author
        
        db = connect("database/database.db")

        checkplayer = db.cursor().execute(f"SELECT dsc_uid FROM player WHERE dsc_uid = \"{ctx.author.id}\"").fetchall()

        if len(checkplayer) == 0:
            await ctx.respond(embed=Embed(description=f"{member.display_name} n'a pas de profil.", color=int(getenv("RED_COLOR"), 16)), ephemeral=True)
            return
        
        db.cursor().execute(f"UPDATE player SET p_xp = p_xp + {exp} WHERE dsc_uid = {member.id}"); db.commit()
        
        await ctx.respond(embed=Embed(description=f"Vous avez rajouté {exp} points d'expérience à {member.mention}.", color=int(getenv("GREEN_COLOR"), 16)), ephemeral=True)
    
    @exp.command(name="remove", description="✨ Retire de l'expérience à un joueur")
    async def remove(
        self,
        ctx: commands.Context,
        exp: Option(
            int,
            description="L'expérience à retirer à un joueur",
            min_value=1,
            required=True
        ),
        member: Option(
            Member,
            description="La personne à qui retirer de l'expérience",
            required=False
        )
    ):
        canDo = False
        for role in ctx.author.roles:
            if role.permissions.moderate_members:
                canDo = True
                break

        if not canDo:
            await ctx.respond(embed=Embed(description="Vous n'avez pas la permission d'utiliser cette commande.", color=int(getenv("RED_COLOR"), 16)), ephemeral=True)
            return    
        
        if member is None:
            member = ctx.author
        
        db = connect("database/database.db")

        checkplayer = db.cursor().execute(f"SELECT dsc_uid FROM player WHERE dsc_uid = \"{ctx.author.id}\"").fetchall()

        if len(checkplayer) == 0:
            await ctx.respond(embed=Embed(description=f"{member.display_name} n'a pas de profil.", color=int(getenv("RED_COLOR"), 16)), ephemeral=True)
            return
        
        player = Player(db.cursor().execute(f"SELECT * FROM player WHERE dsc_uid = {member.id}").fetchall()[0])

        while player.xp < exp:
            db.cursor.execute(f"UPDATE player SET p_lvl = p_lvl - 1, p_xp = p_xp + {ceil(100 * 1.15 ** (player.level - 1))} WHERE dsc_uid = {member.id}")
            db.commit()
            player = Player(db.cursor().execute(f"SELECT * FROM player WHERE dsc_uid = {member.id}").fetchall()[0])


def setup(bot:commands.Bot):
    bot.add_cog(Experience(bot))