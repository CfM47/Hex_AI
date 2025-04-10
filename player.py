from builtins import float
from collections import deque
from random import choice
from board import HexBoard


class Player:
  def __init__(self, player_id: int):
    self.player_id = player_id  # Tu identificador (1 o 2)

  def play(self, board: HexBoard) -> tuple:
    raise NotImplementedError("¡Implementa este método!")

class AiPlayer(Player):
  def __init__(self, player_id: int,):
    super().__init__(player_id)
  def play(self, board: HexBoard) -> tuple:
    min_max = MinMax()
    return min_max.alpha_beta_search(board, self.player_id)

class MinMax:
  """
  min max with ab-prune
  """
  def __init__(self):
    # BONIATO --label to quickly search adjustment lines for my agent
    self.max_depth = 1 # for some reason depth 1 works the best XD
    self.depth = 0

  @staticmethod
  def is_terminal(board: HexBoard) -> bool:
    return board.check_connection(1) or board.check_connection(2)

  @staticmethod
  def utility(board: HexBoard, player_id: int) -> float:
    # BONIATO --label to quickly search adjustment lines for my agent
    total_size = board.size ** 2
    if board.check_connection(player_id):
      return total_size**2 + 100
    if board.check_connection(2):
      return -total_size**2 - 100
    # moves_left = len(board.get_possible_moves())
    # if moves_left >= board.size * 0.80:
    #   heuristics = [big_island_size_heuristic, bridges_heuristic]
    #   weights = [0.2, 0.8]
    # if moves_left >= board.size * 0.50:
    #   heuristics = [max_island_size_heuristic, bridges_heuristic, moves_needed_heuristic]
    #   weights = [0.2, 0.4, 0.4]
    # else:
    #   heuristics = [big_island_size_heuristic, bridges_heuristic, moves_needed_heuristic]
    #   weights = [0.2, 0.3, 0.5]
    # if moves_left <= board.size * 0.15:
    #   heuristics = [max_island_size_heuristic, moves_needed_heuristic]
    #   weights = [0.3, 0.7]
    heuristics = [moves_needed_heuristic, bridges_heuristic]
    weights = [1, 0.5]
    value = 0
    for i in range(len(heuristics)):
      value += weights[i] * heuristics[i](board, player_id)
    return value

  def alpha_beta_search(self, board: HexBoard, player_id: int) -> tuple:
    possible_moves = board.get_possible_moves()
    if self.max_depth == 0:
      return choice(possible_moves)
    # if len(possible_moves) <= 20:
    #   self.max_depth = 3
    value, move = self.max_value(board, player_id, -float('inf'), float('inf'))
    return move

  def max_value(self, board: HexBoard, player_id: int, alpha: float, beta: float) -> (int, tuple):
    if MinMax.is_terminal(board) or self.depth >= self.max_depth:
      return self.utility(board, get_opponent_id(player_id)), None

    value = -float('inf')
    move = None
    possible_moves = board.get_possible_moves()
    if len(possible_moves) <= 20:
      self.max_depth = 3
    while len(possible_moves) > 0:
      row, col = pick_random(possible_moves)

      opponent = get_opponent_id(player_id)

      board.board[row][col] = player_id
      self.depth += 1
      value2, action2 = self.min_value(board, opponent, alpha, beta)
      self.depth -= 1
      board.board[row][col] = 0

      if value2 > value:
        value, move = value2, (row, col)
        alpha = max(alpha, value)
      if value >= beta:
        break
    return value, move

  def min_value(self, board: HexBoard, player_id: int, alpha: float, beta: float) -> (int, tuple):
    if MinMax.is_terminal(board) or self.depth >= self.max_depth:
      return self.utility(board, get_opponent_id(player_id)), None

    value = float('inf')
    move = None
    possible_moves = board.get_possible_moves()
    while len(possible_moves) > 0:
      row, col = pick_random(possible_moves)

      opponent = get_opponent_id(player_id)

      board.board[row][col] = player_id
      self.depth += 1
      value2, action2 = self.max_value(board, opponent, alpha, beta)
      self.depth -= 1
      board.board[row][col] = 0

      if value2 < value:
        value, move = value2, (row, col)
        beta = min(beta, value)
      if value <= beta:
        break
    return value, move

# heuristics
def max_island_size_heuristic(state: HexBoard, player_id: int) -> float:
  dsu = get_islands_info(state)
  maximum_size = [.0, -float('inf'), -float('inf')]
  cells = [(i, j) for i in range(state.size) for j in range(state.size)]
  for cell in cells:
    row, col = cell
    color = state.board[row][col]
    if color != 0:
      maximum_size[color] = max(maximum_size[color], dsu[color].size[cell])

  opponent = get_opponent_id(player_id)
  return (maximum_size[player_id] - maximum_size[opponent]) / state.size

