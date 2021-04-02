from numpy import sqrt


DIGIT_NUMBER = 9  # Number of digits (in the case of standard Sudoku puzzles, this is 9).
BOX_NUMBER = int(sqrt(DIGIT_NUMBER))
CANDIDATE_NUMBER = 1000  # Number of candidates (i.e. population size).
ELITE_NUMBER = int(0.05*CANDIDATE_NUMBER)  # Number of elites.
GENERATION_NUMBER = 1000  # Number of generations.

BOX_SIZE = 600
FONT_SIZE = 36
class RenderOption:
    NORMAL = 0
    FOUNDED = 1
    NOT_FOUND = 2
    ONLY_TEXT = 3