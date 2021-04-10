import random
from numpy import copy as npCopy

from .candidate import Candidate
from .selection import selection
from .crossover import crossover
from .settings import DIGIT_NUMBER, MUTATION_RATE, POPULATION_SIZE, ELITE_NUMBER, CROSSOVER_RATE

class Population:
    """ A set of candidate solutions to the Sudoku puzzle. These candidates are also known as
    the chromosomes in the population. """
    def __init__(self):
        self.candidates = []
        self.populationSize = POPULATION_SIZE
        self.elitism = ELITE_NUMBER
        self.mutationRate = MUTATION_RATE
        self.crossoverRate = CROSSOVER_RATE
    
    def initializeCandidates(self, number, given, tracker):
        """
        Generates an initial population of size "number".

        Parameters:
            - number (int): Number of candidates to generate
            - given (array): The given chromosome of the Sudoku problem
            - tracker (array): Helper array to help evaluate candidates' fitness
        """

        self.candidates = []
        for _ in range(number):
            candidate = Candidate()
            # For each sub grid of candidate
            for i in range(DIGIT_NUMBER):
                # Generate a list of possible value to fill in
                shuffledBlock = list(range(1, DIGIT_NUMBER + 1))

                # Remove all the given values in this sub grid of the given chromosome from possible values list
                for j in range(DIGIT_NUMBER):
                    if given[i][j] != 0:
                        candidate.gene[i][j] = given[i][j]

                        shuffledBlock.remove(given[i][j])

                # Shuffle the list so that possible values can be filled in randomly
                random.shuffle(shuffledBlock)
                for j in range(DIGIT_NUMBER):
                    # Fill possible value to unknown cell in the sub grid
                    if given[i][j] == 0:
                        candidate.gene[i][j] = shuffledBlock.pop()

            self.candidates.append(candidate)
        
        # Evaluate fitness for the population
        self.evaluate(tracker)

    def localSearch(self, coef, given, tracker):
        newPopulation = []
        for candidate in self.candidates:
            newPopulation.extend(candidate.localSearch(coef, given))
        
        list(map(lambda x: x.updateFitness(tracker), newPopulation))
        
        newPopulation.sort(key = lambda x: -x.fitness)
        topNum = 10
        topFit = newPopulation[:topNum]
        newPopulation = newPopulation[topNum:]
        # random.shuffle(newPopulation)
        self.candidates = topFit + random.choices(newPopulation, k=self.populationSize - topNum)
    
    def sort(self):
        """ Sort the population based on fitness. """
        self.candidates.sort(key = lambda x: -x.fitness)
    
    def evaluate(self, tracker):
        """ Evaluate fitness of every candidate/chromosome in the population. """
        list(map(lambda x: x.updateFitness(tracker), self.candidates))
        self.sort()

    def nextGen(self, given, tracker):
        """ 
        Find the next generation of the population".

        Parameters:
            - given (array): The given chromosome of the Sudoku problem, helps in mutation process of candidates
            - tracker (array): Helper array to help evaluate candidates' fitness
        """
        elites = []
        numElite = self.elitism

        # Extract top candidate from population. These elite candidates will 
        # go to the next generation without any change
        for i in range(numElite):
            elite = Candidate()
            elite.gene = npCopy(self.candidates[i].gene)
            elites.append(elite)

        selectCandidates = selection.call(self.candidates, self.populationSize - numElite)

        newPopulation = []
        for _ in range(0, self.populationSize - numElite, 2):
            # Select 2 parents
            parents = [selectCandidates.pop(), selectCandidates.pop()]
            # parents = selection.call(self.candidates, 2)

            # Crossover them to generate new child for next generation with a crossover rate
            child1, child2 = crossover.call(parents[0], parents[1], self.crossoverRate)

            # Add child to the next genration population
            newPopulation.append(child1)
            newPopulation.append(child2)
        
        self.candidates = newPopulation
        # Mutate candidates in the next generation with a mutation rate
        list(map(lambda x: x.mutate(self.mutationRate, given), self.candidates))
        self.candidates.extend(elites)

        # Evaluate fitness for the next generation
        self.evaluate(tracker)