from player import Player
from random import choice

class RandomPlayer(Player):
  def __init__(self, color):
    Player.__init__(self, color)
  def play(self, board):
    possible = board.get_possible_moves()
    move = choice(possible)
    return move