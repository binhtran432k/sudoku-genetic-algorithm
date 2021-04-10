import random
from numpy import zeros, copy as npCopy

from .mutation import mutation
from .fitness import fitness
from .settings import DIGIT_NUMBER, BLOCK_NUMBER

class Candidate:
    def __init__(self):
        self.gene = zeros((DIGIT_NUMBER, DIGIT_NUMBER), dtype=int)
        self.fitness = 0
        
        # The fitness matrix stores fitness scores for each row of
        # sub-grid and each col of sub-grid in the chromosome
        self.fitnessMatrix = zeros((2, BLOCK_NUMBER), dtype=int)
        self.localSearchMethod = mutation.swapMutate

    def updateFitness(self, tracker):
        """
        Calculates the fitness value for a candidate.
        """
        self.fitness = fitness.call(self, tracker)

    def mutate(self, mutationRate, given):
        """
        Mutates a candidate with a mutationRate.
        """
        r = random.random()
        if r < mutationRate:  # Mutate.
            return mutation.call(self, given)
    
        return False

    def localSearch(self, coef, given):
        candidateList = []
        for _ in range(coef):
            candidate = Candidate()
            candidate.gene = npCopy(self.gene)
            candidate.localSearchMethod(self, given)
            candidateList.append(candidate)
        
        return candidateList
