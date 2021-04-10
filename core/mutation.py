import random
from .settings import DIGIT_NUMBER, MUTATION_CHOICE, MutationOption

class Mutation:
    def __init__(self):
        self.call = self.getChoice()

    def getChoice(self, option=MUTATION_CHOICE):
        if option == MutationOption.RANDOM:
            return self.randomMutate
        elif option == MutationOption.SWAP:
            return self.swapMutate
        elif option == MutationOption.MULTI_SWAP:
            return self.multiSwapMutate
        elif option == MutationOption.ALL_SWAP:
            return self.allSwapMutate
        elif option == MutationOption.RANDOM_RESET:
            return self.randomResetMutate

    def randomMutate(self, candidate, given):
        randomMethods = [self.swapMutate, self.randomResetMutate]
        randomWeights = [0.8, 0.2]
        method = random.choices(randomMethods, weights=randomWeights)[0]
        return method(candidate, given)

    def swapMutate(self, candidate, given):
        """  Mutate a candidate gene. Two numerals within a
        sub-block that are not given in the starting point are 
        selected randomly and their positions are swapped.
        
        Parameters:
            - candidate (Candidate): The candidate to mutate
            - given (array): Helper array that determines all fixed values in the statring Sudoku puzzle
        """
        randomBlock = random.randint(0, DIGIT_NUMBER - 1)
        possibleSwaps = []
        success = False

        # Get all unknown cells index
        for blockElementIndex in range(DIGIT_NUMBER):
            if given[randomBlock][blockElementIndex] == 0:
                possibleSwaps.append(blockElementIndex)

        # Select two indexes and swap their values
        if len(possibleSwaps) > 1:
            success = True
            random.shuffle(possibleSwaps)
            firstIndex, secondIndex = random.choices(possibleSwaps, k=2)
            tmp = candidate.gene[randomBlock][firstIndex]
            candidate.gene[randomBlock][firstIndex] = candidate.gene[randomBlock][secondIndex]
            candidate.gene[randomBlock][secondIndex] = tmp
        
        return success

    def multiSwapMutate(self, candidate, given):
        """  Mutate a candidate gene. Performs 1 to 5 swap mutations to the candidate gene
        
        Parameters:
            - candidate (Candidate): The candidate to mutate
            - given (array): Helper array that determines all fixed values in the statring Sudoku puzzle
        """
        self.weights = [0.625, 0.304, 0.066, 0.005, 0.0001]
        # Randomly select 1 to 5 swap actions to perform
        numSwap = random.choices(list(range(1, 6)), weights=self.weights, k=1)[0]
        success = False

        for _ in range(numSwap):
            randomBlock = random.randint(0, DIGIT_NUMBER - 1)
            possibleSwaps = []
            # Get all unknown cells index
            for blockElementIndex in range(DIGIT_NUMBER):
                if given[randomBlock][blockElementIndex] == 0:
                    possibleSwaps.append(blockElementIndex)

            # Select two indexes and swap their values
            if len(possibleSwaps) > 1:
                success = True
                random.shuffle(possibleSwaps)
                firstIndex, secondIndex = random.choices(possibleSwaps, k=2)
                tmp = candidate.gene[randomBlock][firstIndex]
                candidate.gene[randomBlock][firstIndex] = candidate.gene[randomBlock][secondIndex]
                candidate.gene[randomBlock][secondIndex] = tmp
        
        return success

    def allSwapMutate(self, candidate, given):
        """  Mutate a candidate gene. Performs swap mutations to each sub-block in 
        the gene with a rate of 16%.
        
        Parameters:
            - candidate (Candidate): The candidate to mutate
            - given (array): Helper array that determines all fixed values in the statring Sudoku puzzle
        """
        for block in range(DIGIT_NUMBER):
            if random.random() < 0.16:
                possibleSwaps = []
                for blockElementIndex in range(DIGIT_NUMBER):
                    if given[block][blockElementIndex] == 0:
                        possibleSwaps.append(blockElementIndex)
                if len(possibleSwaps) > 1:
                    random.shuffle(possibleSwaps)
                    firstIndex, secondIndex = random.choices(possibleSwaps, k=2)
                    tmp = candidate.gene[block][firstIndex]
                    candidate.gene[block][firstIndex] = candidate.gene[block][secondIndex]
                    candidate.gene[block][secondIndex] = tmp
        
        return True

    def randomResetMutate(self, candidate, given):
        """  Mutate a candidate gene. Selects a sub-block and sets randomly values to
        all cells contain unknown value in the statring Sudoku puzzle
        
        Parameters:
            - candidate (Candidate): The candidate to mutate
            - given (array): Helper array that determines all fixed values in the statring Sudoku puzzle
        """
        randomBlock = random.randint(0, DIGIT_NUMBER - 1)
        possibleValues = list(range(1, DIGIT_NUMBER + 1))
        for blockElementIndex in range(DIGIT_NUMBER):
            if given[randomBlock][blockElementIndex] != 0:
                possibleValues.remove(given[randomBlock][blockElementIndex])

        random.shuffle(possibleValues)
        for blockElementIndex in range(DIGIT_NUMBER):
            if given[randomBlock][blockElementIndex] == 0:
                candidate.gene[randomBlock][blockElementIndex] = possibleValues.pop()
        
        return True

mutation = Mutation()