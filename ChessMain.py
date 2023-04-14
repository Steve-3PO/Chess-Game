import ChessEngine
import pygame as p

width = height = 512
dimensions = 8
sq_size = height // dimensions
max_fps = 15
imgs = {}
p.init()

def loadImages():
    pieces = ["bP", "bR", "bN", "bB", "bK", "bQ", "wP", "wR", "wN", "wB", "wK", "wQ"]
    for piece in pieces:
        imgs[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sq_size, sq_size))


def main():
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    
    game = ChessEngine.GameState()
    validMoves = game.getValidMoves()
    moveMade = False
    
    loadImages()
    sqSelected = ()
    running = True
    playerClicks = []
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//sq_size
                row = location[1]//sq_size
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], game.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        game.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    game.undoMove()
                    moveMade = True
                    
        if moveMade:
            validMoves = game.getValidMoves()
            moveMade = False            
                
        clock.tick(max_fps)
        p.display.flip()
        drawGameState(screen, game)

def drawGameState(screen, game):
    drawBoard(screen)
    drawPieces(screen, game.board)
    
    
def drawBoard(screen):
    colors = [p.Color('white'), p.Color('grey')]
    for r in range(dimensions):
        for c in range(dimensions):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
    
    
def drawPieces(screen, board):
    for r in range(dimensions):
        for c in range(dimensions):
            piece = board[r][c]
            if piece != '..':
                screen.blit(imgs[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
    
if __name__ == '__main__':
    main()
    
