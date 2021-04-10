from .candidate import Candidate
from .settings import CROSSOVER_CHOICE, CrossoverOption
import random
from numpy import copy as npCopy, concatenate as npConcatenate

class Crossover:
    def __init__(self):
        self.call = self.getChoice()

    def getChoice(self, option=CROSSOVER_CHOICE):
        if option == CrossoverOption.RANDOM:
            return self.randomCrossover
        elif option == CrossoverOption.ONE_POINT:
            return self.onePointCrossover
        elif option == CrossoverOption.TWO_POINT:
            return self.twoPointcrossover
        elif option == CrossoverOption.ROW_COL:
            return self.rowColCrossover
        elif option == CrossoverOption.UNIFORM:
            return self.uniformCrossover
        elif option == CrossoverOption.CHOICE:
            return self.choiceCrossover
        elif option == CrossoverOption.HALF:
            return self.halfCrossover
    
    def randomCrossover(self, parent1, parent2, crossoverRate):
        randomMethods = [self.onePointCrossover, self.rowColCrossover,
                self.uniformCrossover, self.twoPointcrossover]
        randomWeights = [0.3, 0.4, 0.2, 0.1]
        method = random.choices(randomMethods, weights=randomWeights, k=1)[0]
        return method(parent1, parent2, crossoverRate)

    def onePointCrossover(self, parent1, parent2, crossoverRate):
        """ Create two new child candidates by crossing over parent genes.
        Parent genes are splitted by one point and then concatenate to generate child genes
        
        Parameters:
            - parent1 (Candidate): First parent to crossover
            - parent2 (Candidate): Second parent to crossover
            - crossoverRate (float): Ratio defines if these parents are crossover or not
        
        Return:
            Tuple of two child generate from the crossover process
        """

        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        grid1 = npCopy(parent1.gene)
        grid2 = npCopy(parent2.gene)

        gridSize = len(parent1.gene)

        r = random.random()
        if r < crossoverRate:
            # Get a ranom crossover point to split parent genes
            crossPoint = random.randint(1, gridSize - 2)
            child1.gene = npConcatenate((grid1[:crossPoint], grid2[crossPoint:]), axis=0)
            child2.gene = npConcatenate((grid2[:crossPoint], grid1[crossPoint:]), axis=0)
        else:
            child1.gene = grid1
            child2.gene = grid2

        return child1, child2

    def twoPointcrossover(self, parent1, parent2, crossoverRate):
        """ Create two new child candidates by crossing over parent genes.
        Parent genes are splitted by two point and then concatenate to generate child genes 
        
        Parameters:
            - parent1 (Candidate): First parent to crossover
            - parent2 (Candidate): Second parent to crossover
            - crossoverRate (float): Ratio defines if these parents are crossover or not
        
        Return:
            Tuple of two child generate from the crossover process
        """

        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        grid1 = npCopy(parent1.gene)
        grid2 = npCopy(parent2.gene)

        gridSize = len(parent1.gene)
        r = random.random()
        if r < crossoverRate:
            # Select two crossover point
            crossPoint1 = random.randint(1, gridSize - 2)
            crossPoint2 = random.randint(crossPoint1 + 1, gridSize - 1)
            # Swap all sub-blocks between two crossover points to generate new child
            child1.gene = npConcatenate((grid1[:crossPoint1], grid2[crossPoint1:crossPoint2], grid1[crossPoint2:]), axis=0)
            child2.gene = npConcatenate((grid2[:crossPoint1], grid1[crossPoint1:crossPoint2], grid2[crossPoint2:]), axis=0)
        else:
            child1.gene = grid1
            child2.gene = grid2

        return child1, child2

    def rowColCrossover(self, parent1, parent2, crossoverRate):
        """ Create two new child candidates by crossing over parent genes.
            When two child individuals are generated from two parents, scores are obtained 
            for each of the three rows that constitute the sub-blocks of the parents, 
            and a child inherits the ones with the highest scores. Then the columns are 
            compared in the same way and the other child inherits the ones with the highest scores. 
        
        Parameters:
            - parent1 (Candidate): First parent to crossover
            - parent2 (Candidate): Second parent to crossover
            - crossoverRate (float): Ratio defines if these parents are crossover or not
        
        Return:
            Tuple of two child generate from the crossover process
        """

        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        grid1 = parent1.gene
        grid2 = parent2.gene

        r = random.random()
        if r < crossoverRate:
            rowScore1 = parent1.fitnessMatrix[0]
            rowScore2 = parent2.fitnessMatrix[0]

            colScore1 = parent1.fitnessMatrix[1]
            colScore2 = parent2.fitnessMatrix[1]

            for i in range(3):
                # For each row of sub-block, the first child will inherit the row
                # with the highest fitness score between two parents
                if rowScore1[i] > rowScore2[i]:
                    child1.gene[3*i:3*(i+1)] = npCopy(grid1[3*i:3*(i+1)])
                else:
                    child1.gene[3*i:3*(i+1)] = npCopy(grid2[3*i:3*(i+1)])
                
                # For each col of sub-block, the first child will inherit the col
                # with the highest fitness score between two parents
                if colScore1[i] > colScore2[i]:
                    for j in range(3):
                        child2.gene[j * 3 + i] = npCopy(grid1[j * 3 + i])
                else:
                    for j in range(3):
                        child2.gene[j * 3 + i] = npCopy(grid2[j * 3 + i])
        else:
            child1.gene = npCopy(grid1)
            child2.gene = npCopy(grid2)

        return child1, child2

    def uniformCrossover(self, parent1, parent2, crossoverRate):
        """ Create two new child candidates by crossing over parent genes. 
        Parent genes will swap 2 consecutive sub-blocks to generate child genes
        
        Parameters:
            - parent1 (Candidate): First parent to crossover
            - parent2 (Candidate): Second parent to crossover
            - crossoverRate (float): Ratio defines if these parents are crossover or not
        
        Return:
            Tuple of two child generate from the crossover process
        """

        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        grid1 = npCopy(parent1.gene)
        grid2 = npCopy(parent2.gene)

        gridSize = len(parent1.gene)
        r = random.random()
        if r < crossoverRate:
            # Select a sub-block and swap them between two parents
            crossPoint = random.randint(0, gridSize - 1)
            tmp = grid1[crossPoint]
            grid1[crossPoint] = grid2[crossPoint]
            grid2[crossPoint] = tmp
            child1.gene = grid1
            child2.gene = grid2
        else:
            child1.gene = grid1
            child2.gene = grid2

        return child1, child2

    def choiceCrossover(self, parent1, parent2, crossoverRate):
        """ Create two new child candidates by crossing over parent genes.
        The child will randomly choose each sub grid from first parent or second parent 
        
        Parameters:
            - parent1 (Candidate): First parent to crossover
            - parent2 (Candidate): Second parent to crossover
            - crossoverRate (float): Ratio defines if these parents are crossover or not
        
        Return:
            Tuple of two child generate from the crossover process
        """

        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        grid1 = parent1.gene
        grid2 = parent2.gene

        gridSize = len(parent1.gene)
        r = random.random()
        if r < crossoverRate:
            for i in range(gridSize):
                # Randomly select sub-block from two parents to generate new child
                blocks = [grid1[i], grid2[i]]
                child1.gene[i] = npCopy(random.choice(blocks))
                child2.gene[i] = npCopy(random.choice(blocks))
        else:
            child1.gene = npCopy(grid1)
            child2.gene = npCopy(grid2)

        return child1, child2

    def halfCrossover(self, parent1, parent2, crossoverRate):
        """ Create two new child candidates by crossing over parent genes. 
        The first child will randomly choose each sub grid from first parent or second parent
        and the second child will get all unchoosen sub grid
        
        Parameters:
            - parent1 (Candidate): First parent to crossover
            - parent2 (Candidate): Second parent to crossover
            - crossoverRate (float): Ratio defines if these parents are crossover or not
        
        Return:
            Tuple of two child generate from the crossover process
        """

        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        grid1 = parent1.gene
        grid2 = parent2.gene

        gridSize = len(parent1.gene)
        r = random.random()
        if r < crossoverRate:
            for i in range(gridSize):
                # Randomly select sub-block from two parents to generate new child
                if random.random() < 0.5:
                    child1.gene[i] = npCopy(grid1[i])
                    child2.gene[i] = npCopy(grid2[i])
                else:
                    child1.gene[i] = npCopy(grid2[i])
                    child2.gene[i] = npCopy(grid1[i])
        else:
            child1.gene = npCopy(grid1)
            child2.gene = npCopy(grid2)

        return child1, child2

crossover = Crossover()