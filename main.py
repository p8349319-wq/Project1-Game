# main.py

from PlayerManager import PlayerManager
from Player import Player
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
    print("6. Exit")
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


def main():
    """Main program loop with match-case"""
    manager = PlayerManager()
    running = True

    while running:
        show_menu()

        try:
            choice = int(input("Enter your choice (1-6): ").strip())
        except ValueError:
            print("❌ Invalid input. Please enter a number between 1 and 6.")
            continue

        # استفاده از match-case (نیاز به پایتون 3.10+)
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
                print("\n👋 Goodbye! Thanks for playing!")
                running = False

            case _:
                print("❌ Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()