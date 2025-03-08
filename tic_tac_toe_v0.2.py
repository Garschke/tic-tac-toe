import os
from random import choice

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


def get_easy_ai_move(board, ai_marker, player_marker):
    """Get a random move for the AI."""
    empty_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)
                   if board[r][c] == " "]
    return choice(empty_cells)


def get_medium_ai_move(board, ai_marker, player_marker):
    # Check if AI can win in the next move
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == " ":
                board[row][col] = ai_marker
                if check_winner(board, ai_marker):
                    return row, col
                board[row][col] = " "  # Undo move

    # Check if the player can win in the next move and block
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == " ":
                board[row][col] = player_marker
                if check_winner(board, player_marker):
                    return row, col
                board[row][col] = " "  # Undo move

    # Prioritize center, then corners, then other spots
    priority_moves = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2),
                      (0, 1), (1, 0), (1, 2), (2, 1)]
    for row, col in priority_moves:
        if board[row][col] == " ":
            return row, col

    # If no other move is found, pick randomly
    empty_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)
                   if board[r][c] == " "]
    return choice(empty_cells)


def minimax(board, depth, is_maximizing, ai_marker, player_marker):
    if check_winner(board, ai_marker):
        return 1
    elif check_winner(board, player_marker):
        return -1
    elif is_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = ai_marker
                    score = minimax(board, depth + 1, False, ai_marker,
                                    player_marker)
                    board[row][col] = " "  # Undo move
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = player_marker
                    score = minimax(board, depth + 1, True, ai_marker,
                                    player_marker)
                    board[row][col] = " "  # Undo move
                    best_score = min(score, best_score)
        return best_score

def get_hard_ai_move(board, ai_marker, player_marker):
    best_score = -float('inf')
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = ai_marker
                score = minimax(board, 0, False, ai_marker, player_marker)
                board[row][col] = " "  # Undo move
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def tic_tac_toe():
    """Main function to run the Tic Tac Toe game."""
    board = [[EMPTY_CELL for _ in range(BOARD_SIZE)]
             for _ in range(BOARD_SIZE)]
    board_info = [[str(i + 1 + j * BOARD_SIZE)
                   for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    players = [PLAYER_X, PLAYER_O]
    turn = 0
    spot_taken = False
    game_over = False
    player_mode = ""    # no initial selection ""
    selection_made = False

    # Select Player Mode
    while player_mode not in ["1", "2", "3", "4"]:
        clear_screen()
        print_board(board, board_info)
        if selection_made is True:
            print("\nOnly enter valid options (1-4)")
        else:
            print("\n")
        player_mode_options = """
Select mode:
 1. Two player
 2. One player (vs Computer AI - Easy)
 3. One player (vs Computer AI - Medium)
 4. One player (vs Computer AI - Hard)

"""
        player_mode = input(player_mode_options)
        selection_made = True

    while not game_over:
        clear_screen()
        print_board(board, board_info)
        if spot_taken:
            print("\n\nSpot already taken! Try again.")
            spot_taken = False
        else:
            if players[turn] == PLAYER_O and player_mode != "1":
                # computer move
                if player_mode == "2":
                    row, col = get_easy_ai_move(board, PLAYER_O, PLAYER_X)
                elif player_mode == "3":
                    row, col = get_medium_ai_move(board, PLAYER_O, PLAYER_X)
                elif player_mode == "4":
                    row, col = get_hard_ai_move(board, PLAYER_O, PLAYER_X)
                board[row][col] = players[turn]
            else:
                # players move
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
