from Player import Player
import Enum_classes
from Enum_classes import special_event
from Enum_classes import player_status
import asyncio
import random
import copy
from os import urandom


class battle_engine:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.player1_clone = copy.copy(player1)
        self.player2_clone = copy.copy(player2)

    def _restore_player(self, player: Player, clone: Player):
        player.health = clone.health
        player.attack = clone.attack
        player.defense = clone.defense
        player.speed = clone.speed
        player.luck = clone.luck

    def start_battle(self):
        self.player1.status = player_status.IN_MATCH
        self.player2.status = player_status.IN_MATCH
        return f"⚔️  ---Match starts {self.player1.name} VS {self.player2.name}--- ⚔️"

    def special_event(self, player: Player):
        player_weights = Enum_classes.calculate_special_events_weight(
            Enum_classes.weights, player
        )
        return random.choices(
            list(player_weights.keys()), list(player_weights.values())
        )[0]

    def special_event_message(self, attack_event, defense_event, attacker: Player, defender: Player):
        messages = []

        if attack_event not in [special_event.NO_EVENT, special_event.DEFENSE]:
            attack_messages = [
                f"⚡ <<{attack_event.value}>> Wow! Special event for {attacker.name}!",
                f"😱 GOD is that even possible! <<{attack_event.value}>> for {attacker.name}!",
                f"🌟 Special event happened: {attack_event.value}, Such a lucky player!",
            ]
            messages.append(random.choices(attack_messages)[0])

        if defense_event == special_event.DEFENSE:
            defense_messages = [
                f"🛡️  But wait! {defender.name} activates <<{defense_event.value}>>!",
                f"💪 Not so fast! {defender.name} counters with <<{defense_event.value}>>!",
                f"✨ Incredible! {defender.name} responds with {defense_event.value}!",
            ]
            messages.append(random.choices(defense_messages)[0])

        if (
            attack_event not in [special_event.NO_EVENT, special_event.DEFENSE]
            and defense_event == special_event.DEFENSE
        ):
            combined = [
                f"🔥 INSANE ROUND! {attacker.name} unleashes <<{attack_event.value}>> but {defender.name} counters with <<{defense_event.value}>>!",
                f"💥 CLASH OF EVENTS! <<{attack_event.value}>> VS <<{defense_event.value}>>! Who will win?",
                f"🌪️  DOUBLE EVENT! {attacker.name} with <<{attack_event.value}>> meets {defender.name}'s <<{defense_event.value}>>!",
            ]
            return random.choices(combined)[0]

        if messages:
            return messages[0]
        return None

    def player_attack(self, attacker: Player, event):
        speed = attacker.speed
        attack = attacker.attack
        if event == special_event.ATTACK:
            n = 2
        elif event == special_event.EXTRA_Attack:
            attack *= 2
            n = 1.5
        elif event == special_event.SPEED:
            speed = attacker.speed * 1.05
            n = 1.5
        else:
            n = 1.5
        damage = (n * attack * speed) / 14
        return damage

    def player_defense(self, defender: Player, event):
        defense_value = defender.defense
        if event == special_event.DEFENSE:
            defense_value *= 1.5
        defense = defense_value * 0.5
        return defense

    def apply_damage(self, attacker: Player, defender: Player, attacker_event, defender_event):
        attack = self.player_attack(attacker, attacker_event)
        defense = self.player_defense(defender, defender_event)
        damage_taken = attack - defense
        if damage_taken < 0:
            damage_taken = 0
        defender.health -= damage_taken
        return damage_taken

    def check_game_winner(self):
        if self.player1.health <= 0:
            self.player2.status = player_status.WIN
            self.player1.status = player_status.LOSE
            self._restore_player(self.player1, self.player1_clone)
            self._restore_player(self.player2, self.player2_clone)
            self.player2.wins += 1
            self.player1.losses += 1
            return (
                f"💀 {self.player1.name} has no health left! 🏆 {self.player2.name} WINS!",
                self.player2,
                self.player1,
            )
        elif self.player2.health <= 0:
            self.player2.status = player_status.LOSE
            self.player1.status = player_status.WIN
            self._restore_player(self.player1, self.player1_clone)
            self._restore_player(self.player2, self.player2_clone)
            self.player1.wins += 1
            self.player2.losses += 1
            return (
                f"💀 {self.player2.name} has no health left! 🏆 {self.player1.name} WINS!",
                self.player1,
                self.player2,
            )
        else:
            return None, None, None

    def _decide_winner_by_health(self):
        if self.player1.health > self.player2.health:
            self.player1.status = player_status.WIN
            self.player2.status = player_status.LOSE
            self._restore_player(self.player1, self.player1_clone)
            self._restore_player(self.player2, self.player2_clone)
            self.player1.wins += 1
            self.player2.losses += 1
            print(f"\n🏆 {self.player1.name} wins with more health remaining!")
            return self.player1, self.player2
        elif self.player2.health > self.player1.health:
            self.player2.status = player_status.WIN
            self.player1.status = player_status.LOSE
            self._restore_player(self.player1, self.player1_clone)
            self._restore_player(self.player2, self.player2_clone)
            self.player2.wins += 1
            self.player1.losses += 1
            print(f"\n🏆 {self.player2.name} wins with more health remaining!")
            return self.player2, self.player1
        else:
            return None, None

    async def game_round(self, number_of_rounds):
        round = 0
        while round < number_of_rounds:
            print(f"\n🔔 ========== Round {round + 1} START ========== 🔔")
            await asyncio.sleep(1.0)

            print(f"\n⚔️  {self.player1.name}'s turn to attack!")
            await asyncio.sleep(0.8)
            attack_event = self.special_event(self.player1)
            defense_event = self.special_event(self.player2)
            message = self.special_event_message(
                attack_event, defense_event, self.player1, self.player2
            )
            if message:
                print(message)
                await asyncio.sleep(1.2)
            damage = self.apply_damage(
                self.player1, self.player2, attack_event, defense_event
            )
            print(
                f"💢 {self.player1.name} deals {damage:.1f} damage! {self.player2.name} has {self.player2.health:.1f} HP left! ❤️"
            )
            await asyncio.sleep(1.0)

            win_message, winner, loser = self.check_game_winner()
            if win_message:
                print(f"\n{win_message}")
                return winner, loser

            print(f"\n⚔️  {self.player2.name}'s turn to attack!")
            await asyncio.sleep(0.8)
            attack_event = self.special_event(self.player2)
            defense_event = self.special_event(self.player1)
            message = self.special_event_message(
                attack_event, defense_event, self.player2, self.player1
            )
            if message:
                print(message)
                await asyncio.sleep(1.2)
            damage = self.apply_damage(
                self.player2, self.player1, attack_event, defense_event
            )
            print(
                f"💢 {self.player2.name} deals {damage:.1f} damage! {self.player1.name} has {self.player1.health:.1f} HP left! ❤️"
            )
            await asyncio.sleep(1.0)

            win_message, winner, loser = self.check_game_winner()
            if win_message:
                print(f"\n{win_message}")
                return winner, loser

            round += 1

        # Rounds finished - decide by health!
        print("\n📊 Rounds finished! Health remaining:")
        print(f"   {self.player1.name}: {self.player1.health:.1f} HP")
        print(f"   {self.player2.name}: {self.player2.health:.1f} HP")

        winner, loser = self._decide_winner_by_health()

        if winner:
            return winner, loser

        # Exact same health - rematch!
        self._restore_player(self.player1, self.player1_clone)
        self._restore_player(self.player2, self.player2_clone)
        print("\n🤝 Same health! It's a DRAW! 🤝")
        print("⚔️  Rematch to define the winner!")
        random.seed(urandom(16))
        rematch_battle = battle_engine(self.player1, self.player2)
        print(rematch_battle.start_battle())
        return await rematch_battle.game_round(3)

    def process(self, rounds: int):
        print(self.start_battle())
        return asyncio.run(self.game_round(rounds))

    def __call__(self, rounds: int):
        return self.process(rounds)