from tkinter import Tk, Canvas, Frame, Button, Label, filedialog

from .settings import ClearButtonOption, DIGIT_NUMBER, BLOCK_NUMBER, BOARD_SIZE, DIGIT_SIZE, LINE_COLOR
from .settings import DIGIT_SPACE, DUPLICATE_DIGIT_BG, DUPLICATE_DIGIT_GIVEN_BG, FONT_FAMILY
from .settings import OpenButtonOption, SOLUTION_DIGIT_BG, SOLUTION_DIGIT_GIVEN_BG
from .settings import SolveButtonOption, TRANSPARENT_DIGIT_BG, WriteButtonOption
from .settings import GIVEN_DIGIT_COLOR, NORMAL_DIGIT_COLOR, TEXT_SIZE
from .given import given

class Ui:
    """
    The UI of the sudoku app
    """
    def __init__(self):
        # Initial window of app
        self.window = Tk()
        self.window.title("Sudoku") # app title
        self.window.resizable(0, 0) # make it cannot resize because size is fixed
        self.mainBody = None # main body of app, it store sudoku board
        self.board = None # sudoku board
        self.boardItems = [] # use to store items
        self.boardItemBgs = [] # use to store items background
        # Button list
        self.openButton = None
        self.writeButton = None
        self.clearButton = None
        self.solveButton = None
        self.createWidgets()

        # Command list to assign to button, use for app
        self.openCmd = None
        self.writeCmd = None
        self.clearCmd = None
        self.solveCmd = None
        self.pressCmd = None
        self.clickCmd = None

    def mainloop(self):
        """
        Keep the app showing when exit is not clicked
        """
        self.window.mainloop()

    def createWidgets(self):
        """
        Create all widgets for the UI
        """
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
        """"
        Intialize the board for sudoku
        """
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
                    (i+1)*BOARD_SIZE/DIGIT_NUMBER, BOARD_SIZE, fill=LINE_COLOR)
            # Horizontal lines
            self.board.create_line(0, (i+1)*BOARD_SIZE/DIGIT_NUMBER, BOARD_SIZE,
                    (i+1)*BOARD_SIZE/DIGIT_NUMBER, fill=LINE_COLOR)

        # Create big seperate digit set line
        for i in range(BLOCK_NUMBER - 1):
            # Vertical lines
            self.board.create_line((i+1)*BOARD_SIZE/BLOCK_NUMBER, 0,
                    (i+1)*BOARD_SIZE/BLOCK_NUMBER, BOARD_SIZE, width=5, fill=LINE_COLOR)
            # Horizontal lines
            self.board.create_line(0, (i+1)*BOARD_SIZE/BLOCK_NUMBER, BOARD_SIZE,
                    (i+1)*BOARD_SIZE/BLOCK_NUMBER, width=5, fill=LINE_COLOR)

    def drawItem(self, row, col, value, color=NORMAL_DIGIT_COLOR):
        """
        Draw specific item value to board
        """
        # Make item be empty when value is zero else set it to value
        if (value == 0):
            self.board.itemconfig(self.boardItems[row][col],
                    text="", fill=color)
        else:
            self.board.itemconfig(self.boardItems[row][col],
                    text=str(value), fill=color)

    def drawItemBg(self, row, col, color=DUPLICATE_DIGIT_BG):
        """
        Draw background of specific item to board
        """
        self.board.itemconfig(self.boardItemBgs[row][col],
            fill=color)

    def drawGivenBoard(self, color=GIVEN_DIGIT_COLOR):
        """
        Draw all given items to board
        """
        for row in range(DIGIT_NUMBER):
            for col in range(DIGIT_NUMBER):
                if (given.values[row][col] != 0):
                    self.drawItem(row, col, given.values[row][col], color)

    def drawRemainBoard(self, values, color=NORMAL_DIGIT_COLOR):
        """
        Draw all specific items values to board except given values
        """
        for row in range(DIGIT_NUMBER):
            for col in range(DIGIT_NUMBER):
                if (given.values[row][col] == 0):
                    self.drawItem(row, col, values[row][col], color)

    def drawDuplicateBg(self):
        """
        Draw background for all duplicated values else keep transparent
        """
        for row in range(DIGIT_NUMBER):
            for col in range(DIGIT_NUMBER):
                color = DUPLICATE_DIGIT_BG
                if (given.duplicateValues[row][col] == 0):
                    color = TRANSPARENT_DIGIT_BG
                elif (given.values[row][col] != 0):
                    color = DUPLICATE_DIGIT_GIVEN_BG
                self.drawItemBg(row, col, color)

    def drawSolutionBg(self):
        """
        Draw solution background to board
        """
        for row in range(DIGIT_NUMBER):
            for col in range(DIGIT_NUMBER):
                color = SOLUTION_DIGIT_BG
                if (given.duplicateValues[row][col] != 0):
                    color = TRANSPARENT_DIGIT_BG
                elif (given.values[row][col] != 0):
                    color = SOLUTION_DIGIT_GIVEN_BG
                self.drawItemBg(row, col, color)

    def openButtonSwitch(self, option):
        """
        Control Open button UI when it is clicked
        """
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
        """
        Control Write button UI when it is clicked
        """
        if option == WriteButtonOption.WRITE:
            self.writeButton["text"] = "Save"
            self.writeButton["state"] = "normal"
            self.openButtonSwitch(OpenButtonOption.DISABLED)
            self.clearButtonSwitch(ClearButtonOption.NORMAL)
            self.solveButtonSwitch(SolveButtonOption.WRITE)
        elif option == WriteButtonOption.SAVE:
            self.writeButton["text"] = "Write"
            self.writeButton["state"] = "normal"
            self.openButtonSwitch(OpenButtonOption.NORMAL)
            self.clearButtonSwitch(ClearButtonOption.DISABLED)
            self.solveButtonSwitch(SolveButtonOption.READY)
            self.solveButtonSwitch(SolveButtonOption.DISABLED)
        elif option == WriteButtonOption.NORMAL:
            self.writeButton["state"] = "normal"
        elif option == WriteButtonOption.DISABLED:
            self.writeButton["state"] = "disabled"
        self.writeButton.update()

    def clearButtonSwitch(self, option):
        """
        Control Clear button UI when it is clicked
        """
        if option == ClearButtonOption.NORMAL:
            self.clearButton["state"] = "normal"
        elif option == ClearButtonOption.DISABLED:
            self.clearButton["state"] = "disabled"
        self.clearButton.update()

    def solveButtonSwitch(self, option):
        """
        Control Solve button UI when it is clicked
        """
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
        elif option == SolveButtonOption.RELOAD:
            self.solveButton["text"] = "Resolve"
            self.solveButton["state"] = "normal"
            self.openButtonSwitch(OpenButtonOption.NORMAL)
            self.clearButtonSwitch(ClearButtonOption.NORMAL)
        elif option == SolveButtonOption.WRITE:
            self.solveButton["text"] = "Cancel"
            self.solveButton["state"] = "normal"
        self.solveButton.update()

    def showStatistic(self, txt):
        """
        Show statistic text to UI
        """
        self.statistic["text"] = txt

    def getPuzzleDialog(self, path="puzzles"):
        """
        Open get puzzle path dialog and return it to open
        """
        return filedialog.askopenfilename(initialdir=path)

    def savePuzzleDialog(self, path="puzzles"):
        """
        Open get puzzle path dialog and return it to save
        """
        return filedialog.asksaveasfile(initialdir=path, mode="w", defaultextension=".txt")

    def loadCommamd(self):
        """
        Load all command to buttons, click and press aciton
        """
        self.openButton["command"] = self.openCmd
        self.writeButton["command"] = self.writeCmd
        self.clearButton["command"] = self.clearCmd
        self.solveButton["command"] = self.solveCmd
        self.window.bind('<Key>', self.pressCmd)
        self.board.bind('<Button-1>', self.clickCmd)

    def clickToLogicalPosition(self, x, y):
        """
        Convert Posion of clicked position to sudoku puzzle board position
        """
        row = int(y/(BOARD_SIZE/DIGIT_NUMBER))
        col = int(x/(BOARD_SIZE/DIGIT_NUMBER))
        return row, col