import pygame as p

def move_to_coord(move):
    x = ord(move[0]) - ord('a')
    y = int(move[1]) - 1
    return x, y

class GameState:
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['..', '..', '..', '..', '..', '..', '..', '..'],
            ['..', '..', '..', '..', '..', '..', '..', '..'],
            ['..', '..', '..', '..', '..', '..', '..', '..'],
            ['..', '..', '..', '..', '..', '..', '..', '..'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
            ]
        
        self.whitemove = True
        self.movelog = []
    
    def show_board(self):
        for row in self.board:
            for piece in row:
                print(piece, end="")
            print('')


    IMGS = {}
    def loadImages():
        pieces = ["bP", "bR", "bN", "bB", "bK", "bQ", "wP", "wR" "wN" "wB" "wK" "wQ"]
        for piece in pieces:
        IMGS[piece] = p.image.load("images/" + piece ".png")

    def move_piece(self, move):

        

        board[] = board[]
        board[] = '.'
        

        
    