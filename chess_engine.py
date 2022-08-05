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
    
    def get_chess_notation(self):
        return self.get_rank_file(self.start_square_row, self.start_square_column) + self.get_rank_file(self.end_square_row, self.end_square_column)
    def get_rank_file(self, row, column):
        return self.column_to_file[column] + self.row_to_rank[row]

