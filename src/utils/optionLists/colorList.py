from discord import OptionChoice
from os import getenv

colorList = [
    OptionChoice("Défaut", int(getenv("DEFAULT_COLOR"), 16)),
    OptionChoice("Rouge", 0xF00020),
    OptionChoice("Vert", 0x008020),
    OptionChoice("Bleu", 0x0E4BEF),
    OptionChoice("Jaune", 0xFEE347),
    OptionChoice("Mauve", 0x9370DB),
    OptionChoice("Blanc", 0xFEFEFE),
    OptionChoice("Gris", 0x7F7F7F),
    OptionChoice("Aucune", 0x2F3136)
]
