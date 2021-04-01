from sudoku import Candidate

class Given(Candidate):
    """ The grid containing the given/known values. """

    def __init__(self, values, Nd):
        self.values = values
        self.Nd = Nd
        return
        
    def is_row_duplicate(self, row, value):
        """ Check whether there is a duplicate of a fixed/given value in a row. """
        for column in range(0, self.Nd):
            if(self.values[row][column] == value):
                return True
        return False

    def is_column_duplicate(self, column, value):
        """ Check whether there is a duplicate of a fixed/given value in a column. """
        for row in range(0, self.Nd):
            if(self.values[row][column] == value):
                return True
        return False

    def is_block_duplicate(self, row, column, value):
        """ Check whether there is a duplicate of a fixed/given value in a 3 x 3 block. """
        i = 3*(int(row/3))
        j = 3*(int(column/3))

        if((self.values[i][j] == value)
           or (self.values[i][j+1] == value)
           or (self.values[i][j+2] == value)
           or (self.values[i+1][j] == value)
           or (self.values[i+1][j+1] == value)
           or (self.values[i+1][j+2] == value)
           or (self.values[i+2][j] == value)
           or (self.values[i+2][j+1] == value)
           or (self.values[i+2][j+2] == value)):
            return True
        else:
            return False
