import sys
from core import App

def main(argv):
    app = App()
    puzzle = "puzzle"
    if len(argv) >= 1:
        for e in argv:
            puzzle += "_" + str(e)
    else:
        puzzle += "_easy"
    app.run(puzzle)

if __name__ == "__main__":
    main(sys.argv[1:])
