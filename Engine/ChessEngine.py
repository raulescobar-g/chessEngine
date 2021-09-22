import numpy as np
from .chessMoves import Move

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
        self.moveFunctions = {'p':self.getPawnMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves, 'B':self.getBishopMoves, 'Q':self.getQueenMoves, 'K':self.getKingMoves}



    def makeMove(self,move):
        self.board[move.s_row][move.s_col] = '--'
        self.board[move.e_row][move.e_col] = move.piece
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) > 0:
            move = self.moveLog.pop()
            self.board[move.s_row][move.s_col] = move.piece
            self.board[move.e_row][move.e_col] = move.captured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
    
        return moves



    def getPawnMoves(self,r,c,moves): #no enpassants or promotion
        enemyColor = 'b' if self.whiteToMove else 'w'
        i = -1 if enemyColor=='b' else 1
        
        if self.board[r+i][c] == '--':
            moves.append(Move((r,c), (r+i,c), self.board))
            if ((r == 6 and enemyColor == 'b') or (r == 1 and enemyColor == 'w')) and self.board[r+2*i][c] == '--':
                moves.append(Move((r,c), (r+2*i,c), self.board))

        if c-1 >= 0 and self.board[r+i][c-1][0] == enemyColor:
                moves.append(Move((r,c), (r+i,c-1), self.board))

        if c+1 <= 7 and self.board[r+i][c+1][0] == enemyColor:
            moves.append(Move((r,c), (r+i,c+1), self.board))
        

        

    def getRookMoves(self,r,c,moves): #no castling
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endcol = c + d[1] * i
                endrow = r + d[0] * i
                if 0 <= endrow <= 7 and 0 <= endcol <= 7:
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
        friendlyColor = 'w' if self.whiteToMove else 'b'
        directions = [(1,2),(-1,2),(1,-2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
        for d in directions:
            endrow = r + d[0]
            endcol = c + d[1]
            if 0 <= endrow <= 7 and 0 <= endcol <= 7:
                if self.board[endrow][endcol][0] != friendlyColor:
                    moves.append(Move((r,c),(endrow,endcol),self.board))

    def getBishopMoves(self,r,c,moves):
        enemyColor = 'b' if self.whiteToMove else 'w'
        directions = [(1,1),(-1,-1),(1,-1),(-1,1)]
        for d in directions:
            for i in range(1,8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow <= 7 and 0 <= endcol <= 7:
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
        if self.whiteToMove:
            for i in range(-1,2):
                for j in range(-1,2):
                    if r+i >= 0 and r+i <= 7 and c+j >= 0 and c+j <= 7 and ( self.board[r+i][c+j] == '--' or self.board[r+i][c+j][0] != 'w'):
                        moves.append(Move((r,c), (r+i,c+j), self.board))
        else:
            for i in range(-1,2):
                for j in range(-1,2):
                    if r+i >= 0 and r+i <= 7 and c+j >= 0 and c+j <= 7 and (self.board[r+i][c+j] == '--' or  self.board[r+i][c+j][0] != 'b'):
                        moves.append(Move((r,c), (r+i,c+j), self.board))




