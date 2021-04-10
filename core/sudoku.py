from .population import Population
from .given import given
from .settings import POPULATION_SIZE, MAX_GENERATION, RenderOption
from .settings import DIGIT_NUMBER, MAX_STALE_COUNT, GOAL
from .helper import encodePuzzle, copyGrid, sameRowIndexes, sameColumnIndexes, sameBlockIndexes

class Sudoku:
    def __init__(self, render):
        self.render = render # render the ui when change
        self.reinitializationCount = 0 # count the reinitialization
        self.exitFlag = False # cancel solving when it is True
        self.encodedGiven = encodePuzzle(given.values)
        self.trackGrid = None
        self.population = Population()

    def fillPredetermined(self):
        """
        Fills some predetermined cells of the Sudoku grid using a pencil marking method.
        """
        self.trackGrid = copyGrid(self.encodedGiven, lambda i, j: set(range(1, DIGIT_NUMBER + 1)))

        def pencilMark(i, j):
            """
            Marks the value of grid[i][j] element in it's row, column and block.

            Parameters:
                - i (int): Block's index.
                - j (int): Block's element index.

            Returns: The more completed version of the grid.
            """
            # remove from same block cells
            for a, b in sameBlockIndexes(i, j, itself=False):
                self.trackGrid[a][b].discard(self.encodedGiven[i][j])

            # remove from same row cells
            for a, b in sameRowIndexes(i, j, itself=False):
                self.trackGrid[a][b].discard(self.encodedGiven[i][j])

            # remove from same column cells
            for a, b in sameColumnIndexes(i, j, itself=False):
                self.trackGrid[a][b].discard(self.encodedGiven[i][j])

        for i in range(DIGIT_NUMBER):
            for j in range(DIGIT_NUMBER):
                if self.encodedGiven[i][j] != 0:
                    pencilMark(i, j)

        while True:
            anythingChanged = False

            for i in range(DIGIT_NUMBER):
                for j in range(DIGIT_NUMBER):
                    if self.encodedGiven[i][j] != 0:
                        continue

                    elif len(self.trackGrid[i][j]) == 0:
                        renderTxt = 'The puzzle is unsolvable'
                        self.render(renderTxt, RenderOption.NOT_FOUND)
                        return False
                    elif len(self.trackGrid[i][j]) == 1:
                        self.encodedGiven[i][j] = list(self.trackGrid[i][j])[0]
                        pencilMark(i, j)

                        anythingChanged = True

            if not anythingChanged:
                return True

    def solve(self):
        """
        Solves a given Sudoku puzzle using a genetic algorithm.
        """
        self.exitFlag = False

        # Fill all predetermined value for the puzzle
        self.fillPredetermined()
        print(*self.encodedGiven, sep="\n")
        renderTxt = "Initializing..."
        self.render(renderTxt, RenderOption.ONLY_TEXT)

        # Generate initial candidates
        self.population.initializeCandidates(POPULATION_SIZE, self.encodedGiven, self.trackGrid)
        prevBestFitness = 0
        stale = 0
        cumElites = []
        self.reinitializationCount = 0

        # For up to 2000 generations...
        for i in range(MAX_GENERATION):
            if self.exitFlag:
                return

            # Update the best candidate for each generation
            given.bestCandidate = self.population.candidates[0]
            prevBestFitness = self.population.candidates[0].fitness

            if i % 1 == 0:
                print("Generation %d" % i)
                print("Best score: %d" % prevBestFitness)
                print("Worst score: %d" % self.population.candidates[-1].fitness)

            renderTxt = "Generation %d\n" % i
            renderTxt += "Best fitness: %d\n" % prevBestFitness
            renderTxt += "Worst fitness: %d\n" % self.population.candidates[-1].fitness
            renderTxt += "Reinitialization count: %d\n" % self.reinitializationCount

            # Check for a solution
            if prevBestFitness == GOAL:
                renderTxt = "Solution found at generation %d!" % i
                self.render(renderTxt, RenderOption.FOUNDED)
                return
            else:
                self.render(renderTxt)

            # Go to next generation if the current population doesn't have solution
            self.population.nextGen(self.encodedGiven, self.trackGrid)

            # Check for stale population
            if self.population.candidates[0].fitness != prevBestFitness:
                stale = 0
            else:
                stale += 1

            # Re-seed the population if 30 generations have passed with the fittest value not improving.
            if stale > MAX_STALE_COUNT:
                # print("The population has gone stale. Searching in local space...")
                # self.population.localSearch(3, self.given, self.track_grid)
                self.reinitializationCount += 1
                renderTxt = "The population has gone stale. Reinitializing..."
                self.render(renderTxt, RenderOption.ONLY_TEXT)
                
                # Store the top few solutions (candiddates) from each stale population
                # When enough top solutions accumulate, a new population is created from these best solutions
                # and used as an initial population when the GA is restarted.
                if len(cumElites) < POPULATION_SIZE:
                    numElite = int(POPULATION_SIZE * 0.1)
                    cumElites.extend(self.population.candidates[:numElite])
                    self.population.initializeCandidates(POPULATION_SIZE, self.encodedGiven, self.trackGrid)
                else:
                    print("Activate cumulative method")
                    self.population.candidates = cumElites
                    cumElites = []
                stale = 0
        
        renderTxt = "No solution found."
        self.render(renderTxt, RenderOption.NOT_FOUND)
        return None
