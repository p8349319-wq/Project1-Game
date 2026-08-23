# match.py

from random import randint


class Match:
    """Class to handle a match between two players"""

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        self.loser = None
        self.is_played = False

    def play(self):
        """Simulate a match between two players"""
        if self.is_played:
            print("⚠️ This match has already been played!")
            return

        # Calculate scores based on player stats
        score1 = self._calculate_score(self.player1)
        score2 = self._calculate_score(self.player2)

        # Determine winner
        if score1 > score2:
            self.winner = self.player1
            self.loser = self.player2
        elif score2 > score1:
            self.winner = self.player2
            self.loser = self.player1
        else:
            # In case of tie, use luck factor
            if self.player1.luck > self.player2.luck:
                self.winner = self.player1
                self.loser = self.player2
            else:
                self.winner = self.player2
                self.loser = self.player1

        # Update player stats
        self.winner.wins += 1
        self.loser.losses += 1
        self.is_played = True

        print(f"⚔️ Match: {self.player1.name} vs {self.player2.name}")
        print(f"   Score: {score1} - {score2}")
        print(f"   🏆 Winner: {self.winner.name}!\n")

        return self.winner, self.loser

    def _calculate_score(self, player):
        """Calculate a player's score based on their stats"""
        # Random factor adds unpredictability
        random_factor = randint(0, 20)
        return (
            player.attack * 0.3
            + player.defense * 0.3
            + player.speed * 0.2
            + player.rating * 0.2
            + random_factor
        )

    def __str__(self):
        if self.is_played:
            return f"Match: {self.player1.name} vs {self.player2.name} -> Winner: {self.winner.name}"
        else:
            return f"Match: {self.player1.name} vs {self.player2.name} (Not played yet)"
