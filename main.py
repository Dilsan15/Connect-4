import numpy as np
import pygame
import math

ROWCOUNT = 6
COLUMCOUNT = 7

BLUE = (0, 0, 225)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def createBoard():
    board = np.zeros((6, 7))
    return board


def dropPiece(board, row, col, piece):
    board[row][col] = piece


def isValidLocation(board, col):
    return board[ROWCOUNT - 1][col] == 0


def getNextOpenRow(board, col):
    for r in range(ROWCOUNT):
        if board[r][col] == 0:
            return r


def winningMove(board, piece):
    for c in range(COLUMCOUNT - 3):
        for r in range(ROWCOUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    for c in range(COLUMCOUNT):
        for r in range(ROWCOUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    for c in range(COLUMCOUNT - 3):
        for r in range(ROWCOUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                    board[r + 3][c + 3] == piece:
                return True

    for c in range(COLUMCOUNT - 3):
        for r in range(3, ROWCOUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                    board[r - 3][c + 3] == piece:
                return True


def drawBoard(board):
    for c in range(COLUMCOUNT):
        for r in range(ROWCOUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), rADIUS)

    for c in range(COLUMCOUNT):
        for r in range(ROWCOUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), Height - int(r * SQUARESIZE + SQUARESIZE / 2)), rADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), Height - int(r * SQUARESIZE + SQUARESIZE / 2)), rADIUS)
    pygame.display.update()


myBoard = createBoard()

gameOver = False
turn = 0
pygame.init()
SQUARESIZE = 100

Width = COLUMCOUNT * SQUARESIZE
Height = (ROWCOUNT + 1) * SQUARESIZE

Size = (Width, Height)

rADIUS = int(SQUARESIZE // 2 - 5)

screen = pygame.display.set_mode(Size)
drawBoard(myBoard)
pygame.display.update()

myFont = pygame.font.SysFont("monospace", 75)

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, Width, SQUARESIZE))
            posX = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posX, int(SQUARESIZE / 2)), rADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posX, int(SQUARESIZE / 2)), rADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, Width, SQUARESIZE))

            if turn == 0:
                posX = event.pos[0]
                Col = int(math.floor(posX / SQUARESIZE))
                if isValidLocation(myBoard, Col):
                    row = getNextOpenRow(myBoard, Col)
                    dropPiece(myBoard, row, Col, 1)

                    if winningMove(myBoard, 1):
                        Label = myFont.render("Player 1 Wins", True, RED)
                        screen.blit(Label, (40, 10))
                        gameOver = True

            else:
                posX = event.pos[0]
                Col = int(math.floor(posX / SQUARESIZE))
                if isValidLocation(myBoard, Col):
                    row = getNextOpenRow(myBoard, Col)
                    dropPiece(myBoard, row, Col, 2)

                    if winningMove(myBoard, 2):
                        Label = myFont.render("Player 2 Wins", True, YELLOW)
                        screen.blit(Label, (40, 10))
                        gameOver = True

            turn += 1
            turn = turn % 2

            drawBoard(myBoard)
            if gameOver:
                pygame.time.wait(3000)
