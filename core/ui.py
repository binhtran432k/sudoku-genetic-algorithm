from tkinter import Tk, Canvas, Frame, Button, Label
from numpy import zeros

from .settings import DIGIT_NUMBER, BOX_NUMBER, BOARD_SIZE, DIGIT_SIZE, DIGIT_SPACE, FONT_FAMILY, SolveButtonOption
from .settings import GIVEN_DIGIT_COLOR, NORMAL_DIGIT_COLOR, TEXT_SIZE

class Ui:
    def __init__(self):
        self.givenValues = None

        self.window = Tk()
        self.window.title("Sudoku")
        self.window.resizable(0, 0)
        self.mainBody = None
        self.board = None
        self.boardItems = []
        self.solveButton = None
        self.createWidgets()

        self.solveCmd = None

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
        self.board = Canvas(self.mainBody, width=BOARD_SIZE, height=BOARD_SIZE)
        self.board.grid(row=0, column=0)

        # Create button to solve game
        self.solveButton = Button(self.sizebar, width=20, font=(FONT_FAMILY,TEXT_SIZE),
                text="Solve")
        self.solveButton.grid(row=0, column=0, padx=5, pady=10)
        self.solveButton["state"] = "disabled"
        # Create statistic of sudoku
        self.statistic = Label(self.sizebar, font=(FONT_FAMILY,TEXT_SIZE), wraplength=300)
        self.statistic.grid(row=2, column=0, pady=10)

        self.initializeBoard()
        for row in range(DIGIT_NUMBER):
            rowTemp = []
            for col in range(DIGIT_NUMBER):
                rowTemp.append(self.board.create_text(
                        BOARD_SIZE*(col)/DIGIT_NUMBER + DIGIT_SPACE,
                        BOARD_SIZE*(row)/DIGIT_NUMBER + DIGIT_SPACE,
                        font=(FONT_FAMILY, DIGIT_SIZE),
                        text=" ", fill=NORMAL_DIGIT_COLOR))
            self.boardItems.append(rowTemp)

    def initializeBoard(self):
        for i in range(BOX_NUMBER - 1):
            # Create big vertical seperate digit set line
            self.board.create_line((i+1)*BOARD_SIZE/BOX_NUMBER, 0,
                    (i+1)*BOARD_SIZE/BOX_NUMBER, BOARD_SIZE, width=3)
            # Create big horizontal seperate digit set line
            self.board.create_line(0, (i+1)*BOARD_SIZE/BOX_NUMBER, BOARD_SIZE,
                    (i+1)*BOARD_SIZE/BOX_NUMBER, width=3)
        
        for i in range(DIGIT_NUMBER - 1):
            # Create small vertical seperate digit line
            self.board.create_line((i+1)*BOARD_SIZE/DIGIT_NUMBER, 0,
                    (i+1)*BOARD_SIZE/DIGIT_NUMBER, BOARD_SIZE, fill="gray")
            # Create small horizontal seperate digit line
            self.board.create_line(0, (i+1)*BOARD_SIZE/DIGIT_NUMBER, BOARD_SIZE,
                    (i+1)*BOARD_SIZE/DIGIT_NUMBER, fill="gray")

    def drawItem(self, row, col, value, color=NORMAL_DIGIT_COLOR):
        if (value == 0):
            self.board.itemconfig(self.boardItems[row][col],
                    text=" ", fill=color)
        else:
            self.board.itemconfig(self.boardItems[row][col],
                    text=str(value), fill=color)

    def drawGivenBoard(self, values, color=GIVEN_DIGIT_COLOR):
        self.givenValues = values
        for row in range(DIGIT_NUMBER):
            for col in range(DIGIT_NUMBER):
                if (values[row][col] != 0):
                    self.drawItem(row, col, values[row][col], color)

    def drawRemainBoard(self, values, color=NORMAL_DIGIT_COLOR):
        for row in range(DIGIT_NUMBER):
            for col in range(DIGIT_NUMBER):
                if (self.givenValues[row][col] == 0):
                    self.drawItem(row, col, values[row][col], color)

    def solveButtonSwitch(self, option):
        if option == SolveButtonOption.STOP:
            self.solveButton["state"] = "disabled"
            self.solveButton["text"] = "Stopping.."
        elif option == SolveButtonOption.SOLVE:
            self.solveButton["text"] = "Stop"
            self.solveButton["state"] = "normal"
        elif option == SolveButtonOption.READY:
            self.solveButton["text"] = "Solve"
            self.solveButton["state"] = "normal"
        self.solveButton.update()

    def loadCommamd(self):
        self.solveButton["command"] = self.solveCmd