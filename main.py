import numpy as np
COSTS = {'insert': 1,
         'delete': 1,
         'substitute': 2}

ARROW = ['-', '|', '\\']
class EditDistanceCalculator:
    def __init__(self, src_str, dst_str):
        self.src = src_str
        self.dst = dst_str
        self.table_shape = (len(src_str)+1,len(dst_str)+1,2)
        self.dp = np.zeros(shape=self.table_shape, dtype=np.int8)
        self.diag_length = min(self.table_shape[:2])
    
    def fill_table(self):
        for i in range(self.diag_length):
            self.compute_row(i)
            self.compute_col(i)

    def compute_cell(self, row, col):
        candidates = []
        if row != 0: candidates.append((self.dp[row-1,col,0] + COSTS['delete'], 1))
        if col != 0: candidates.append((self.dp[row,col-1,0] + COSTS['insert'], 0))
        if len(candidates) == 2: 
            sub_cost = 0 if src_str[row-1]==dst_str[col-1] else COSTS['substitute'] 
            candidates.append((self.dp[row-1,col-1,0] + sub_cost, 2))
        
        candidates = np.asarray(candidates)

        if len(candidates)==0:
            self.dp[row,col] = 0
        else:  
            self.dp[row,col] = candidates[np.argmin(candidates[:,0])]

    def compute_row(self, row_index):
        for col in range(self.table_shape[1]):
            self.compute_cell(row_index,col)

    def compute_col(self, col_index):
        for row in range(self.table_shape[0]):
            self.compute_cell(row,col_index)

    def print_table(self):
        print('-----------------------')
        table = np.reshape(self.dp, (self.table_shape))
        for row in table:
            for cell in row:
                print("{:3d}({})".format(cell[0],ARROW[cell[1]]), end=" ")
            print()
        print('-----------------------')
        print("Min Edit Distance is {}".format(table[-1,-1,0]))

    def get_optimal_path(self):
        row = self.dp.shape[0] - 1
        col = self.dp.shape[1] - 1
        edits = []
        while col > 0 or row > 0:
            current_edit = self.dp[row,col,1]
            if current_edit == 0:
                edits.append(" insert '{}' ".format(self.dst[col-1]))
                col -= 1
            if current_edit == 1:
                edits.append(" delete '{}' ".format(self.src[row-1]))
                row -= 1
            if current_edit == 2:
                if self.src[row-1] != self.dst[col-1]:
                    edits.append(" substitute '{}' with '{}'".format(
                        self.src[row-1],self.dst[col-1]))
                row -= 1
                col -= 1
        return edits[::-1]

if __name__=="__main__":
    src_str = "mohammad amin"
    dst_str = "parchami araghi"

    calculator = EditDistanceCalculator(src_str, dst_str)
    calculator.fill_table()
    calculator.print_table()
    edits = calculator.get_optimal_path()
    print(*edits, sep='\n')