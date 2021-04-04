from numpy import zeros

from .candidate import Candidate
from .settings import BLOCK_NUMBER, DIGIT_NUMBER

class Given:
    """ The grid containing the given/known values. """

    def __init__(self):
        self.values = None
        self.helper = None
        self.bestCandidate = None
        self.zeroCandidate = Candidate()
        self.zeroCandidate.values = zeros((DIGIT_NUMBER, DIGIT_NUMBER), dtype=int)
        self.zeroCandidate.fitness = 0.0
        return
        
    def isRowDuplicate(self, row, value):
        """ Check whether there is a duplicate of a fixed/given value in a row. """
        for column in range(0, DIGIT_NUMBER):
            if(self.values[row][column] == value):
                return True
        return False

    def isColumnDuplicate(self, column, value):
        """ Check whether there is a duplicate of a fixed/given value in a column. """
        for row in range(0, DIGIT_NUMBER):
            if(self.values[row][column] == value):
                return True
        return False

    def isBlockDuplicate(self, row, column, value):
        """ Check whether there is a duplicate of a fixed/given value in a 3 x 3 block. """
        beginRow = int(row/3)*3
        beginCol = int(column/3)*3
        for i in range(BLOCK_NUMBER):
            for j in range(BLOCK_NUMBER):
                if self.values[beginRow+i][beginCol+j] == value:
                    return True
        return False

    def loadHelper(self):
        """ Determine the legal values that each square can take. """
        self.helper = Candidate()
        self.helper.values = [[[] for j in range(0, DIGIT_NUMBER)] for i in range(0, DIGIT_NUMBER)]
        for row in range(0, DIGIT_NUMBER):
            for column in range(0, DIGIT_NUMBER):
                for value in range(1, DIGIT_NUMBER + 1):
                    if((self.values[row][column] == 0) and
                            not (self.isColumnDuplicate(column, value) or
                            self.isBlockDuplicate(row, column, value) or
                            self.isRowDuplicate(row, value))):
                        # Value is available.
                        self.helper.values[row][column].append(value)
                    elif(self.values[row][column] != 0):
                        # Given/known value from file.
                        self.helper.values[row][column].append(self.values[row][column])
                        break

    def resetBestCandidate(self):
        self.bestCandidate = self.zeroCandidate

    def loadValues(self, values):
        self.values = values
        self.resetBestCandidate()

    def updateDuplicateValues(self):
        self.duplicateValues = zeros((DIGIT_NUMBER, DIGIT_NUMBER), dtype=int)
        testValues = self.bestCandidate.values
        for i in range(DIGIT_NUMBER):
            testRowDuplicate = zeros(DIGIT_NUMBER)
            for j in range(DIGIT_NUMBER):
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

given = Given()