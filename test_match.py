from Battle_Engine import battle_engine
from Player import Player
import unittest
class Test_Battle(unittest.TestCase):
    def setUp(self):
        self.player1 = Player(
            name = "ali",
            attack = 60,
            defense = 30,
            luck = 20,
            speed = 30,
            rating=1500,
            wins=3,
            losses=5
        )
        self.player2 = Player(
                name = "reza",
                 attack = 40,
                defense = 40,
                luck = 26,
                speed = 50,
                rating=1500,
                wins=3,
                losses=5
                )
        self.battle = battle_engine(self.player1,self.player2)
 
    def test_match_start(self):
        self.assertEqual(self.battle.start_battle(),"---Match starts ali VS reza---")
if __name__ == "__main__":
    unittest.main()