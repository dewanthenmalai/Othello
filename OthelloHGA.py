import numpy as np
import sys
import multiprocessing as mp
from Othello import Othello
from OthelloAI import OthelloAI
from time import process_time

def ValidateInputs(args):
    return (len(args) == 3) and (int(args[0]) > 0) and (int(args[1]) > 0) and (int(args[2]) > 0)
    
def SwapPlayer(turnPlayer):
    match turnPlayer:
        case 'white':
            return 'black'
        case 'black':
            return 'white'

def RunGame(player1, player2, heuristics):
    AI = {
        'white': OthelloAI('white', heuristic=heuristics[player2]),
        'black': OthelloAI('black', heuristic=heuristics[player1])
    }
    game = Othello()
    turnPlayer = 'black'
    while(not game.EvaluateEnd()):
        legalMoves = game.EvaluateMoves(turnPlayer)
        if not legalMoves:
            turnPlayer = SwapPlayer(turnPlayer)
            continue
        bestMove = AI[turnPlayer].GetBestMove(game)
        game.ApplyMove(bestMove, turnPlayer)
        SwapPlayer(turnPlayer)
    winner = game.EvaluateWinner()
    match winner:
        case 'white':
            return player2
        case 'black':
            return player1
        case 'draw':
            return None

def RunSingleGeneration(startHeuristic, population, matchCount):
    heuristics = [startHeuristic]
    wins = np.ones(population)
    #I'm only using half the available CPUs because I'm running this locally and don't want to commit 100% of machine resources to this
    pool = mp.Pool(mp.cpu_count()//2)
    winners = []
    for i in range(population-1):
        newHeuristic = startHeuristic + np.random.normal(0, 25, size=(8,8))
        heuristics.append(newHeuristic)
    for matchNum in range(matchCount):
        results = [pool.apply_async(RunGame, args=(i, j, heuristics)) for j in range(population) for i in range(population)]
        output = [p.get() for p in results]
        winners.append(list(filter(None, output)))
    for index in winners:
        wins[index] += 1
    pool.close()
    pool.join()
    return np.average(heuristics, weights=wins, axis=0)
    
def main(generations, genPop, genIter):
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
        print(f'Generation: {i+1}')
        heuristic = RunSingleGeneration(heuristic, genPop, genIter)
    
    
    print(heuristic)
    
if __name__ == '__main__':
    if not ValidateInputs(sys.argv[1:]):
        exit(-1)
    processStart = process_time()
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    processEnd = process_time()
    print(f'Total time: {processEnd-processStart}')
