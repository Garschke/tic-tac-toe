import os


def print_board(board, board_info):
    tic_tac_toe = """
 ____  ____  ___       ____   __    ___       ____  _____  ____
(_  _)(_  _)/ __) ___ (_  _) /__\  / __) ___ (_  _)(  _  )( ___)
  )(   _)(_( (__ (___)  )(  /(__)\( (__ (___)  )(   )(_)(  )__)
 (__) (____)\___)      (__)(__)(__)\___)      (__) (_____)(____)

    """
    print(tic_tac_toe)
    row_index = 0
    for row in board:
        row_index = row_index + 1
        print(" " * 16 + " | ".join(row) + " " * 13 +
              " | ".join(board_info[row_index - 1]))
        if row_index < 3:
            print(" " * 15 + "-" * 11 +
                  " " * 11 + "-" * 11)  # Print horizontal lines


def check_winner(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_draw(board):
    return all(cell != " " for row in board for cell in row)


def get_move():
    while True:
        try:
            move = int(input("Enter position (1-9): ")) - 1
            if move < 0 or move >= 9:
                raise ValueError
            return divmod(move, 3)  # Convert to row, col
        except ValueError:
            print("Invalid input. Enter a number between 1 and 9.")


def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    # board = [["X", "O", "X"], ["O", "X", "O"], ["X", "O", "X"]]
    board_info = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
    players = ["X", "O"]
    turn = 0
    spot_taken = False
    game_over = False

    while not game_over:
        # Clears terminal screen
        os.system('clear' if os.name == 'posix' else 'cls')
        print_board(board, board_info)
        if spot_taken:
            print("\n\nSpot already taken! Try again.")
            spot_taken = False
        else:
            print("\n\n")
        print("Select a position to place your mark (1-9)\n")
        print(f"Player {players[turn]}'s turn\n")
        row, col = get_move()

        if board[row][col] != " ":
            spot_taken = True
            continue

        os.system('clear' if os.name == 'posix' else 'cls')
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
