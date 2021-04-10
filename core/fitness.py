from numpy import zeros
from .helper import sameColumnIndexes, sameRowIndexes
from .settings import BLOCK_NUMBER, FITNESS_CHOICE, FitnessOption

class Fitness:
    def __init__(self):
        self.call = self.getChoice()

    def getChoice(self, option=FITNESS_CHOICE):
        if option == FitnessOption.DIFFERENT:
            return self.differentFitness
        elif option == FitnessOption.PERFECT:
            return self.perfectFitness

    def differentFitness(self, candidate, tracker=None):
        """  The fitness of a candidate solution is determined by
        total sum of number of different numberals in each row and column
        
        Parameters:
            - candidate (Candidate): The candidate to evaluate
            - tracker (array): Helper array that determines all possible values for each cell in the chromosome
        """
        rowFitness = 0
        colFitness = 0
        candidate.fitnessMatrix = zeros((2, BLOCK_NUMBER), dtype=int)

        # calculate rows duplicates
        for a, b in sameColumnIndexes(0, 0):
            row = set()
            for x, y in sameRowIndexes(a, b):
                value = candidate.gene[x][y]
                row.add(value)

            rowFitness += len(row)
            candidate.fitnessMatrix[0][a // BLOCK_NUMBER] += len(row)
        
        for a, b in sameRowIndexes(0, 0):
            col = set()
            for x, y in sameColumnIndexes(a, b):
                value = candidate.gene[x][y]
                col.add(value)

            colFitness += len(col)
            candidate.fitnessMatrix[1][a] += len(col)

        return rowFitness + colFitness

    def perfectFitness(self, candidate, tracker=None):
        """  The fitness of a candidate solution is determined by
        sum of number of different numberals in each row and column
        minus total number of cell that contains invalid value
        
        Parameters:
            - candidate (Candidate): The candidate to evaluate
            - tracker (array): Helper array that determines all possible values for each cell in the chromosome
        """
        rowFitness = 0
        colFitness = 0
        duplicatesCount = 0
        candidate.fitnessMatrix = zeros((2, BLOCK_NUMBER), dtype=int)

        # calculate rows duplicates
        for a, b in sameColumnIndexes(0, 0):
            row = set()
            for x, y in sameRowIndexes(a, b):
                value = candidate.gene[x][y]
                row.add(value)
                if value not in tracker[x][y]:
                    duplicatesCount += 1

            rowFitness += len(row)
            candidate.fitnessMatrix[0][a // BLOCK_NUMBER] += len(row)
        
        for a, b in sameRowIndexes(0, 0):
            col = set()
            for x, y in sameColumnIndexes(a, b):
                value = candidate.gene[x][y]
                col.add(value)
                if value not in tracker[x][y]:
                    duplicatesCount += 1

            colFitness += len(col)
            candidate.fitnessMatrix[1][a] += len(col)

        return rowFitness + colFitness - duplicatesCount

fitness = Fitness()