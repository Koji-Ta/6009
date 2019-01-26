def format_sudoku(board):
    """
    Format a sudoku board to be printed to the screen
    """
    def _row_divider(board):
        out = '+'
        for i in range(9):
            out += '-'
            if i % 3 == 2:
                out += '+'
        return out
    out = ''
    for i in range(9):
        if i % 3 == 0:
            out += _row_divider(board) + '\n'
        out += '|'
        for j in range(9):
            out += ' ' if board[i][j] == 0 else str(board[i][j])
            if j % 3 == 2:
                out += '|'
        out += '\n'
    out += _row_divider(board)
    return out


def values_in_row(board, r):
    """
    Return a list containing all of the values in a given row.
    """
    return board[r]


def values_in_column(board, c):
    """
    Return a list containing all of the values in a given column.
    """
    return [board[r][c] for r in range(len(board))]


def values_in_subgrid(board, sr, sc):
    """
    Return a list containing all of the values in a given subgrid.
    """
    return [board[r][c]
            for r in range(sr*3, (sr+1)*3)
            for c in range(sc*3, (sc+1)*3)]


def solve_sudoku(board):
    """
    Given a sudoku board (as a list-of-lists of numbers, where 0 represents an
    empty square), return a solved version of the puzzle.
    """
    pass


grid1 = [[5,1,7,6,0,0,0,3,4],
         [2,8,9,0,0,4,0,0,0],
         [3,4,6,2,0,5,0,9,0],
         [6,0,2,0,0,0,0,1,0],
         [0,3,8,0,0,6,0,4,7],
         [0,0,0,0,0,0,0,0,0],
         [0,9,0,0,0,0,0,7,8],
         [7,0,3,4,0,0,5,6,0],
         [0,0,0,0,0,0,0,0,0]]
grid2 = [[5,1,7,6,0,0,0,3,4],
         [0,8,9,0,0,4,0,0,0],
         [3,0,6,2,0,5,0,9,0],
         [6,0,0,0,0,0,0,1,0],
         [0,3,0,0,0,6,0,4,7],
         [0,0,0,0,0,0,0,0,0],
         [0,9,0,0,0,0,0,7,8],
         [7,0,3,4,0,0,5,6,0],
         [0,0,0,0,0,0,0,0,0]]
grid3 = [[0,0,1,0,0,9,0,0,3],  # http://www.extremesudoku.info/sudoku.html
         [0,8,0,0,2,0,0,9,0],
         [9,0,0,1,0,0,8,0,0],
         [1,0,0,5,0,0,4,0,0],
         [0,7,0,0,3,0,0,5,0],
         [0,0,6,0,0,4,0,0,7],
         [0,0,8,0,0,5,0,0,6],
         [0,3,0,0,7,0,0,4,0],
         [2,0,0,3,0,0,9,0,0]]

for grid in [grid1, grid2, grid3]:
    print(format_sudoku(grid))
    print()
