import os

from HumanPlayer import HumanPlayer
from RandomPlayer import RandomPlayer
from board import HexBoard
from player import AiPlayer
from utils import get_input, get_int_input


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def game() -> int:
    """
  Main function to initialize a game of Hex.
  """
    #clear()
    #print("Welcome to the game of Hex!")
    #input("Press enter to continue...")
    # clear()
    # type1 = get_input("Enter the type of player 1: ", {"h": "Human", "c": "Computer"})
    # clear()
    # type2 = get_input("Enter the type of player 2: ", {"h": "Human", "c": "Computer"})
    #clear()
    #size = get_int_input("Enter the size of the board: ", 2, 20)
    size = 11
    p1 = RandomPlayer(1)
    p2 = AiPlayer(2)
    players = [None, p1, p2]
    board = HexBoard(size)
    turn = True
    while board.winner == 0:
      #clear()
      #board.print_board()
      #print()
      p = 1 if turn else 2
      piece = players[p].play(board)
      while not piece:
        print("invalid movement")
        piece = players[p].play(board)
      row, col = piece
      board.place_piece(row, col, p)
      turn = not turn
    #clear()
    #board.print_board()
    #print(f"The winner is {board.winner}")
    #input()
    return board.winner


def main():
  count = [0, 0, 0]
  for i in range(200):
    winner = game()
    print(f"Match {winner}")
    count[winner] +=1
  ratio = count[2]
  print(ratio)

if __name__ == "__main__":
    main()
