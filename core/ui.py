from tkinter import Tk, Canvas, Frame, Button, Label, filedialog

from .settings import ClearButtonOption, DIGIT_NUMBER, BLOCK_NUMBER, BOARD_SIZE, DIGIT_SIZE, DIGIT_SPACE, DUPLICATE_DIGIT_BG, DUPLICATE_DIGIT_GIVEN_BG, FONT_FAMILY, OpenButtonOption, SOLUTION_DIGIT_BG, SOLUTION_DIGIT_GIVEN_BG, SolveButtonOption, TRANSPARENT_DIGIT_BG, WriteButtonOption
from .settings import GIVEN_DIGIT_COLOR, NORMAL_DIGIT_COLOR, TEXT_SIZE
from .given import given

class Ui:
    def __init__(self):
        self.window = Tk()
        self.window.title("Sudoku")
        self.window.resizable(0, 0)
        self.mainBody = None
        self.board = None
        self.boardItems = []
        self.boardItemBgs = []
        self.solveButton = None
        self.createWidgets()

        self.openCmd = None
        self.writeCmd = None
        self.clearCmd = None
        self.solveCmd = None
        self.pressCmd = None
        self.clickCmd = None

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

        # Create button to open game
        self.openButton = Button(self.sizebar, width=20, font=(FONT_FAMILY,TEXT_SIZE),
                text="Open")
        self.openButton.grid(row=0, column=0, padx=5, pady=10)
        # Create button to write game
        self.writeButton = Button(self.sizebar, width=20, font=(FONT_FAMILY,TEXT_SIZE),
                text="Write")
        self.writeButton.grid(row=1, column=0, padx=5, pady=10)
        # Create button to clear game
        self.clearButton = Button(self.sizebar, width=20, font=(FONT_FAMILY,TEXT_SIZE),
                text="Clear", state="disabled")
        self.clearButton.grid(row=2, column=0, padx=5, pady=10)
        # Create button to solve game
        self.solveButton = Button(self.sizebar, width=20, font=(FONT_FAMILY,TEXT_SIZE),
                text="Solve", state="disabled")
        self.solveButton.grid(row=3, column=0, padx=5, pady=10)
        # Create statistic of sudoku
        self.statistic = Label(self.sizebar, font=(FONT_FAMILY,TEXT_SIZE), wraplength=300)
        self.statistic.grid(row=4, column=0, pady=10)

        self.initializeBoard()

    def initializeBoard(self):
        """" Intialize the board for sudoku """
        # Initialize digit for board
        for row in range(DIGIT_NUMBER):
            rowTemp = []
            rowTemp2 = []
            for col in range(DIGIT_NUMBER):
                rowTemp2.append(self.board.create_rectangle(
                        BOARD_SIZE*(col)/DIGIT_NUMBER,
                        BOARD_SIZE*(row)/DIGIT_NUMBER,
                        BOARD_SIZE*(col+1)/DIGIT_NUMBER,
                        BOARD_SIZE*(row+1)/DIGIT_NUMBER,
                        fill=TRANSPARENT_DIGIT_BG
                    ))
                rowTemp.append(self.board.create_text(
                        BOARD_SIZE*(col)/DIGIT_NUMBER + DIGIT_SPACE,
                        BOARD_SIZE*(row)/DIGIT_NUMBER + DIGIT_SPACE,
                        font=(FONT_FAMILY, DIGIT_SIZE),
                        text=" ", fill=NORMAL_DIGIT_COLOR
                    ))
            self.boardItems.append(rowTemp)
            self.boardItemBgs.append(rowTemp2)

        # Create small line
        for i in range(DIGIT_NUMBER - 1):
            # Vertical lines
            self.board.create_line((i+1)*BOARD_SIZE/DIGIT_NUMBER, 0,
                    (i+1)*BOARD_SIZE/DIGIT_NUMBER, BOARD_SIZE, fill="gray")
            # Horizontal lines
            self.board.create_line(0, (i+1)*BOARD_SIZE/DIGIT_NUMBER, BOARD_SIZE,
                    (i+1)*BOARD_SIZE/DIGIT_NUMBER, fill="gray")

        # Create big seperate digit set line
        for i in range(BLOCK_NUMBER - 1):
            # Vertical lines
            self.board.create_line((i+1)*BOARD_SIZE/BLOCK_NUMBER, 0,
                    (i+1)*BOARD_SIZE/BLOCK_NUMBER, BOARD_SIZE, width=3)
            # Horizontal lines
            self.board.create_line(0, (i+1)*BOARD_SIZE/BLOCK_NUMBER, BOARD_SIZE,
                    (i+1)*BOARD_SIZE/BLOCK_NUMBER, width=3)

    def drawItem(self, row, col, value, color=NORMAL_DIGIT_COLOR):
        """ Draw item to board """
        if (value == 0):
            self.board.itemconfig(self.boardItems[row][col],
                    text="", fill=color)
        else:
            self.board.itemconfig(self.boardItems[row][col],
                    text=str(value), fill=color)

    def drawItemBg(self, row, col, color=DUPLICATE_DIGIT_BG):
        """ Draw background of item to board """
        self.board.itemconfig(self.boardItemBgs[row][col],
            fill=color)

    def drawGivenBoard(self, color=GIVEN_DIGIT_COLOR):
        for row in range(DIGIT_NUMBER):
            for col in range(DIGIT_NUMBER):
                if (given.values[row][col] != 0):
                    self.drawItem(row, col, given.values[row][col], color)

    def drawRemainBoard(self, values, color=NORMAL_DIGIT_COLOR):
        for row in range(DIGIT_NUMBER):
            for col in range(DIGIT_NUMBER):
                if (given.values[row][col] == 0):
                    self.drawItem(row, col, values[row][col], color)

    def drawDuplicateBg(self):
        for row in range(DIGIT_NUMBER):
            for col in range(DIGIT_NUMBER):
                color = DUPLICATE_DIGIT_BG
                if (given.duplicateValues[row][col] == 0):
                    color = TRANSPARENT_DIGIT_BG
                elif (given.values[row][col] != 0):
                    color = DUPLICATE_DIGIT_GIVEN_BG
                self.drawItemBg(row, col, color)

    def drawSolutionBg(self):
        for row in range(DIGIT_NUMBER):
            for col in range(DIGIT_NUMBER):
                color = SOLUTION_DIGIT_BG
                if (given.duplicateValues[row][col] != 0):
                    color = TRANSPARENT_DIGIT_BG
                elif (given.values[row][col] != 0):
                    color = SOLUTION_DIGIT_GIVEN_BG
                self.drawItemBg(row, col, color)

    def openButtonSwitch(self, option):
        if option == OpenButtonOption.OPEN:
            self.openButton["text"] = "Close"
            self.openButton["state"] = "normal"
            self.writeButtonSwitch(WriteButtonOption.DISABLED)
            self.clearButtonSwitch(ClearButtonOption.NORMAL)
            self.solveButtonSwitch(SolveButtonOption.NORMAL)
        elif option == OpenButtonOption.CLOSE:
            self.openButton["text"] = "Open"
            self.openButton["state"] = "normal"
            self.writeButtonSwitch(WriteButtonOption.NORMAL)
            self.clearButtonSwitch(ClearButtonOption.DISABLED)
            self.solveButtonSwitch(SolveButtonOption.DISABLED)
        elif option == OpenButtonOption.NORMAL:
            self.openButton["state"] = "normal"
        elif option == OpenButtonOption.DISABLED:
            self.openButton["state"] = "disabled"
        self.openButton.update()

    def writeButtonSwitch(self, option):
        if option == WriteButtonOption.WRITE:
            self.writeButton["text"] = "Save"
            self.writeButton["state"] = "normal"
            self.openButtonSwitch(OpenButtonOption.DISABLED)
            self.clearButtonSwitch(ClearButtonOption.NORMAL)
        elif option == WriteButtonOption.SAVE:
            self.writeButton["text"] = "Write"
            self.writeButton["state"] = "normal"
            self.openButtonSwitch(OpenButtonOption.NORMAL)
            self.clearButtonSwitch(ClearButtonOption.DISABLED)
        elif option == WriteButtonOption.NORMAL:
            self.writeButton["state"] = "normal"
        elif option == WriteButtonOption.DISABLED:
            self.writeButton["state"] = "disabled"
        self.writeButton.update()

    def clearButtonSwitch(self, option):
        if option == ClearButtonOption.NORMAL:
            self.clearButton["state"] = "normal"
        elif option == ClearButtonOption.DISABLED:
            self.clearButton["state"] = "disabled"
        self.clearButton.update()

    def solveButtonSwitch(self, option):
        if option == SolveButtonOption.CANCEL:
            self.solveButton["state"] = "disabled"
            self.solveButton["text"] = "Canceling.."
        elif option == SolveButtonOption.SOLVE:
            self.solveButton["text"] = "Cancel"
            self.solveButton["state"] = "normal"
            self.openButtonSwitch(OpenButtonOption.DISABLED)
            self.clearButtonSwitch(ClearButtonOption.DISABLED)
        elif option == SolveButtonOption.READY:
            self.solveButton["text"] = "Solve"
            self.solveButton["state"] = "normal"
            self.openButtonSwitch(OpenButtonOption.NORMAL)
            self.clearButtonSwitch(ClearButtonOption.NORMAL)
        elif option == SolveButtonOption.NORMAL:
            self.solveButton["state"] = "normal"
        elif option == SolveButtonOption.DISABLED:
            self.solveButton["state"] = "disabled"
        self.solveButton.update()

    def showStatistic(self, txt):
        self.statistic["text"] = txt

    def getPuzzleDialog(self, path="puzzles"):
        return filedialog.askopenfilename(initialdir=path)

    def savePuzzleDialog(self, path="puzzles"):
        return filedialog.asksaveasfile(initialdir=path, mode="w", defaultextension=".txt")

    def loadCommamd(self):
        self.openButton["command"] = self.openCmd
        self.writeButton["command"] = self.writeCmd
        self.clearButton["command"] = self.clearCmd
        self.solveButton["command"] = self.solveCmd
        self.window.bind('<Key>', self.pressCmd)
        self.board.bind('<Button-1>', self.clickCmd)

    def clickToLogicalPosition(self, x, y):
        row = int(y/(BOARD_SIZE/DIGIT_NUMBER))
        col = int(x/(BOARD_SIZE/DIGIT_NUMBER))
        return row, col