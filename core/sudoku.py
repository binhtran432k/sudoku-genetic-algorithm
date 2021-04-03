from numpy import copy
from numpy.random import normal
from .population import Population
from .candidate import Candidate
from .crossover import CycleCrossover
from .parentselection import Tournament
from .settings import CANDIDATE_NUMBER, ELITE_NUMBER, GENERATION_NUMBER, RenderOption

class Sudoku:
    """ Solves a given Sudoku puzzle using a genetic algorithm. """

    def __init__(self, given, render):
        self.given = given
        self.render = render
        self.bestValues = None
        self.reseedCount = 0
        self.exitFlag = False
        return
    
    def solve(self):
        renderTxt = "Seeding..."
        self.exitFlag = False
        self.render(renderTxt, None, RenderOption.ONLY_TEXT)
        mutationNumber = 0  # Number of mutations.
        
        # Mutation parameters.
        phi = 0
        sigma = 1
        mutationRate = 0.06
    
        # Create an initial population.
        self.population = Population()
        self.population.seed(CANDIDATE_NUMBER, self.given)
    
        # For up to 10000 generations...
        stale = 0
        self.reseedCount = 0
        for generation in range(0, GENERATION_NUMBER):
            if (self.exitFlag):
                return
            print("Generation %d" % generation)
            
            # Check for a solution.
            bestFitness = 0.0
            self.bestValues = None
            for c in range(0, CANDIDATE_NUMBER):
                fitness = self.population.candidates[c].fitness
                if(fitness == 1):
                    print("Solution found at generation %d!" % generation)
                    print(self.population.candidates[c].values)
                    renderTxt = "Solution found at generation %d!" % generation
                    self.render(renderTxt, self.population.candidates[c].values, RenderOption.FOUNDED)
                    return self.population.candidates[c]

                # Find the best fitness.
                if(fitness > bestFitness):
                    bestFitness = fitness
                    self.bestValues = self.population.candidates[c].values

            print("Best fitness: %f" % bestFitness)
            renderTxt = "Reseed count: %d\n" % self.reseedCount
            renderTxt += "Generation %d\n" % generation
            renderTxt += "Best fitness: %f\n" % bestFitness
            renderTxt += "Mutation rate: %f\n" % mutationRate
            self.render(renderTxt, self.bestValues)

            # Create the next population.
            nextPopulation = []

            # Select elites (the fittest candidates) and preserve them for the next generation.
            self.population.sort()
            elites = []
            for e in range(0, ELITE_NUMBER):
                elite = Candidate()
                elite.values = copy(self.population.candidates[e].values)
                elites.append(elite)

            # Create the rest of the candidates.
            for count in range(ELITE_NUMBER, CANDIDATE_NUMBER, 2):
                # Select parents from population via a tournament.
                t = Tournament()
                parent1 = t.compete(self.population.candidates)
                parent2 = t.compete(self.population.candidates)
                
                ## Cross-over.
                cc = CycleCrossover()
                child1, child2 = cc.crossover(parent1, parent2, crossoverRate=1.0)
                child1.updateFitness()
                child2.updateFitness()
                
                # Mutate child1.
                old_fitness = child1.fitness
                success = child1.mutate(mutationRate, self.given)
                child1.updateFitness()
                if(success):
                    mutationNumber += 1
                    if(child1.fitness > old_fitness):  # Used to calculate the relative success rate of mutations.
                        phi = phi + 1
                
                # Mutate child2.
                old_fitness = child2.fitness
                success = child2.mutate(mutationRate, self.given)
                child2.updateFitness()
                if(success):
                    mutationNumber += 1
                    if(child2.fitness > old_fitness):  # Used to calculate the relative success rate of mutations.
                        phi = phi + 1
                
                # Add children to new population.
                nextPopulation.append(child1)
                nextPopulation.append(child2)

            # Append elites onto the end of the population. These will not have been affected by crossover or mutation.
            for e in range(0, ELITE_NUMBER):
                nextPopulation.append(elites[e])
                
            # Select next generation.
            self.population.candidates = nextPopulation
            self.population.updateFitness()
            
            # Calculate new adaptive mutation rate (based on Rechenberg's 1/5 success rule). This is to stop too much mutation as the fitness progresses towards unity.
            if(mutationNumber == 0):
                phi = 0  # Avoid divide by zero.
            else:
                phi = phi / mutationNumber
            
            if(phi > 0.2):
                sigma = sigma/0.998
            elif(phi < 0.2):
                sigma = sigma*0.998

            mutationRate = abs(normal(loc=0.0, scale=sigma, size=None))
            mutationNumber = 0
            phi = 0

            # Check for stale population.
            self.population.sort()
            if(self.population.candidates[0].fitness != self.population.candidates[1].fitness):
                stale = 0
            else:
                stale += 1

            # Re-seed the population if 100 generations have passed with the fittest two candidates always having the same fitness.
            if(stale >= 100):
                print("The population has gone stale. Re-seeding...")
                self.reseedCount += 1
                renderTxt = "The population has gone stale. Re-seeding..."
                self.render(renderTxt, None, RenderOption.ONLY_TEXT)
                self.population.seed(CANDIDATE_NUMBER, self.given)
                stale = 0
                sigma = 1
                phi = 0
                mutationNumber = 0
                mutationRate = 0.06

        
        print("No solution found.")
        renderTxt = "No solution found."
        self.render(renderTxt, self.bestValues, RenderOption.NOT_FOUND)
        return None
