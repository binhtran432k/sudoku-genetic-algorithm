from numpy import zeros
import random
random.seed()
from .candidate import Candidate
from .settings import DIGIT_NUMBER
from .given import given

class Population:
    """ A set of candidate solutions to the Sudoku puzzle. These candidates are also known as
    the chromosomes in the population. """

    def __init__(self):
        self.candidates = []
        return

    def seed(self, candidateNum):
        self.candidates = []
        
        # Seed a new population.       
        for p in range(0, candidateNum):
            g = Candidate()
            for i in range(0, DIGIT_NUMBER): # New row in candidate.
                row = zeros(DIGIT_NUMBER)
                
                # Fill in the givens.
                for j in range(0, DIGIT_NUMBER): # New column j value in row i.
                
                    # If value is already given, don't change it.
                    if(given.values[i][j] != 0):
                        row[j] = given.values[i][j]
                    # Fill in the gaps using the helper board.
                    elif(given.values[i][j] == 0):
                        row[j] = given.helper.values[i][j][random.randint(0, len(given.helper.values[i][j])-1)]

                # If we don't have a valid board, then try again. There must be no duplicates in the row.
                while(len(list(set(row))) != DIGIT_NUMBER):
                    for j in range(0, DIGIT_NUMBER):
                        if(given.values[i][j] == 0):
                            row[j] = given.helper.values[i][j][random.randint(0, len(given.helper.values[i][j])-1)]

                g.values[i] = row

            self.candidates.append(g)
        
        # Compute the fitness of all candidates in the population.
        self.updateFitness()
        
        print("Seeding complete.")
        
        return
        
    def updateFitness(self):
        """ Update fitness of every candidate/chromosome. """
        for candidate in self.candidates:
            candidate.updateFitness()
        return
        
    def sort(self):
        """ Sort the population based on fitness. """
        self.candidates.sort(key=lambda x:-x.fitness)
        return