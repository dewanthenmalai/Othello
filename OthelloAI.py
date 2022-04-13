import numpy as np
import time
import copy
from Othello import Othello

class OthelloAI:
    
    class MinimaxNode:
        
        def __init__(self, board, value, move):
            self.board = board
            self.value = value
            self.move = move
	
    def __init__(self, AIcolor, heuristic=None):
        self.color = AIcolor
        if heuristic is None:
            self.heuristic = np.full((8,8), 100, dtype=int)
            for i in range(8):
                self.heuristic[0, i] = 200
                self.heuristic[7, i] = 200
                self.heuristic[i, 0] = 200
                self.heuristic[i, 7] = 200
            self.heuristic[0,0] = 500
            self.heuristic[0,7] = 500
            self.heuristic[7,0] = 500
            self.heuristic[7,7] = 500
        else:
            self.heuristic = heuristic
    
    def OppositeColor(self, color):
        if color == 'white':
            return 'black'
        elif color == 'black':
            return 'white'
        else:
            raise RuntimeError("Invalid player color")
	
    def EvaluateHeuristic(self, player, board):
        match player:
            case 'white':
                return np.sum(np.multiply(board.whiteBoard, self.heuristic) - np.multiply(board.blackBoard, self.heuristic))
            case 'black':
                return np.sum(np.multiply(board.blackBoard, self.heuristic) - np.multiply(board.whiteBoard, self.heuristic))
            case _:
                raise RuntimeError("Invalid player")
    
    # need a method that creates a copy of the game state and returns the result of a move
    def ForecastMove(self, board, move, player):
        newGame = Othello()
        newGame.blackBoard = copy.deepcopy(board.blackBoard)
        newGame.whiteBoard = copy.deepcopy(board.whiteBoard)
        return newGame
    
    # Initial call is self.Minimax(origin, maxDepth, -np.inf, np.inf, AIPlayer)
    def Minimax(self, node, depth, alpha, beta, maxPlayer, firstIter):
        if depth == 0 or node.board.EvaluateEnd():
            terminalNode = self.MinimaxNode(node.board, self.EvaluateHeuristic(maxPlayer, node.board), node.move)
            return terminalNode
        legalMoves = node.board.EvaluateMoves(maxPlayer)
        if not legalMoves:
            newGame = Othello()
            newGame.blackBoard = copy.deepcopy(board.blackBoard)
            newGame.whiteBoard = copy.deepcopy(board.whiteBoard)
            return self.Minimax(self.MinimaxNode(newGame, 0, node.move), depth-1, alpha, beta, self.OppositeColor(maxPlayer, firstIter))
        if maxPlayer == self.color:
            node.value = -np.inf
            childNode = None
            for move in legalMoves:
                if firstIter:
                    node.move = move
                    firstIter = False
                childNode = self.Minimax(self.MinimaxNode(self.ForecastMove(node.board, move, maxPlayer), np.inf, node.move), depth-1, alpha, beta, self.OppositeColor(maxPlayer), firstIter)
                node.value = max(node.value, childNode.value)
                if node.value >= beta:
                    break;
                alpha = max(alpha, node.value)
            return childNode
        else:
            node.value = -np.inf
            childNode = None
            for move in legalMoves:
                childNode = self.Minimax(self.MinimaxNode(self.ForecastMove(node.board, move, maxPlayer),-np.inf, node.move), depth-1, alpha, beta, self.OppositeColor(maxPlayer), firstIter)
                node.value = max(node.value, childNode.value)
                if node.value <= alpha:
                    break
                beta = min(beta, node.value)
            return childNode
    
    # Iterative Deepening algo so AI only takes a few seconds per move
    def GetBestMove(self, board):
        i = 1
        bestNode = None
        startTime = time.time_ns()
        while (time.time_ns() - startTime) < 250000000:
            startNode = self.MinimaxNode(board, -np.inf, None)
            bestNode = self.Minimax(startNode, i, -np.inf, np.inf, self.color, True)
            i += 1
        return bestNode.move