def big_island_size_heuristic(state: HexBoard, player_id: int) -> float:
  dsu = get_islands_info(state)
  total_size = [0, 0, 0]
  cells = [(i, j) for i in range(state.size) for j in range(state.size)]
  for cell in cells:
    row, col = cell
    color = state.board[row][col]
    if color != 0 and dsu[color].size[cell] > 1:
      total_size[color] += dsu[color].size[cell]

  opponent = get_opponent_id(player_id)
  return (total_size[player_id] - total_size[opponent]) / state.size

def bridges_heuristic(state: HexBoard, player_id: int) -> float:
  # a heuristic that values moves that connect previously unconnected tokens
  cells = [(i, j) for i in range(state.size) for j in range(state.size)]

  # strong connections count
  bridges_count = [0, 0, 0]
  for row, col in cells:
    neighbors = get_neighbors(state.size, row, col, get_all=True)
    for i in range(len(neighbors)):
      r, c = neighbors[i]
      if not is_pos_ok(state.size,(r,c)):
        continue
      color = state.board[r][c]
      for di in [2, 3]:
        r2, c2 = neighbors[(i+di) % len(neighbors)]
        if is_pos_ok(state.size,(r2,c2)) and state.board[r2][c2] == color:
          bridges_count[color] += 1

  opponent = get_opponent_id(player_id)
  return bridges_count[player_id] - bridges_count[opponent]

def moves_needed_heuristic(state: HexBoard, player_id: int) -> float:
  opponent = get_opponent_id(player_id)
  min_moves_player = bfs(state, player_id)
  min_moves_opponent = bfs(state, opponent)
  return min_moves_opponent - 1.5 * min_moves_player

# utils-----------------------------------

def get_opponent_id(player_id: int) -> int:
  return (player_id % 2) + 1

def pick_random(seq: list):
  item = choice(seq)
  #item = seq[0]
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
    if root_x == root_y:
      return
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

def get_islands_info(state: HexBoard) -> list:
  cells = [(i, j) for i in range(state.size) for j in range(state.size)]
  dsu = [None, DisjointSet(cells), DisjointSet(cells)]
  for row, col in cells:
    neighbors = get_neighbors(state.size, row, col)
    color = state.board[row][col]
    for r, c in neighbors:
      if color != 0 and state.board[r][c] == color:
        dsu[color].union((row, col), (r, c))

  return dsu

def get_end(size, player_id)-> tuple[int, int]:
  down = (size, 0)
  right = (0, size)
  return [None, right, down][player_id]

def bfs(state: HexBoard, player_id: int) -> int:
  opponent = get_opponent_id(player_id)
  q = deque()
  w = [1, 0, 0]
  w[opponent] = float('inf')
  w[player_id] = 0
  d = {}
  visited = set()

  for i in range(state.size):
    row, col = (i, 0)
    if player_id == 2:
      row, col = col, row

    color = state.board[row][col]
    if color == opponent:
      continue
    d[(row, col)] = w[color]
    if color == player_id: q.appendleft((row, col))
    else: q.append((row, col))

  while len(q) > 0:
    row, col = q.popleft()
    if (row, col) in visited:
      continue
    visited.add((row, col))

    neighbors = get_neighbors(state.size, row, col)
    for r, c in neighbors:
      color = state.board[r][c]
      if color == opponent:
        continue

      new_d = d[(row, col)] + w[color]
      d[(r, c)] = min(d[(r,c)], new_d) if (r, c) in d else new_d

      if color == player_id: q.appendleft((r, c))
      else: q.append((r, c))

  result = float('inf')
  for i in range(state.size):
    row, col = (i, state.size - 1)
    if player_id == 2:
      row, col = col, row
    if (row, col) in d:
      result = min(result, d[(row, col)])
  return result

def get_neighbors(size: int, row: int, col: int, get_all: bool = False) -> list[tuple[int, int]]:
  d = [
    (-1, 0),  # Arriba
    (-1, 1),  # Arriba derecha
    (0, 1),  # Derecha
    (1, 0),  # Abajo
    (1, -1),  # Abajo izquierda
    (0, -1)  # Izquierda
  ]

  result: list[tuple[int, int]] = []
  for i in range(6):
    move = (row + d[i][0], col + d[i][1])
    if is_pos_ok(size, move) or get_all:
      result.append(move)
  return result

def is_pos_ok(size: int, pos: tuple[int, int]) -> bool:
  (x, y) = pos
  return 0 <= x < size and 0 <= y < size

def pretty_print(matrix):
  for i in range(len(matrix)):
    whitespaces = " " * i
    print(whitespaces, end='')
    for j in range(len(matrix)):
      print(f"{round(matrix[i][j], 2)} |", end='')
    print()
  input()
