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
        self.numOfPivots = len(matrix[0])
        for row in matrix:
            self.rows.append(Row(row))
            
    def solve(self):
        for piv in range(self.numOfPivots):
            p = piv+1
            pValue = self.rows[piv].getValue(piv);
            for row in self.rows[p:]:                       # Every value underneath the pivot.
                if row.getValue(piv) * pValue > 0:          # Same sign.
                    row.scale(-pValue / row.getValue(piv))  # Note that we reverse the sign here.
                else:
                    row.scale(pValue / row.getValue(piv))   # Note that we do NOT reverse the sign here.
                    
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
    
        