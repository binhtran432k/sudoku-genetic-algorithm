from numpy import copy, zeros
import random
random.seed()
from .candidate import Candidate
from .settings import DIGIT_NUMBER

class CycleCrossover:
    """ Crossover relates to the analogy of genes within each parent candidate mixing together
    in the hopes of creating a fitter child candidate. Cycle crossover is used here (see e.g. A.
    E. Eiben, J. E. Smith. Introduction to Evolutionary Computing. Springer, 2007). """

    def __init__(self):
        return
    
    def crossover(self, parent1, parent2, crossoverRate):
        """ Create two new child candidates by crossing over parent genes. """
        child1 = Candidate()
        child2 = Candidate()
        
        # Make a copy of the parent genes.
        child1.values = copy(parent1.values)
        child2.values = copy(parent2.values)

        r = random.uniform(0, 1.1)
        while(r > 1):  # Outside [0, 1] boundary. Choose another.
            r = random.uniform(0, 1.1)
            
        # Perform crossover.
        if (r < crossoverRate):
            # Pick a crossover point. Crossover must have at least 1 row (and at most Nd-1) rows.
            crossoverPoint1 = random.randint(0, 8)
            crossoverPoint2 = random.randint(1, 9)
            while(crossoverPoint1 == crossoverPoint2):
                crossoverPoint1 = random.randint(0, 8)
                crossoverPoint2 = random.randint(1, 9)
                
            if(crossoverPoint1 > crossoverPoint2):
                temp = crossoverPoint1
                crossoverPoint1 = crossoverPoint2
                crossoverPoint2 = temp
                
            for i in range(crossoverPoint1, crossoverPoint2):
                child1.values[i], child2.values[i] = self.crossoverRows(child1.values[i], child2.values[i])

        return child1, child2

    def crossoverRows(self, Child1Row, Child2Row): 
        newChild1Row = zeros(DIGIT_NUMBER)
        newChild2Row = zeros(DIGIT_NUMBER)

        remaining = list(range(1, DIGIT_NUMBER+1))
        cycle = 0
        
        while((0 in newChild1Row) and (0 in newChild2Row)):  # While child rows not complete...
            if(cycle % 2 == 0):  # Even cycles.
                # Assign next unused value.
                index = self.findUnuesd(Child1Row, remaining)
                start = Child1Row[index]
                remaining.remove(Child1Row[index])
                newChild1Row[index] = Child1Row[index]
                newChild2Row[index] = Child2Row[index]
                next = Child2Row[index]
                
                while(next != start):  # While cycle not done...
                    index = self.findValue(Child1Row, next)
                    newChild1Row[index] = Child1Row[index]
                    remaining.remove(Child1Row[index])
                    newChild2Row[index] = Child2Row[index]
                    next = Child2Row[index]

                cycle += 1

            else:  # Odd cycle - flip values.
                index = self.findUnuesd(Child1Row, remaining)
                start = Child1Row[index]
                remaining.remove(Child1Row[index])
                newChild1Row[index] = Child2Row[index]
                newChild2Row[index] = Child1Row[index]
                next = Child2Row[index]
                
                while(next != start):  # While cycle not done...
                    index = self.findValue(Child1Row, next)
                    newChild1Row[index] = Child2Row[index]
                    remaining.remove(Child1Row[index])
                    newChild2Row[index] = Child1Row[index]
                    next = Child2Row[index]
                    
                cycle += 1
            
        return newChild1Row, newChild2Row  
           
    def findUnuesd(self, parentRow, remaining):
        for i in range(0, len(parentRow)):
            if(parentRow[i] in remaining):
                return i

    def findValue(self, parentRow, value):
        for i in range(0, len(parentRow)):
            if(parentRow[i] == value):
                return i
