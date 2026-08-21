from Player import Player
import Special_Event 
from Special_Event import special_event
import asyncio
import random

class battle_engine:
    def __init__(self,player1: Player,player2: Player):
        self.player1 = player1
        self.player2 = player2
    def start_battle(self):
        return(f"---Match starts {self.player1.name} VS {self.player2.name}---")
    async def game_round(self,number_of_rounds):
            round = 0
            while(round < number_of_rounds):
                print(f"Round {round} START: ")
                await asyncio.sleep(0.4)
                print(f"Player {self.player1.name} turn to attack:")
                await asyncio.sleep(0.5)
                event = self.special_event()
                self.special_event_message(event,self.player1)
                await asyncio.sleep(0.6)
                print(f"Player {self.player2.name} turn to attack:")
                await asyncio.sleep(0.5)
                event = self.special_event()
                self.special_event_message(event,self.player2)
    def special_event():
         return random.choices(list(Special_Event.weights.keys()),list(Special_Event.weights.values()))[0]
    def special_event_message(self, event, player: Player):
        if event != special_event.NO_EVENT:
            list_messages = [
                f"Special event happend: {event.value}, Such a lucky player!",
                f"<<{event.value}>> Wow! Special event for {player.name}",
                f"GOD is that even possible! <<{event.value}>>",
            ]
            message = random.choices(list_messages)[0]
            print(message)
            return message
        else:
            return None
              
         

    
 