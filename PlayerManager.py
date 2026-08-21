class PlayerManager:
    def __init__(self):
        self.players = []

    def add_Player(self, player):
        self.players.append(player)
        print(f"Added player {player.name}")

    def remove_Player(self, Player_ID):
        for player in self.players:
            if player.ID == Player_ID:
                self.players.remove(player)
                print(f"Removed player {Player_ID}")
                return
        print("Player not found")

    def search_Player(self, Player_ID):
        for player in self.players:
            if player.ID == Player_ID:
                return player
        return None

    def get_Players(self):
        if not self.players:
            self.players = []
            return
        else:
            for player in self.players:
                print(player)

    def top_players(self):
        if not self.players:
            return []
        else:
            return sorted(self.players, key=lambda player: player.wins, reverse= True)

