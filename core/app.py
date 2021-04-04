from os import makedirs, path as osPath
from numpy import loadtxt, savetxt
import threading

from .given import given
from .sudoku import Sudoku
from .settings import DIGIT_NUMBER, OpenButtonOption, RenderOption, SolveButtonOption, WriteButtonOption
from .ui import Ui

class App:
    def __init__(self):
        self.puzzle = None
        self.puzzlePath = None
        self.sudoku = None
        self.solveThread = None
        self.opening = False
        self.writing = False
        self.solving = False
        self.keyWaiting = False
        self.currentRowColumn = None
        self.ui = Ui()
        self.ui.openCmd = self.open
        self.ui.writeCmd = self.write
        self.ui.clearCmd = self.clear
        self.ui.solveCmd = self.solve
        self.ui.clickCmd = self.click
        self.ui.pressCmd = self.press
        self.ui.loadCommamd()

    def load(self, path):
        # Load a configuration to solve.
        with open(path, "r") as f:
            values = loadtxt(f).reshape((DIGIT_NUMBER, DIGIT_NUMBER)).astype(int)
            given.loadValues(values)
            self.sudoku = Sudoku(self.render)
            self.solveThread = threading.Thread(target=self.sudoku.solve)
            self.ui.drawGivenBoard()
        return

    def save(self, path, solution):
        # Save a configuration to a file.
        dirPath = osPath.dirname(osPath.abspath(path))
        makedirs(dirPath, exist_ok=True)
        with open(path, "w") as f:
            savetxt(f, solution.reshape(DIGIT_NUMBER, DIGIT_NUMBER), fmt='%d')
        return

    def render(self, text, option=RenderOption.NORMAL):
        self.ui.showStatistic(text)
        if option != RenderOption.ONLY_TEXT:
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
            self.save("./solutions/" + self.puzzle, given.bestCandidate.values)
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
            self.ui.solveButtonSwitch(SolveButtonOption.CANCEL)
            self.sudoku.exitFlag = True
            self.solveThread.join()
            self.solveThread = threading.Thread(target=self.sudoku.solve)
            self.solving = False
            self.ui.solveButtonSwitch(SolveButtonOption.READY)

    def clear(self):
        self.ui.showStatistic("")
        self.ui.drawRemainBoard(given.values)
        given.resetBestCandidate()
        given.updateDuplicateValues()
        self.ui.drawDuplicateBg()

    def open(self):
        if not self.opening:
            puzzlePath = self.ui.getPuzzleDialog()
            try:
                self.puzzle = osPath.basename(puzzlePath)
                self.load(puzzlePath)
            except:
                return
            self.ui.openButtonSwitch(OpenButtonOption.OPEN)
            self.opening = True
        else:
            given.resetBestCandidate()
            given.updateDuplicateValues()
            given.loadValues(given.zeroCandidate.values)
            self.sudoku = None
            self.solveThread = None
            self.ui.drawRemainBoard(given.values)
            self.ui.drawGivenBoard()
            self.ui.drawDuplicateBg()
            self.ui.openButtonSwitch(OpenButtonOption.CLOSE)
            self.opening = False

    def write(self):
        if not self.writing:
            self.ui.writeButtonSwitch(WriteButtonOption.WRITE)
            given.resetBestCandidate(True)
            self.writing = True
        else:
            try:
                saveFile = self.ui.savePuzzleDialog()
                savetxt(saveFile, given.bestCandidate.values.reshape(DIGIT_NUMBER, DIGIT_NUMBER), fmt='%d')
                saveFile.close()
            except:
                return
            self.clear()
            self.ui.writeButtonSwitch(WriteButtonOption.SAVE)
            self.writing = False

    def click(self, event):
        if self.solving:
            return
        if self.keyWaiting:
            self.keyWaiting = False
            row, col = self.currentRowColumn
            self.ui.drawItem(row,col,"")
            return
        else:
            if self.opening or self.writing:
                row, col = self.ui.clickToLogicalPosition(event.x, event.y)
                if given.values[row][col] != 0:
                    return
                self.ui.drawItem(row,col,"X")
                self.currentRowColumn = (row, col)
            else:
                return
            self.keyWaiting = True

    def press(self, event):
        if not self.keyWaiting:
            return
        row, col = self.currentRowColumn
        if event.char in list(map(chr,range(ord("1"),ord("9")+1))):
            given.bestCandidate.values[row,col] = int(event.char)
            self.ui.drawRemainBoard(given.bestCandidate.values)
            given.updateDuplicateValues()
            self.ui.drawDuplicateBg()
        else:
            self.ui.drawItem(row,col,"")
        self.keyWaiting = False

    def run(self, puzzle = None):
        if puzzle != None:
            self.puzzle = puzzle + ".txt"
            self.load("puzzles/"+self.puzzle)
            self.ui.solveButtonSwitch(SolveButtonOption.READY)
        self.ui.mainloop()