import ChessEngine
import pygame as p

width = height = 512
dimensions = 8
sq_size = height // dimensions
max_fps = 15
imgs = {}
p.init()

def show_board(self):
    for row in self.board:
        for piece in row:
            print(piece, end="")
        print('')

def loadImages():
    pieces = ["bP", "bR", "bN", "bB", "bK", "bQ", "wP", "wR", "wN", "wB", "wK", "wQ"]
    for piece in pieces:
        imgs[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sq_size, sq_size))


def main():
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game = ChessEngine.GameState()
    loadImages()
    
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        clock.tick(max_fps)
        p.display.flip()
        drawGameState(screen, game)

def drawGameState(screen, game):
    drawBoard(screen)
    drawPieces(screen, game.board)
    
    
def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(dimensions):
        for c in range(dimensions):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
    
    
def drawPieces(screen, board):
    pass
    
if __name__ == '__main__':
    main()
    
