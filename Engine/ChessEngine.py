from Engine.castleRights import CastleRights
import numpy as np
from .chessMoves import Move
from .castleRights import CastleRights

'''
Stores state of game and determines valid moves
'''

class GameState():

    def __init__(self):
        self.board = np.array(  [['bR','bN','bB','bQ','bK','bB','bN','bR'],
                                ['bp','bp','bp','bp','bp','bp','bp','bp'],
                                ['--','--','--','--','--','--','--','--'], 
                                ['--','--','--','--','--','--','--','--'],
                                ['--','--','--','--','--','--','--','--'],
                                ['--','--','--','--','--','--','--','--'],
                                ['wp','wp','wp','wp','wp','wp','wp','wp'],
                                ['wR','wN','wB','wQ','wK','wB','wN','wR']])
        
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions =    {'p':self.getPawnMoves, 'R':self.getRookMoves, 
                                'N':self.getKnightMoves, 'B':self.getBishopMoves, 
                                'Q':self.getQueenMoves, 'K':self.getKingMoves}
        self.whiteKingloc = (7, 4)
        self.blackKingloc = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()
        self.currentCastleRights = CastleRights(True,True,True,True)
        self.castleRightsLog = [CastleRights(self.currentCastleRights.wks,self.currentCastleRights.bks,self.currentCastleRights.wqs,self.currentCastleRights.bqs)]



    def makeMove(self,move):
        self.board[move.s_row][move.s_col] = '--'
        self.board[move.e_row][move.e_col] = move.piece
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.piece == 'wK':
            self.whiteKingloc = (move.e_row,move.e_col)
        elif move.piece == 'bK':
            self.blackKingloc = (move.e_row,move.e_col)

        if move.piece[1] == 'p' and abs(move.s_row - move.e_row) == 2:
            self.enpassantPossible = ((move.s_row + move.e_row) // 2 , move.e_col)
        else:
            self.enpassantPossible = ()

        if move.isEnpassantMove:
            self.board[move.s_row][move.e_col] = '--'
            
        if move.isPawnPromotion:
            promotedPiece = input("Promote to Q, R, B, or N: ")
            self.board[move.e_row][move.e_col] = move.piece[0] + promotedPiece

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastleRights.wks,self.currentCastleRights.bks,self.currentCastleRights.wqs,self.currentCastleRights.bqs))

        if move.isCastleMove:
            if move.e_col - move.s_col == 2:
                self.board[move.e_row][move.e_col-1] = self.board[move.e_row][move.e_col+1]
                self.board[move.e_row][move.e_col+1] = '--'
            else:
                self.board[move.e_row][move.e_col+1] = self.board[move.e_row][move.e_col-2]
                self.board[move.e_row][move.e_col-2] = '--'


        


    def undoMove(self):
        if len(self.moveLog) > 0:
            move = self.moveLog.pop()
            self.board[move.s_row][move.s_col] = move.piece
            self.board[move.e_row][move.e_col] = move.captured
            self.whiteToMove = not self.whiteToMove
            if move.piece == 'wK':
                self.whiteKingloc = (move.s_row,move.s_col)
            elif move.piece == 'bK':
                self.blackKingloc = (move.s_row,move.s_col)

            if move.isEnpassantMove:
                self.board[move.e_row][move.e_col] = '--'
                self.board[move.s_row][move.e_col] = move.captured
                self.enpassantPossible = (move.e_row, move.e_col)

            if move.piece[1] == 'p' and abs(move.s_row - move.e_row) == 2:
                self.enpassantPossible = ()

            self.castleRightsLog.pop()
            self.currentCastleRights = self.castleRightsLog[-1]

            if move.isCastleMove:
                if move.e_col - move.s_col == 2:
                    self.board[move.e_row][move.e_col+1] = self.board[move.e_row][move.e_col-1]
                    self.board[move.e_row][move.e_col-1] = '--'
                else:
                    self.board[move.e_row][move.e_col-2] = self.board[move.e_row][move.e_col+1]
                    self.board[move.e_row][move.e_col+1] = '--'

    def updateCastleRights(self,move):
        if move.piece == 'wK':
            self.currentCastleRights.wks = False
            self.currentCastleRights.wqs = False
        elif move.piece == 'bK':
            self.currentCastleRights.bks = False
            self.currentCastleRights.bqs = False
        elif move.piece == 'wR':
            if move.s_row == 7:
                if move.s_col == 0:
                    self.currentCastleRights.wqs = False
                elif move.s_col == 7:
                    self.currentCastleRights.wks = False
        elif move.piece == 'bR':
            if move.s_row == 0:
                if move.s_col == 0:
                    self.currentCastleRights.bqs = False
                elif move.s_col == 7:
                    self.currentCastleRights.bks = False

    def getValidMoves(self):
        moves = []
        self.inCheck,self.pins,self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove:
            kingRow = self.whiteKingloc[0]
            kingCol = self.whiteKingloc[1]
        else:
            kingRow = self.blackKingloc[0]
            kingCol = self.blackKingloc[1]

        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()

                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]

                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []

                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow,checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)

                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                
                for i in range(len(moves) -1, -1, -1):
                    if moves[i].piece[1] != 'K':
                        if not (moves[i].e_row, moves[i].e_col) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow,kingCol,moves)
            
        else:
            moves = self.getAllPossibleMoves()

        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squreUnderAttack(self.whiteKingloc[0],self.whiteKingloc[1])
        else:
            return self.squreUnderAttack(self.blackKingloc[0],self.blackKingloc[1])

    def squreUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.e_row == r and move.e_col == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            s_row = self.whiteKingloc[0]
            s_col = self.whiteKingloc[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            s_row = self.blackKingloc[0]
            s_col = self.blackKingloc[1]
        
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1,8):
                e_row = s_row + d[0] * i
                e_col = s_col + d[1] * i

                if 0 <= e_row <= 7 and 0 <= e_col <= 7:
                    endPiece = self.board[e_row][e_col]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (e_row, e_col, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]

                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == 'B') or (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((e_row,e_col,d[0],d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break

        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for m in knightMoves:
            e_row = s_row + m[0]
            e_col = s_row + m[1]
            if 0 <= e_row <= 7 and 0 <= e_col <= 7:
                endPiece = self.board[e_row][e_col]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((e_row,e_col,m[0],m[1]))
        return inCheck,pins,checks

    def getPawnMoves(self,r,c,moves): 
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'

        isPawnPromotion = False
        
        if self.board[r+ moveAmount][c] == '--':
            if not piecePinned or pinDirection == (moveAmount,0):
                if r+moveAmount == backRow:
                    isPawnPromotion = True
                moves.append(Move((r,c), (r+moveAmount,c), self.board,isPawnPromotion=isPawnPromotion))

                if r == startRow and self.board[r+2*moveAmount][c] == '--':
                    moves.append(Move((r,c), (r+2*moveAmount,c), self.board))

        if c-1 >= 0:
            if not piecePinned or pinDirection == (moveAmount,-1):
                if self.board[r+moveAmount][c-1][0] == enemyColor:
                    if r+moveAmount == backRow:
                        isPawnPromotion = True
                    moves.append(Move((r,c), (r+moveAmount,c-1), self.board,isPawnPromotion=isPawnPromotion))
                if (r+moveAmount,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+moveAmount,c-1), self.board,isEnpassantMove=True))

        if c+1 <= 7:
            if not piecePinned or pinDirection == (i,1):
                if self.board[r+moveAmount][c+1][0] == enemyColor:
                    if r+moveAmount == backRow:
                        isPawnPromotion = True
                    moves.append(Move((r,c), (r+moveAmount,c+1), self.board,isPawnPromotion=isPawnPromotion))
                if (r+moveAmount,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+moveAmount,c+1), self.board, isEnpassantMove=True))
        
    def getRookMoves(self,r,c,moves): #no castling
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endcol = c + d[1] * i
                endrow = r + d[0] * i
                if 0 <= endrow <= 7 and 0 <= endcol <= 7:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        if self.board[endrow][endcol] == '--':
                            moves.append(Move((r,c),(endrow,endcol),self.board))
                        elif (self.board[endrow][endcol][0] == enemyColor):
                            moves.append(Move((r,c),(endrow,endcol),self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKnightMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        friendlyColor = 'w' if self.whiteToMove else 'b'
        directions = [(1,2),(-1,2),(1,-2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
        for d in directions:
            endrow = r + d[0]
            endcol = c + d[1]
            if 0 <= endrow <= 7 and 0 <= endcol <= 7:
                if not piecePinned:
                    if self.board[endrow][endcol][0] != friendlyColor:
                        moves.append(Move((r,c),(endrow,endcol),self.board))

    def getBishopMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        enemyColor = 'b' if self.whiteToMove else 'w'
        directions = [(1,1),(-1,-1),(1,-1),(-1,1)]
        for d in directions:
            for i in range(1,8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow <= 7 and 0 <= endcol <= 7:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        if self.board[endrow][endcol] == '--':
                            moves.append(Move((r,c),(endrow,endcol),self.board))
                        elif (self.board[endrow][endcol][0] == enemyColor):
                            moves.append(Move((r,c),(endrow,endcol),self.board))
                            break
                        else:
                            break
                else:
                    break

    def getQueenMoves(self,r,c,moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)

    def getKingMoves(self,r,c,moves): #no castling support
        friendlyColor = 'w' if self.whiteToMove else 'b'
        for i in range(-1,2):
            for j in range(-1,2):
                if r+i >= 0 and r+i <= 7 and c+j >= 0 and c+j <= 7 and (self.board[r+i][c+j][0] != friendlyColor):
                        
                    if friendlyColor == 'w':
                        self.whiteKingloc = (r+i, c+j)
                    else:
                        self.blackKingloc = (r+i, c+j)
                    
                    inCheck, pins, checks = self.checkForPinsAndChecks()

                    if not inCheck:
                        moves.append(Move((r,c), (r+i,c+j), self.board))
                    
                    if friendlyColor == 'w':
                        self.whiteKingloc = (r,c)
                    else:
                        self.blackKingloc = (r,c)
        self.getCastleMoves(r,c,moves,friendlyColor)

        

    
    def getCastleMoves(self,r,c,moves,allyColor):
        if (self.whiteToMove and self.currentCastleRights.wks) or (not self.whiteToMove and self.currentCastleRights.bks):
            self.getKingsideCastleMoves(r,c,moves,allyColor)
        if (self.whiteToMove and self.currentCastleRights.wqs) or (not self.whiteToMove and self.currentCastleRights.bqs):
            self.getQueensideCastleMoves(r,c,moves,allyColor)

    def getKingsideCastleMoves(self,r,c, moves, allyColor):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squreUnderAttack(r,c+1) and not self.squreUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove=True))

    def getQueensideCastleMoves(self,r,c,moves,allyColor):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squreUnderAttack(r,c-1) and not self.squreUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board,isCastleMove=True))