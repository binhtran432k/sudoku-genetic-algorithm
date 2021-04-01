import sys
from sudoku import Sudoku

def main(argv):
    s = Sudoku()
    puzzle = "puzzle_easy"
    s.load("./puzzles/" + puzzle + ".txt")
    solution = s.solve()
    if(solution):
        s.save("./solutions/" + puzzle + ".txt", solution)

if __name__ == "__main__":
    main(sys.argv[1:])
