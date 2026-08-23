from Battle_Engine import battle_engine
from Player import Player
from Enum_classes import special_event, player_status
import unittest
from unittest.mock import patch


class Test_Battle(unittest.TestCase):
    def setUp(self):
        self.player1 = Player(name="ali")
        self.player2 = Player(name="reza")
        self.battle = battle_engine(self.player1, self.player2)

    def test_init(self):
        self.assertEqual(self.battle.player1.name, "ali")
        self.assertEqual(self.battle.player2.name, "reza")

    def test_init_clones_players(self):
        self.assertEqual(self.battle.player1_clone.health, self.player1.health)
        self.assertEqual(self.battle.player2_clone.health, self.player2.health)

    def test_start_battle(self):
        result = self.battle.start_battle()
        self.assertEqual(
            result,
            f"⚔️  ---Match starts {self.player1.name} VS {self.player2.name}--- ⚔️",
        )

    def test_start_battle_sets_status(self):
        self.battle.start_battle()
        self.assertEqual(self.player1.status, player_status.IN_MATCH)
        self.assertEqual(self.player2.status, player_status.IN_MATCH)

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

    def test_special_event_message_defense_not_in_attack(self):
        result = self.battle.special_event_message(
            special_event.DEFENSE, special_event.NO_EVENT, self.player1, self.player2
        )
        self.assertIsNone(result)

    def test_special_event_message_all_attack_events(self):
        for event in [
            special_event.ATTACK,
            special_event.SPEED,
            special_event.EXTRA_Attack,
        ]:
            result = self.battle.special_event_message(
                event, special_event.NO_EVENT, self.player1, self.player2
            )
            self.assertIsNotNone(result)

    def test_player_attack_no_event(self):
        result = self.battle.player_attack(self.player1, special_event.NO_EVENT)
        expected = (1.5 * self.player1.attack * self.player1.speed) / 14
        self.assertEqual(result, expected)

    def test_player_attack_attack_event(self):
        result = self.battle.player_attack(self.player1, special_event.ATTACK)
        expected = (2 * self.player1.attack * self.player1.speed) / 14
        self.assertEqual(result, expected)

    def test_player_attack_extra_attack_event(self):
        result = self.battle.player_attack(self.player1, special_event.EXTRA_Attack)
        expected = (1.5 * (self.player1.attack * 2) * self.player1.speed) / 14
        self.assertEqual(result, expected)

    def test_player_attack_speed_event(self):
        result = self.battle.player_attack(self.player1, special_event.SPEED)
        expected = (1.5 * self.player1.attack * (self.player1.speed * 1.2)) / 14
        self.assertEqual(result, expected)

    def test_player_defense_no_event(self):
        result = self.battle.player_defense(self.player2, special_event.NO_EVENT)
        expected = self.player2.defense * 0.5
        self.assertEqual(result, expected)

    def test_player_defense_defense_event(self):
        result = self.battle.player_defense(self.player2, special_event.DEFENSE)
        expected = (self.player2.defense * 1.5) * 0.5
        self.assertEqual(result, expected)

    def test_apply_damage_reduces_health(self):
        initial_health = self.player2.health
        damage = self.battle.apply_damage(
            self.player1, self.player2, special_event.NO_EVENT, special_event.NO_EVENT
        )
        self.assertEqual(self.player2.health, initial_health - damage)

    def test_apply_damage_never_negative(self):
        with (
            patch.object(self.player1, "attack", 1),
            patch.object(self.player1, "speed", 1),
            patch.object(self.player2, "defense", 100),
        ):
            damage = self.battle.apply_damage(
                self.player1,
                self.player2,
                special_event.NO_EVENT,
                special_event.DEFENSE,
            )
            self.assertEqual(damage, 0)

    def test_check_game_winner_player1_loses(self):
        self.player1.health = 0
        message, winner, loser = self.battle.check_game_winner()
        self.assertEqual(winner, self.player2)
        self.assertEqual(loser, self.player1)
        self.assertEqual(self.player1.status, player_status.LOSE)
        self.assertEqual(self.player2.status, player_status.WIN)

    def test_check_game_winner_player2_loses(self):
        self.player2.health = 0
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
        self.player1.health = 0
        message, winner, loser = self.battle.check_game_winner()
        self.assertEqual(
            message,
            f"💀 {self.player1.name} has no health left! 🏆 {self.player2.name} WINS!",
        )

    def test_check_game_winner_message_player2_loses(self):
        self.player2.health = 0
        message, winner, loser = self.battle.check_game_winner()
        self.assertEqual(
            message,
            f"💀 {self.player2.name} has no health left! 🏆 {self.player1.name} WINS!",
        )

    def test_check_game_winner_restores_stats(self):
        original_health = self.player2.health
        self.player1.health = 0
        self.battle.check_game_winner()
        self.assertEqual(self.player2.health, original_health)

    def test_check_game_winner_updates_wins(self):
        self.player1.health = 0
        self.battle.check_game_winner()
        self.assertEqual(self.player2.wins, 1)
        self.assertEqual(self.player1.losses, 1)

    def test_decide_winner_by_health_player1_wins(self):
        self.player1.health = 800
        self.player2.health = 500
        winner, loser = self.battle._decide_winner_by_health()
        self.assertEqual(winner, self.player1)
        self.assertEqual(loser, self.player2)
        self.assertEqual(self.player1.status, player_status.WIN)
        self.assertEqual(self.player2.status, player_status.LOSE)

    def test_decide_winner_by_health_player2_wins(self):
        self.player1.health = 300
        self.player2.health = 700
        winner, loser = self.battle._decide_winner_by_health()
        self.assertEqual(winner, self.player2)
        self.assertEqual(loser, self.player1)
        self.assertEqual(self.player2.status, player_status.WIN)
        self.assertEqual(self.player1.status, player_status.LOSE)

    def test_decide_winner_by_health_draw(self):
        self.player1.health = 500
        self.player2.health = 500
        winner, loser = self.battle._decide_winner_by_health()
        self.assertIsNone(winner)
        self.assertIsNone(loser)

    def test_decide_winner_by_health_updates_wins(self):
        self.player1.health = 800
        self.player2.health = 500
        self.battle._decide_winner_by_health()
        self.assertEqual(self.player1.wins, 1)
        self.assertEqual(self.player2.losses, 1)

    def test_restore_player(self):
        original_health = self.player1.health
        self.player1.health = 0
        self.battle._restore_player(self.player1, self.battle.player1_clone)
        self.assertEqual(self.player1.health, original_health)


if __name__ == "__main__":
    unittest.main()