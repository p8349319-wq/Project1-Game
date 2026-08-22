# main.py

from PlayerManager import PlayerManager
from Player import Player
from Tournament import Tournament
from Player import InvalidNameError


def show_menu():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("🎮 WELCOME TO THE GAME")
    print("=" * 50)
    print("1. Create a new player")
    print("2. Show all players")
    print("3. Search player by ID")
    print("4. Remove player by ID")
    print("5. Show top players by wins")
    print("6. Start tournament (8 players)")
    print("7. Exit")
    print("=" * 50)


def create_player(manager):
    """Handle player creation with proper error handling"""
    try:
        name = input("Enter your name (English letters only): ").strip()
        player = Player(name)
        manager.add_player(player)
    except InvalidNameError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


def search_player(manager):
    """Handle player search"""
    try:
        player_id = int(input("Enter player ID to search: "))
        player = manager.search_player(player_id)
        if player:
            print("\n✅ Player found:")
            print("=" * 50)
            print(player)
        else:
            print(f"❌ Player with ID {player_id} not found.")
    except ValueError:
        print("❌ Invalid ID. Please enter a number.")


def remove_player(manager):
    """Handle player removal"""
    try:
        player_id = int(input("Enter player ID to remove: "))
        manager.remove_player(player_id)
    except ValueError:
        print("❌ Invalid ID. Please enter a number.")


def start_tournament(manager):
    """Start a tournament with 8 players"""
    players = manager.players

    if len(players) < 8:
        print(f"❌ Not enough players! Need 8 players, but only have {len(players)}.")
        print(f"   Please create {8 - len(players)} more player(s).")
        return

    if len(players) > 8:
        print(f"⚠️ You have {len(players)} players. Using first 8 for the tournament.")
        selected_players = players[:8]
    else:
        selected_players = players

    try:
        tournament = Tournament(selected_players)
        champion = tournament.start_tournament()
        tournament.display_bracket()

        print("\n🎉 Tournament completed successfully!")
        print(f"🏆 Champion: {champion.name} with {champion.wins} wins!")

    except Exception as e:
        print(f"❌ Tournament error: {e}")


def main():
    """Main program loop with match-case"""
    manager = PlayerManager()
    running = True

    while running:
        show_menu()

        try:
            choice = int(input("Enter your choice (1-7): ").strip())
        except ValueError:
            print("❌ Invalid input. Please enter a number between 1 and 7.")
            continue

        match choice:
            case 1:
                create_player(manager)

            case 2:
                manager.get_all_players()

            case 3:
                search_player(manager)

            case 4:
                remove_player(manager)

            case 5:
                manager.get_top_players()

            case 6:
                start_tournament(manager)

            case 7:
                print("\n👋 Goodbye! Thanks for playing!")
                running = False

            case _:
                print("❌ Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
