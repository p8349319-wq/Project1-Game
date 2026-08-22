from Battle_Engine import battle_engine
from Player import Player
import unittest
from Special_Event import special_event
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
    def test_special_event_random(self):
        result = str(battle_engine.special_event(self))
        valid_events = ["special_event.ATTACK","special_event.DEFENSE","special_event.SPEED","special_event.NO_EVENT","special_event.EXTRA_ROUND"]
        self.assertIn(result,valid_events)
    def test_special_event_message_all_cases(self):
        for event in [special_event.ATTACK, special_event.DEFENSE, special_event.SPEED,special_event.EXTRA_Attack]:
            result = self.battle.special_event_message(event, self.player1)
            valid_messages = [
                f"Special event happend: {event.value}, Such a lucky player!",
                f"<<{event.value}>> Wow! Special event for {self.player1.name}",
                f"GOD is that even possible! <<{event.value}>>",
            ]
            self.assertIn(result, valid_messages)

    def test_special_event_message_no_event(self):
        result = self.battle.special_event_message(special_event.NO_EVENT, self.player1)
        self.assertIsNone(result)
if __name__ == "__main__":
    unittest.main()