from numpy import loadtxt, savetxt
from .given import Given
from .settings import digitNumber
from .sudoku import Sudoku

class App:
    def __init__(self):
        self.puzzle = None
        self.sudoku = None

    def load(self, path):
        # Load a configuration to solve.
        with open(path, "r") as f:
            values = loadtxt(f).reshape((digitNumber, digitNumber)).astype(int)
            self.sudoku = Sudoku(Given(values))
        return

    def save(self, path, solution):
        # Save a configuration to a file.
        with open(path, "w") as f:
            savetxt(f, solution.values.reshape(digitNumber, digitNumber), fmt='%d')
        return

    def run(self, puzzle):
        self.puzzle = puzzle
        self.load("./puzzles/" + self.puzzle + ".txt")
        solution = self.sudoku.solve()
        if(solution):
            self.save("./solutions/" + self.puzzle + ".txt", solution)