
from copy import deepcopy
import random
from math import inf, log, sqrt, e
from multiprocessing import Pool
import sys
sys.setrecursionlimit(100000)

############# Alpha Beta Pruning Mini Max

piece_score = {"k": 0, "q": 9, "r": 5, "b": 3, "n": 3, "p": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"wn": knight_scores,
                         "bn": knight_scores[::-1],
                         "wb": bishop_scores,
                         "bb": bishop_scores[::-1],
                         "wq": queen_scores,
                         "bq": queen_scores[::-1],
                         "wr": rook_scores,
                         "br": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)
    # move ordering - implement later //TODO
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score

def scoreBoard(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    if game_state.checkmate:
        if game_state.white_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "k":
                    piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score

    return score

def minMax(gamestate, valid_moves, return_queue):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(gamestate, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if gamestate.white_move else -1)
    return_queue.put(next_move)

############# Monte Carlo Tree Search

class node():
    def __init__(self):
        self.state = None
        self.action = ''
        self.children = set()
        self.parent = None
        self.N = 0
        self.n = 0
        self.v = 0

def ucb1(curr_node):
    ans = curr_node.v+2*(sqrt(log(curr_node.N+e+(10**-6))/(curr_node.n+(10**-10))))
    return ans

def rollout(curr_node):
    valid_moves = curr_node.state.get_valid_moves()
    if(curr_node.state.game_over() or len(valid_moves)==0):
        board = curr_node.state
        if(board.checkmate and board.white_move):
            return (-1,curr_node)
        elif(board.checkmate and not board.white_move):
            return (1,curr_node)
        else:
            return (0.5,curr_node)
    
    #valid_moves = curr_node.state.get_valid_moves()
    #print(len(valid_moves))
    
    for i in valid_moves:
        temp = deepcopy(curr_node.state)
        temp.make_move(i)
        child = node()
        child.state = temp
        child.parent = curr_node
        curr_node.children.add(child)
    rnd_state = random.choice(list(curr_node.children))

    return rollout(rnd_state)

def expand(curr_node,white):
    if(len(curr_node.children)==0):
        return curr_node
    max_ucb = -inf
    if(white):
        idx = -1
        max_ucb = -inf
        sel_child = None
        for i in curr_node.children:
            tmp = ucb1(i)
            if(tmp>max_ucb):
                idx = i
                max_ucb = tmp
                sel_child = i

        return(expand(sel_child,0))

    else:
        idx = -1
        min_ucb = inf
        sel_child = None
        for i in curr_node.children:
            tmp = ucb1(i)
            if(tmp<min_ucb):
                idx = i
                min_ucb = tmp
                sel_child = i

        return expand(sel_child,1)

def rollback(curr_node,reward):
    curr_node.n+=1
    curr_node.v+=reward
    while(curr_node.parent!=None):
        curr_node.N+=1
        curr_node = curr_node.parent
    return curr_node

def monteCarlo(gamestate, valid_moves, return_queue, depth=3):
    curr_node = node()
    curr_node.state = gamestate
    map_state_move = dict()
    for move in valid_moves:
       temp = deepcopy(gamestate)
       temp.make_move(move)
       child = node()
       child.state = temp
       child.parent = curr_node
       curr_node.children.add(child)
       map_state_move[child] = move
    while (depth>0):
        if gamestate.white_move:
            idx = -1
            max_ucb = -inf
            sel_child = None
            for i in curr_node.children:
                tmp = ucb1(i)
                if tmp>max_ucb:
                    idx = i
                    max_ucb = tmp
                    sel_chil = i
            ex_child = expand(sel_child, 0)
            reward, state = rollout(ex_child)
            curr_node = rollback(state, reward)
            depth -= 1
        else:
            idx = -1
            min_ucb = inf
            sel_child = None
            for i in curr_node.children:
                tmp = ucb1(i)
                if(tmp<min_ucb):
                    idx = i
                    min_ucb = tmp
                    sel_child = i

            ex_child = expand(sel_child,1)

            reward,state = rollout(ex_child)

            curr_node = rollback(state,reward)
            depth-=1
        if(gamestate.white_move):
            mx = -inf
            idx = -1
            selected_move = random.choice(valid_moves)
            for i in (curr_node.children):
                tmp = ucb1(i)
                if(tmp>mx):
                    mx = tmp
                    selected_move = map_state_move[i]
            return_queue.put(selected_move)
        else:
            mn = inf
            idx = -1
            selected_move = random.choice(valid_moves)
            for i in (curr_node.children):
                tmp = ucb1(i)
                if(tmp<mn):
                    mn = tmp
                    selected_move = map_state_move[i]
            return_queue.put(selected_move)



###############################################################################

class algo():
    ALGO_MAP = {'min-max': minMax, 'monte-carlo': monteCarlo}
    AI = ALGO_MAP['min-max']
    depth = 1

    def __init__(self, algo):
        self.AI = self.ALGO_MAP[algo]

    def makeMove(self, gamestate, valid_moves, return_queue):
        return self.AI(gamestate, valid_moves, return_queue)
