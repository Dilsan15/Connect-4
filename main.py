import numpy as np
import pygame
import sys
import math

import os

rOWCOUNT = 6
cOLUMCOUNT = 7

bLUE = (0, 0, 225)
bLACK = (0, 0, 0)
rED = (255, 0, 0)
yELLOW = (255, 255, 0)


def createBoard():
    board = np.zeros((6, 7))
    return board


def dropPiece(board, row, col, piece):
    board[row][col] = piece


def isValidLocation(board, col):
    return board[rOWCOUNT - 1][col] == 0


def getNextOpenRow(board, col):
    for r in range(rOWCOUNT):
        if board[r][col] == 0:
            return r


def winningMove(board, piece):
    for c in range(cOLUMCOUNT - 3):
        for r in range(rOWCOUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    for c in range(cOLUMCOUNT):
        for r in range(rOWCOUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    for c in range(cOLUMCOUNT - 3):
        for r in range(rOWCOUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                    board[r + 3][c + 3] == piece:
                return True

    for c in range(cOLUMCOUNT - 3):
        for r in range(3, rOWCOUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                    board[r - 3][c + 3] == piece:
                return True


def drawBoard(board):
    for c in range(cOLUMCOUNT):
        for r in range(rOWCOUNT):
            pygame.draw.rect(screen, bLUE, (c * sQUARESIZE, r * sQUARESIZE + sQUARESIZE, sQUARESIZE, sQUARESIZE))
            pygame.draw.circle(screen, bLACK, (
                int(c * sQUARESIZE + sQUARESIZE / 2), int(r * sQUARESIZE + sQUARESIZE + sQUARESIZE / 2)), rADIUS)

    for c in range(cOLUMCOUNT):
        for r in range(rOWCOUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, rED, (
                    int(c * sQUARESIZE + sQUARESIZE / 2), Height - int(r * sQUARESIZE + sQUARESIZE / 2)), rADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, yELLOW, (
                    int(c * sQUARESIZE + sQUARESIZE / 2), Height - int(r * sQUARESIZE + sQUARESIZE / 2)), rADIUS)
    pygame.display.update()


myBoard = createBoard()

gameOver = False
turn = 0
pygame.init()
sQUARESIZE = 100

Width = cOLUMCOUNT * sQUARESIZE
Height = (rOWCOUNT + 1) * sQUARESIZE

Size = (Width, Height)

rADIUS = int(sQUARESIZE // 2 - 5)

screen = pygame.display.set_mode(Size)
drawBoard(myBoard)
pygame.display.update()

myFont = pygame.font.SysFont("monospace", 75)

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, bLACK, (0, 0, Width, sQUARESIZE))
            posX = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, rED, (posX, int(sQUARESIZE / 2)), rADIUS)
            else:
                pygame.draw.circle(screen, yELLOW, (posX, int(sQUARESIZE / 2)), rADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, bLACK, (0, 0, Width, sQUARESIZE))

            if turn == 0:
                posX = event.pos[0]
                Col = int(math.floor(posX / sQUARESIZE))
                if isValidLocation(myBoard, Col):
                    row = getNextOpenRow(myBoard, Col)
                    dropPiece(myBoard, row, Col, 1)

                    if winningMove(myBoard, 1):
                        Label = myFont.render("Player 1 Wins", True, rED)
                        screen.blit(Label, (40, 10))
                        gameOver = True

            else:
                posX = event.pos[0]
                Col = int(math.floor(posX / sQUARESIZE))
                if isValidLocation(myBoard, Col):
                    row = getNextOpenRow(myBoard, Col)
                    dropPiece(myBoard, row, Col, 2)

                    if winningMove(myBoard, 2):
                        Label = myFont.render("Player 2 Wins", True, yELLOW)
                        screen.blit(Label, (40, 10))
                        gameOver = True

            turn += 1
            turn = turn % 2

            drawBoard(myBoard)
            if gameOver:
                pygame.time.wait(3000)
