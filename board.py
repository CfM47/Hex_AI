class HexBoard:
  def __init__(self, size: int):
    self.size = size  # Tamaño N del tablero (NxN)
    self.board = [[0 for _ in range(size)] for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
    # 1 vertical player
    # 2 horizontal player
    # to check if position i,j creates a path to a border, for checking winner in O(1) time
    # if value is positive represents up/left border else represents down/right border
    self.pathMask  = [[0 for _ in range(size)] for _ in range(size)]
    self.winner = 0

  def clone(self) -> "HexBoard":
    """Devuelve una copia del tablero actual"""
    new_board = HexBoard(self.size)
    new_board.board = self.board.copy()
    new_board.pathMask = self.pathMask.copy()
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
    if player_id == 1:
      if row == 0:
        self.pathMask[row][col] = player_id
        has_start_path = True
      elif row == self.size - 1:
        self.pathMask[row][col] = -player_id
    elif player_id == 2:
      if col == 0:
        self.pathMask[row][col] = player_id
        has_start_path = True
      elif col == self.size - 1:
        self.pathMask[row][col] = player_id

    neighbors = self.get_neighbors(row, col)
    for r, c in neighbors:
      if self.pathMask[r][c] == 0:
        continue
      if self.pathMask[row][col] == 0 and abs(self.pathMask[r][c]) == self.board[row][col]:
        self.pathMask[row][col] = self.pathMask[r][c]
        continue

      if self.pathMask[row][col] == -self.pathMask[r][c]:
        self.winner = abs(self.pathMask[r][c])
        break
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
    for i in range(self.size):
      offset = self.size - i
      whitespaces = " " * offset
      print(whitespaces, end='')
      for j in range(self.size):
        color_char = self.get_char_color(self.board[i][j])
        print(f"({color_char})", end='')
      print()