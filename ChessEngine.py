class GameState:
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
            ]
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves, 
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        
        self.whitemove = True
        self.movelog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = () # coordinates for a possible en passant capture
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move) # log move in case we must undo
        self.whitemove = not self.whitemove # swap players
        # update king locations if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        
        # pawn promotion   
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
            
        # enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' # captured pawn
            
        # update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: # enpassant only on 2 space advancing pawns
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()
            
        # castle
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: # king side
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] # move rook
                self.board[move.endRow][move.endCol + 1] = '--' # remove old rook
            else: # queen side
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2] # move rook
                self.board[move.endRow][move.endCol - 2] = '--' # remove old rook
                
        # update castling rights when rook or king is moved
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
    
    '''
    undo from moveLog
    '''    
    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whitemove = not self.whitemove # undo switch
            
            # update kings position if moved
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
                
            # undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] == '--' # leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
                
            # undo 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
            
            # undo castling rights
            self.castleRightsLog.pop() # remove the new castle rights from last move
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            
            # undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: # king side
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else: # queen side
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
    
    '''
    update castle rights given move
    '''                
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: # left rook
                    self.currentCastlingRight.wqs = False
                if move.startCol == 7: # right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: # left rook
                    self.currentCastlingRight.bqs = False
                if move.startCol == 7: # right rook
                    self.currentCastlingRight.bks = False         
                        
    '''
    all moves considering checks
    '''                            
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        
        # generate all possible moves
        moves = self.getAllPossibleMoves()
        
        # make each move
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whitemove = not self.whitemove # change and check if opponents moves attack king
            if self.inCheck():
                moves.remove(moves[i]) # not valid move if in check
            self.whitemove = not self.whitemove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        
        if self.whitemove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves
    
    '''
    determine if player checked
    '''
    def inCheck(self):
        if self.whitemove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        
    '''
    determine if enemy can attack r, c square
    '''
    def squareUnderAttack(self, r, c):
        self.whitemove = not self.whitemove # switch to opponent turn
        oppMoves = self.getAllPossibleMoves()
        self.whitemove = not self.whitemove # switch back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: # square attacked
                return True
        return False
    
    '''
    all moves excluding checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # each row
            for c in range(len(self.board[r])): # each col
                turn = self.board[r][c][0]
                if (turn == "w" and self.whitemove) or (turn == "b" and not self.whitemove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # calls the function for the specific piece   
        return moves
    
    '''
    pawn moves
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whitemove: # white pawn moves
            if self.board[r - 1][c] == "--": # empty square ahead of pawn
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--": # empty square 2 spaces ahead and starting pawn pos
                    moves.append(Move((r, c), (r - 2, c), self.board))
            # captures            
            if (c - 1) >= 0:
                if self.board[r - 1][c - 1][0] == "b": # piece to left + opponent color
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))
                    
            if (c + 1) <= 7:
                if self.board[r - 1][c + 1][0] == "b": # piece to right + opponent color
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))    
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))
                    
        else: # black pawn moves
            if self.board[r + 1][c] == "--": # empty square ahead 1 space
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--": # empty square ahead 2 spaces
                    moves.append(Move((r, c), (r + 2, c), self.board))
            # captures            
            if (c - 1) >= 0: #  capture left
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))           
            if (c + 1) <= 7: # capture right
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))  
    
    '''
    rook moves
    '''    
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whitemove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i    
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]      
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    
    '''
    bishop moves
    '''    
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) 
        enemyColor = "b" if self.whitemove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i    
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]   
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break 
    
    '''
    knight moves
    '''       
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whitemove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    
    '''
    queen moves
    '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
    
    '''
    king moves
    '''
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whitemove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                    
    '''
    add all valid castle moves for king at r, c to moves list
    '''
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return # cannot castle in check
        if (self.whitemove and self.currentCastlingRight.wks) or (not self.whitemove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whitemove and self.currentCastlingRight.wqs) or (not self.whitemove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)
            
    '''
    king side castle moves
    '''
    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--': # if spaces are empty
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2): # and spaces are not attacked
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove = True))
                
    '''
    queen side castle moves
    '''
    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3]: # if spaces are empty
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2): # and spaces are not attacked
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove = True))

'''
castle rights
'''
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks 
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs               


'''
move class
'''        
class Move():
    
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        # en passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        # castle move
        self.isCastleMove = isCastleMove
        # move identifier
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
        
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
        
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    