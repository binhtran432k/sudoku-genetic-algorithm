import numpy
import random
random.seed()
from sudoku import Given, Population, Candidate, CycleCrossover, Tournament

class Sudoku:
    """ Solves a given Sudoku puzzle using a genetic algorithm. """

    def __init__(self):
        self.given = None
        self.digitNumber = 9  # Number of digits (in the case of standard Sudoku puzzles, this is 9).
        self.candidateNumber = 1000  # Number of candidates (i.e. population size).
        self.eliteNumber = int(0.05*self.candidateNumber)  # Number of elites.
        self.generationNumber = 1000  # Number of generations.
        return
    
    def load(self, path):
        # Load a configuration to solve.
        with open(path, "r") as f:
            values = numpy.loadtxt(f).reshape((self.digitNumber, self.digitNumber)).astype(int)
            self.given = Given(values, self.digitNumber)
        return

    def save(self, path, solution):
        # Save a configuration to a file.
        with open(path, "w") as f:
            numpy.savetxt(f, solution.values.reshape(self.digitNumber, self.digitNumber), fmt='%d')
        return
        
    def solve(self):
        mutationNumber = 0  # Number of mutations.
        
        # Mutation parameters.
        phi = 0
        sigma = 1
        mutation_rate = 0.06
    
        # Create an initial population.
        self.population = Population(self.digitNumber)
        self.population.seed(self.candidateNumber, self.given)
    
        # For up to 10000 generations...
        stale = 0
        for generation in range(0, self.generationNumber):
        
            print("Generation %d" % generation)
            
            # Check for a solution.
            best_fitness = 0.0
            for c in range(0, self.candidateNumber):
                fitness = self.population.candidates[c].fitness
                if(fitness == 1):
                    print("Solution found at generation %d!" % generation)
                    print(self.population.candidates[c].values)
                    return self.population.candidates[c]

                # Find the best fitness.
                if(fitness > best_fitness):
                    best_fitness = fitness

            print("Best fitness: %f" % best_fitness)

            # Create the next population.
            next_population = []

            # Select elites (the fittest candidates) and preserve them for the next generation.
            self.population.sort()
            elites = []
            for e in range(0, self.eliteNumber):
                elite = Candidate(self.digitNumber)
                elite.values = numpy.copy(self.population.candidates[e].values)
                elites.append(elite)

            # Create the rest of the candidates.
            for count in range(self.eliteNumber, self.candidateNumber, 2):
                # Select parents from population via a tournament.
                t = Tournament()
                parent1 = t.compete(self.population.candidates)
                parent2 = t.compete(self.population.candidates)
                
                ## Cross-over.
                cc = CycleCrossover(self.digitNumber)
                child1, child2 = cc.crossover(parent1, parent2, crossover_rate=1.0)
                child1.update_fitness()
                child2.update_fitness()
                
                # Mutate child1.
                old_fitness = child1.fitness
                success = child1.mutate(mutation_rate, self.given)
                child1.update_fitness()
                if(success):
                    mutationNumber += 1
                    if(child1.fitness > old_fitness):  # Used to calculate the relative success rate of mutations.
                        phi = phi + 1
                
                # Mutate child2.
                old_fitness = child2.fitness
                success = child2.mutate(mutation_rate, self.given)
                child2.update_fitness()
                if(success):
                    mutationNumber += 1
                    if(child2.fitness > old_fitness):  # Used to calculate the relative success rate of mutations.
                        phi = phi + 1
                
                # Add children to new population.
                next_population.append(child1)
                next_population.append(child2)

            # Append elites onto the end of the population. These will not have been affected by crossover or mutation.
            for e in range(0, self.eliteNumber):
                next_population.append(elites[e])
                
            # Select next generation.
            self.population.candidates = next_population
            self.population.update_fitness()
            
            # Calculate new adaptive mutation rate (based on Rechenberg's 1/5 success rule). This is to stop too much mutation as the fitness progresses towards unity.
            if(mutationNumber == 0):
                phi = 0  # Avoid divide by zero.
            else:
                phi = phi / mutationNumber
            
            if(phi > 0.2):
                sigma = sigma/0.998
            elif(phi < 0.2):
                sigma = sigma*0.998

            mutation_rate = abs(numpy.random.normal(loc=0.0, scale=sigma, size=None))
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
                self.population.seed(self.candidateNumber, self.given)
                stale = 0
                sigma = 1
                phi = 0
                mutationNumber = 0
                mutation_rate = 0.06
        
        print("No solution found.")
        return None
