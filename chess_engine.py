class gamestate():
    def __init__(self):
        self.board = [
                        ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
                        ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                        ['--', '--', '--', '--', '--', '--', '--', '--'],
                        ['--', '--', '--', '--', '--', '--', '--', '--'],
                        ['--', '--', '--', '--', '--', '--', '--', '--'],
                        ['--', '--', '--', '--', '--', '--', '--', '--'],
                        ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                        ['wr', 'wn', 'wb', 'wk', 'wq', 'wb', 'wn', 'wr']
                     ]
        self.white_move = True
        self.move_log = []
        self.move_functions = {'p': self.get_pawn_moves, 'q': self.get_queen_moves, 'k':self.get_king_moves, 
                               'n':self.get_knight_moves, 'r':self.get_rook_moves, 'b':self.get_bishop_moves}

    def make_move(self, move):
        #make old spot blank
        #make new spot equal to piece
        #white move is false
        self.board[move.start_square_row][move.start_square_column] = '--'
        self.board[move.end_square_row][move.end_square_column] = move.piece_moved
        self.move_log.append(move)
        
        self.white_move = not self.white_move

    def undo_move(self):
        if len(self.move_log) != 0:
            last_move = self.move_log.pop()
            self.board[last_move.start_square_row][last_move.start_square_column] = last_move.piece_moved
            self.board[last_move.end_square_row][last_move.end_square_column] = last_move.piece_captured
            self.white_move = not self.white_move

    def get_valid_moves(self):
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                if (turn == 'w' and self.white_move) or (turn == 'b' and not self.white_move):
                    self.move_functions[piece](r, c, moves)
        return moves
    def get_pawn_moves(self, r, c, moves):
        if self.white_move: #white moves go forward by subtraction
            #blank move
            if self.board[r - 1][c] == '--': #1 square move
                moves.append(move((r,c),(r-1,c), self.board))
                if r == 6 and self.board[r - 2][c] == '--': #2 square move
                    moves.append(move((r,c),(r-2,c),self.board))
            
            #capture moves. can only capture diagonally and cant go off the board
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(move((r,c),(r-1,c-1),self.board))
            if c+1 < len(self.board):   
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(move((r,c),(r-1,c+1),self.board))

        if not self.white_move:
            if self.board[r + 1][c] == '--':
                moves.append(move((r,c),(r+1,c), self.board))
                if r == 1 and self.board[r + 2][c] == '--':
                    moves.append(move((r,c),(r+2,c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(move((r,c),(r+1,c-1),self.board))
            if c+1 < len(self.board):    
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(move((r,c),(r+1,c+1),self.board))

    def get_rook_moves(self, r, c, moves):
        #something is bugged in here
        #ill try again later
        print("made it to rook")
        r_place = r
        c_place = c
        if self.white_move:
            print("made it to white")
            for x in reversed(range(r_place)):
                if self.board[x][c][0] == 'b' or self.board[x][c][0] == 'w':
                    break
                if self.board[x][c][0] == '--':
                    print("appended x")
                    moves.append(move((r,c),(x,c),self.board))
            for x2 in range(7 - r_place):
                if self.board[x2][c][0] == 'b' or self.board[x2][c][0] == 'w':
                    break
                if self.board[x2][c][0]=='--':
                    print("appended x2")
                    moves.append(move((r,c),(x2,c),self.board))
            print("made it to reversed y")
            for y in reversed(range(c_place)):
                print("inside reversed")
                print(r)
                print(y)
                if self.board[r][y][0] == '--':# or self.board[r][y][0] == 'w':
                    print("inside break")
                    #break
                elif self.board[r][y][0]=='--':
                    print("appended y")
                    moves.append(move((r,c),(r,y),self.board))
                    print(r)
                    print(y)
            for y2 in range(7-c_place):
                if self.board[r][y2][0]=='b' or self.board[r][y2][0]=='w':
                    break
                if self.board[r][y2][0]=='--':
                    print("appended y2")
                    moves.append(move((r,c),(r,y2),self.board))
            
        #every spot open to its:
            #left
            #right
            #up
            #down
        #no diagonals
            #has to stop at the first taken spot closest to the piece both left and right
            #cant do regular loop bc then u can slide the rook through a piece

    def get_queen_moves(self, r, c, moves):
        #moves the same as a bishop and a rook. so does this work?
        self.move_functions["b"](r, c, moves)
        self.move_functions["r"](r, c, moves)

    def get_bishop_moves(self, r, c, moves):
        pass 
    def get_knight_moves(self, r, c, moves):
        if self.white_move:        
            #up 2 left 1 x
            #up 2 right 1 x
            #down 2 right 1 x
            #down 2 left 1 x
            #left 2 down 1 x
            #left 2 up 1 x
            #right 2 up 1 x
            #right 2 down 1

            if c + 1 < 7:
                if r-2>=0:
                    if self.board[r-2][c+1]=='--' or self.board[r-2][c+1][0]=='b':
                        moves.append(move((r,c),(r-2,c+1),self.board))
                if r+2 < len(self.board[0]):
                    if self.board[r+2][c+1]=='--' or self.board[r-2][c+1][0]=='b':
                        moves.append(move((r,c),(r+2,c+1),self.board))
                    
            if c - 1 >= 0:
                if r-2>=0:
                    if self.board[r-2][c-1]=='--' or self.board[r-2][c-1][0]=='b':
                        moves.append(move((r,c),(r-1,c-1),self.board))
                if r+2 < len(self.board[0]):
                    if self.board[r+2][c-1]=='--' or self.board[r-2][c-1][0]=='b':
                        moves.append(move((r,c),(r+2,c-1),self.board))
            if c + 2 < 7:
                if r-1>=0:
                    if self.board[r-1][c+2]=='--' or self.board[r-1][c+2][0]=='b':
                        moves.append(move((r,c),(r-1,c+2),self.board))
                if r+1 < len(self.board[0]):
                    if self.board[r+1][c+2]=='--' or self.board[r+1][c+2][0]=='b':
                        moves.append(move((r,c),(r+1,c+2),self.board))
            if c - 2 >= 0:
                if r-1>=0:
                    if self.board[r-1][c-2]=='--' or self.board[r-1][c-2][0]=='b':
                        moves.append(move((r,c),(r-1,c-2),self.board))
                if r+1 < len(self.board[0]):
                    if self.board[r+1][c-2]=='--' or self.board[r+1][c-2][0]=='b':
                        moves.append(move((r,c),(r+1,c-2),self.board))
        if not self.white_move:        
            if c + 1 < 7:
                if r-2 < len(self.board[0]):
                    if self.board[r-2][c+1]=='--' or self.board[r-2][c+1][0]=='b':
                        moves.append(move((r,c),(r-2,c+1),self.board))
                if r+2 >= 0:
                    if self.board[r+2][c+1]=='--' or self.board[r-2][c+1][0]=='b':
                        moves.append(move((r,c),(r+2,c+1),self.board))
                    
            if c - 1 >= 0:
                if r-2 < len(self.board[0]):
                    if self.board[r-2][c-1]=='--' or self.board[r-2][c-1][0]=='b':
                        moves.append(move((r,c),(r-1,c-1),self.board))
                if r+2 >= 0:
                    if self.board[r+2][c-1]=='--' or self.board[r-2][c-1][0]=='b':
                        moves.append(move((r,c),(r+2,c-1),self.board))
            if c + 2 < 7:
                if r-1 < len(self.board[0]):
                    if self.board[r-1][c+2]=='--' or self.board[r-1][c+2][0]=='b':
                        moves.append(move((r,c),(r-1,c+2),self.board))
                if r+1 >= 0:
                    if self.board[r+1][c+2]=='--' or self.board[r+1][c+2][0]=='b':
                        moves.append(move((r,c),(r+1,c+2),self.board))
            if c - 2 >= 0:
                if r-1 < len(self.board[0]):
                    if self.board[r-1][c-2]=='--' or self.board[r-1][c-2][0]=='b':
                        moves.append(move((r,c),(r-1,c-2),self.board))
                if r+1 >= 0:
                    if self.board[r+1][c-2]=='--' or self.board[r+1][c-2][0]=='b':
                        moves.append(move((r,c),(r+1,c-2),self.board))
            
    def get_king_moves(self, r, c, moves):
        #left 1
            #down 1
            #same row 
            #up 1
        #right 1
            #down 1
            #same row
            #up 1
        if self.white_move: #white moves go forward by subtraction
            if self.board[r - 1][c] == '--' or self.board[r-1][c]=='b':
                moves.append(move((r,c),(r-1,c), self.board)) 
            if c-1 >= 0:
                if r-1>=0:
                    if self.board[r-1][c-1][0] == 'b' or self.board[r-1][c-1]=='--':
                        moves.append(move((r,c),(r-1,c-1),self.board))
                if r+1<len(self.board[0]):
                    if self.board[r+1][c-1] == '--' or self.board[r+1][c-1][0] == 'b':
                        moves.append(move((r,c),(r+1,c-1), self.board))
            if c+1 < len(self.board):   
                if r-1>=0:    
                    if self.board[r-1][c+1][0] == 'b' or self.board[r-1][c+1]=='--':
                        moves.append(move((r,c),(r-1,c+1),self.board))
                if r+1<len(self.board[0]): 
                    if self.board[r+1][c+1]=='--' or self.board[r+1][c+1][0]=='b':
                         moves.append(move((r,c),(r-1,c+1),self.board))

        if not self.white_move:
            if self.board[r + 1][c] == '--':
                moves.append(move((r,c),(r+1,c), self.board))
                if r == 1 and self.board[r + 2][c] == '--':
                    moves.append(move((r,c),(r+2,c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(move((r,c),(r+1,c-1),self.board))
            if c+1 < len(self.board):    
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(move((r,c),(r+1,c+1),self.board))


 #       if self.white_move:
 #           if c-1>=0:
 #               if r-1<=0:
 #                   if self.board[r-1][c-1]=='--' or self.board[r-1][c-1]=='b':
 #                       moves.append(move((r,c),(r-1,c-1), self.board))
 #               if r+1 < len(self.board[0]):
 #                   if self.board[r+1][c-1]=='--' or self.board[r+1][c-1]=='b':
 #                       moves.append(move((r,c),(r+1,c-1),self.board))
#                if self.board[r][c-1]=='--' or self.board[r][c-1]=='b':
 #                   moves.append(move((r,c),(r,c-1),self.board))
  #          if c+1<7:
   #             if r-1>=-0:
    #                if self.board[r-1][c+1]=='--' or self.board[r-1][c+1]=='b':
     #                   moves.append(move((r,c),(r-1,c+1), self.board))
      #          if r+1<len(self.board[0]):
       #                 if self.board[r+1][c+1]=='--' or self.board[r+1][c+1]=='b':
        #                    moves.append(move((r,c),(r+1,c+1),self.board))
         #       if self.board[r][c+1]=='--' or self.board[r][c+1]=='b':
          #          moves.append(move((r,c),(r,c+1),self.board))

class move():
    #map key values 
    row_ranks = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    row_to_rank = {v: k for k, v in row_ranks.items()}

    column_files = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    column_to_file = {v: k for k, v in column_files.items()}

    def __init__(self, start_square, end_square, board):
        self.start_square_row = start_square[0]
        self.start_square_column = start_square[1]
        self.end_square_row = end_square[0]
        self.end_square_column = end_square[1]

        self.piece_moved = board[self.start_square_row][self.start_square_column]
        self.piece_captured = board[self.end_square_row][self.end_square_column]
            
        self.moveID = self.start_square_row * 1000 + self.start_square_column * 100 + self.end_square_row * 10 + self.end_square_column

    "overriding equal"
    def __eq__(self, other):
        if isinstance(other, move):
            return self.moveID == other.moveID
        return False    

    def get_chess_notation(self):
        return self.get_rank_file(self.start_square_row, self.start_square_column) + self.get_rank_file(self.end_square_row, self.end_square_column)
    def get_rank_file(self, row, column):
        return self.column_to_file[column] + self.row_to_rank[row]

