import numpy as np

class Othello:
    
    whiteBoard = np.zeros((8,8), dtype=int)
    blackBoard = np.zeros((8,8), dtype=int)
    
    ALL_DIRECTIONS = {
        'north': [0, -1],
        'northeast': [1, -1],
        'east': [1, 0],
        'southeast': [1, 1],
        'south': [0, 1],
        'southwest': [-1, 1],
        'west': [-1, 0],
        'northwest': [-1, -1]
    }
    
    def __init__(self):
        
        self.whiteBoard[3, 3] = 1
        self.whiteBoard[4, 4] = 1
        self.blackBoard[3, 4] = 1
        self.blackBoard[4, 3] = 1
    
    def IterateDirection(self, location, direction):
        return np.add(location, self.ALL_DIRECTIONS[direction])
    
    def IsOutofBounds(self, location):
        return ((location[0] > 7) or (location[0] < 0) or (location[1] > 7) or (location[1] < 0))
    
    def IsEmpty(self, location):
        return ((self.whiteBoard[tuple(location)] == 0) and (self.blackBoard[tuple(location)] == 0))
    
    def EvaluateWhiteMoves(self, location):
        retVal = False
        for key in self.ALL_DIRECTIONS:
            newLoc = self.IterateDirection(location, key)
            if self.IsOutofBounds(newLoc):
                continue
            while self.blackBoard[tuple(newLoc)] == 1:
                newLoc = self.IterateDirection(newLoc, key)
                if self.IsOutofBounds(newLoc) or self.IsEmpty(newLoc):
                    break
                if self.whiteBoard[tuple(newLoc)] == 1:
                    retVal = True
                    break
        return retVal
    
    def EvaluateBlackMoves(self, location):
        retVal = False
        for key in self.ALL_DIRECTIONS:
            newLoc = self.IterateDirection(location, key)
            if self.IsOutofBounds(newLoc):
                continue
            while self.whiteBoard[tuple(newLoc)] == 1:
                newLoc = self.IterateDirection(newLoc, key)
                if self.IsOutofBounds(newLoc) or self.IsEmpty(newLoc):
                    break
                if self.blackBoard[tuple(newLoc)] == 1:
                    retVal = True
                    break
        return retVal
    
    def EvaluateMoves(self, color):
        legalMoves = []
        for x in range(8):
            for y in range(8):
                validMove = False
                if not self.IsEmpty([x, y]):
                    continue
                match color:
                    case 'white':
                        validMove = self.EvaluateWhiteMoves([x, y])
                    case 'black':
                        validMove = self.EvaluateBlackMoves([x, y])
                    case _:
                        raise RuntimeError("Invalid player")
                if validMove:
                    legalMoves.append((x, y))
        return legalMoves
    
    def Flip(self, newColor, location):
        match newColor:
            case 'white':
                self.whiteBoard[location] = 1
                self.blackBoard[location] = 0
            case 'black':
                self.whiteBoard[location] = 0
                self.blackBoard[location] = 1
            case _:
                raise RuntimeError("Invalid player")
    
    def ApplyWhiteMove(self, location):
        self.whiteBoard[tuple(location)] = 1
        for key in self.ALL_DIRECTIONS:
            toFlip = []
            newLoc = self.IterateDirection(location, key)
            if self.IsOutofBounds(newLoc):
                continue
            while self.blackBoard[tuple(newLoc)] == 1:
                toFlip.append(tuple(newLoc))
                newLoc = self.IterateDirection(newLoc, key)
                if self.IsOutofBounds(newLoc) or self.IsEmpty(newLoc):
                    break
                if self.whiteBoard[tuple(newLoc)] == 1:
                    for piece in toFlip:
                        self.Flip('white', piece)
                    break
    
    def ApplyBlackMove(self, location):
        self.blackBoard[tuple(location)] = 1
        for key in self.ALL_DIRECTIONS:
            toFlip = []
            newLoc = self.IterateDirection(location, key)
            if self.IsOutofBounds(newLoc):
                continue
            while self.whiteBoard[tuple(newLoc)] == 1:
                toFlip.append(tuple(newLoc))
                newLoc = self.IterateDirection(newLoc, key)
                if self.IsOutofBounds(newLoc) or self.IsEmpty(newLoc):
                    break
                if self.blackBoard[tuple(newLoc)] == 1:
                    for piece in toFlip:
                        self.Flip('black', piece)
                    break
    
    def ApplyMove(self, location, color):
        match color:
            case 'white':
                self.ApplyWhiteMove(location)
            case 'black':
                self.ApplyBlackMove(location)
            case _:
                raise RuntimeError("Invalid player")
    
    def EvaluateEnd(self):
        return np.sum(self.whiteBoard) + np.sum(self.blackBoard) == 64
    
    def EvaluateWinner(self):
        whiteScore = np.sum(self.whiteBoard)
        blackScore = np.sum(self.blackBoard)
        if whiteScore > blackScore:
            return 'white'
        elif blackScore > whiteScore:
            return 'black'
        else:
            return 'draw'
    