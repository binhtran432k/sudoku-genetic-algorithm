from numpy import zeros
import random
random.seed()
from .candidate import Candidate
from .settings import digitNumber

class Population:	
    """ A set of candidate solutions to the Sudoku puzzle. These candidates are also known as the chromosomes in the population. """

    def __init__(self):
        self.candidates = []
        return

    def seed(self, Nc, given):
        self.candidates = []
        
        # Determine the legal values that each square can take.
        helper = Candidate()
        helper.values = [[[] for j in range(0, digitNumber)] for i in range(0, digitNumber)]
        for row in range(0, digitNumber):
            for column in range(0, digitNumber):
                for value in range(1, 10):
                    if((given.values[row][column] == 0) and not (given.is_column_duplicate(column, value) or given.is_block_duplicate(row, column, value) or given.is_row_duplicate(row, value))):
                        # Value is available.
                        helper.values[row][column].append(value)
                    elif(given.values[row][column] != 0):
                        # Given/known value from file.
                        helper.values[row][column].append(given.values[row][column])
                        break

        # Seed a new population.       
        for p in range(0, Nc):
            g = Candidate()
            for i in range(0, digitNumber): # New row in candidate.
                row = zeros(digitNumber)
                
                # Fill in the givens.
                for j in range(0, digitNumber): # New column j value in row i.
                
                    # If value is already given, don't change it.
                    if(given.values[i][j] != 0):
                        row[j] = given.values[i][j]
                    # Fill in the gaps using the helper board.
                    elif(given.values[i][j] == 0):
                        row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j])-1)]

                # If we don't have a valid board, then try again. There must be no duplicates in the row.
                while(len(list(set(row))) != digitNumber):
                    for j in range(0, digitNumber):
                        if(given.values[i][j] == 0):
                            row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j])-1)]

                g.values[i] = row

            self.candidates.append(g)
        
        # Compute the fitness of all candidates in the population.
        self.update_fitness()
        
        print("Seeding complete.")
        
        return
        
    def update_fitness(self):
        """ Update fitness of every candidate/chromosome. """
        for candidate in self.candidates:
            candidate.update_fitness()
        return
        
    def sort(self):
        """ Sort the population based on fitness. """
        self.candidates.sort(key=lambda x:-x.fitness)
        return