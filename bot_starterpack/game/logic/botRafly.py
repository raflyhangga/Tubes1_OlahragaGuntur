from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position
from typing import Optional, Tuple, List
from ..util import get_direction
import random


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
    
    def goToDiamond(self, board: Board) -> Tuple[int,int]:
        existing_diamond = board.diamonds
        nearest_diamond = min(existing_diamond, key= lambda x : self.getLength(x.position))
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