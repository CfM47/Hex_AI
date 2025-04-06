from dsu import DisjointSet
from copy import deepcopy

class HexBoard:
  def __init__(self, size: int):
    self.size = size  # Tamaño N del tablero (NxN)
    self.board = [[0 for _ in range(size)] for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
    self.winner = 0
    # initialize dsu for checking the winner
    cells = [(i,j) for i in range(size) for j in range(size)]
    self.top = (-1, 0)
    self.down = (size, 0)
    self.left = (0, -1)
    self.right = (0, size)
    self.dsu = [None, None, None]
    self.dsu[1] = DisjointSet(cells + [self.left, self.right])
    self.dsu[2] = DisjointSet(cells + [self.top, self.down])
    for i in range(size):
      self.dsu[1].union((i, 0), self.left)
      self.dsu[1].union((i, size-1), self.right)
      self.dsu[2].union((0, i), self.top)
      self.dsu[2].union((size-1, i), self.down)

  def clone(self) -> "HexBoard":
    """Devuelve una copia del tablero actual"""
    new_board = HexBoard(self.size)
    new_board.board = deepcopy(self.board)
    return new_board

  def place_piece(self, row: int, col: int, player_id: int) -> bool:
    """Coloca una ficha si la casilla está vacía."""
    if row < 0 or row >= self.size or col < 0 or col >= self.size:
      raise IndexError('row of column index out of the board')
    if player_id not in [1, 2]:
      raise IndexError('whose player id is this XD')
    if self.board[row][col] != 0:
      return False
    self.board[row][col] = player_id

    # updating dsu with winning info
    neighbors = self.get_neighbors(row, col)
    for r, c in neighbors:
      if self.board[r][c] == self.board[row][col]:
        self.dsu[player_id].union((row, col), (r, c))
    if self.dsu[1].find_set(self.left) == self.dsu[1].find_set(self.right):
      self.winner = 1
    elif self.dsu[2].find_set(self.top) == self.dsu[2].find_set(self.down):
      self.winner = 2

    return True


  def get_neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
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
      r_ok = 0 <= ri < self.size
      c_ok = 0 <= ci < self.size
      if r_ok and c_ok:
        result.append((ri, ci))
    return result
  def get_possible_moves(self) -> list:
    """Devuelve todas las casillas vacías como tuplas (fila, columna)."""
    result = []
    for i in range(self.size):
      for j in range(self.size):
        if self.board[i][j] == 0:
          result.append((i, j))
    return result

  def check_connection(self, player_id: int) -> bool:
    """Verifica si el jugador ha conectado sus dos lados"""
    return self.winner == player_id

  @staticmethod
  def get_char_color(color: int):
    return [" ", "■", "O"][color]

  def print_board(self):
    offset = 0
    for i in range(self.size):
      offset = (offset + 1) % 2
      whitespaces = " " * offset
      print(whitespaces, end='')
      for j in range(self.size):
        color_char = self.get_char_color(self.board[i][j])
        print(f"({color_char})", end='')
      print()