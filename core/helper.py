from numpy import array as npArray, zeros_like as zerosLike
from .settings import BLOCK_NUMBER, DIGIT_NUMBER

def sameColumnIndexes(i, j, itself=True):
    """
    A generator function that yields indexes of the elements that are in the same column as the input indexes.

    Parameters:
        - i (int): Block's index.
        - j (int): Block's element index.
        - itself (bool) (optional=True): Indicates whether to yield the input indexes or not.
    """

    DIGIT_NUMBER = BLOCK_NUMBER * BLOCK_NUMBER
    blockColumn = i % BLOCK_NUMBER
    cellColumn = j % BLOCK_NUMBER

    for a in range(blockColumn, DIGIT_NUMBER, BLOCK_NUMBER):
        for b in range(cellColumn, DIGIT_NUMBER, BLOCK_NUMBER):
            if (a, b) == (i, j) and not itself:
                continue

            yield (a, b)


def sameRowIndexes(i, j, itself=True):
    """
    A generator function that yields indexes of the elements that are in the same row as the input indexes.

    Parameters:
        - i (int): Block's index.
        - j (int): Block's element index.
        - itself (bool) (optional=True): Indicates whether to yield the input indexes or not.
    """

    blockRow = int(i / BLOCK_NUMBER)
    cellRow = int(j / BLOCK_NUMBER)

    for a in range(blockRow * BLOCK_NUMBER, blockRow * BLOCK_NUMBER + BLOCK_NUMBER):
        for b in range(cellRow * BLOCK_NUMBER, cellRow * BLOCK_NUMBER + BLOCK_NUMBER):
            if (a, b) == (i, j) and not itself:
                continue

            yield (a, b)


def sameBlockIndexes(i, j, itself=True):
    """
    A generator function that yields indexes of the elements that are in the same Block as the input indexes.

    Parameters:
        - i (int): Block's index.
        - j (int): Block's element index.
        - itself (bool) (optional=True): Indicates whether to yield the input indexes or not.
    """

    for k in range(BLOCK_NUMBER * BLOCK_NUMBER):
        if k == j and not itself:
            continue

        yield (i, k)


def getCellsFromIndexes(grid, indexes):
    """
    A generator function that yields the values of a list of grid indexes.

    Parameters:
        - grid (list)
        - indexes (list) : e.g. [(1, 2), (3, 10)]
    """

    for a, b in indexes:
        yield grid[a][b]

def copyGrid(grid, elementGennerator=None):
    """
    Returns an empty Sudoku grid.

    Parameters:
        - elementGennerator (function) (optional=None): Is is used to generate initial values of the grid's elements.
            If it's not given, all grid's elements will be "None".
    """

    return npArray([
        [
            (0 if elementGennerator is None else elementGennerator(i, j))
            for j in range(len(grid))
        ] for i in range(len(grid))
    ])

def encodePuzzle(grid):
    """
    Returns chromosome of Sudoku puzzle. The chromosome of a puzzle is 
    defined as an array of 81 numbers that is divided into nine sub block.

    Parameters:
        - grid: Sudoku puzzle
    """
    chromosome = [[] for i in range(DIGIT_NUMBER)]
    for j in range(DIGIT_NUMBER):
        for i in range(DIGIT_NUMBER):
            chromosome[
                int(i / BLOCK_NUMBER) +
                int(j / BLOCK_NUMBER) * BLOCK_NUMBER
                ].append(grid[j][i])

    return npArray(chromosome)

def decodePuzzle(chromosome):
    """
    Returns Sudoku puzzle of chromosome.

    Parameters:
        - chromosome: Chromosome.
    """
    grid = zerosLike(chromosome)

    i = 0
    for a, b in sameColumnIndexes(0, 0, BLOCK_NUMBER):
        row = list(getCellsFromIndexes(chromosome, sameRowIndexes(a, b, BLOCK_NUMBER)))
        grid[i] = npArray(row)
        i +=1

    return grid