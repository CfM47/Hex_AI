from random import choice

from base_player import Player
from board import HexBoard


class AiPlayer(Player):
  def __init__(self, player_id: int):
    super().__init__(player_id)
  def play(self, board: HexBoard) -> tuple:
    min_max = MinMax(2)
    return min_max.minimax_search(board, self.player_id)

def get_opponent_id(player_id: int) -> int:
  return (player_id % 2) + 1

class MinMax:
  def __init__(self, max_depth):
    self.max_depth = max_depth
    self.depth = 0

  @staticmethod
  def is_terminal(board: HexBoard) -> int:
    return board.check_connection(1) or board.check_connection(2)

  @staticmethod
  def utility(board: HexBoard, player_id) -> int | float:
    opponent = get_opponent_id(player_id)
    if board.check_connection(opponent):
      return 0
    elif board.check_connection(player_id):
      return 1
    else:
      return 0.5

  def minimax_search(self, board: HexBoard, player_id: int) -> tuple:
    value, move = self.max_value(board, player_id)
    return move

  def max_value(self, board: HexBoard, player_id: int) -> (int, tuple):
    if MinMax.is_terminal(board) or self.depth >= self.max_depth:
      return MinMax.utility(board, player_id), None
    value = -float('inf')
    move = None
    possible_moves = board.get_possible_moves()
    while len(possible_moves) > 0:
      move = choice(possible_moves)
      possible_moves.remove(move)
      row, col = move
      board2 = board.clone()
      board2.place_piece(row, col, player_id)
      opponent = get_opponent_id(player_id)
      self.depth += 1
      value2, action2 = self.min_value(board2, opponent)
      self.depth -= 1
      if value2 > value:
        value, move = value2, (row, col)
    return value, move

  def min_value(self, board: HexBoard, player_id: int) -> (int, tuple):
    if MinMax.is_terminal(board) or self.depth >= self.max_depth:
      return MinMax.utility(board, player_id), None
    value = float('inf')
    move = None
    possible_moves = board.get_possible_moves()
    while len(possible_moves) > 0:
      move = choice(possible_moves)
      possible_moves.remove(move)
      row, col = move
      board2 = board.clone()
      board2.place_piece(row, col, player_id)
      opponent = get_opponent_id(player_id)
      self.depth += 1
      value2, action2 = self.max_value(board2, opponent)
      self.depth -= 1
      if value2 < value:
        value, move = value2, (row, col)
    return value, move