# terminal and gui core classes

import chess_engine as engine
import algo_engine
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import random
from multiprocessing import Process, Queue
    
player_one = True # human white
player_two = False # human black

class gui():
    def __init__(self, gamestate, computer, algo):
        self.gamestate = gamestate
        self.computer = computer
        self.algo = algo
        self.WIDTH = self.HEIGHT = 500
        self.DIMENSION = 8
        self.PIECE_SIZE = self.HEIGHT / self.DIMENSION
        self.MAX_FPS = 15
        self.IMAGES = {}

    def play(self):
        valid_moves, checkmate, stalemate = self.gamestate.get_valid_moves()
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        clock = pygame.time.Clock()
        pygame.display.set_caption("Silver Chess")
        self.load_images()
        moveMade = False #until a valid move is made, then you shouldnt regenerate an expensive function like get valid moves
        ai_thinking = False
        move_finder_process = None
        move_undone = False

        #tuple
        square_selected = ()
        #array
        player_clicks = []
        
        if self.computer != "disabled":
            AI = algo_engine.algo(self.algo)
            AI.depth = 3
        
        running = True
        checkmate, stalemate = False, False
        while (running):
                if self.computer == "autoplay":
                    if not ai_thinking:
                        ai_thinking = True
                        return_queue = Queue()  # used to pass data between threads
                        move_finder_process = Process(target=AI.makeMove, args=(self.gamestate, valid_moves, return_queue))
                        move_finder_process.start()

                    if not move_finder_process.is_alive():
                        ai_move = return_queue.get()
                        if ai_move is None:
                            ai_move = random.choice(valid_moves)
                        print(ai_move.get_chess_notation())
                        self.gamestate.make_move(ai_move)
                        moveMade = True
                        ai_thinking = False

                human_turn = True
                if self.computer == "against":
                    human_turn = (self.gamestate.white_move and player_one) or (not self.gamestate.white_move and player_two)

                if self.computer != "autoplay":
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            #Needs to:
                            #-Move the piece to the next clicked spot IF the spot is empty --
                            #-deselect the piece if the player clicks the same piece again
                            mouse_location = pygame.mouse.get_pos()
                            column = int(mouse_location[0] // self.PIECE_SIZE)
                            row = int(mouse_location[1] // self.PIECE_SIZE)

                            if  square_selected == (row, column):
                                square_selected = ()
                                player_clicks = []
                            else:
                                square_selected = (row, column)
                                player_clicks.append(square_selected)
                            if len(player_clicks) == 2 and human_turn:
                                move = engine.move(player_clicks[0], player_clicks[1], self.gamestate.board)
                                print(move.get_chess_notation())
                                for i in range(len(valid_moves)):
                                    if move == valid_moves[i]:
                                        self.gamestate.make_move(valid_moves[i])
                                        moveMade = True
                                
                                        square_selected = ()
                                        player_clicks = []
                                if not moveMade:
                                    player_clicks = [square_selected]
                        
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_u:
                                self.gamestate.undo_move()
                                valid_moves, checkmate, stalemate = self.gamestate.get_valid_moves()
                                if ai_thinking:
                                    move_finder_process.terminate()
                                    ai_thinking = False
                                moveMade = True
                                move_undone = True

                    if self.computer == "against" and not human_turn and not move_undone:
                        if not ai_thinking:
                            ai_thinking = True
                            return_queue = Queue()  # used to pass data between threads
                            move_finder_process = Process(target=AI.makeMove, args=(self.gamestate, valid_moves, return_queue))
                            move_finder_process.start()

                        if not move_finder_process.is_alive():
                            ai_move = return_queue.get()
                            if ai_move is None:
                                ai_move = random.choice(valid_moves)
                            print(ai_move.get_chess_notation())
                            self.gamestate.make_move(ai_move)
                            moveMade = True
                            ai_thinking = False

                if moveMade:
                    valid_moves, checkmate, stalemate = self.gamestate.get_valid_moves()
                    moveMade = False
                    move_undone = False

                self.load_gamestate(screen, self.gamestate)
                clock.tick(self.MAX_FPS)
                pygame.display.flip()

                if checkmate or stalemate:
                    time.sleep(5) # let the winner bask in their glory for 5 seconds then close game
                    running = False
                    
    #king and knight are the same initial. So Im delegating knight to night
    def load_images(self):
        pieces = {'wk', 'wr', 'wb', 'wq', 'wn', 'wp', 'bk', 'br', 'bb', 'bq', 'bn', 'bp'}
        for piece in pieces:
            #Image['wk'] = white king
            self.IMAGES[piece] = pygame.transform.scale(pygame.image.load("assets/" + piece + ".png"), (self.PIECE_SIZE, self.PIECE_SIZE))
        self.IMAGES['board'] = pygame.transform.scale(pygame.image.load("assets/board.png"), (self.WIDTH, self.HEIGHT))

    def load_gamestate(self, screen, gamestate):
        self.load_board(screen)
        self.load_pieces(screen, gamestate.board)

    def load_board(self, screen):
        screen.blit(self.IMAGES['board'], (0, 0))

    def load_pieces(self, screen, board):
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                piece = board[row][column]
                if piece != '--':
                    screen.blit(self.IMAGES[piece], pygame.Rect(column * self.PIECE_SIZE, row * self.PIECE_SIZE, self.PIECE_SIZE, self.PIECE_SIZE))



##############################################################################################################################################################



# NOTE: needs to be update with upgrades i've given to gui. PRIORITY: LOW

class cmd():
    def __init__(self, gamestate, computer, algo):
        self.gamestate = gamestate
        self.computer = computer
        self.algo = algo
    
    def play(self):
        valid_moves, checkmate, stalemate = self.gamestate.get_valid_moves()
        moveMade = False #until a valid move is made, then you shouldnt regenerate an expensive function like get valid moves

        if self.computer != "disabled":
            AI = algo_engine.algo(self.algo)
            AI.depth = 3

        self.printBoard(self.gamestate.board)
        checkmate, stalemate = False, False
        
        running = True
        while (running):
                if self.computer != "disabled":
                    move = AI.makeMove(self.gamestate, 1, self.gamestate.white_move)
                    self.gamestate.make_move(move)
                    moveMade = True

                if self.computer != "autoplay":
                    # NOTE: this current implementation of user input parsing is wrong, i should write a finite automaton to solve this
                    userMove = input(">> ")
                    if not self.validNotation(userMove):
                        print("ERROR: Invalid Notation")
                        userMove = input(">> ")
                    if userMove == "u":
                        self.gamestate.undo_move()
                        valid_moves, checkmate, stalemate = self.gamestate.get_valid_moves()
                    if userMove == "q":
                        exit(0)

                    if self.gamestate.moveState(): # white turn, so player goes
                        move = engine.move.notated(userMove, self.gamestate.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                self.gamestate.make_move(valid_moves[i])
                                moveMade = True

                if moveMade:
                    valid_moves, checkmate, stalemate = self.gamestate.get_valid_moves()
                    moveMade = False

                self.printBoard(self.gamestate.board)
                if checkmate or stalemate:
                    running = False

    def printBoard(self, board):
        pattern = 0
        for r in board:
            for c in r:
                if c == "--" and pattern%2!=0: print("##", end =" ")
                elif c == "--" and pattern%2==0: print("  ", end=" ")
                else: print(c, end =" ")
                pattern += 1
            print("\n")
            pattern += 1

    def validNotation(self, userMove):
        return False if userMove[0].lower() not in "abcdefgh" or int(userMove[1]) not in range(9) or userMove[2].lower() not in "abcdefgh" or int(userMove[3]) not in range(9) else True


