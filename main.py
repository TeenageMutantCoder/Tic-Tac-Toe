#!/usr/bin/python3
import pygame


pygame.init()
pygame.font.init()


def turnInfo(surface, turn, width, height):
    font = pygame.font.Font(None, 70)
    surface.fill((255,255,255))

    if checkWinner(board):
        if checkWinner(board) == "Tie":
            text = font.render("There was a tie.", 1, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (width//2, height //2)
            surface.blit(text, text_rect)
        else:
            text = font.render(checkWinner(board) + " has won!", 1, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (width//2, height //2)
            surface.blit(text, text_rect)
    else:
        text = font.render(turn + "\'s turn...", 1, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (width//2, height //2)
        surface.blit(text, text_rect)


def winInfo(surface, size):
    global wins
    font = pygame.font.Font(None, 70)
    winsX = wins.count("X")
    winsO = wins.count("O")
    ties = wins.count("Tie")
    text = font.render(f"X: {winsX}    O: {winsO}    Tie: {ties}", 1, (0,0,0))
    text_rect = text.get_rect()
    text_rect.center = (size[0] // 2, size[1] // 2)

    surface.fill((255, 255, 255))
    surface.blit(text, text_rect)


def draw(surface, board, width, spacing, offset, font):
    surface.fill((255,255,255))
    for x in range(4):
        pygame.draw.line(surface, (0,0,0), (x * spacing, 0),
                         (x * spacing, width))
        pygame.draw.line(surface, (0,0,0), (0, x * spacing),
                         (width, x * spacing))

    for rowIndex, row in enumerate(board):
        for colIndex, col in enumerate(row):
            surface.blit(font.render(col, False, (0,0,0)),
                     (rowIndex * spacing + offset,
                      colIndex * spacing + offset))


def isFull(board):
    return not any(col == "" for row in board for col in row)


def checkWinner(board):
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    for row in board:
        if row[0] == row[1] == row[2]:
            return row[0]
    for num in range(3):
        if board[0][num] == board[1][num] == board[2][num]:
            return board[0][num]
    if isFull(board):
        return "Tie"


def checkInput(event, spacing, offset):
    if event.button == 1:  # Left Mouse Button
        for row in range(3):
            for col in range(3):
                if spacing * row < event.pos[0] < spacing * (row + 1):
                    if spacing * col + offset < event.pos[1]:
                        if event.pos[1] < spacing * (col + 1) + offset:
                            playTurn(row, col)


def playTurn(row, col):
    global board, turn, wins
    if checkWinner(board):
        wins.append(checkWinner(board))
        board = [["", "", ""],
                 ["", "", ""],
                 ["", "", ""]]
        turn = "X"
    else:
        if board[row][col] == "":
            board[row][col] = turn
            turn = "X" if turn == "O" else "O"


def main():
    global board, turn, wins
    width = 500
    rows = 3
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    turn = "X"
    wins = []
    spacing = width // rows
    offset = spacing // 4
    font = pygame.font.Font(None, 170)
    icon = pygame.image.load("icon1.png")

    win = pygame.display.set_mode((width, width + width//8 * 2))
    pygame.display.set_caption("Tic-Tac-Toe")
    pygame.display.set_icon(icon)

    turnSurface = pygame.Surface((width, width//8)).convert()
    gameSurface = pygame.Surface((width, width)).convert()
    winSurface = pygame.Surface((width, width//8)).convert()

    while True:
        draw(gameSurface, board, width, spacing, offset, font)
        turnInfo(turnSurface, turn, width, turnSurface.get_height())
        winInfo(winSurface, winSurface.get_size())
        win.blit(turnSurface, (0,0))
        win.blit(gameSurface, (0, 0 + turnSurface.get_height()))
        win.blit(winSurface, (0, 0 + turnSurface.get_height() + width))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                checkInput(event, spacing, turnSurface.get_height())


main()
