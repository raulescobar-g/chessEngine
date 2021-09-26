import numpy as np

class Move():

    ranksToRows = {'1':7,'2':6,'3':5,'4':4,'5':3,'6':2,'7':1,'8':0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self,start,end,board,isPawnPromotion=False,isEnpassantMove=False,isCastleMove=False):
        self.s_row = start[0]
        self.s_col = start[1]
        self.e_row = end[0]
        self.e_col = end[1]
        self.piece = board[self.s_row][self.s_col]
        self.captured = board[self.e_row][self.e_col]

        self.isPawnPromotion = isPawnPromotion

        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.captured = 'wp' if self.piece == 'bp' else 'bp'
        
        self.isCastleMove = isCastleMove

        
        self.moveID = str(self.s_row) + str(self.s_col) + str(self.e_row) + str(self.e_col)
        


    def __eq__(self,other):
        return isinstance(other,Move) and self.moveID == other.moveID

    def getChessNotation(self):
        return self.getRankFile(self.s_row,self.s_col) + self.getRankFile(self.e_row,self.e_col)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]