from Battle_Engine import battle_engine
from Player import Player
from Enum_classes import special_event, player_status
import unittest


class Test_Battle(unittest.TestCase):
    def setUp(self):
        self.player1 = Player(
            name="ali",
            attack=60,
            defense=30,
            speed=50,
            luck=20,
            rating=1700,
            wins=0,
            losses=0,
            heal=1500,
            status=player_status.IN_MATCH,
        )
        self.player2 = Player(
            name="reza",
            attack=50,
            defense=40,
            speed=60,
            rating=1600,
            luck=30,
            wins=0,
            losses=0,
            heal=1500,
            status=player_status.IN_MATCH,
        )
        self.battle = battle_engine(self.player1, self.player2)

    def test_start_battle(self):
        result = self.battle.start_battle()
        self.assertEqual(result, "⚔️  ---Match starts ali VS reza--- ⚔️")

    def test_start_battle_sets_status(self):
        self.battle.start_battle()
        self.assertEqual(self.player1.status, player_status.IN_MATCH)
        self.assertEqual(self.player2.status, player_status.IN_MATCH)

    def test_init(self):
        self.assertEqual(self.battle.player1.name, "ali")
        self.assertEqual(self.battle.player2.name, "reza")

    def test_special_event_returns_valid_event(self):
        result = self.battle.special_event(self.player1)
        self.assertIn(result, list(special_event))

    def test_special_event_message_attack_only(self):
        result = self.battle.special_event_message(
            special_event.ATTACK, special_event.NO_EVENT, self.player1, self.player2
        )
        valid_messages = [
            f"⚡ <<{special_event.ATTACK.value}>> Wow! Special event for {self.player1.name}!",
            f"😱 GOD is that even possible! <<{special_event.ATTACK.value}>> for {self.player1.name}!",
            f"🌟 Special event happened: {special_event.ATTACK.value}, Such a lucky player!",
        ]
        self.assertIn(result, valid_messages)

    def test_special_event_message_defense_only(self):
        result = self.battle.special_event_message(
            special_event.NO_EVENT, special_event.DEFENSE, self.player1, self.player2
        )
        valid_messages = [
            f"🛡️  But wait! {self.player2.name} activates <<{special_event.DEFENSE.value}>>!",
            f"💪 Not so fast! {self.player2.name} counters with <<{special_event.DEFENSE.value}>>!",
            f"✨ Incredible! {self.player2.name} responds with {special_event.DEFENSE.value}!",
        ]
        self.assertIn(result, valid_messages)

    def test_special_event_message_both_events(self):
        result = self.battle.special_event_message(
            special_event.ATTACK, special_event.DEFENSE, self.player1, self.player2
        )
        valid_messages = [
            f"🔥 INSANE ROUND! {self.player1.name} unleashes <<{special_event.ATTACK.value}>> but {self.player2.name} counters with <<{special_event.DEFENSE.value}>>!",
            f"💥 CLASH OF EVENTS! <<{special_event.ATTACK.value}>> VS <<{special_event.DEFENSE.value}>>! Who will win?",
            f"🌪️  DOUBLE EVENT! {self.player1.name} with <<{special_event.ATTACK.value}>> meets {self.player2.name}'s <<{special_event.DEFENSE.value}>>!",
        ]
        self.assertIn(result, valid_messages)

    def test_special_event_message_no_event(self):
        result = self.battle.special_event_message(
            special_event.NO_EVENT, special_event.NO_EVENT, self.player1, self.player2
        )
        self.assertIsNone(result)

    def test_player_attack_no_event(self):
        result = self.battle.player_attack(self.player1, special_event.NO_EVENT)
        expected = (2 * 60 * 50) / 10
        self.assertEqual(result, expected)

    def test_player_attack_attack_event(self):
        result = self.battle.player_attack(self.player1, special_event.ATTACK)
        expected = (2.5 * 60 * 50) / 10
        self.assertEqual(result, expected)

    def test_player_attack_extra_attack_event(self):
        result = self.battle.player_attack(self.player1, special_event.EXTRA_Attack)
        expected = (2 * (60 * 2) * 50) / 10
        self.assertEqual(result, expected)

    def test_player_attack_speed_event(self):
        result = self.battle.player_attack(self.player1, special_event.SPEED)
        expected = (2 * 60 * (50 * 1.3)) / 10
        self.assertEqual(result, expected)

    def test_player_defense_no_event(self):
        result = self.battle.player_defense(self.player2, special_event.NO_EVENT)
        expected = 2.5 * 40
        self.assertEqual(result, expected)

    def test_player_defense_defense_event(self):
        result = self.battle.player_defense(self.player2, special_event.DEFENSE)
        expected = 2.5 * (40 * 1.5)
        self.assertEqual(result, expected)

    def test_apply_damage_reduces_health(self):
        initial_heal = self.player2.heal
        damage = self.battle.apply_damage(
            self.player1, self.player2, special_event.NO_EVENT, special_event.NO_EVENT
        )
        self.assertEqual(self.player2.heal, initial_heal - damage)

    def test_apply_damage_never_negative(self):
        self.player1.attack = 1
        self.player1.speed = 1
        self.player2.defense = 100
        damage = self.battle.apply_damage(
            self.player1, self.player2, special_event.NO_EVENT, special_event.DEFENSE
        )
        self.assertEqual(damage, 0)

    def test_check_game_winner_player1_loses(self):
        self.player1.heal = 0
        message, winner, loser = self.battle.check_game_winner()
        self.assertEqual(winner, self.player2)
        self.assertEqual(loser, self.player1)
        self.assertEqual(self.player1.status, player_status.LOSE)
        self.assertEqual(self.player2.status, player_status.WIN)

    def test_check_game_winner_player2_loses(self):
        self.player2.heal = 0
        message, winner, loser = self.battle.check_game_winner()
        self.assertEqual(winner, self.player1)
        self.assertEqual(loser, self.player2)
        self.assertEqual(self.player2.status, player_status.LOSE)
        self.assertEqual(self.player1.status, player_status.WIN)

    def test_check_game_winner_no_winner(self):
        message, winner, loser = self.battle.check_game_winner()
        self.assertIsNone(message)
        self.assertIsNone(winner)
        self.assertIsNone(loser)

    def test_check_game_winner_message_player1_loses(self):
        self.player1.heal = 0
        message, winner, loser = self.battle.check_game_winner()
        self.assertEqual(
            message,
            f"💀 {self.player1.name} has no health left! 🏆 {self.player2.name} WINS!",
        )

    def test_check_game_winner_message_player2_loses(self):
        self.player2.heal = 0
        message, winner, loser = self.battle.check_game_winner()
        self.assertEqual(
            message,
            f"💀 {self.player2.name} has no health left! 🏆 {self.player1.name} WINS!",
        )

    def test_special_event_all_events(self):
        for event in [
            special_event.ATTACK,
            special_event.DEFENSE,
            special_event.SPEED,
            special_event.EXTRA_Attack,
        ]:
            result = self.battle.special_event_message(
                event, special_event.NO_EVENT, self.player1, self.player2
            )
            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
