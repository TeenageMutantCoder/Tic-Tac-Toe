#!/usr/bin/python3
import pygame
import sys


class Game():
    def __init__(self, width):
        pygame.init()
        pygame.font.init()
        self.width = width
        self.rows = 3
        self.board = [["", "", ""], 
                      ["", "", ""], 
                      ["", "", ""]]
        self.current_turn = "X"
        self.wins = []
        self.spacing = self.width // self.rows
        self.offset = self.spacing // 4
        self.game_font = pygame.font.Font(None, 170)
        self.surface_font = pygame.font.Font(None, 70)
        icon = pygame.image.load("tic-tac-toe/assets/icon.ico")
        pygame.display.set_icon(icon)
        self.surface_height = self.width//8
        self.window = pygame.display.set_mode((self.width, self.width + self.surface_height * 2))
        pygame.display.set_caption("Tic-Tac-Toe")
        self.turn_surface = pygame.Surface((self.width, self.surface_height)).convert()
        self.game_surface = pygame.Surface((self.width, self.width)).convert()
        self.win_surface = pygame.Surface((self.width, self.surface_height)).convert()

        self.update()


    def draw(self):
        self.draw_grid()
        self.draw_turn_info()
        self.draw_win_info()
        pygame.display.flip()

    def draw_turn_info(self):
        self.turn_surface.fill((255,255,255))
        winner = self.check_winner()
        if winner:
            if winner == "Tie":
                text = self.surface_font.render("There was a tie.", True, (0,0,0))
            else:
                text = self.surface_font.render(winner + " has won!", True, (0,0,0))

            text_rect = text.get_rect()
            text_rect.center = (self.width // 2, self.surface_height // 2)
            self.turn_surface.blit(text, text_rect)
    
        else:
            text = self.surface_font.render(self.current_turn + "\'s turn...", True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (self.width // 2, self.surface_height // 2)
            self.turn_surface.blit(text, text_rect)
        
        self.window.blit(self.turn_surface, (0,0))


    def draw_win_info(self):
        winsX = self.wins.count("X")
        winsO = self.wins.count("O")
        ties = self.wins.count("Tie")
        text = self.surface_font.render(f"X: {winsX}    O: {winsO}    Tie: {ties}", True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (self.width // 2, self.surface_height // 2)

        self.win_surface.fill((255, 255, 255))
        self.win_surface.blit(text, text_rect)
        self.window.blit(self.win_surface, (0, 0 + self.surface_height + self.width))


    def draw_grid(self):
        self.game_surface.fill((255,255,255))
        for count in range(4):
            pygame.draw.line(self.game_surface, (0,0,0), (count * self.spacing, 0),
                            (count * self.spacing, self.width))
            pygame.draw.line(self.game_surface, (0,0,0), (0, count * self.spacing),
                            (self.width, count * self.spacing))

        for rowIndex, row in enumerate(self.board):
            for colIndex, col in enumerate(row):
                self.game_surface.blit(self.game_font.render(col, False, (0,0,0)),
                        (rowIndex * self.spacing + self.offset,
                        colIndex * self.spacing + self.offset))
        
        self.window.blit(self.game_surface, (0, 0 + self.surface_height))


    def is_full(self):
        return not any(col == "" for row in self.board for col in row)


    def check_winner(self):
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]
        for row in self.board:
            if row[0] == row[1] == row[2]:
                return row[0]
        for num in range(3):
            if self.board[0][num] == self.board[1][num] == self.board[2][num]:
                return self.board[0][num]
        if self.is_full():
            return "Tie"


    def check_input(self, event):
        if event.button == 1:  # Left Mouse Button
            for row in range(3):
                for col in range(3):
                    if self.spacing * row < event.pos[0] < self.spacing * (row + 1):
                        if self.spacing * col + self.offset < event.pos[1]:
                            if event.pos[1] < self.spacing * (col + 1) + self.offset:
                                self.play_turn(row, col)


    def play_turn(self, row, col):
        winner = self.check_winner()
        if winner:
            self.wins.append(winner)
            self.board = [["", "", ""],
                         ["", "", ""],
                         ["", "", ""]]
            self.current_turn = "X"
        else:
            if self.board[row][col] == "":
                self.board[row][col] = self.current_turn
                self.current_turn = "X" if self.current_turn == "O" else "O"


    def update(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_input(event)

if __name__ == "__main__":
    Game(500)