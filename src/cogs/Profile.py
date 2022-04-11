from math import ceil
from discord import Embed, Member, Option, OptionChoice, SlashCommandGroup
from discord.ext import commands
from sqlite3 import connect
from datetime import datetime
from os import getenv

colorList = [
    OptionChoice("Rouge", 0xF00020),
    OptionChoice("Vert", 0x008020),
    OptionChoice("Bleu", 0x0E4BEF),
    OptionChoice("Jaune", 0xFEE347),
    OptionChoice("Mauve", 0x9370DB),
    OptionChoice("Blanc", 0xFEFEFE),
    OptionChoice("Gris", 0x7F7F7F)
]

class Player():
    def __init__(self, request: list):
        self.p_id: int = request[0]
        self.dsc_uid: str = request[1]
        self.color: int = request[2] if request[2] is not None else int(getenv("DEFAULT_COLOR"), 16)
        self.desc: str = request[3] if request[3] is not None else ''
        self.img: str = request[4] if request[4] is not None else ''
        self.xp: int = request[5]
        self.level: int = request[6]
        self.money: int = request[7]
        self.currentHP: int = request[8]
        self.maxHP: int = request[9]
        self.currentMP: int = request[10]
        self.maxMP: int = request[11]
        self.currentEP: int = request[12]
        self.maxEP: int = request[13]
        self.physicalForce: int = request[14]
        self.magicForce: int = request[15]
        self.physicalResistance: int = request[16]
        self.magicResistance: int = request[17]
        self.speed: int = request[18]
        self.freeStatPoints: int = request[19]

