import os

from HumanPlayer import HumanPlayer
from RandomPlayer import RandomPlayer
from board import HexBoard
from player import AiPlayer, big_island_size_heuristic, max_island_size_heuristic, bridges_heuristic, \
    moves_needed_heuristic
from utils import get_input, get_int_input
from time import time_ns


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def game(print_board=False) -> (int, list[int]):
    """
  Main function to initialize a game of Hex.
  """
    size = 11
    p1 = RandomPlayer(1)
    p2 = AiPlayer(
        2,
        [moves_needed_heuristic, bridges_heuristic],
        [1, 1])
    players = [None, p1, p2]
    board = HexBoard(size)
    turn = True

    turn_count = 1
    response_time = [0, 0, 0]
    moves = []

    winner = 0
    while winner == 0:

      if print_board:
        input()
        clear()
        board.print_board()
        print()

      p = 1 if turn else 2
      start_time = time_ns() / 1e9
      piece = players[p].play(board)
      end_time = time_ns() / 1e9
      response_time[p] = end_time - start_time

      if print_board:
        print(f"Response time: {response_time[p]}")

      while not piece:
        print("invalid movement")
        piece = players[p].play(board)
      row, col = piece
      board.place_piece(row, col, p)
      moves.append(piece)
      turn = not turn
      turn_count += 1

      if board.check_connection(1):
          winner = 1
      if board.check_connection(2):
          winner = 2

    if print_board:
      clear()
      board.print_board()
      print(f"The winner is {winner}")
      print(moves)
      input()
    return winner, response_time


def main():
  count = [0, 0, 0]
  total = 20
  for i in range(total):
    winner, response_time = game(True)
    print(f"Winner match {i}: {winner}")
    print(f"Average response time: {response_time[1] / total}")
    print(f"Average response time: {response_time[2] / total}")
    count[winner] +=1
  print(f"Player 1 wins: {count[1]/total}")
  print(f"Player 2 wins: {count[2]/total}")

if __name__ == "__main__":
    main()
