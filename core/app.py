from os import makedirs, path as osPath
from numpy import loadtxt, savetxt
import threading

from .given import given
from .sudoku import Sudoku
from .settings import DIGIT_NUMBER, OpenButtonOption, RenderOption, SolveButtonOption, WriteButtonOption
from .helper import decodePuzzle, encodePuzzle
from .ui import Ui

class App:
    def __init__(self):
        self.puzzle = None # puzzle name
        self.puzzlePath = None
        self.sudoku = None # sudoku algorithm
        self.solveThread = None # thread for solving sudoku game, must be restart manual
        # State of app sudoku
        self.opening = False
        self.writing = False
        self.solving = False
        self.keyWaiting = False
        # Flag to skip the reload solution
        self.skipReload = False
        # Store value when click to manual solve or write new puzzle
        self.currentRowColumn = None
        # The UI of app
        self.ui = Ui()
        # List of command will pass to ui button
        self.ui.openCmd = self.open
        self.ui.writeCmd = self.write
        self.ui.clearCmd = self.clear
        self.ui.solveCmd = self.solve
        self.ui.clickCmd = self.click
        self.ui.pressCmd = self.press
        self.ui.loadCommamd() # load the command to button

    def load(self, path):
        """
        Load a puzzle to solve.
        """
        with open(path, "r") as f:
            values = loadtxt(f).reshape((DIGIT_NUMBER, DIGIT_NUMBER)).astype(int)
            given.loadValues(values)
            # Initialize sudoku algorithm
            self.sudoku = Sudoku(self.render)
            # Manual create new thread to solve
            self.solveThread = threading.Thread(target=self.sudoku.solve, daemon=True)
            # Draw to UI the puzzle
            self.ui.drawGivenBoard()

    def save(self, path, solution):
        """
        Save a solution to a file.
        """
        dirPath = osPath.dirname(osPath.abspath(path))
        # Create new folder if not exist
        makedirs(dirPath, exist_ok=True)
        with open(path, "w") as f:
            savetxt(f, solution.reshape(DIGIT_NUMBER, DIGIT_NUMBER), fmt='%d')

    def render(self, text, option=RenderOption.NORMAL):
        """
        Render the current best solution to UI, use for the algorithm.
        """
        self.ui.showStatistic(text)
        # Decode the current puzzle from best candidate of algorithm
        currentValues = decodePuzzle(given.bestCandidate.gene)
        if option != RenderOption.ONLY_TEXT:
            # Update statistics and sudoku board values
            self.ui.showStatistic(text)
            self.ui.drawRemainBoard(currentValues)
            win = given.updateDuplicateValues()
            # Draw win background if solution is found else draw the duplicate values
            if win:
                self.ui.drawSolutionBg()
            else:
                self.ui.drawDuplicateBg()
        if option in [RenderOption.FOUNDED,RenderOption.NOT_FOUND]:
            # Ready for resolving in the future
            self.solveThread = threading.Thread(target=self.sudoku.solve, daemon=True)
            self.ui.solveButtonSwitch(SolveButtonOption.READY)
            self.solving = False
            self.skipReload = False
        elif option == RenderOption.RELOADED:
            # Ready for resolve when the solution is loaded from file
            self.ui.solveButtonSwitch(SolveButtonOption.RELOAD)
            self.skipReload = True
        if option == RenderOption.FOUNDED:
            # Save the solution to file
            self.save("solutions/" + self.puzzle, currentValues)
        self.ui.window.update()

    def solve(self):
        """
        Solve command for Solve button
        """
        ## If the app is in writing state, this will cancel the write
        # action and return to initial state
        if self.writing:
            self.clear()
            self.ui.writeButtonSwitch(WriteButtonOption.SAVE)
            self.writing = False
            return
        # Reload the solution if flag skipReload is not set
        if not self.skipReload:
            try:
                with open("solutions/" + self.puzzle, "r") as f:
                    values = loadtxt(f).reshape((DIGIT_NUMBER, DIGIT_NUMBER)).astype(int)
                    given.bestCandidate.gene = encodePuzzle(values)
                    win = given.updateDuplicateValues()
                    if win:
                        self.render("Solution Reloaded", option=RenderOption.RELOADED)
                        return
                    else:
                        self.clear()
            except:
                # Solve by using algorithm if solution file not found
                pass
        # If the solving state is not set it will solve the game, else cancel solving
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
            self.solveThread.join() # wait for thread close
            # Recreate solve thread for use in future
            self.solveThread = threading.Thread(target=self.sudoku.solve, daemon=True)
            self.solving = False
            self.skipReload = False
            self.ui.solveButtonSwitch(SolveButtonOption.READY)

    def clear(self):
        """
        Clear command for Clear button
        """
        # Clear the puzzle board and renew statistic as open recently
        self.ui.showStatistic("")
        self.ui.drawRemainBoard(given.values)
        given.resetBestCandidate(True)
        given.updateDuplicateValues()
        self.ui.drawDuplicateBg()
        # Reset skipReload flag
        if self.skipReload:
            self.ui.solveButtonSwitch(SolveButtonOption.READY)
            self.skipReload = False

    def open(self):
        """
        Open command for Open button
        """
        # if the puzzle is not opening open one puzzle else close
        if not self.opening:
            # Open dialog to get puzzle path
            puzzlePath = self.ui.getPuzzleDialog()
            try:
                self.puzzle = osPath.basename(puzzlePath)
                self.load(puzzlePath)
            except:
                # Cancel the open action if select right
                return
            # rename the app with puzzle file name
            self.ui.window.title("Sudoku - " + self.puzzle)
            self.ui.openButtonSwitch(OpenButtonOption.OPEN)
            self.opening = True
        else:
            # Close puzzle and reset all to initial state
            given.resetBestCandidate()
            given.updateDuplicateValues()
            given.loadValues(given.zeroCandidate.gene)
            self.sudoku = None
            self.solveThread = None
            self.ui.drawRemainBoard(given.values)
            self.clear()
            self.ui.openButtonSwitch(OpenButtonOption.CLOSE)
            # Rename the app to initial
            self.ui.window.title("Sudoku")
            self.opening = False
            # Reset skipReload flag
            if self.skipReload:
                self.ui.solveButtonSwitch(SolveButtonOption.READY)
                self.skipReload = False

    def write(self):
        """
        Write command for Write button
        """
        ## If the app is not in writing state, go to it and prepare for writ new puzzle,
        # else save the current puzzle to file
        if not self.writing:
            self.ui.writeButtonSwitch(WriteButtonOption.WRITE)
            given.resetBestCandidate(True)
            self.writing = True
        else:
            # Open dialog to get path to save puzzle
            try:
                currentValues = decodePuzzle(given.bestCandidate.gene)
                saveFile = self.ui.savePuzzleDialog()
                savetxt(saveFile, currentValues.reshape(DIGIT_NUMBER, DIGIT_NUMBER), fmt='%d')
                saveFile.close()
            except:
                # cancel save action file has not been saved
                return
            # Reset to initial state
            self.clear()
            self.ui.writeButtonSwitch(WriteButtonOption.SAVE)
            self.writing = False

    def click(self, event):
        """
        Click command for click aciton from UI
        """
        # Not doing anything when app is in solving state
        if self.solving:
            return
        ## If app is in keyWaiting, restore the previous clicked value to before value,
        # else make app wait for key pressing
        if self.keyWaiting:
            self.keyWaiting = False
            row, col, value = self.currentRowColumn
            valueStr = ""
            if value != 0:
                valueStr = str(value)
            self.ui.drawItem(row,col,valueStr)
            return
        else:
            if self.opening or self.writing:
                row, col = self.ui.clickToLogicalPosition(event.x, event.y)
                if given.values[row][col] != 0:
                    return
                self.ui.drawItem(row,col,"X")
                currentValues = decodePuzzle(given.bestCandidate.gene)
                self.currentRowColumn = (row, col, currentValues[row][col])
            else:
                return
            self.keyWaiting = True

    def press(self, event):
        """
        Press key command for press key aciton from UI
        """
        # Do nothing if app is not in keyWaiting state
        if not self.keyWaiting:
            return
        row, col, value = self.currentRowColumn
        currentValues = decodePuzzle(given.bestCandidate.gene)
        # Set value to key pressed when it is in [1-9] else clear it and set value to 0
        if event.char in list(map(chr,range(ord("1"),ord("9")+1))):
            currentValues[row,col] = int(event.char)
        else:
            currentValues[row,col] = 0
        given.bestCandidate.gene = encodePuzzle(currentValues)
        # Draw the updated puzzle
        self.ui.drawRemainBoard(currentValues)
        win = given.updateDuplicateValues()
        if win:
            self.ui.drawSolutionBg()
        else:
            self.ui.drawDuplicateBg()
        self.keyWaiting = False

    def run(self, puzzle = None):
        """
        Run the app and keep showing until close
        """
        if puzzle != None:
            self.puzzle = puzzle + ".txt"
            self.load("puzzles/"+self.puzzle)
            self.ui.solveButtonSwitch(SolveButtonOption.READY)
        self.ui.mainloop()