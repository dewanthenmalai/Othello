import numpy as np
import sys
from Othello import Othello
from OthelloAI import OthelloAI
from time import process_time

class OthelloHGA:
    
    def SwapPlayer(self, turnPlayer):
        match turnPlayer:
            case 'white':
                return 'black'
            case 'black':
                return 'white'
    
    def RunGame(self, heuristic1, heuristic2):
        AI = {
            'white': OthelloAI('white', heuristic=heuristic2),
            'black': OthelloAI('black', heuristic=heuristic1)
        }
        game = Othello()
        turnPlayer = 'black'
        while(not game.EvaluateEnd()):
            legalMoves = game.EvaluateMoves(turnPlayer)
            if not legalMoves:
                turnPlayer = self.SwapPlayer(turnPlayer)
                continue
            bestMove = AI[turnPlayer].GetBestMove(game)
            game.ApplyMove(bestMove, turnPlayer)
            self.SwapPlayer(turnPlayer)
        winner = game.EvaluateWinner()
        match winner:
            case 'white':
                return -1
            case 'black':
                return 1
            case 'draw':
                return 0
    
    def RunSingleGeneration(self, startHeuristic, population, matchCount):
        heuristics = [startHeuristic]
        wins = np.ones(population)
        for i in range(population-1):
            newHeuristic = startHeuristic + np.random.normal(0, 20, size=(8,8))
            heuristics.append(newHeuristic)
        for matchNum in range(matchCount):
            for i in range(population):
                for j in range(population): # need to give each heuristic a chance to go first so games are doubled up
                    winner = self.RunGame(heuristics[i], heuristics[j])
                    match winner:
                        case 1:
                            wins[i] += 1
                        case -1:
                            wins[j] += 1
        
        return np.average(heuristics, weights=wins, axis=0)
    
def main(generations, genPop, genIter):
    processStart = process_time()
    GARunner = OthelloHGA()
    # set up simple/naive initial heuristic
    heuristic = np.full((8,8), 100)
    for i in range(8):
        heuristic[0, i] = 200
        heuristic[7, i] = 200
        heuristic[i, 0] = 200
        heuristic[i, 7] = 200
    heuristic[0,0] = 500
    heuristic[0,7] = 500
    heuristic[7,0] = 500
    heuristic[7,7] = 500
    
    for i in range(generations):
        heuristic = GARunner.RunSingleGeneration(heuristic, genPop, genIter)
    
    processEnd = process_time()
    print(f'Total time: {processEnd-processStart}')
    print(heuristic)
    
if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(-1)
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
