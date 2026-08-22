import re
Name_Pattern = re.compile(r'[A-Z][a-z]+')
def name_validation(name):
    return bool(Name_Pattern.match(name))

ID_Pattern = re.compile(r'^36\d{4}$')
def id_validation(id):
    return bool(ID_Pattern.match(id))

def id_generator():
    for i in range(0, 8):
        return 360000 + i


class Player:
    def __init__(self, name, rating, attack, defense, speed, luck,heal,status, wins, losses):
        self.name = name
        self.ID =id_generator()
        self.rating = rating
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.luck = luck
        self.heal = heal
        self.status = status
        self.wins = wins
        self.losses = losses

    def __str__(self):
        return f"{self.name} \n Rating: {self.rating} \n Attack: {self.attack} \n Defense: {self.defense} \n Speed: {self.speed} \n Luck: {self.luck}"

    def set_rating(self, rating):
        if rating < 0 or rating > 100:
            raise InputError()
        return f"your rating is {self.attack}"

    def set_attack(self, attack):
        if attack < 0 or attack > 100:
            raise InputError()
        return f"your rating is {self.attack}"

    def set_defense(self, defense):
        if defense < 0 or defense > 100:
            raise InputError()
        return f"your rating is {self.defense}"

    def set_speed(self, speed):
        if speed < 0 or speed > 100:
            raise InputError()
        return f"your rating is {self.speed}"

class InputError(Exception):
    def __init__(self, message=" your input must be between 1 and 100"):
        super().__init__(message)

