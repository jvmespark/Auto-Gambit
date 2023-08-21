
from copy import deepcopy
import random

# NOTE: Likely crashing when it calculates a checkmate in 3 and shuts down the program prematurely? working theory

def minMax(gamestate, N):
    # call at move state only. later look to abstract to classes but for now just build this one function that is called only on its move.
    blackScoring = {'bp': -1,
          'bn': -3,
          'bb': -3,
          'br': -5,
          'bq': -9,
          'bk': 0,
          'wp': 1,
          'wn': 3,
          'wb': 3,
          'wr': 5,
          'wq': 9,
          'wk': 0,
          }
    scoring = blackScoring
    def eval_board(gamestate):
        score = 0
        board = gamestate.board
        for r in board:
            for c in r:
                if c != "--":
                    score += scoring[str(c)]
        return score
    
    moves, checkmate, stalemate = gamestate.get_valid_moves()
    if checkmate or stalemate or N == 0:
        return None
    best_move = random.choice(moves)
    scores = []

    for move in moves:
        temp = deepcopy(gamestate)              
        temp.make_move(move)
        if N>1:
            temp_best_move = minMax(temp,N-1)
            if not temp_best_move == None:
                temp.make_move(temp_best_move)

        scores.append(eval_board(temp))

    #print(N, len(moves), checkmate, stalemate, len(scores), scores)

    if not gamestate.moveState: #black turn
        best_move = moves[scores.index(max(scores))]

    else: # white turn
        best_move = moves[scores.index(min(scores))]

    return best_move