class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    profile = SlashCommandGroup("profile", "Commandes relatives aux profils")
    
    @commands.user_command(name="Afficher le profil", description="Affiche le profil de l'utilisateur")
    async def showProfile(self, ctx: commands.Context, member: Member = None):
        await self.show(self, ctx, member)

    @profile.command(name="show", description="📜 Affiche votre profil ou celui d'un membre du serveur")
    async def show(
        self,
        ctx: commands.Context,
        member: Option(
            Member,
            description="Membre du serveur dont vous souhaitez afficher le profil",
            required=False,
            default=None
        )):
        db = connect("database/database.db")
        if member is None:
            member = ctx.author

        player = db.cursor().execute(f"SELECT * FROM player WHERE dsc_uid = \"{member.id}\"").fetchall()
        
        if len(player) == 0:
            await ctx.respond(embed = Embed(description=f"{member.mention} n'a pas encore de profil.", color=int(getenv("RED_COLOR"), 16)), ephemeral=True)
            return

        player = Player(player[0])

        profileEmbed = Embed(title=f"Profil de {member.display_name}", color=player.color, description=player.desc)
        profileEmbed.set_image(url=player.img)
        
        profileEmbed.add_field(name="** **", value=f"⏫ **Niveau** `{player.level}`\n✨ **Exp :** `{player.xp}/{ceil(100 * (1.15 ** player.level))}`\n🪙 **Argent :** `{player.money}`\n\n❤️ **PV :** `{player.currentHP}/{player.maxHP}`\n🌀 **PM :** `{player.currentMP}/{player.maxMP}`\n💪🏻 **PE :** `{player.currentEP}/{player.maxEP}`", inline=True)
        profileEmbed.add_field(name="** **", value=f"🤜🏻 **Force Physique :** `{player.physicalForce}`\n💥 **Force Magique :** `{player.magicForce}`\n\n🖐🏻 **Résistance Physique :** `{player.physicalResistance}`\n🛡️ **Résistance Magique :** `{player.magicResistance}`\n\n💨 **Vitesse :** `{player.speed}`", inline=True)

        profileEmbed.set_footer(text=f"KiyoBot | {player.freeStatPoints} points de stats à attribuer", icon_url=self.bot.user.avatar.url)
        
        await ctx.respond(embed=profileEmbed)

    @profile.command(name="create", description="📜 Crée votre profil")
    async def create(
        self,
        ctx: commands.Context,
        description: Option(
            str,
            description="Description souhaitée pour votre profil",
            required=False,
            default=None
        ),
        color: Option(
            int,
            description="Couleur souhaitée pour votre profil",
            required=False,
            default=None,
            choices=colorList
        ),
        img: Option(
            str,
            description="URL de l'image souhaitée pour votre profil",
            required=False,
            default=None
        )):
        db = connect("database/database.db")
        
        if len(db.cursor().execute(f"SELECT * FROM player WHERE dsc_uid = \"{ctx.author.id}\"").fetchall()) != 0:
            await ctx.respond(embed=Embed(description=f"Vous avez déjà un profil !", color=int(getenv("RED_COLOR"), 16)), ephemeral=True)
            return
        
        db.cursor().execute(f"INSERT INTO player (dsc_uid) VALUES (\"{ctx.author.id}\")")
        
        if img is not None:
            db.cursor().execute(f"UPDATE player SET p_img = \"{img}\" WHERE dsc_uid = \"{ctx.author.id}\"")
        if color is not None:
            db.cursor().execute(f"UPDATE player SET p_col = {color} WHERE dsc_uid = \"{ctx.author.id}\"")
        if description is not None:
            db.cursor().execute(f"UPDATE player SET p_desc = \"{description}\" WHERE dsc_uid = \"{ctx.author.id}\"")

        db.commit()    

        await ctx.respond(embed=Embed(description = "Votre profil a été créé avec succès.", color=int(getenv("GREEN_COLOR"), 16), timestamp = datetime.utcnow()))

    @profile.command(name="edit", description="📜 Modifie votre profil")
    async def edit(
        self,
        ctx: commands.Context,
        description: Option(
            str,
            description="Description souhaitée pour votre profil",
            required=False,
            default=None
        ),
        color: Option(
            int,
            description="Couleur souhaitée pour votre profil",
            required=False,
            default=None,
            choices=colorList
        ),
        img: Option(
            str,
            description="URL de l'image souhaitée pour votre profil",
            required=False,
            default=None
        )):
        if img is None and color is None and description is None:
            await ctx.respond(embed=Embed(description=f"Vous n'avez pas spécifié de changement à apporter !", color=int(getenv("RED_COLOR"), 16)), ephemeral=True)
            return
        
        db = connect("database/database.db")
        
        if len(db.cursor().execute(f"SELECT * FROM player WHERE dsc_uid = \"{ctx.author.id}\"").fetchall()) == 0:
            await ctx.respond(embed=Embed(description=f"Vous n'avez pas encore de profil !", color=int(getenv("RED_COLOR"), 16)), ephemeral=True)
            return

        if img is not None:
            db.cursor().execute(f"UPDATE player SET p_img = \"{img}\" WHERE dsc_uid = \"{ctx.author.id}\"")
        if color is not None:
            db.cursor().execute(f"UPDATE player SET p_col = {color} WHERE dsc_uid = \"{ctx.author.id}\"")
        if description is not None:
            db.cursor().execute(f"UPDATE player SET p_desc = \"{description}\" WHERE dsc_uid = \"{ctx.author.id}\"")

        db.commit()    

        await ctx.respond(embed=Embed(description = "Votre profil a été modifié avec succès.", color=int(getenv("GREEN_COLOR"), 16), timestamp = datetime.utcnow()))

    @profile.command(name="delete", description="📜 Supprime votre profil")
    async def delete(self, ctx: commands.Context):
        db = connect("database/database.db")
        
        if len(db.cursor().execute(f"SELECT * FROM player WHERE dsc_uid = \"{ctx.author.id}\"").fetchall()) == 0:
            await ctx.respond(embed=Embed(f"Vous n'avez pas de profil !", color=int(getenv("RED_COLOR"), 16)), ephemeral=True)
            return
        
        db.cursor().execute(f"DELETE FROM player WHERE dsc_uid = \"{ctx.author.id}\"")
        db.commit()

        await ctx.respond(embed=Embed(description = "Votre profil a été supprimé avec succès.", color=int(getenv("GREEN_COLOR"), 16), timestamp = datetime.utcnow()))

def setup(bot:commands.Bot):
    bot.add_cog(Profile(bot))