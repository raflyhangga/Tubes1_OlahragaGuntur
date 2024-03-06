from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position, Properties
from typing import Optional, Tuple, List
from ..util import get_direction
import random, sys
import numpy as np

"""
TO-DO:
1. Pulang ke base terus ketemu teleporter jadi ngeloop
2. Evade dari bot yang mau nginjek
"""

class greedyGanteng(BaseLogic):
    def __init__(self) -> None:
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.current_position: Position = None

    def isInventoryFull(self,board_bot: GameObject) -> bool:
        # Check if the players inventory full
        return board_bot.properties.inventory_size == board_bot.properties.diamonds
    
    def roamAround(self,board:Board) -> Tuple[int,int]:
        random_idx = random.randint(0,3)
        return self.directions[random_idx]
    
    def getLength(self,pos1:Position) -> float:
        deltaX = abs(pos1.x - self.current_position.x)
        deltaY = abs(pos1.y - self.current_position.y)
        return (deltaX**2 + deltaY**2)**(1/2)
    
    def goToDiamond(self, board: Board,board_bot: GameObject) -> Tuple[int,int]:
        valid = True
        while(valid):
            existing_diamonds = board.diamonds
            nearest_diamond = min(existing_diamonds, key= lambda x : self.getLength(x.position))
            if(nearest_diamond.properties.points + board_bot.properties.diamonds > board_bot.properties.inventory_size):
                existing_diamonds = List(filter(lambda gana: nearest_diamond.id != gana.id,existing_diamonds))
                valid = False
            else:
                valid = True

        delta_x,delta_y = get_direction(
            self.current_position.x,
            self.current_position.y,
            nearest_diamond.position.x,
            nearest_diamond.position.y
        )
        return delta_x,delta_y

    def goToBase(self,board_bot: GameObject, board: Board) -> Tuple[int,int]:
        base = board_bot.properties.base
        self.goal_position = base
        delta_x, delta_y = get_direction(
                self.current_position.x,
                self.current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        return delta_x,delta_y

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        self.current_position = board_bot.position
        if not self.isInventoryFull(board_bot):
            return self.goToDiamond(board)
        else:
            return self.goToBase(board_bot,board)
        
class PricePerLength(greedyGanteng):
    def getPricePerLength(self,position:Position,gana:Properties) -> float:
        length = self.getLength(position)
        if(gana.points):
            return gana.points / length
        else:
            return sys.float_info.max
        

    def goToPPLDiamond(self) -> Tuple[int,int]:
        existing_diamonds = [diamond for diamond in self.current_board.diamonds if diamond.properties.points + self.player_bot.properties.diamonds <= self.player_bot.properties.inventory_size]
        print(len(existing_diamonds))
        nearest_diamond = max(existing_diamonds, key= lambda x : self.getPricePerLength(x.position,x.properties)) 

        delta_x,delta_y = get_direction(
            self.current_position.x,
            self.current_position.y,
            nearest_diamond.position.x,
            nearest_diamond.position.y
        )

        return delta_x,delta_y

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        self.current_position = board_bot.position
        self.player_bot = board_bot
        self.current_board = board

        bx,by = board_bot.properties.base.x, board_bot.properties.base.y
        base_pos = Position(by, bx)

        # If distance to home is super close and diamonds > 0, go home immedieately
        if self.player_bot.properties.diamonds > 1 and self.getLength(base_pos) < 2:
            return self.goToBase(board_bot, board)
        elif self.player_bot.properties.diamonds > 0 and self.getLength(base_pos) <= 1 :
            return self.gotBase(board_bot, board)


        # If time is 10 seconds or less, diamonds not empty, go home
        time_left = self.player_bot.properties.milliseconds_left // 1000
        if time_left < 10 and self.player_bot.properties.diamonds > 0:
            return self.goToBase(board_bot, board)


        if not self.isInventoryFull(board_bot):
            return self.goToPPLDiamond()
        else:
            return self.goToBase(board_bot,board)

