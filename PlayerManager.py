# player_manager.py

from Player import Player


class PlayerManager:
    def __init__(self):
        self.players = []

    def add_player(self, player):
        """Add a player to the manager"""
        if not isinstance(player, Player):
            raise TypeError("Only Player objects can be added")
        self.players.append(player)
        print(f"✅ Player '{player.name}' added successfully! (ID: {player.ID})")

    def remove_player(self, player_id):
        """Remove a player by ID"""
        for i, player in enumerate(self.players):
            if player.ID == player_id:
                removed = self.players.pop(i)
                print(
                    f"✅ Player '{removed.name}' (ID: {player_id}) removed successfully!"
                )
                return True
        print(f"❌ Player with ID {player_id} not found.")
        return False

    def search_player(self, player_id):
        """Search for a player by ID"""
        for player in self.players:
            if player.ID == player_id:
                return player
        return None

    def get_all_players(self):
        """Display all players"""
        if not self.players:
            print("❌ No players found.")
            return

        print("\n" + "=" * 50)
        print(f"📋 Total Players: {len(self.players)}")
        print("=" * 50)
        for player in self.players:
            print(player)
            print("-" * 50)

    def get_top_players(self, count=5):
        """Get top players by wins"""
        if not self.players:
            print("❌ No players found.")
            return []

        sorted_players = sorted(self.players, key=lambda p: p.wins, reverse=True)
        top = sorted_players[:count]

        print("\n" + "=" * 50)
        print(f"🏆 Top {len(top)} Players by Wins")
        print("=" * 50)
        for i, player in enumerate(top, 1):
            print(f"{i}. {player.name} (ID: {player.ID}) - Wins: {player.wins}")

        return top

    def get_player_stats(self, player_id):
        """Get detailed stats for a specific player"""
        player = self.search_player(player_id)
        if player:
            print("\n📊 Player Statistics")
            print("=" * 50)
            print(player)
            return player
        else:
            print(f"❌ Player with ID {player_id} not found.")
            return None
