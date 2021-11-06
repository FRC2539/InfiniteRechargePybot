import math

class Matrix:
    """
    Well I was hoping it wouldn't come to this 
    but it seems as though the internet is full
    of idiots who don't know how to make a functional
    RREF calculator. Hopefully I'm different. I 
    am going to make this super simple and really
    low level. Just to get the job done.
    """
    
    def __init__(self, matrix):
        self.m = []
        self.pivots = len(matrix[0]) - 1           # Because of augmentation
        self.rows = len(matrix)
        for row in matrix:
            self.m.append(Row(row))
            
    def solve(self):
        self.rearrange()
        self.display()

        if self.rows < self.pivots:
            self.pivots = self.rows

        for pivotSelector in range(self.pivots):
            selectedRow = self.m[pivotSelector]
            print('d ' + str(selectedRow))
            a = selectedRow.getValue(pivotSelector)
            for i in range(pivotSelector+1, self.rows):         # This line might break it.
                rowBelow = self.m[i]
                b = rowBelow.getValue(pivotSelector)
                conversion = (b / a) * -1
                try:
                    invConversion = (1 / conversion)
                except ZeroDivisionError:
                    continue
                selectedRow.scale(conversion)
                result = rowBelow.combine(selectedRow)
                self.m[i] = result
                selectedRow.scale(invConversion)

        for pivotSelector in range(self.pivots):
            selectedRow = self.m[pivotSelector]
            a = selectedRow.getValue(pivotSelector)
            for i in range(pivotSelector):         # This line might break it.
                rowAbove = self.m[i]
                b = rowAbove.getValue(pivotSelector)
                conversion = (b / a) * -1
                try:
                    invConversion = (1 / conversion)
                except(ZeroDivisionError):
                    continue
                selectedRow.scale(conversion)
                result = rowAbove.combine(selectedRow)
                self.m[i] = result
                selectedRow.scale(invConversion)

        for i in range(len(self.m)):
            if not self.m[i].isEmpty():
                selectedRow = self.m[i]
                pivot = selectedRow.getValue(i)
                selectedRow.scale(1 / pivot)

        self.display()
                            
    def display(self):
        print('------')
        for row in self.m:
            print(row.getRow())
        print('------')
        
    def rearrange(self):
        self.m.sort(key=lambda x: x.numOfZeros(), reverse=False)

                    
class Row:
    """
    Makes doing elementary row operations easier.
    """
    
    def __init__(self, r):
        self.columns = r
        
    def combine(self, other):
        return Row([i + j for i, j in zip(self.columns, other.columns)])
    
    def scale(self, scalar):
        self.columns = [i * scalar for i in self.columns]
        
    def getValue(self, index):
        return self.columns[index]
    
    def getRow(self):
        return self.columns
    
    def isEmpty(self):
        return self.numOfZeros() == len(self.columns)

    def numOfZeros(self):
        return self.columns.count(0)
        