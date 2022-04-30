from os import getenv

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
