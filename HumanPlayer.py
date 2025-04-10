from player import Player
from utils import get_int_input
class HumanPlayer(Player):
  def __init__(self, color):
    Player.__init__(self, color)
  def play(self, board):
    x = get_int_input("Enter X", 0, board.size)
    y = get_int_input("Enter Y", 0, board.size)
    possible = board.get_possible_moves()
    if (x, y) not in possible:
     return False
    return x, y