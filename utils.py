def get_input(message: str, valid_inputs: dict) -> str or None:
    while True:
        print(message)
        for key in valid_inputs.keys():
            print(f"{valid_inputs[key]} [{key}]")
        user_input = input()

        if user_input in valid_inputs:
            return user_input
        else:
            print("Invalid input. Please try again.")
            print("Valid inputs are: ", valid_inputs)


def get_int_input(message: str, min_val: int, max_val: int) -> int or None:
    while True:
        print(message)
        user_input = input()

        try:
            user_input = int(user_input)
            if user_input < min_val or user_input > max_val:
                print(f"Input must be between {min_val} and {max_val}. Please try again.")
            else:
                return user_input
        except ValueError:
            print("Invalid input. Please try again.")


# copied this here to avoid circular import errors
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