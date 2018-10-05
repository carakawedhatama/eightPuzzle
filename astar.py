import random
import math

_goalPuzzle = [[1,2,3],
               [4,5,6],
               [7,8,0]]

def index(item, seq):
    try:
        return seq.index(item)
    except:
        return -1

class EightPuzzle:

    def __init__(self):
        self.mhorizontalValue = 0
        self.mDepth = 0
        self.mParent = None
        self.puzzleMatrix = []
        for i in range(3):
            self.puzzleMatrix.append(_goalPuzzle[i][:])

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.puzzleMatrix == other.puzzleMatrix

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.puzzleMatrix[row]))
            res += '\r\n'
        return res

    def _clone(self):
        p = EightPuzzle()
        for i in range(3):
            p.puzzleMatrix[i] = self.puzzleMatrix[i][:]
        return p

    def GetMove(self):
        row, col = self.Find(0)
        free = []
        
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 2:
            free.append((row + 1, col))
        if col < 2:
            free.append((row, col + 1))

        return free

    def GenerateMove(self):
        free = self.GetMove()
        zero = self.Find(0)

        def Swap_and_clone(a, b):
            p = self._clone()
            p.Swap(a,b)
            p.mDepth = self.mDepth + 1
            p.mParent = self
            return p

        return map(lambda pair: Swap_and_clone(zero, pair), free)

    def GeneratePathSolution(self, path):
        if self.mParent == None:
            return path
        else:
            path.append(self)
            return self.mParent.GeneratePathSolution(path)

    def solve(self, h):
        def is_solved(puzzle):
            return puzzle.puzzleMatrix == _goalPuzzle

        openl = [self]
        closedl = []
        move_count = 0
        while len(openl) > 0:
            x = openl.pop(0)
            move_count += 1
            if (is_solved(x)):
                if len(closedl) > 0:
                    return x.GeneratePathSolution([]), move_count
                else:
                    return [x]

            succ = x.GenerateMove()
            idx_open = idx_closed = -1
            for move in succ:
                idx_open = index(move, openl)
                idx_closed = index(move, closedl)
                hval = h(move)
                fval = hval + move.mDepth

                if idx_closed == -1 and idx_open == -1:
                    move.mhorizontalValue = hval
                    openl.append(move)
                elif idx_open > -1:
                    copy = openl[idx_open]
                    if fval < copy.mhorizontalValue + copy.mDepth:
                        copy.mhorizontalValue = hval
                        copy.mParent = move.mParent
                        copy.mDepth = move.mDepth
                elif idx_closed > -1:
                    copy = closedl[idx_closed]
                    if fval < copy.mhorizontalValue + copy.mDepth:
                        move.mhorizontalValue = hval
                        closedl.remove(copy)
                        openl.append(move)

            closedl.append(x)
            openl = sorted(openl, key=lambda p: p.mhorizontalValue + p.mDepth)

        return [], 0

    def InitPuzzle(self, step_count):
        for i in range(step_count):
            row, col = self.Find(0)
            free = self.GetMove()
            target = random.choice(free)
            self.Swap((row, col), target)            
            row, col = target

    def Find(self, value):
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.puzzleMatrix[row][col] == value:
                    return row, col
    
    def Peek(self, row, col):
        return self.puzzleMatrix[row][col]

    def Poke(self, row, col, value):
        self.puzzleMatrix[row][col] = value

    def Swap(self, pos_a, pos_b):
        temp = self.Peek(*pos_a)
        self.Poke(pos_a[0], pos_a[1], self.Peek(*pos_b))
        self.Poke(pos_b[0], pos_b[1], temp)

def Heuristic(puzzle, item_total_calc, total_calc):
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.Peek(row, col) - 1
            mCols = val % 3
            mRows = val / 3

            if mRows < 0: 
                mRows = 2

            t += item_total_calc(row, mRows, col, mCols)

    return total_calc(t)

def ManhattanDistance(puzzle):
    return Heuristic(puzzle,
                lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                lambda t : t)

def h_default(puzzle):
    return 0

def main():
    p = EightPuzzle()
    p.InitPuzzle(20)
    print(p)

    path, count = p.solve(ManhattanDistance)
    path.reverse()
    for i in path: 
        print(i)

if __name__ == "__main__":
    main()