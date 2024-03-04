from typing import Tuple
from game.logic.base import BaseLogic
from game.models import GameObject, Board
from math import dist

class NaiveAvoidBots(BaseLogic) :

    def movedir(self, dx,dy) :
        if dx : return ((1,0) if dx > 0 else (-1,0))
        return ((0,1) if dy > 0 else (0,-1))

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        
        # Get info
        x,y = board_bot.position.x, board_bot.position.y
        bots,diamonds = board.bots,board.diamonds
        bx,by = board_bot.properties.base.x, board_bot.properties.base.y
        bots = [b for b in bots if (b.id != board_bot.id)]

        print("Diamonds: ", board_bot.properties.diamonds)
        print("Distance from bots: ")
        for b in bots :
            print(f"bot-{b.id}: ", dist((b.position.x,b.position.y), (x,y)))


        # If home is really close (and I have diamonds), go home!
        if (dist((bx,by), (x,y)) <= 1) and (board_bot.properties.diamonds > 0):
            dx, dy = board_bot.properties.base.x - board_bot.position.x, board_bot.properties.base.y - board_bot.position.y
            print("Force go home, dist = ", dist((bx,by),(x,y)))
            return self.movedir(dx,dy)

        # Bot avoid guard
        pa,pb = 10**9,10**9
        for b in bots :
            if dist((pa,pb),(x,y)) > dist((b.position.x,b.position.y),(x,y)):
                pa, pb = b.position.x, b.position.y
        if dist((pa,pb),(x,y)) <= 3 :
            print("Evade from: ", pa, pb)
            dx,dy = pa - x, pb - y       
            dx,dy = self.movedir(-dx, -dy)
            # Suren
            if x + dx >= 15 :
                return (-1,0)
            elif x + dx < 0 :
                return (1,0)
            elif y + dy >= 15 :
                return (0,-1)
            elif y + dy < 0 :
                return (0,1)
            else :
                return (dx,dy)
        
        # Return home
        if board_bot.properties.diamonds + 1 >= board_bot.properties.inventory_size:
            print("Going home...")
            dx,dy = board_bot.properties.base.x - board_bot.position.x, board_bot.properties.base.y - board_bot.position.y
            return self.movedir(dx,dy)

        else:
            print("Finding nearest diamond...")
            nearest = min(diamonds, key=lambda d : dist((d.position.x,d.position.y),(x,y)))
            dx,dy = nearest.position.x - x, nearest.position.y - y
            return self.movedir(dx,dy)
