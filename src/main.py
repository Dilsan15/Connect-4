# imports to build/destroy display amd conduct calc
import numpy as np
import pygame
import math
import sys

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
COL_BLUE = (0, 0, 225)
COL_BLACK = (0, 0, 0)
COL_RED = (255, 0, 0)
COL_YELLOW = (255, 255, 0)


# Uses np to create a list of Zeros, which is used to depict the board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# drops piece on board based on where the user wants it to go
def drop_piece(board, row_num, col_num, piece):
    board[row_num][col_num] = piece


# Makes sure that the spot which was wanted to be placed on is not taken
def is_valid_location(board, col_num):
    return board[ROW_COUNT - 1][col_num] == 0


# Gets information about what height the token being place is at
def get_next_own_row(board, col_num):
    for r in range(ROW_COUNT):
        if board[r][col_nm] == 0:
            return r


# Figures out if a winning move has been made
def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                    board[r + 3][c + 3] == piece:
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                    board[r - 3][c + 3] == piece:
                return True


# Makes the board visible
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen_set, COL_BLUE,
                             (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen_set, COL_BLACK, (
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                               TOKEN_RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen_set, COL_RED, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), board_height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   TOKEN_RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen_set, COL_YELLOW, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), board_height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   TOKEN_RADIUS)
    pygame.display.update()


# Variables which are used as assets for the GUI and Initialization of pygame
my_board = create_board()
game_over = False
user_turn = 0
pygame.init()
SQUARE_SIZE = 100

board_width = COLUMN_COUNT * SQUARE_SIZE
board_height = (ROW_COUNT + 1) * SQUARE_SIZE

board_size = (board_width, board_height)

TOKEN_RADIUS = int(SQUARE_SIZE // 2 - 5)

screen_set = pygame.display.set_mode(board_size)
draw_board(my_board)
pygame.display.update()

my_font = pygame.font.SysFont("monospace", 75)

# Logic which runs all functions and run the game

while not game_over:

    for window_event in pygame.event.get():
        if window_event.type == pygame.QUIT:
            sys.exit()

        if window_event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen_set, COL_BLACK, (0, 0, board_width, SQUARE_SIZE))
            pos_x = window_event.pos[0]
            if user_turn == 0:
                pygame.draw.circle(screen_set, COL_RED, (pos_x, int(SQUARE_SIZE / 2)), TOKEN_RADIUS)
            else:
                pygame.draw.circle(screen_set, COL_YELLOW, (pos_x, int(SQUARE_SIZE / 2)), TOKEN_RADIUS)
            pygame.display.update()

        if window_event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen_set, COL_BLACK, (0, 0, board_width, SQUARE_SIZE))

            if user_turn == 0:
                pos_x = window_event.pos[0]
                col = int(math.floor(pos_x / SQUARE_SIZE))
                if is_valid_location(my_board, col):
                    row = get_next_own_row(my_board, col)
                    drop_piece(my_board, row, col, 1)

                    if winning_move(my_board, 1):
                        winner_text = my_font.render("Player 1 Wins", True, COL_RED)
                        screen_set.blit(winner_text, (40, 10))
                        game_over = True

            else:
                pos_x = window_event.pos[0]
                col = int(math.floor(pos_x / SQUARE_SIZE))
                if is_valid_location(my_board, col):
                    row = get_next_own_row(my_board, col)
                    drop_piece(my_board, row, col, 2)

                    if winning_move(my_board, 2):
                        winner_text = my_font.render("Player 2 Wins", True, COL_YELLOW)
                        screen_set.blit(winner_text, (40, 10))
                        game_over = True

            user_turn += 1
            user_turn = user_turn % 2

            draw_board(my_board)
            if game_over:
                pygame.time.wait(3000)
