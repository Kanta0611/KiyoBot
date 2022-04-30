from discord import OptionChoice

statNames = [
    OptionChoice("Points de vie", "p_hp"),
    OptionChoice("Points de magie", "p_mp"),
    OptionChoice("Points d'endurance", "p_ep"),
    OptionChoice("Force physique", "p_pforce"),
    OptionChoice("Force magique", "p_mforce"),
    OptionChoice("Résistance physique", "p_pres"),
    OptionChoice("Résistance magique", "p_mres"),
    OptionChoice("Vitesse", "p_speed")
]

statLongNames = [
    OptionChoice("p_hp", "Points de vie"),
    OptionChoice("p_mp", "Points de magie"),
    OptionChoice("p_ep", "Points d'endurance"),
    OptionChoice("p_pforce", "Force physique"),
    OptionChoice("p_mforce", "Force magique"),
    OptionChoice("p_pres", "Résistance physique"),
    OptionChoice("p_mres", "Résistance magique"),
    OptionChoice("p_speed", "Vitesse")
]