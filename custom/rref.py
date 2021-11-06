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
        self.rows = []
        self.numOfPivots = len(matrix[0]) - 1
        for row in matrix:
            self.rows.append(Row(row))
            
    def solve(self):
        self.rearrange()
        self.display()
        
                            
    def display(self):
        print('------')
        for row in self.rows:
            print(row.getRow())
        print('------')
        
    def rearrange(self):
        self.rows.sort(key=lambda x: x.numOfZeros(), reverse=False)

                    
class Row:
    """
    Makes doing elementary row operations easier.
    """
    
    def __init__(self, r):
        self.columns = r
        
    def combine(self, other):
        return [i + j for i, j in zip(self.columns, other.columns)]
    
    def scale(self, scalar):
        self.columns = [i * scalar for i in self.columns]
        
    def getValue(self, index):
        return self.columns[index]
    
    def getRow(self):
        return self.columns
    
    def numOfZeros(self):
        return self.columns.count(0)
        