import os

BOARD_SIZE = 3
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY_CELL = " "


def print_board(board, board_info):
    tic_tac_toe = """
 ____  ____  ___       ____   __    ___       ____  _____  ____
(_  _)(_  _)/ __) ___ (_  _) /__\  / __) ___ (_  _)(  _  )( ___)
  )(   _)(_( (__ (___)  )(  /(__)\( (__ (___)  )(   )(_)(  )__)
 (__) (____)\___)      (__)(__)(__)\___)      (__) (_____)(____)

    """
    print(tic_tac_toe)
    for row_index, row in enumerate(board):
        print(" " * 16 + " | ".join(row) + " " * 13 +
              " | ".join(board_info[row_index]))
        if row_index < BOARD_SIZE - 1:
            print(" " * 15 + "-" * 11 +
                  " " * 11 + "-" * 11)  # Print horizontal lines


def check_winner(board, player):
    """Check if the given player has won."""
    for i in range(BOARD_SIZE):
        if all(board[i][j] == player for j in range(BOARD_SIZE)) or \
           all(board[j][i] == player for j in range(BOARD_SIZE)):
            return True
    if all(board[i][i] == player for i in range(BOARD_SIZE)) or \
       all(board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
        return True
    return False


def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != EMPTY_CELL for row in board for cell in row)


def get_move():
    """Get a valid move from the player."""
    while True:
        try:
            move = int(input("Enter position (1-9): ")) - 1
            if move < 0 or move >= BOARD_SIZE * BOARD_SIZE:
                raise ValueError
            return divmod(move, BOARD_SIZE)  # Convert to row, col
        except ValueError:
            print("Invalid input. Enter a number between 1 and 9.")


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def tic_tac_toe():
    """Main function to run the Tic Tac Toe game."""
    board = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board_info = [[str(i + 1 + j * BOARD_SIZE) for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    players = [PLAYER_X, PLAYER_O]
    turn = 0
    spot_taken = False
    game_over = False

    while not game_over:
        clear_screen()
        print_board(board, board_info)
        if spot_taken:
            print("\n\nSpot already taken! Try again.")
            spot_taken = False
        else:
            print("\n\n")
        print("Select a position to place your mark (1-9)\n")
        print(f"Player {players[turn]}'s turn\n")
        row, col = get_move()

        if board[row][col] != EMPTY_CELL:
            spot_taken = True
            continue

        clear_screen()
        board[row][col] = players[turn]

        print_board(board, board_info)

        gameover = """
  ___    __    __  __  ____    _____  _  _  ____  ____    _
 / __)  /__\  (  \/  )( ___)  (  _  )( \/ )( ___)(  _ \  (_)
( (_-. /(__)\  )    (  )__)    )(_)(  \  /  )__)  )   /   _
 \___/(__)(__)(_/\/\_)(____)  (_____)  \/  (____)(_)\_)  (_)
"""

        if check_winner(board, players[turn]):
            print(gameover)
            print(f"\n\nPlayer {players[turn]} wins!\n\n")
            game_over = True

        elif is_draw(board):
            print(gameover)
            print("\n\nIt's a draw!\n\n")
            game_over = True

        turn = 1 - turn  # Switch player


if __name__ == "__main__":
    tic_tac_toe()
