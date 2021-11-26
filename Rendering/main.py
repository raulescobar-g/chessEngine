import sys
sys.path.insert(1, '/Users/raulescobar/Documents/chessEngine')

import pygame as p
from Engine.ChessEngine import GameState
from Engine.chessMoves import Move

w = h = 512
d = 8
square_d = h // d

max_fps = 15

images = {}

def loadImages():
    pieces = ['wp','wR','wN','wK','wQ','wB','bp','bR','bN','bK','bQ','bB']
    for piece in pieces:
        images[piece] = p.transform.scale( p.image.load('piece_images/' + piece + '.png'), (square_d,square_d)) 



def main():
    p.init()
    screen = p.display.set_mode((w,h))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = GameState()

    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True

    curr_square = ()    #most recent click coordinates
    clicks = []         #keeps track of clicks

    gameOver = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False


            elif (e.type == p.MOUSEBUTTONDOWN):
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // square_d
                    row = location[1] // square_d
                    if curr_square == (row,col):
                        curr_square = ()
                        clicks = []
                    else:
                        curr_square = (row,col)
                        clicks.append(curr_square)

                    if len(clicks) == 2:
                        move = Move(clicks[0], clicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                curr_square = ()
                                clicks = []
                        if not moveMade:
                            clicks = [curr_square]
                


            elif e.type == p.KEYDOWN:
                if e.key == p.K_BACKSPACE:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    curr_square = ()
                    clicks = []
                    moveMade = False
                    animate = False


        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False


        
        drawGameState(screen, gs,validMoves,curr_square)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, "White wins by checkmate")
        elif gs.stalemate:
            drawText(screen, "Stalemate")

        clock.tick(max_fps)
        p.display.flip()

def highlightSquares(screen, gs, validMoves, squareSelected):
    if squareSelected != ():
        r,c = squareSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((square_d,square_d))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*square_d,r*square_d))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.s_row == r and move.s_col == c:
                    screen.blit(s, (square_d * move.e_col, square_d * move.e_row))




def drawGameState(screen, gs,validMoves, squareSelected):
    drawBoard(screen)
    highlightSquares(screen,gs,validMoves,squareSelected)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(d):
        for c in range(d):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*square_d, r*square_d,square_d,square_d))


def drawPieces(screen,board):
    for r in range(d):
        for c in range(d):
            piece = board[r][c]
            if piece != '--':
                screen.blit(images[piece], p.Rect(c*square_d, r*square_d,square_d,square_d))

def animateMove(move, screen, board, clock):
    global colors
    dr = move.e_row - move.s_row
    dc = move.e_col - move.s_col
    fps = 8
    frameCount = fps * (abs(dr) + abs(dc))
    for frame in range(frameCount+1):
        r,c = (move.s_row + dr * frame/frameCount, move.s_col + dc * frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.e_row + move.e_col) % 2]
        endSquare = p.Rect(move.e_col * square_d, move.e_row*square_d, square_d, square_d)
        p.draw.rect(screen, color, endSquare)
        if move.captured != '--':
            screen.blit(images[move.captured],endSquare)
        screen.blit(images[move.piece], p.Rect(c*square_d,r*square_d,square_d,square_d))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = p.font.SysFont("Helvetics", 32, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0,0,w,h).move(w/2 - textObject.get_width()/2, h/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

    


if __name__ == "__main__":
    main()
    