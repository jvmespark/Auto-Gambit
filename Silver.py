import pygame
import chess_engine as engine

WIDTH = HEIGHT = 500
DIMENSION = 8
PIECE_SIZE = HEIGHT / DIMENSION
MAX_FPS = 15

IMAGES = {}

#king and knight are the same initial. So Im delegating knight to night
def load_images():
    pieces = {'wk', 'wr', 'wb', 'wq', 'wn', 'wp', 'bk', 'br', 'bb', 'bq', 'bn', 'bp'}
    for piece in pieces:
        #Image['wk'] = white king
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("assets/" + piece + ".png"), (PIECE_SIZE, PIECE_SIZE))
    IMAGES['board'] = pygame.transform.scale(pygame.image.load("assets/board.png"), (WIDTH, HEIGHT))

def load_gamestate(screen, gamestate):
    load_board(screen)
    load_pieces(screen, gamestate.board)

def load_board(screen):
    screen.blit(IMAGES['board'], (0, 0))

def load_pieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != '--':
                screen.blit(IMAGES[piece], pygame.Rect(column * PIECE_SIZE, row * PIECE_SIZE, PIECE_SIZE, PIECE_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("PyChess")
    
    gamestate = engine.gamestate()
    load_images()

    running = True
    while (running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #Needs to:
                    #-Move the piece to the next clicked spot IF the spot is empty --
                    #-deselect the piece if the player clicks the same piece again
                    mouse_location = pygame.mouse.get_pos()
                    column = mouse_location[0] // PIECE_SIZE
                    row = mouse_location[1] // PIECE_SIZE
                    
            load_gamestate(screen, gamestate)
            clock.tick(MAX_FPS)
            pygame.display.flip()

if __name__ == "__main__":
    main()
