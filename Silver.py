
import chess_engine as engine
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import argparse

WIDTH = HEIGHT = 500
DIMENSION = 8
PIECE_SIZE = HEIGHT / DIMENSION
MAX_FPS = 15
IMAGES = {}
STATE = "GRAPHICS"

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

def playGUI(against, selfplay, algo):
    gamestate = engine.gamestate()
    valid_moves, checkmate, stalemate = gamestate.get_valid_moves()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Silver Chess")
    load_images()
    moveMade = False #until a valid move is made, then you shouldnt regenerate an expensive function like get valid moves
    
    #tuple
    square_selected = ()
    #array
    player_clicks = []
    
    
    running = True
    checkmate, stalemate = False, False
    while (running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #Needs to:
                    #-Move the piece to the next clicked spot IF the spot is empty --
                    #-deselect the piece if the player clicks the same piece again
                    mouse_location = pygame.mouse.get_pos()
                    column = int(mouse_location[0] // PIECE_SIZE)
                    row = int(mouse_location[1] // PIECE_SIZE)

                    if  square_selected == (row, column):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, column)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2:
                        move = engine.move(player_clicks[0], player_clicks[1], gamestate.board)
                        print(move.get_chess_notation())
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gamestate.make_move(valid_moves[i])
                                moveMade = True
                        
                                square_selected = ()
                                player_clicks = []
                        if not moveMade:
                            player_clicks = [square_selected]
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_u:
                        gamestate.undo_move()
                        valid_moves, checkmate, stalemate = gamestate.get_valid_moves()

            if moveMade:
                valid_moves, checkmate, stalemate = gamestate.get_valid_moves()
                moveMade = False

            load_gamestate(screen, gamestate)
            clock.tick(MAX_FPS)
            pygame.display.flip()

            if checkmate or stalemate:
                time.sleep(5) # let the winner bask in their glory for 5 seconds then close game
                running = False

def printBoard(board):
    pattern = 0
    for r in board:
        for c in r:
            if c == "--" and pattern%2!=0: print("##", end =" ")
            elif c == "--" and pattern%2==0: print("  ", end=" ")
            else: print(c, end =" ")
            pattern += 1
        print("\n")
        pattern += 1

def validNotation(userMove):
    return False if userMove[0].lower() not in "abcdefgh" or int(userMove[1]) not in range(9) or userMove[2].lower() not in "abcdefgh" or int(userMove[3]) not in range(9) else True

def playTerminal(against, selfplay, algo):
    if against:
        # for now, default player as white
        print("against")
    if selfplay:
        print("selfplay")
    print(algo)

    gamestate = engine.gamestate()
    valid_moves, checkmate, stalemate = gamestate.get_valid_moves()
    moveMade = False #until a valid move is made, then you shouldnt regenerate an expensive function like get valid moves
    printBoard(gamestate.board)
    checkmate, stalemate = False, False
    
    running = True
    while (running):
            # NOTE: this current implementation of user input parsing is wrong, i should write a finite automaton to solve this
            userMove = input(">> ")
            if not validNotation(userMove):
                print("ERROR: Invalid Notation")
                userMove = input(">> ")
            if userMove == "u":
                gamestate.undo_move()
                valid_moves, checkmate, stalemate = gamestate.get_valid_moves()
            if userMove == "q":
                exit(0)


            move = engine.move.notated(userMove, gamestate.board)
            for i in range(len(valid_moves)):
                if move == valid_moves[i]:
                    gamestate.make_move(valid_moves[i])
                    moveMade = True

            if moveMade:
                valid_moves, checkmate, stalemate = gamestate.get_valid_moves()
                moveMade = False

            printBoard(gamestate.board)
            if checkmate or stalemate:
                running = False

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    FUNCTION_MAP = {'gui' : playGUI, 'cmd' : playTerminal}

    command_help = "gui: play with a mouse on a GUI interface.\ncmd: play on terminal with traditional chess notation."
    parser.add_argument('command', choices=FUNCTION_MAP.keys(), help=command_help)

    parser.add_argument("--against", action="store_true", help="Play against the AI algorithm.")
    parser.add_argument("--selfplay", action="store_true", help="Have the engine against itself.")
    parser.add_argument('--algo',
                    default=["min-max"],
                    help='Enable a specific algorithm to be used as the backend for the engine.\nOptions:\nmin-max[default]\nalpha-beta\n',
                    type=str,
                    nargs=1
                    )

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    args = parser.parse_args()

    against, selfplay, algo = args.against, args.selfplay, args.algo[0]

    playMode = FUNCTION_MAP[args.command]
    playMode(against, selfplay, algo)
        

if __name__ == "__main__":
    main()
