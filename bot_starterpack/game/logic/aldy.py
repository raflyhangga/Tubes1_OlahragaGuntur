from typing import Tuple
from game.logic.base import BaseLogic
from game.models import GameObject, Board
from queue import Queue
from math import dist

class AldyDPP(BaseLogic) :
    def __init__(self) :
        self.movequeue = Queue()
    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        if not self.movequeue.empty() :
            return self.movequeue.get()
        elif board_bot.properties.inventory_size == board_bot.properties.diamonds :
            dx,dy = board_bot.properties.base.x - board_bot.position.x, board_bot.properties.base.y - board_bot.position.y
            if dx : return ((1,0) if dx > 0 else (-1,0))
            return ((0,1) if dy > 0 else (0,-1))
        else:
            x,y = board_bot.position.x, board_bot.position.y
            bots,diamonds = board.bots,board.diamonds
            nearest = min(diamonds, key=lambda d : dist((d.position.x,d.position.y),(x,y)))
            dx,dy = nearest.position.x - x, nearest.position.y - y
            if dx : return ((1,0) if dx > 0 else (-1,0))
            return ((0,1) if dy > 0 else (0,-1))