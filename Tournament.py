from Battle_Engine import battle_engine
from random import shuffle


class Tournament:
    def __init__(self, players):
        if len(players) != 8:
            raise ValueError("Tournament requires exactly 8 players!")
        self.players = players
        self.rounds = []
        self.winner = None
        self.loser = None
        self.current_round = 0

    def start_tournament(self):
        print("\n" + "=" * 60)
        print("🏆 TOURNAMENT STARTED! 🏆")
        print("=" * 60)
        print(f"Participants: {', '.join([p.name for p in self.players])}")
        print("=" * 60 + "\n")

        shuffle(self.players)

        print("🔴 ROUND 1: QUARTER-FINALS")
        print("-" * 60)
        quarter_final_winners = self._play_round(self.players, "Quarter-Final")

        print("\n🔴 ROUND 2: SEMI-FINALS")
        print("-" * 60)
        semi_final_winners = self._play_round(quarter_final_winners, "Semi-Final")

        print("\n🔴 ROUND 3: FINAL")
        print("-" * 60)
        final_battle = battle_engine(semi_final_winners[0], semi_final_winners[1])
        self.winner, self.loser = final_battle(3)

        self._announce_champion()
        return self.winner

    def _play_round(self, players, round_name):
        winners = []
        battles = []

        for i in range(0, len(players), 2):
            battle = battle_engine(players[i], players[i + 1])
            battles.append(battle)
            winner, loser = battle(3)
            winners.append(winner)

        self.rounds.append({"name": round_name, "battles": battles, "winners": winners})

        return winners

    def _announce_champion(self):
        print("\n" + "=" * 60)
        print("🏆 TOURNAMENT COMPLETED! 🏆")
        print("=" * 60)
        print(f"👑 CHAMPION: {self.winner.name} (ID: {self.winner.ID})")
        print(f"   Rating: {self.winner.rating}")
        print(f"   Wins: {self.winner.wins}")
        print("=" * 60 + "\n")

    def display_bracket(self):
        print("\n" + "=" * 60)
        print("📊 TOURNAMENT BRACKET")
        print("=" * 60)

        for round_info in self.rounds:
            print(f"\n{round_info['name']}:")
            for battle in round_info["battles"]:
                print(f"  ⚔️  {battle.player1.name} VS {battle.player2.name}")

        if self.winner:
            print(f"\n🏆 Champion: {self.winner.name}")

    def get_winner(self):
        return self.winner

    def get_all_battles(self):
        all_battles = []
        for round_info in self.rounds:
            all_battles.extend(round_info["battles"])
        return all_battles
