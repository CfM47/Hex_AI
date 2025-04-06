from builtins import float
from random import choice
from typing import Callable

from base_player import Player
from board import HexBoard


class AiPlayer(Player):
  def __init__(self, player_id: int, heuristic: Callable[[HexBoard, int], float]):
    super().__init__(player_id)
    self.heuristic = heuristic
  def play(self, board: HexBoard) -> tuple:
    min_max = MinMax(2, self.heuristic)
    return min_max.alpha_beta_search(board, self.player_id)

class MinMax:
  """
  min max with ab-prune
  """
  def __init__(self, max_depth, heuristic: Callable[[HexBoard, int], float]):
    self.max_depth = max_depth
    self.heuristic = heuristic
    self.depth = 0

  @staticmethod
  def is_terminal(board: HexBoard) -> int:
    return board.check_connection(1) or board.check_connection(2)

  def utility(self, board: HexBoard, player_id: int) -> float:
    return self.heuristic(board, player_id)
    # opponent = get_opponent_id(player_id)
    # if board.check_connection(opponent):
    #   return 0
    # elif board.check_connection(player_id):
    #   return 1
    # else:
    #   return 0.5

  def alpha_beta_search(self, board: HexBoard, player_id: int) -> tuple:
    value, move = self.max_value(board, player_id, -float('inf'), float('inf'))
    return move

  def max_value(self, board: HexBoard, player_id: int, alpha: float, beta: float) -> (int, tuple):
    if MinMax.is_terminal(board) or self.depth >= self.max_depth:
      return self.utility(board, player_id), None

    value = -float('inf')
    move = None
    possible_moves = board.get_possible_moves()
    while len(possible_moves) > 0:
      move = pick_random(possible_moves)
      row, col = move

      board2 = board.clone()
      board2.place_piece(row, col, player_id)
      opponent = get_opponent_id(player_id)

      self.depth += 1
      value2, action2 = self.min_value(board2, opponent, alpha, beta)
      self.depth -= 1

      if value2 > value:
        value, move = value2, (row, col)
        alpha = max(alpha, value)
      if value >= beta:
        return value, move
    return value, move

  def min_value(self, board: HexBoard, player_id: int, alpha: float, beta: float) -> (int, tuple):
    if MinMax.is_terminal(board) or self.depth >= self.max_depth:
      return self.utility(board, player_id), None

    value = float('inf')
    move = None
    possible_moves = board.get_possible_moves()
    while len(possible_moves) > 0:
      move = pick_random(possible_moves)
      row, col = move

      board2 = board.clone()
      board2.place_piece(row, col, player_id)
      opponent = get_opponent_id(player_id)

      self.depth += 1
      value2, action2 = self.max_value(board2, opponent, alpha, beta)
      self.depth -= 1

      if value2 < value:
        value, move = value2, (row, col)
        beta = min(beta, value)
      if value <= beta:
        return value, move
    return value, move

# heuristics
def max_island_size_heuristic(state: HexBoard, player_id: int) -> float:
  cells = [(i,j) for i in range(state.size) for j in range(state.size)]
  dsu = [None, DisjointSet(cells), DisjointSet(cells)]
  for row in range(state.size):
    for col in range(state.size):
      neighbors = get_neighbors(state.size, row, col)
      color = state.board[row][col]
      for r, c in neighbors:
        if color != 0 and state.board[r][c] == color:
          dsu[color].union((row, col), (r, c))

  maximum_size = [.0, -float('inf'), float('inf')]
  for cell in cells:
    row, col = cell
    color = state.board[row][col]
    if color != 0:
      maximum_size[color] = max(maximum_size[color], dsu[color].size[cell])

  opponent = get_opponent_id(player_id)
  return (maximum_size[player_id] - maximum_size[opponent]) / state.size

# utils-----------------------------------

def get_opponent_id(player_id: int) -> int:
  return (player_id % 2) + 1


def pick_random(seq: list):
  item = choice(seq)
  seq.remove(item)
  return item

# disjoint-set may be useful to heuristics
class DisjointSet:
  def __init__(self, elems):
    self.elems = elems
    self.parent = {}
    self.rank = {}
    self.size = {}
    self.max_size = 0
    for x in elems:
      self.make_set(x)

  def make_set(self, x):
    self.parent[x] = x
    self.rank[x] = 0
    self.size[x] = 1
    self.max_size = 1

  def union(self, x, y):
    root_x = self.find_set(x)
    root_y = self.find_set(y)
    self.link(root_x, root_y)

  def link(self, x, y):
    if self.rank[x] > self.rank[y]:
      self.parent[y] = x
      self.size[x] += self.size[y]
      self.max_size = max(self.max_size, self.size[x])
    else:
      self.parent[x] = y
      self.size[y] += self.size[x]
      self.max_size = max(self.max_size, self.size[y])
    if self.rank[x] == self.rank[y]:
      self.rank[y] += 1

  def find_set(self, x):
    if x != self.parent[x]:
      self.parent[x] = self.find_set(self.parent[x])
      return self.parent[x]
    return x


def get_neighbors(size: int, row: int, col: int) -> list[tuple[int, int]]:
  if row % 2 == 0:
    # Para filas pares (i par):
    # (i, j - 1) → Izquierda
    # (i, j + 1) → Derecha
    # (i - 1, j) → Arriba
    # (i + 1, j) → Abajo
    # (i - 1, j + 1) → Arriba-Derecha
    # (i + 1, j + 1) → Abajo-Derecha
    dr = [0, 0, -1, 1, -1, 1]
    dc = [-1, 1, 0, 0, 1, 1]
  else:
    # Para filas impares (i impar):
    # (i, j - 1) → Izquierda
    # (i, j + 1) → Derecha
    # (i - 1, j) → Arriba
    # (i + 1, j) → Abajo
    # (i - 1, j - 1) → Arriba-Izquierda
    # (i + 1, j - 1) → Abajo-Izquierda
    dr = [0, 0, -1, 1, -1, 1]
    dc = [-1, 1, 0, 0, -1, -1]

  result: list[tuple[int, int]] = []
  for i in range(6):
    ri = row + dr[i]
    ci = col + dc[i]
    r_ok = 0 <= ri < size
    c_ok = 0 <= ci < size
    if r_ok and c_ok:
      result.append((ri, ci))
  return result