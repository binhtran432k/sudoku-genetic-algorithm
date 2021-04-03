from numpy import sqrt

""" Genetic Algorithm Settings """
DIGIT_NUMBER = 9  # Number of digits (Standard Sudoku is 9).
BOX_NUMBER = int(sqrt(DIGIT_NUMBER)) # Number of digits on 1 row per box.
CANDIDATE_NUMBER = 1000  # Number of candidates (i.e. population size).
ELITE_NUMBER = int(0.05*CANDIDATE_NUMBER)  # Number of elites (Elites will alive after generation).
GENERATION_NUMBER = 1000  # Number of generations.

""" UI Setting """
BOARD_SIZE = 600
DIGIT_SIZE = 36
DIGIT_SPACE = int((BOARD_SIZE/DIGIT_NUMBER)/2)
TEXT_SIZE = 18
FONT_FAMILY = "*"
NORMAL_DIGIT_COLOR = "blue"
GIVEN_DIGIT_COLOR = "black"
FAILED_DIGIT_BG = "red"
# UI Option
class RenderOption:
    NORMAL = 0
    FOUNDED = 1
    NOT_FOUND = 2
    ONLY_TEXT = 3
class SolveButtonOption:
    SOLVE = 0
    STOP = 1
    READY = 2