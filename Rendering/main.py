import sys
sys.path.insert(1, '/Users/raulescobar/Documents/chess_engine')

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

    loadImages()
    running = True

    curr_square = ()    #most recent click coordinates
    clicks = []         #keeps track of clicks

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False


            elif (e.type == p.MOUSEBUTTONDOWN):
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
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    curr_square = ()
                    clicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_BACKSPACE:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        
        drawGameState(screen, gs)
        clock.tick(max_fps)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

def drawBoard(screen):
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
    


if __name__ == "__main__":
    main()
    