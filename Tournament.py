# tournament.py

from Match import Match
from random import shuffle


class Tournament:
    """Class to handle a knockout tournament with 8 players"""

    def __init__(self, players):
        if len(players) != 8:
            raise ValueError("Tournament requires exactly 8 players!")

        self.players = players
        self.rounds = []
        self.winner = None
        self.current_round = 0

    def start_tournament(self):
        """Start the tournament and simulate all matches"""
        print("\n" + "=" * 60)
        print("🏆 TOURNAMENT STARTED! 🏆")
        print("=" * 60)
        print(f"Participants: {', '.join([p.name for p in self.players])}")
        print("=" * 60 + "\n")

        # Shuffle players for randomness
        shuffle(self.players)

        # Quarter-finals (Round 1) - 4 matches
        print("🔴 ROUND 1: QUARTER-FINALS")
        print("-" * 60)
        quarter_final_winners = self._play_round(self.players, "Quarter-Final")

        # Semi-finals (Round 2) - 2 matches
        print("\n🔴 ROUND 2: SEMI-FINALS")
        print("-" * 60)
        semi_final_winners = self._play_round(quarter_final_winners, "Semi-Final")

        # Final (Round 3) - 1 match
        print("\n🔴 ROUND 3: FINAL")
        print("-" * 60)
        final_match = Match(semi_final_winners[0], semi_final_winners[1])
        self.winner, self.loser = final_match.play()

        # Announce champion
        self._announce_champion()

        return self.winner

    def _play_round(self, players, round_name):
        """Play a round of matches and return winners"""
        winners = []
        matches = []

        # Create and play matches
        for i in range(0, len(players), 2):
            match = Match(players[i], players[i + 1])
            matches.append(match)
            winner, loser = match.play()
            winners.append(winner)

        # Store round info
        self.rounds.append({
            'name': round_name,
            'matches': matches,
            'winners': winners
        })

        return winners

    def _announce_champion(self):
        """Announce the tournament winner"""
        print("\n" + "=" * 60)
        print("🏆 TOURNAMENT COMPLETED! 🏆")
        print("=" * 60)
        print(f"👑 CHAMPION: {self.winner.name} (ID: {self.winner.ID})")
        print(f"   Rating: {self.winner.rating}")
        print(f"   Wins: {self.winner.wins}")
        print("=" * 60 + "\n")

    def display_bracket(self):
        """Display the tournament bracket"""
        print("\n" + "=" * 60)
        print("📊 TOURNAMENT BRACKET")
        print("=" * 60)

        for round_info in self.rounds:
            print(f"\n{round_info['name']}:")
            for match in round_info['matches']:
                print(f"  {match}")

        if self.winner:
            print(f"\n🏆 Champion: {self.winner.name}")

    def get_winner(self):
        """Return the tournament winner"""
        return self.winner

    def get_all_matches(self):
        """Return all matches played in the tournament"""
        all_matches = []
        for round_info in self.rounds:
            all_matches.extend(round_info['matches'])
        return all_matches