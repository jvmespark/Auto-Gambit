
from copy import deepcopy
import random


# add whiteTurn boolean as parameter
def minMax(gamestate, N, whiteMove):
    # call at move state only. later look to abstract to classes but for now just build this one function that is called only on its move.
    blackScoring = {
          'bp': -1,
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
    whiteScoring = {
          'wp': -1,
          'wn': -3,
          'wb': -3,
          'wr': -5,
          'wq': -9,
          'wk': 0,
          'bp': 1,
          'bn': 3,
          'bb': 3,
          'br': 5,
          'bq': 9,
          'bk': 0,
          }
    scoring = blackScoring 
    if whiteMove:
        scoring = whiteScoring
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
            temp_best_move = minMax(temp,N-1, whiteMove)
            if not temp_best_move == None:
                temp.make_move(temp_best_move)

        scores.append(eval_board(temp))

    #print(N, len(moves), checkmate, stalemate, len(scores), scores)


    # this thing is all bugged, not sure why
    if not gamestate.moveState() and not whiteMove: # black turn checking black perspective
        best_move = moves[scores.index(max(scores))]
    if not gamestate.moveState() and whiteMove: # white turn checking black perspective
        best_move = moves[scores.index(min(scores))]
    if gamestate.moveState() and not whiteMove: # black turn checking white perspective
        best_move = moves[scores.index(min(scores))]
    if gamestate.moveState() and whiteMove: # white turn checking white perspective
        best_move = moves[scores.index(max(scores))]

    return best_move



#####################################################################################################################################################

class algo():
    ALGO_MAP = {'min-max': minMax}
    AI = ALGO_MAP['min-max']
    depth = 1

    def __init__(self, algo):
        self.AI = self.ALGO_MAP[algo]

    def makeMove(self, gamestate, depth, whiteMove):
        return self.AI(gamestate, depth, whiteMove)
