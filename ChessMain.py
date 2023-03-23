import ChessEngine
import pygame as p

width = height = 512
dimensions = 8
sq_size = height // dimensions
max_fps = 15
imgs = {}
p.init()

#game = ChessEngine.GameState()
#game.show_board()


def show_board(self):
    for row in self.board:
        for piece in row:
            print(piece, end="")
        print('')


def loadImages():
    pieces = ["bP", "bR", "bN", "bB", "bK", "bQ", "wP", "wR" "wN" "wB" "wK" "wQ"]
    for piece in pieces:
        imgs[piece] = p.transform.scale(p.image.load("images/" + piece ".png"), (sq_size, sq_size))


