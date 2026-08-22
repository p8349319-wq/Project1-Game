from random import randint
import re

# exceptions.py

class InvalidNameError(Exception):
    """Custom exception for name validation errors"""
    def __init__(self, message="Invalid name."):
        self.message = message
        super().__init__(self.message)

# validation.py
def validate_name(name):
    """
    Validate name - only English letters allowed
    """
    pattern = r'^[a-zA-Z\s]{2,30}$'

    # Check if empty
    if not name or len(name.strip()) == 0:
        raise InvalidNameError("Name cannot be empty.")

    name = name.strip()

    # Check length
    if len(name) < 2:
        raise InvalidNameError("Name must be at least 2 characters long.")
    if len(name) > 30:
        raise InvalidNameError("Name must not exceed 30 characters.")

    # Check allowed characters (only English letters and spaces)
    if not re.match(pattern, name):
        raise InvalidNameError("Name must contain only English letters and spaces.")

    # Check leading/trailing spaces
    if name != name.strip():
        raise InvalidNameError("Name should not start or end with space.")

    return name




# player.py
class Player:
    _id_counter = 360000  # Class variable for ID generation

    def __init__(self, name):
        self.name = validate_name(name)  # Validate name on creation
        self.ID = self._generate_id()

        self.rating = randint(40, 100)
        self.attack = randint(40, 100)
        self.defense = randint(40, 100)
        self.speed = randint(40, 100)
        self.health = randint(1000, 2000)
        self.luck = randint(40, 100)
        self.wins = 0
        self.losses = 0

    @classmethod
    def _generate_id(cls):
        """Generate unique ID for each player"""
        current_id = cls._id_counter
        cls._id_counter += 1
        return current_id


    def __str__(self):
        return f"ID: {self.ID}\nName: {self.name}\nRating: {self.rating}\nAttack: {self.attack}\n Health: {self.health}\nDefense: {self.defense}\nSpeed: {self.speed}\nLuck: {self.luck}\nWins: {self.wins}\nLosses: {self.losses}"