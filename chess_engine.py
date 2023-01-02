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
                        ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
                     ]
        self.white_move = True
        self.move_log = []
        self.move_functions = {'p': self.get_pawn_moves, 'q': self.get_queen_moves, 'k':self.get_king_moves, 
                               'n':self.get_knight_moves, 'r':self.get_rook_moves, 'b':self.get_bishop_moves}
        #keep track of king pos
        self.white_king_location = (7,4)
        self.black_king_location = (0,4)

        #no valid moves and the king is in check
        self.checkmate = False
        #no valid moves and the kings is not in check
        self.statemate = False
        self.enpassant_coordinates = () #coordinates where empassant is possible

    def make_move(self, move):
        #make old spot blank
        #make new spot equal to piece
        #white move is false
        self.board[move.start_square_row][move.start_square_column] = '--'
        self.board[move.end_square_row][move.end_square_column] = move.piece_moved
        self.move_log.append(move)
        
        #update king pos
        if move.piece_moved == 'wk':
            self.white_king_location = (move.end_square_row, move.end_square_column)
        elif move.piece_moved == 'bk':
            self.black_king_location = (move.end_square_row, move.end_square_column)

        if move.pawn_promotion:
#            change = input("Change pawn to: 'q', 'r'\n")
            self.board[move.end_square_row][move.end_square_column] = move.piece_moved[0] + 'q'

        if move.enpassant:
            self.board[move.start_square_row][move.end_square_column] = '--'

        if move.piece_moved[1] == 'p' and abs(move.start_square_row - move.end_square_row) == 2:
            self.enpassant_coordinates=((move.start_square_row+move.end_square_row)//2,move.end_square_column)
        else:
            self.enpassant_coordinates=()

        self.white_move = not self.white_move

    def undo_move(self):
        if len(self.move_log) != 0:
            last_move = self.move_log.pop()
            self.board[last_move.start_square_row][last_move.start_square_column] = last_move.piece_moved
            self.board[last_move.end_square_row][last_move.end_square_column] = last_move.piece_captured
       
            #update kings pos
            if last_move.piece_moved == 'wk':
                self.white_king_location = (last_move.start_square_row, last_move.start_square_column)
            elif last_move.piece_moved == 'bk':
                self.black_king_location = (last_move.start_square_row, last_move.start_square_column)
            
            if last_move.enpassant:
                self.board[last_move.end_square_row][last_move.end_square_column]='--'
                self.board[last_move.start_square_row][last_move.end_square_column]=last_move.piece_captured
                self.enpassant_coordinates=(last_move.end_square_row,last_move.end_square_column)
            if last_move.piece_moved[1]=='p' and abs(last_move.start_square_row-last_move.end_square_row)==2:
                self.enpassant_coordinates=()

            self.white_move = not self.white_move
    
    def get_valid_moves(self):
        temp_enpassant = self.enpassant_coordinates
        moves = self.get_all_possible_moves()
        for i in reversed(range(len(moves))):
            self.make_move(moves[i])
            #make move swaps moves, but we need to still check the move players, so we switch it back
            self.white_move = not self.white_move
            #if self.in_check():
            #    #if king is under attack, its not a valid move
            #    moves.remove(moves[i])
            self.white_move = not self.white_move
            self.undo_move() #cancel out the make move
        
            if len(moves)==0:
                if self.in_check():
                    self.checkmate = True
                else:
                    self.stalemate = True
            else:
                self.checkmate = False
                self.stalemate = False
        
        self.enpassant_coordinates = temp_enpassant
        return moves

    def in_check(self):
        if self.white_move:
            return self.square_attacked(self.white_king_location[0], self.white_king_location[1])
        if not self.white_move:
            return self.square_attacked(self.black_king_location[0], self.black_king_location[1])

    def square_attacked(self, r, c):
        self.white_move = not self.white_move
        enemy_moves = self.get_all_possible_moves()
        self.white_move = not self.white_move
        for move in enemy_moves:
            if move.end_square_row == r and move.end_square_column == c:
                return True
        return False
        
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
                elif (r-1,c-1)==self.enpassant_coordinates:
                    moves.append(move((r,c),(r-1,c-1),self.board,enpassant_possible=True))
            if c+1 < len(self.board):   
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1)==self.enpassant_coordinates:
                    moves.append(move((r,c),(r-1,c+1),self.board,enpassant_possible=True))
 
        if not self.white_move:
            if self.board[r + 1][c] == '--':
                moves.append(move((r,c),(r+1,c), self.board))
                if r == 1 and self.board[r + 2][c] == '--':
                    moves.append(move((r,c),(r+2,c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1)==self.enpassant_coordinates:
                    moves.append(move((r,c),(r+1,c-1),self.board,enpassant_possible=True))
 
            if c+1 < len(self.board):    
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(move((r,c),(r+1,c+1),self.board))
                elif (r+1,c+1)==self.enpassant_coordinates:
                    moves.append(move((r,c),(r+1,c+1),self.board,enpassant_possible=True))
 
    def get_rook_moves(self, r, c, moves):

        #every spot open to its:
            #left
            #right
            #up
            #down
        #no diagonals
            #has to stop at the first taken spot closest to the piece both left and right
            #first taken spot can be captured tho
            #cant do regular loop bc then u can slide the rook through a piece
        
        #CURRENT PROBLEM:
            #rook can take its own side piece
            #this is bc i said if its w OR b
            #i can fix this by splitting the up
            #w being only break

        if self.white_move:
            for y in reversed(range(r)):
                if self.board[y][c][0] == 'b':
                    moves.append(move((r,c),(y,c),self.board))
                    break
                if self.board[y][c][0] == 'w':
                    break
                if self.board[y][c] == '--':
                    moves.append(move((r,c),(y,c),self.board))
            for y2 in range(r + 1, 8): #original problem was that it was breaking at its own piece
                if self.board[y2][c][0] == 'b':
                    moves.append(move((r,c),(y2,c),self.board))
                    break 
                if self.board[y2][c][0] == 'w':
                    break
                if self.board[y2][c]=='--':
                    moves.append(move((r,c),(y2,c),self.board))

            for x in reversed(range(c)):
                if self.board[r][x][0] == 'b':
                    moves.append(move((r,c),(r,x),self.board))
                    break 
                if self.board[r][x][0] == 'w':
                    break
                if self.board[r][x]=='--':
                    moves.append(move((r,c),(r,x),self.board))
            for x2 in range(c + 1, 8):
                if self.board[r][x2][0]=='b':
                    moves.append(move((r,c),(r,x2),self.board))
                    break 
                if self.board[r][x2][0] == 'w':
                    break;
                if self.board[r][x2]=='--':
                    moves.append(move((r,c),(r,x2),self.board))

        if not self.white_move:
            for y in reversed(range(r)):
                if self.board[y][c][0] == 'w':
                    moves.append(move((r,c),(y,c),self.board))
                    break
                if self.board[y][c][0] == 'b':
                    break
                if self.board[y][c] == '--':
                    moves.append(move((r,c),(y,c),self.board))
            for y2 in range(r + 1, 8):
                if self.board[y2][c][0] == 'w':
                    moves.append(move((r,c),(y2,c),self.board))
                    break 
                if self.board[y2][c][0] == 'b':
                    break
                if self.board[y2][c]=='--':
                    moves.append(move((r,c),(y2,c),self.board))
            for x in reversed(range(c)):
                if self.board[r][x][0] == 'w':
                    moves.append(move((r,c),(r,x),self.board))
                    break
                if self.board[r][x][0] == 'b':
                    break
                if self.board[r][x]=='--':
                    moves.append(move((r,c),(r,x),self.board))
            for x2 in range(c + 1, 8):
                if self.board[r][x2][0]=='w':
                    moves.append(move((r,c),(r,x2),self.board))
                    break 
                if self.board[r][x2][0] == 'b':
                    break
                if self.board[r][x2]=='--':
                    moves.append(move((r,c),(r,x2),self.board))

    def get_queen_moves(self, r, c, moves):
        #moves the same as a bishop and a rook. so does this work?
        self.move_functions["b"](r, c, moves)
        self.move_functions["r"](r, c, moves)

    def get_bishop_moves(self, r, c, moves):
        
        #r and c move at the same rate at the same time, diagonally
        #stop at first piece
        #first piece can be captured
        #can go backwards

        #current problem: its not working lol

        if self.white_move:
            #left up
            for x, y in zip(reversed(range(c)), reversed(range(r))):
                if self.board[y][x][0]=='b':
                    moves.append(move((r,c),(y,x),self.board))
                    break
                if self.board[y][x][0] == 'w':
                    break
                if self.board[y][x]=='--':
                    moves.append(move((r,c),(y,x),self.board))

           #right up
            for x2, y2 in zip(range(c + 1, 8), reversed(range(r))):
                if self.board[y2][x2][0]=='b':
                    moves.append(move((r,c),(y2,x2),self.board))
                    break
                if self.board[y2][x2][0] == 'w':
                    break
                if self.board[y2][x2]=='--':
                    moves.append(move((r,c),(y2,x2),self.board))

           #left down
            for x3, y3 in zip(reversed(range(c)), range(r + 1, 8)):
                if self.board[y3][x3][0]=='b':
                    moves.append(move((r,c),(y3,x3),self.board))
                    break
                if self.board[y3][x3][0]=='w':
                    break
                if self.board[y3][x3]=='--':
                    moves.append(move((r,c),(y3,x3),self.board))

           #right down
            for x4, y4 in zip(range(c + 1, 8), range(r + 1, 8)):
                if self.board[y4][x4][0]=='b':
                    moves.append(move((r,c),(y4,x4),self.board))
                    break
                if self.board[y4][x4][0]=='w':
                    break
                if self.board[y4][x4]=='--':
                    moves.append(move((r,c),(y4,x4),self.board))

        if not self.white_move:
            #left down
            for x, y in zip(reversed(range(c)), range(r + 1, 8)):
                if self.board[y][x][0]=='w':
                    moves.append(move((r,c),(y,x),self.board))
                    break
                if self.board[y][x][0] == 'b':
                    break
                if self.board[y][x]=='--':
                    moves.append(move((r,c),(y,x),self.board))

           #right down
            for x2, y2 in zip(range(c + 1, 8), range(r + 1, 8)):
                if self.board[y2][x2][0]=='w':
                    moves.append(move((r,c),(y2,x2),self.board))
                    break
                if self.board[y2][x2][0] == 'b':
                    break
                if self.board[y2][x2]=='--':
                    moves.append(move((r,c),(y2,x2),self.board))

           #left up
            for x3, y3 in zip(reversed(range(c)), reversed(range(r))):
                if self.board[y3][x3][0]=='w':
                    moves.append(move((r,c),(y3,x3),self.board))
                    break
                if self.board[y3][x3][0]=='b':
                    break
                if self.board[y3][x3]=='--':
                    moves.append(move((r,c),(y3,x3),self.board))

           #right up
            for x4, y4 in zip(range(c + 1, 8), reversed(range(r))):
                if self.board[y4][x4][0]=='w':
                    moves.append(move((r,c),(y4,x4),self.board))
                    break
                if self.board[y4][x4][0]=='b':
                    break
                if self.board[y4][x4]=='--':
                    moves.append(move((r,c),(y4,x4),self.board))

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

            #right 1
            if c + 1 < 7:
                if r-2>=0:
                    if self.board[r-2][c+1]=='--' or self.board[r-2][c+1][0]=='b':
                        moves.append(move((r,c),(r-2,c+1),self.board))
                if r+2 < len(self.board[0]):
                    if self.board[r+2][c+1]=='--' or self.board[r-2][c+1][0]=='b':
                        moves.append(move((r,c),(r+2,c+1),self.board))
            #left 1        
            if c - 1 >= 0:
                if r-2>=0:
                    if self.board[r-2][c-1]=='--' or self.board[r-2][c-1][0]=='b':
                        moves.append(move((r,c),(r-2,c-1),self.board))
                if r+2 < len(self.board[0]):
                    if self.board[r+2][c-1]=='--' or self.board[r-2][c-1][0]=='b':
                        moves.append(move((r,c),(r+2,c-1),self.board))
            #right 2
            if c + 2 < 7:
                if r-1>=0:
                    if self.board[r-1][c+2]=='--' or self.board[r-1][c+2][0]=='b':
                        moves.append(move((r,c),(r-1,c+2),self.board))
                if r+1 < len(self.board[0]):
                    if self.board[r+1][c+2]=='--' or self.board[r+1][c+2][0]=='b':
                        moves.append(move((r,c),(r+1,c+2),self.board))
            #left 2
            if c - 2 >= 0:
                if r-1>=0:
                    if self.board[r-1][c-2]=='--' or self.board[r-1][c-2][0]=='b':
                        moves.append(move((r,c),(r-1,c-2),self.board))
                if r+1 < len(self.board[0]):
                    if self.board[r+1][c-2]=='--' or self.board[r+1][c-2][0]=='b':
                        moves.append(move((r,c),(r+1,c-2),self.board))
        if not self.white_move:    
            #right 1
            if c + 1 < 7:
                if r-2 >= 0:
                    if self.board[r-2][c+1]=='--' or self.board[r-2][c+1][0]=='w':
                        moves.append(move((r,c),(r-2,c+1),self.board))
                if r+2 < len(self.board[0]):
                    if self.board[r+2][c+1]=='--' or self.board[r-2][c+1][0]=='w':
                        moves.append(move((r,c),(r+2,c+1),self.board))
            #left 1         
            if c - 1 >= 0:
                if r-2 >= 0:
                    if self.board[r-2][c-1]=='--' or self.board[r-2][c-1][0]=='w':
                        moves.append(move((r,c),(r-2,c-1),self.board))
                if r+2 < len(self.board[0]):
                    if self.board[r+2][c-1]=='--' or self.board[r+2][c-1][0]=='w':
                        moves.append(move((r,c),(r+2,c-1),self.board))
            #right 2
            if c + 2 < 7:
                if r-1 >= 0:
                    if self.board[r-1][c+2]=='--' or self.board[r-1][c+2][0]=='w':
                        moves.append(move((r,c),(r-1,c+2),self.board))
                if r+1 < len(self.board[0]):
                    if self.board[r+1][c+2]=='--' or self.board[r+1][c+2][0]=='w':
                        moves.append(move((r,c),(r+1,c+2),self.board))
            #left 2
            if c - 2 >= 0:
                if r-1 >= 0:
                    if self.board[r-1][c-2]=='--' or self.board[r-1][c-2][0]=='w':
                        moves.append(move((r,c),(r-1,c-2),self.board))
                if r+1 < len(self.board[0]):
                    if self.board[r+1][c-2]=='--' or self.board[r+1][c-2][0]=='w':
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
            if r-1>=0:
                if self.board[r - 1][c] == '--' or self.board[r-1][c]=='b':
                    moves.append(move((r,c),(r-1,c), self.board)) 
            if r+1<len(self.board[0]):
                if self.board[r + 1][c] == '--' or self.board[r+1][c]=='b':
                    moves.append(move((r,c),(r+1,c), self.board)) 
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
                         moves.append(move((r,c),(r+1,c+1),self.board))

        if not self.white_move:
            if r-1>=0:
                if self.board[r - 1][c] == '--' or self.board[r-1][c]=='w':
                    moves.append(move((r,c),(r-1,c), self.board)) 
            if r+1<len(self.board[0]):
                if self.board[r + 1][c] == '--' or self.board[r+1][c]=='w':
                    moves.append(move((r,c),(r+1,c), self.board)) 
            if c-1 >= 0:
                if r-1>=0:
                    if self.board[r-1][c-1][0] == 'w' or self.board[r-1][c-1]=='--':
                        moves.append(move((r,c),(r-1,c-1),self.board))
                if r+1<len(self.board[0]):
                    if self.board[r+1][c-1] == '--' or self.board[r+1][c-1][0] == 'w':
                        moves.append(move((r,c),(r+1,c-1), self.board))
            if c+1 < len(self.board):   
                if r-1>=0:    
                    if self.board[r-1][c+1][0] == 'w' or self.board[r-1][c+1]=='--':
                        moves.append(move((r,c),(r-1,c+1),self.board))
                if r+1<len(self.board[0]): 
                    if self.board[r+1][c+1]=='--' or self.board[r+1][c+1][0]=='w':
                         moves.append(move((r,c),(r+1,c+1),self.board))
class move():
    #map key values 
    row_ranks = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    row_to_rank = {v: k for k, v in row_ranks.items()}

    column_files = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    column_to_file = {v: k for k, v in column_files.items()}

    def __init__(self, start_square, end_square, board, enpassant_possible = False ):
        self.start_square_row = start_square[0]
        self.start_square_column = start_square[1]
        self.end_square_row = end_square[0]
        self.end_square_column = end_square[1]

        self.piece_moved = board[self.start_square_row][self.start_square_column]
        self.piece_captured = board[self.end_square_row][self.end_square_column]

        self.pawn_promotion = False
        if (self.piece_moved == 'wp' and self.end_square_row == 0) or (self.piece_moved == 'bp' and self.end_square_row == 7):
            self.pawn_promotion = True

        self.enpassant = enpassant_possible
        if self.enpassant:
            self.piece_captured='wp' if self.piece_moved=='bp' else 'bp'

        self.moveID = self.start_square_row * 1000 + self.start_square_column * 100 + self.end_square_row * 10 + self.end_square_column

    #overriding equal
    def __eq__(self, other):
        if isinstance(other, move):
            return self.moveID == other.moveID
        return False    

    def get_chess_notation(self):
        return self.get_rank_file(self.start_square_row, self.start_square_column) + self.get_rank_file(self.end_square_row, self.end_square_column)
    def get_rank_file(self, row, column):
        return self.column_to_file[column] + self.row_to_rank[row]

