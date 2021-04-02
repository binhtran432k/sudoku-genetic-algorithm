from numpy import zeros
import random
random.seed()
from .settings import DIGIT_NUMBER

class Candidate:
    """ A candidate solutions to the Sudoku puzzle. """
    def __init__(self):
        self.values = zeros((DIGIT_NUMBER, DIGIT_NUMBER), dtype=int)
        self.fitness = None
        return

    def update_fitness(self):
        """ The fitness of a candidate solution is determined by how close it is to being the actual solution to the puzzle. The actual solution (i.e. the 'fittest') is defined as a 9x9 grid of numbers in the range [1, 9] where each row, column and 3x3 block contains the numbers [1, 9] without any duplicates (see e.g. http://www.sudoku.com/); if there are any duplicates then the fitness will be lower. """
        
        row_count = zeros(DIGIT_NUMBER)
        column_count = zeros(DIGIT_NUMBER)
        block_count = zeros(DIGIT_NUMBER)
        row_sum = 0
        column_sum = 0
        block_sum = 0

        for i in range(0, DIGIT_NUMBER):  # For each row...
            for j in range(0, DIGIT_NUMBER):  # For each number within it...
                row_count[self.values[i][j]-1] += 1  # ...Update list with occurrence of a particular number.

            row_sum += (1.0/len(set(row_count)))/DIGIT_NUMBER
            row_count = zeros(DIGIT_NUMBER)

        for i in range(0, DIGIT_NUMBER):  # For each column...
            for j in range(0, DIGIT_NUMBER):  # For each number within it...
                column_count[self.values[j][i]-1] += 1  # ...Update list with occurrence of a particular number.

            column_sum += (1.0 / len(set(column_count)))/DIGIT_NUMBER
            column_count = zeros(DIGIT_NUMBER)


        # For each block...
        for i in range(0, DIGIT_NUMBER, 3):
            for j in range(0, DIGIT_NUMBER, 3):
                block_count[self.values[i][j]-1] += 1
                block_count[self.values[i][j+1]-1] += 1
                block_count[self.values[i][j+2]-1] += 1
                
                block_count[self.values[i+1][j]-1] += 1
                block_count[self.values[i+1][j+1]-1] += 1
                block_count[self.values[i+1][j+2]-1] += 1
                
                block_count[self.values[i+2][j]-1] += 1
                block_count[self.values[i+2][j+1]-1] += 1
                block_count[self.values[i+2][j+2]-1] += 1

                block_sum += (1.0/len(set(block_count)))/DIGIT_NUMBER
                block_count = zeros(DIGIT_NUMBER)

        # Calculate overall fitness.
        if (int(row_sum) == 1 and int(column_sum) == 1 and int(block_sum) == 1):
            fitness = 1.0
        else:
            fitness = row_sum * column_sum * block_sum
        
        self.fitness = fitness
        return
        
    def mutate(self, mutation_rate, given):
        """ Mutate a candidate by picking a row, and then picking two values within that row to swap. """

        r = random.uniform(0, 1.1)
        while(r > 1): # Outside [0, 1] boundary - choose another
            r = random.uniform(0, 1.1)
    
        success = False
        if (r < mutation_rate):  # Mutate.
            while(not success):
                row1 = random.randint(0, 8)
                row2 = random.randint(0, 8)
                row2 = row1
                
                from_column = random.randint(0, 8)
                to_column = random.randint(0, 8)
                while(from_column == to_column):
                    from_column = random.randint(0, 8)
                    to_column = random.randint(0, 8)   

                # Check if the two places are free...
                if(given.values[row1][from_column] == 0 and given.values[row1][to_column] == 0):
                    # ...and that we are not causing a duplicate in the rows' columns.
                    if(not given.is_column_duplicate(to_column, self.values[row1][from_column])
                       and not given.is_column_duplicate(from_column, self.values[row2][to_column])
                       and not given.is_block_duplicate(row2, to_column, self.values[row1][from_column])
                       and not given.is_block_duplicate(row1, from_column, self.values[row2][to_column])):
                    
                        # Swap values.
                        temp = self.values[row2][to_column]
                        self.values[row2][to_column] = self.values[row1][from_column]
                        self.values[row1][from_column] = temp
                        success = True
    
        return success
