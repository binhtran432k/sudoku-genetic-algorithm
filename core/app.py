from os import makedirs, path as osPath
from tkinter import Tk, Canvas, Frame, Button, Label
from numpy import loadtxt, savetxt
import threading
from .given import Given
from .settings import DIGIT_NUMBER, BOX_NUMBER, BOX_SIZE, FONT_SIZE, RenderOption
from .sudoku import Sudoku

class App:
    def __init__(self):
        self.puzzle = None
        self.given = None
        self.currentValues = []
        self.sudoku = None
        self.solveThread = None

        self.solving = False

        self.window = Tk()
        self.window.title("Sudoku")
        self.window.resizable(0, 0)
        self.mainBody = None
        self.board = None
        self.boardItems = []
        self.solveButton = None
        self.createWidgets()

    def mainloop(self):
        self.window.mainloop()

    def createWidgets(self):
        # Create main body of window
        self.mainBody = Frame(self.window)
        self.mainBody.grid(row=0, column=0, columnspan=3, sticky="WENS", padx=5, pady=5)
        # Create sizebar of window
        self.sizebar = Frame(self.window)
        self.sizebar.grid(row=0, column=4, sticky="WENS", padx=5, pady=5)

        # Create board sudoku
        self.board = Canvas(self.mainBody, width=BOX_SIZE, height=BOX_SIZE)
        self.board.grid(row=0, column=0)

        # Create button to solve game
        self.solveButton = Button(self.sizebar, width=20, font=("*",16), text="Solve", command=self.solve)
        self.solveButton.grid(row=0, column=0, padx=5, pady=10)
        self.solveButton["state"] = "disabled"
        # Create statistic of sudoku
        self.statistic = Label(self.sizebar, font=("*", 16))
        self.statistic.grid(row=2, column=0, pady=10)

        self.initializeBoard()
        for row in range(DIGIT_NUMBER):
            rowTemp = []
            rowTemp2 = []
            for col in range(DIGIT_NUMBER):
                rowTemp.append(self.board.create_text(
                        BOX_SIZE*(col+1)/DIGIT_NUMBER - FONT_SIZE,
                        BOX_SIZE*(row+1)/DIGIT_NUMBER - FONT_SIZE, font=("*", FONT_SIZE),
                        text=" ", fill="blue"))
                rowTemp2.append(0)
            self.boardItems.append(rowTemp)
            self.currentValues.append(rowTemp2)

    def render(self, text, values, option=RenderOption.NORMAL):
        if option == RenderOption.ONLY_TEXT:
            self.statistic["text"] = text
        else:
            self.statistic["text"] = text
            self.drawRemainBoard(values)
        self.window.update()

    def initializeBoard(self):
        for i in range(BOX_NUMBER - 1):
            # Create big vertical seperate digit set line
            self.board.create_line((i+1)*BOX_SIZE/BOX_NUMBER, 0,
                    (i+1)*BOX_SIZE/BOX_NUMBER, BOX_SIZE, width=3)
            # Create big horizontal seperate digit set line
            self.board.create_line(0, (i+1)*BOX_SIZE/BOX_NUMBER, BOX_SIZE,
                    (i+1)*BOX_SIZE/BOX_NUMBER, width=3)
        
        for i in range(DIGIT_NUMBER - 1):
            # Create small vertical seperate digit line
            self.board.create_line((i+1)*BOX_SIZE/DIGIT_NUMBER, 0,
                    (i+1)*BOX_SIZE/DIGIT_NUMBER, BOX_SIZE, fill="gray")
            # Create small horizontal seperate digit line
            self.board.create_line(0, (i+1)*BOX_SIZE/DIGIT_NUMBER, BOX_SIZE,
                    (i+1)*BOX_SIZE/DIGIT_NUMBER, fill="gray")

    def drawItem(self, row, col, value, color="blue"):
        if (value == 0):
            self.board.itemconfig(self.boardItems[row][col],
                    text=" ", fill=color)
        else:
            self.board.itemconfig(self.boardItems[row][col],
                    text=str(value), fill=color)
        self.currentValues[row][col] = value

    def drawGivenBoard(self, values, color="red"):
        for row in range(DIGIT_NUMBER):
            for col in range(DIGIT_NUMBER):
                if (values[row][col] != 0):
                    self.drawItem(row, col, values[row][col], color)

    def drawRemainBoard(self, values, color="blue"):
        for row in range(DIGIT_NUMBER):
            for col in range(DIGIT_NUMBER):
                if (self.given.values[row][col] == 0):
                    self.drawItem(row, col, values[row][col], color)

    def clearBoard(self):
        self.board.delete("all")
        self.initializeBoard()

    def load(self, path):
        # Load a configuration to solve.
        with open(path, "r") as f:
            values = loadtxt(f).reshape((DIGIT_NUMBER, DIGIT_NUMBER)).astype(int)
            self.given = Given(values)
            self.sudoku = Sudoku(self.given, self.render)
            self.solveThread = threading.Thread(target=self.sudoku.solve)
            self.drawGivenBoard(values)
            self.solveButton["state"] = "normal"
            self.solveButton["text"] = "Solve"
        return

    def save(self, path, solution):
        # Save a configuration to a file.
        dirPath = osPath.dirname(osPath.abspath(path))
        makedirs(dirPath, exist_ok=True)
        with open(path, "w") as f:
            savetxt(f, solution.values.reshape(DIGIT_NUMBER, DIGIT_NUMBER), fmt='%d')
        return

    def solve(self):
        # self.solveButton["state"] = "disabled"
        if not self.solving:
            self.solveButton["text"] = "Stop"
            if not self.solveThread.is_alive():
                self.solveThread.start()
            self.solving = True
        else:
            self.sudoku.exitFlag = True
            self.solveButton["text"] = "Solve"
            self.solveThread.join()
            self.solveThread = threading.Thread(target=self.sudoku.solve)
            self.solving = False
        # if(solution):
        #     self.save("./solutions/" + self.puzzle + ".txt", solution)

    def run(self, puzzle):
        self.puzzle = puzzle
        self.load("./puzzles/" + self.puzzle + ".txt")
        self.mainloop()