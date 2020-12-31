import numpy as np

class EditDistance:
    # Constructor
    def __init__(self, ins_cost = 1, del_cost = 1, rep_cost = 2):
        # init edit costs
        self.ins_cost = ins_cost
        self.del_cost = del_cost
        self.rep_cost = rep_cost

    # Returns a matrix of len(source)+1 by len(target)+1 containing minimum edit distances, and the minimum edit distance (med) required to convert the source string to the target
    def get_min_edit_distance(self, source, target):
        # get cost matrix dimenstions
        m = len(source) 
        n = len(target)

        #initialize cost matrix with zeros and dimensions (m+1,n+1)
        D = np.zeros((m+1, n+1), dtype=int) 
    
        # Fill in column 0, from row 1 to row m, both inclusive
        for row in range(1, m + 1):
            D[row, 0] = D[row - 1, 0] + self.del_cost

        # Fill in row 0, for all columns from 1 to n, both inclusive
        for col in range(1, n + 1):
            D[0,col] = D[0, col - 1] + self.ins_cost
            
        # Loop through row 1 to row m, both inclusive
        for row in range(1, m + 1): 
            
            # Loop through column 1 to column n, both inclusive
            for col in range(1, n + 1):
                
                # Intialize replace cost
                r_cost = self.rep_cost
                
                # Check to see if source character at the previous row matches the target character at the previous column
                if source[row - 1] == target[col - 1]:
                    # Update the replacement cost to 0 if source and target are the same
                    r_cost = 0
                    
                # Update the cost at row, col based on previous entries in the cost matrix
                D[row,col] = min([D[row - 1, col - 1] + r_cost, D[row - 1, col] + self.del_cost, D[row, col - 1] + self.ins_cost])
            
        # Set the minimum edit distance with the cost found at row m, column n
        med = D[m, n]
        
        return D, med