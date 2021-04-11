from math import sqrt

""" Genetic Algorithm Settings """
DIGIT_NUMBER = 9  # Number of digits (Standard Sudoku is 9).
BLOCK_NUMBER = int(sqrt(DIGIT_NUMBER)) # Number of digits on 1 row per box.
POPULATION_SIZE = 1000  # Number of candidates (i.e. population size).
ELITE_NUMBER = 0  # Number of elites (Elites will alive after generation).
MAX_GENERATION = 2000  # Number of generations.
MUTATION_RATE = 0.8
CROSSOVER_RATE = 1
MAX_STALE_COUNT = 30
GOAL = DIGIT_NUMBER*DIGIT_NUMBER*2
# Algorithm Option
class FitnessOption:
    DIFFERENT = 0
    PERFECT = 1
class MutationOption:
    RANDOM = 0
    SWAP = 1
    MULTI_SWAP = 2
    ALL_SWAP = 3
    RANDOM_RESET = 4
class SelectionOption:
    RANKING = 0
    TOURNAMENT = 1
    TOP = 2
class CrossoverOption:
    RANDOM = 0
    ONE_POINT = 1
    TWO_POINT = 2
    ROW_COL = 3
    UNIFORM = 4
    CHOICE = 5
    HALF = 6
# Choose Algorithm Option
FITNESS_CHOICE = FitnessOption.PERFECT
MUTATION_CHOICE = MutationOption.MULTI_SWAP
SELECTION_CHOICE = SelectionOption.TOP
CROSSOVER_CHOICE = CrossoverOption.HALF

""" UI Setting """
BOARD_SIZE = 600
DIGIT_SIZE = 36
DIGIT_SPACE = int((BOARD_SIZE/DIGIT_NUMBER)/2)
TEXT_SIZE = 18
FONT_FAMILY = "*"
LINE_COLOR = "gray"
NORMAL_DIGIT_COLOR = "blue"
GIVEN_DIGIT_COLOR = "gray"
DUPLICATE_DIGIT_BG = "tomato"
DUPLICATE_DIGIT_GIVEN_BG = "orange"
SOLUTION_DIGIT_BG = "spring green"
SOLUTION_DIGIT_GIVEN_BG = "green yellow"
TRANSPARENT_DIGIT_BG = "white"
# UI Option
class RenderOption:
    NORMAL = 0
    FOUNDED = 1
    NOT_FOUND = 2
    ONLY_TEXT = 3
    RELOADED = 4
class OpenButtonOption:
    OPEN = 0
    CLOSE = 1
    NORMAL = 2
    DISABLED = 3
class WriteButtonOption:
    WRITE = 0
    SAVE = 1
    NORMAL = 2
    DISABLED = 3
class ClearButtonOption:
    NORMAL = 0
    DISABLED = 1
class SolveButtonOption:
    SOLVE = 0
    CANCEL = 1
    READY = 2
    NORMAL = 3
    DISABLED = 4
    RELOAD = 5
    WRITE = 6