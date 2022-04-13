from Othello import Othello
from OthelloAI import OthelloAI
import time

class OthelloGame:
	
    def __init__(self):
        self.game = Othello()
        self.turnPlayer = 'black'
        self.AI = {
            'white': OthelloAI('white'),
            'black': OthelloAI('black')
        }
        self.IsAI = {
            'white': 'y',
            'black': 'y'
        }
    
    def FormatPiece(self, x, y):
        return chr((66*self.game.blackBoard[x, y]) + (87*self.game.whiteBoard[x, y]))
    
    def FormatRow(self, rowNum):
        retString = f'{rowNum}|'
        for colNum in range(8):
            retString += f' {self.FormatPiece(rowNum, colNum)} |'
        return retString
    
    def PrintBoard(self):
        print('   0   1   2   3   4   5   6   7  ')
        print(' ---------------------------------')
        for i in range(8):
            print(self.FormatRow(i))
            print(' ---------------------------------')
    
    def PrintMoves(self, moveArray):
        for i in range(len(moveArray)):
            print(f'{i+1}. {moveArray[i]}')
    
    def SwapPlayer(self):
        match self.turnPlayer:
            case 'white':
                self.turnPlayer = 'black'
            case 'black':
                self.turnPlayer = 'white'
    
    def RunGame(self):
        self.IsAI['black'] = input('Is Black an AI?[y/n]: ')
        self.IsAI['white'] = input('Is White an AI?[y/n]: ')
        while(not self.game.EvaluateEnd()):
            print()
            print()
            print(f'The turn player is {self.turnPlayer}')
            print()
            legalMoves = self.game.EvaluateMoves(self.turnPlayer)
            self.PrintBoard()
            if not legalMoves:
                print(f'There is no legal move for {self.turnPlayer}, skipping turn.')
                self.SwapPlayer()
                continue
            if self.IsAI[self.turnPlayer] == 'y':
                bestMove = self.AI[self.turnPlayer].GetBestMove(self.game)
                self.game.ApplyMove(bestMove, self.turnPlayer)
                time.sleep(2)
            else:
                self.PrintMoves(legalMoves)
                moveNum = input(f'Select move for {self.turnPlayer}:')
                self.game.ApplyMove(legalMoves[int(moveNum)-1], self.turnPlayer)
            self.SwapPlayer()
        self.PrintBoard()
        winner = self.game.EvaluateWinner()
        match winner:
            case 'white':
                print('White wins!')
            case 'black':
                print('Black wins!')
            case 'draw':
                print("It's a draw!")
        exit(0)
    
def main():
    game = OthelloGame()
    game.RunGame()

if __name__ == '__main__':
    main()
    