from core.helper import decodePuzzle, encodePuzzle
from numpy import zeros

from .candidate import Candidate
from .settings import DIGIT_NUMBER

class Given:
    """ The grid containing the given/known values. """

    def __init__(self):
        self.helper = None
        self.bestCandidate = None
        self.zeroCandidate = Candidate()
        self.zeroCandidate.gene = zeros((DIGIT_NUMBER, DIGIT_NUMBER), dtype=int)
        self.zeroCandidate.fitness = 0.0
        self.values = self.zeroCandidate.gene

    def resetBestCandidate(self, reuse=False):
        if reuse:
            self.bestCandidate = Candidate()
            self.bestCandidate.gene = encodePuzzle(self.values)
        else:
            self.bestCandidate = self.zeroCandidate

    def loadValues(self, values):
        self.values = values
        self.resetBestCandidate(True)

    def updateDuplicateValues(self):
        self.duplicateValues = zeros((DIGIT_NUMBER, DIGIT_NUMBER), dtype=int)
        testValues = decodePuzzle(self.bestCandidate.gene)
        for i in range(DIGIT_NUMBER):
            testRowDuplicate = zeros(DIGIT_NUMBER)
            for j in range(DIGIT_NUMBER):
                if testValues[i][j] == 0:
                    continue
                if testRowDuplicate[testValues[i][j]-1] == 1:
                    for k in range(j):
                        if testValues[i][k] == testValues[i][j]:
                            self.duplicateValues[i][k] += 1
                            break
                if testRowDuplicate[testValues[i][j]-1] >= 1:
                    self.duplicateValues[i][j] += 1
                testRowDuplicate[testValues[i][j]-1] += 1
        for i in range(DIGIT_NUMBER):
            testColumnDuplicate = zeros(DIGIT_NUMBER)
            for j in range(DIGIT_NUMBER):
                if testValues[j][i] == 0:
                    continue
                if testColumnDuplicate[testValues[j][i]-1] == 1:
                    for k in range(j):
                        if testValues[k][i] == testValues[j][i]:
                            self.duplicateValues[k][i] += 1
                            break
                if testColumnDuplicate[testValues[j][i]-1] >= 1:
                    self.duplicateValues[j][i] += 1
                testColumnDuplicate[testValues[j][i]-1] += 1
        for i in range(DIGIT_NUMBER):
            ii = int(i/3)*3
            jj = int(i%3)*3
            testBlockDuplicate = zeros(DIGIT_NUMBER)
            for j in range(DIGIT_NUMBER):
                iii = ii + int(j/3)
                jjj = jj + int(j%3)
                if testValues[iii][jjj] == 0:
                    continue
                if testBlockDuplicate[testValues[iii][jjj]-1] == 1:
                    for k in range(j):
                        kki = ii + int(k/3)
                        kkj = jj + int(k%3)
                        if testValues[kki][kkj] == testValues[iii][jjj]:
                            self.duplicateValues[kki][kkj] += 1
                            break
                if testBlockDuplicate[testValues[iii][jjj]-1] >= 1:
                    self.duplicateValues[iii][jjj] += 1
                testBlockDuplicate[testValues[iii][jjj]-1] += 1
        # Return False if the puzzle hasn't been solve
        for i in range(DIGIT_NUMBER):
            for j in range(DIGIT_NUMBER):
                if self.duplicateValues[i][j] != 0:
                    return False

        return True

given = Given()