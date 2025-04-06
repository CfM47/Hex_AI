from base_player import Player
from board import HexBoard


class AiPlayer(Player):
  def __init__(self, player_id: int):
    super().__init__(player_id)
  def play(self, board: HexBoard) -> tuple:
    return MinMax.minimax_search(board, self.player_id)

def get_opponent_id(player_id: int) -> int:
  return (player_id % 2) + 1

class MinMax:
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

  @staticmethod
  def minimax_search(board: HexBoard, player_id: int, max_depth=5, depth = 0) -> tuple:
    value, move = MinMax.max_value(board, player_id, max_depth, depth)
    return move

  @staticmethod
  def max_value(board: HexBoard, player_id: int, max_depth=2, depth = 0) -> (int, tuple):
    print(depth)
    if MinMax.is_terminal(board) or depth >= max_depth:
      return MinMax.utility(board, player_id), None
    value = -float('inf')
    move = None
    possible_moves = board.get_possible_moves()
    for row, col in possible_moves:
      board2 = board.clone()
      board2.place_piece(row, col, player_id)
      opponent = get_opponent_id(player_id)
      value2, action2 = MinMax.min_value(board2, opponent, max_depth, depth + 1)
      if value2 > value:
        value, move = value2, (row, col)
    return value, move

  @staticmethod
  def min_value(board: HexBoard, player_id: int, max_depth = 2, depth = 0) -> (int, tuple):
    if MinMax.is_terminal(board) or depth >= max_depth:
      return MinMax.utility(board, player_id), None
    value = float('inf')
    move = None
    possible_moves = board.get_possible_moves()
    for row, col in possible_moves:
      board2 = board.clone()
      board2.place_piece(row, col, player_id)
      opponent = get_opponent_id(player_id)
      value2, action2 = MinMax.max_value(board2, opponent, max_depth, depth + 1)
      if value2 < value:
        value, move = value2, (row, col)
    return value, move