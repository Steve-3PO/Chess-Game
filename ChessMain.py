import ChessEngine, SmartMoveFinder
import pygame as p

'''
game parameters
'''
width = height = 512
dimensions = 8
sq_size = height // dimensions
max_fps = 15
imgs = {}

'''
initalise global dictionary of images 
'''
def loadImages():
    pieces = ["bp", "bR", "bN", "bB", "bK", "bQ", "wp", "wR", "wN", "wB", "wK", "wQ"]
    for piece in pieces:
        imgs[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sq_size, sq_size))


'''
main driver, handling user input and graphics updating
'''
def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    
    playerOne = True # if human playing white, set as true
    playerTwo = False # if AI is playing, set as False
    
    while running:
        humanTurn = (gs.whitemove == True and playerOne) or (not gs.whitemove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
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
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () # reset user click
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            
            # keyboard handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo move with 'z' key
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r: # reset game with 'r' key
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
        
        # AI move finder
        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
                    
        if moveMade:
            if animate:
                animateMove(gs.movelog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            
        drawGameState(screen, gs, validMoves, sqSelected)
        
        if gs.checkmate:
            gameOver = True
            if gs.whitemove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate')                
        clock.tick(max_fps)
        p.display.flip()
        
'''
highlighting
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whitemove else 'b'):
            # highlight selected square
            s = p.Surface((sq_size, sq_size))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*sq_size, r*sq_size))
            # highlight possible moves from square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*sq_size, move.endRow*sq_size))
            
'''
function for all graphics of current gs
'''
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    
'''
draws board and colours it
'''
def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color('grey')]
    for r in range(dimensions):
        for c in range(dimensions):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
    
'''
draw pieces on current gs
'''    
def drawPieces(screen, board):
    for r in range(dimensions):
        for c in range(dimensions):
            piece = board[r][c]
            if piece != '--':
                # if not empty grab the image from dictionary
                screen.blit(imgs[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
                
'''
animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5 # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*sq_size, move.endRow*sq_size, sq_size, sq_size)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(imgs[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(imgs[move.pieceMoved], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
        p.display.flip()
        clock.tick(60)
        
def drawText(screen, text):
    font = p.font.SysFont('Helvitca', 32, True, False)
    textObject = font.render(text, 0, p.Color('Grey'))
    textLocation = p.Rect(0, 0, width, height).move(width/2 - textObject.get_width()/2, height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))
                
if __name__ == '__main__':
    main()
    
