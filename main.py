import os

from HumanPlayer import HumanPlayer
from RandomPlayer import RandomPlayer
from board import HexBoard
from player import AiPlayer
from utils import get_input, get_int_input
from time import time_ns


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def game(print_board=False, logs=False) -> (int, list[int]):
    """
  Main function to initialize a game of Hex.
  """
    size = 11

    p1 = AiPlayer(1)
    p2 = RandomPlayer(2)
    players = [None, p1, p2]
    board = HexBoard(size)
    turn = True

    turn_count = 1
    response_time = [0, 0, 0]
    moves = []

    winner = 0
    while winner == 0:

      if print_board:
        # input()
        clear()
        board.print_board()
        print()

      p = 1 if turn else 2
      copy = board.clone()
      start_time = time_ns() / 1e9
      piece = players[p].play(copy)
      end_time = time_ns() / 1e9
      response_time[p] = end_time - start_time

      if print_board:
        print(f"Response time: {response_time[p]}")

      while not piece:
        print("invalid movement")
        piece = players[p].play(copy)
      row, col = piece
      #print('piece: ', piece)
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

    if logs and not print_board:
      board.print_board()
      print(moves)
    return winner, response_time

def fixed_game(moves: list[tuple], print_board=False, logs=False) -> (int, list[int]):
    size = 11
    board = HexBoard(size)
    turn = True

    turn_count = 1

    winner = 0
    for move in moves:
        if print_board:
            input()
            clear()
            board.print_board()
            print()

        p = 1 if turn else 2
        row, col = move
        board.place_piece(row, col, p)
        turn = not turn
        turn_count += 1

        if board.check_connection(1):
            winner = 1
        if board.check_connection(2):
            winner = 2

    if print_board:
        clear()
        board.print_board()
        if winner != 0:
            print(f"The winner is {winner}")
        print(moves)
        input()

    if logs and not print_board:
        board.print_board()
        print(moves)
    return winner

def main():
  count = [0, 0, 0]
  total = 20
  for i in range(total):
    winner, response_time = game(True, True)
    print(f"Winner match {i}: {winner}")
    print(f"Average response time: {response_time[1] / total}")
    print(f"Average response time: {response_time[2] / total}")
    count[winner] +=1
  print(f"Player 1 wins: {count[1]/total}")
  print(f"Player 2 wins: {count[2]/total}")

  # moves = [(7, 5), (5, 2), (8, 8), (3, 0), (1, 4), (10, 10), (4, 5), (9, 8), (4, 9), (9, 3), (1, 1), (6, 6), (9, 1), (5, 10), (6, 1), (2, 6), (1, 7), (0, 9), (9, 9), (1, 0), (3, 1), (6, 7), (4, 3), (0, 5), (2, 9), (0, 4), (9, 5), (9, 0), (7, 3), (5, 3), (4, 7), (3, 8), (6, 10), (4, 0), (9, 7), (4, 4), (9, 6)]
  #
  # fixed_game(moves, print_board=True, logs=True)

if __name__ == "__main__":
    main()
