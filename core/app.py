from os import makedirs, path as osPath
from numpy import loadtxt, savetxt, zeros, copy as npCopy
import threading

from .given import given
from .sudoku import Sudoku
from .settings import DIGIT_NUMBER, RenderOption, SolveButtonOption
from .ui import Ui

class App:
    def __init__(self):
        self.puzzle = None
        self.sudoku = None
        self.solveThread = None
        self.solving = False
        self.ui = Ui()
        self.ui.solveCmd = self.solve
        self.ui.loadCommamd()

    def load(self, path):
        # Load a configuration to solve.
        with open(path, "r") as f:
            values = loadtxt(f).reshape((DIGIT_NUMBER, DIGIT_NUMBER)).astype(int)
            given.loadValues(values)
            self.sudoku = Sudoku(self.render)
            self.solveThread = threading.Thread(target=self.sudoku.solve)
            self.ui.drawGivenBoard()
            self.ui.solveButtonSwitch(SolveButtonOption.READY)
        return

    def save(self, path, solution):
        # Save a configuration to a file.
        dirPath = osPath.dirname(osPath.abspath(path))
        makedirs(dirPath, exist_ok=True)
        with open(path, "w") as f:
            savetxt(f, solution.reshape(DIGIT_NUMBER, DIGIT_NUMBER), fmt='%d')
        return

    def render(self, text, option=RenderOption.NORMAL):
        if option == RenderOption.ONLY_TEXT:
            self.ui.statistic["text"] = text
        else:
            self.ui.statistic["text"] = text
            self.ui.drawRemainBoard(given.bestCandidate.values)
            given.updateDuplicateValues()
            if (given.bestCandidate.fitness == 1):
                self.ui.drawSolutionBg()
            else:
                self.ui.drawDuplicateBg()
        if option in [RenderOption.FOUNDED,RenderOption.NOT_FOUND]:
            self.solveThread = threading.Thread(target=self.sudoku.solve)
            self.ui.solveButtonSwitch(SolveButtonOption.READY)
            self.solving = False
        if option == RenderOption.FOUNDED:
            self.save("./solutions/" + self.puzzle + ".txt", given.bestCandidate.values)
        self.ui.window.update()

    def solve(self):
        if not self.solving:
            if self.solveThread.is_alive():
                return
            self.solveThread.start()
            self.solving = True
            self.ui.solveButtonSwitch(SolveButtonOption.SOLVE)
        else:
            if not self.solveThread.is_alive():
                return
            self.ui.solveButtonSwitch(SolveButtonOption.STOP)
            self.sudoku.exitFlag = True
            self.solveThread.join()
            self.solveThread = threading.Thread(target=self.sudoku.solve)
            self.solving = False
            self.ui.solveButtonSwitch(SolveButtonOption.READY)

    def clear(self):
        self.ui.statistic["text"] = ""
        self.ui.drawRemainBoard(given.values)

    def run(self, puzzle):
        self.puzzle = puzzle
        self.load("./puzzles/" + self.puzzle + ".txt")
        self.ui.mainloop()