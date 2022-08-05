import pygame

WIDTH = HEIGHT = 500
DIMENSION = 8
PIECE_SIZE = HEIGHT / DIMENSION

IMAGES = {}

#king and knight are the same initial. So Im delegating knight to night
def loadImages():
    pieces = {'wk', 'wr', 'wb', 'wq', 'wn', 'wp', 'bk', 'br', 'bb', 'bq', 'bn', 'bp'}
    for piece in pieces:
        #Image['wk'] = white king
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("assets/" + piece + ".png"), (PIECE_SIZE, PIECE_SIZE))
    IMAGES['board'] = pygame.transform.scale(pygame.image.load("assets/board.png"), (WIDTH, HEIGHT))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("PyChess")

    loadImages()
    screen.blit(IMAGES['board'], (0, 0))
    screen.blit(IMAGES['wr'], (0,0))
    pygame.display.update()

    running = True
    while (running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()


if __name__ == "__main__":
    main()
