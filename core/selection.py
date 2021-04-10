import random
from .settings import SELECTION_CHOICE, SelectionOption

class Selection:
    def __init__(self):
        self.call = self.getChoice()

    def getChoice(self, option=SELECTION_CHOICE):
        if option == SelectionOption.RANKING:
            return self.rankingSelect
        elif option == SelectionOption.TOURNAMENT:
            return self.tournamentSelect
        elif option == SelectionOption.TOP:
            return self.topSelect

    def rankingSelect(self, candidates, number):
        """ Select a number of candidates from given candidates list.
        Fitness level is used to associate a probability of selection with each candidate.
        
        Parameters:
            - candidates (list): given candidates list to select
            - number (int): number of candidates to select
        """
        fitnessWeight = [c.fitness for c in candidates]
        selectedCandidates = random.choices(candidates, weights=fitnessWeight, k=number)

        return selectedCandidates

    def tournamentSelect(self, candidates, number, size=2, selectionRate=0.8):
        """ Select a number of candidates from given candidates list.
        Involves running several "tournaments" among a few individuals (or chromosomes) chosen at random from the population.
        
        Parameters:
            - candidates (list): given candidates list to select
            - number (int): number of candidates to select
        """
        self.size = size
        self.selectionRate = selectionRate
        def compete(competitors):
            competitors.sort(key=lambda x: -x.fitness)
            q = 1 - self.selectionRate
            cumRate = q

            r = random.random()
            for i in range(0, len(competitors) - 1):
                if r < 1 - cumRate:
                    return competitors[i]
                else:
                    cumRate = cumRate * q
            return competitors[-1]
        selectedCandidates = []
        for _ in range(0, number):
            competitors = random.choices(candidates, k=self.size)
            selectedCandidates.append(compete(competitors))

        return selectedCandidates

    def topSelect(self, candidates, number, selectionRate=0.2):
        """ Randomly select a number of candidates from top portion of given candidates list.
        
        Parameters:
            - candidates (list): given candidates list to select
            - number (int): number of candidates to select
        """
        self.selectionRate = selectionRate
        topIndex = int(self.selectionRate * len(candidates))

        return random.choices(candidates[:topIndex], k=number)

selection = Selection()