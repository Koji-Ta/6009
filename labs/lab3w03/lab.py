"""6.009 Lab 3 -- Six Double-Oh Mines"""

# NO IMPORTS ALLOWED!


class MinesGame:
    """
    Class to represent a game of Mines.
    """

    def __init__(self, num_rows, num_cols, bombs):
        """Start a new game.

        Initializes a new instance of `MinesGame` to have the following
        attributes:
           * `dimensions`
           * `state`
           * `board`
           * `mask`

        Each of these should be as described in the handout.

        Parameters:
           num_rows (int): Number of rows
           num_cols (int): Number of columns
           bombs (list/tuple): List of bombs, given in (row, column) pairs,
                               which can be either tuples or lists
        """
        self.dimensions = [num_rows, num_cols]
        self.state = "ongoing"
        self.mask = [[False] * num_cols for _ in range(num_rows)]
        # initial board
        self.board = [[0] * num_cols for _ in range(num_rows)]
        # set bombs
        for row, column in bombs:
            self.board[row][column] = '.'
        # compute number of adjacent bombs
        for r in range(num_rows):
            for c in range(num_cols):
                if self.board[r][c] != '.':
                    self.board[r][c] = self._adjacent_bombs(r, c)

    def _adjacent_bombs(self, row, column):
        """Compute number of adjacent bombs for the given cell"""
        return sum(self.board[r][c] == '.'
                   for r, c in self._get_zone(row, column))

    def _get_zone(self, row, column):
        """Return list of cell coordinate for square 3x3 with center in (row, column)"""
        rows, columns = self.dimensions
        return [(r, c) for r in range(self._strip(row-1, rows),
                                      self._strip(row+1, rows)+1)
                       for c in range(self._strip(column-1, columns),
                                      self._strip(column+1, columns)+1)]

    @staticmethod
    def _strip(val, val_max):
        """Bound value between 0 and val_max-1"""
        return min(val_max-1, max(0, val))

    def dump(self):
        """Print a human-readable representation of this game.

        >>> g = MinesGame(1, 2, [(0, 0)])
        >>> g.dump()
        dimensions: [1, 2]
        board: ['.', 1]
        mask:  [False, False]
        state: ongoing
        """
        lines = ["dimensions: {}".format(self.dimensions),
                 "board: {}".format("\n       ".join(map(str, self.board))),
                 "mask:  {}".format("\n       ".join(map(str, self.mask))),
                 "state: {}".format(self.state),
                 ]
        print("\n".join(lines))


    def dig(self, row, col):
        """Recursively dig up (row, col) and neighboring squares.

        Update self.mask to reveal (row, col); then recursively reveal (dig up)
        its neighbors, as long as (row, col) does not contain and is not adjacent
        to a bomb.  Return an integer indicating how many new squares were
        revealed.

        The state of the game should be changed to "defeat" when at least one bomb
        is visible on the board after digging, "victory" when all safe squares
        (squares that do not contain a bomb) and no bombs are visible, and
        "ongoing" otherwise.

        Parameters:
           row (int): Where to start digging (row)
           col (int): Where to start digging (col)

        Returns:
           int: the number of new squares revealed

        >>> game = MinesGame.from_dict({
        ...         "dimensions": [2, 4],
        ...         "board": [[".", 3, 1, 0],
        ...                   [".", ".", 1, 0]],
        ...         "mask": [[False, True, False, False],
        ...                  [False, False, False, False]],
        ...         "state": "ongoing"})
        >>> game.dig(0, 3)
        4
        >>> game.dump()
        dimensions: [2, 4]
        board: ['.', 3, 1, 0]
               ['.', '.', 1, 0]
        mask:  [False, True, True, True]
               [False, False, True, True]
        state: victory

        >>> game = MinesGame.from_dict({
        ...         "dimensions": [2, 4],
        ...         "board": [[".", 3, 1, 0],
        ...                   [".", ".", 1, 0]],
        ...         "mask": [[False, True, False, False],
        ...                  [False, False, False, False]],
        ...         "state": "ongoing"})
        >>> game.dig(0, 0)
        1
        >>> game.dump()
        dimensions: [2, 4]
        board: ['.', 3, 1, 0]
               ['.', '.', 1, 0]
        mask:  [True, True, False, False]
               [False, False, False, False]
        state: defeat
        """
        if self.state == "defeat" \
                or self.state == "victory" \
                or self.mask[row][col]:
            return 0

        if self.board[row][col] == '.':
            self.mask[row][col] = True
            self.state = "defeat"
            return 1

        result = self._open(row, col)
        if self._is_victory():
            self.state = 'victory'
        return result

    def _open(self, row, col):
        """Open cells and return number of them"""
        viewed = set()

        def rec_open(row, col):
            """Recursively open cells"""
            self.mask[row][col] = True
            viewed.add((row, col))
            if self.board[row][col] != 0:
                return 1
            return 1 + sum(rec_open(r, c)
                           for r, c in self._get_zone(row, col)
                           if (r, c) not in viewed)
        return rec_open(row, col)

    def _is_victory(self):
        """True if victory game"""
        close = sum(not visible for row in self.mask for visible in row)
        bombs = sum(cell == '.' for row in self.board for cell in row)
        return bombs == close

    def render(self, xray=False):
        """Prepare a game for display.

        Returns a two-dimensional array (list of lists) of "_" (hidden
        squares), "." (bombs), " " (empty squares), or "1", "2", etc. (squares
        neighboring bombs).  game.mask indicates which squares should be
        visible.  If xray is True (the default is False), the mask is ignored
        and all cells are shown.

        Parameters:
           xray (bool): Whether to reveal all tiles or just the ones allowed by
                        the mask

        Returns:
           A 2D array (list of lists) representing the rendered board

        >>> g = MinesGame.from_dict({
        ...         "dimensions": [2, 4],
        ...         "state": "ongoing",
        ...         "board": [[".", 3, 1, 0],
        ...                   [".", ".", 1, 0]],
        ...         "mask":  [[False, True, True, False],
        ...                   [False, False, True, False]]})
        >>> g.render(False)
        [['_', '3', '1', '_'], ['_', '_', '1', '_']]

        >>> g.render()
        [['_', '3', '1', '_'], ['_', '_', '1', '_']]

        >>> g.render(True)
        [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
        """
        rep = [[' ' if cell == 0 else str(cell) for cell in row]
                                                for row in self.board]
        if not xray:
            for r in range(self.dimensions[0]):
                for c in range(self.dimensions[1]):
                    if not self.mask[r][c]:
                        rep[r][c] = '_'
        return rep

    def render_ascii(self, xray=False):
        """Render a game as ASCII art.

        Returns a string-based representation of the game.  Each tile of
        the game board should be rendered as in the `render` method.

        Parameters:
           xray (bool): Whether to reveal all tiles or just the ones allowed by
                        the mask

        Returns:
           A string-based representation of game

        >>> g = MinesGame.from_dict({"dimensions": [2, 4],
        ...                     "state": "ongoing",
        ...                     "board": [[".", 3, 1, 0],
        ...                               [".", ".", 1, 0]],
        ...                     "mask":  [[True, True, True, False],
        ...                               [False, False, True, False]]})
        >>> print(g.render_ascii())
        .31_
        __1_
        """
        rep = self.render(xray)
        return '\n'.join(''.join(row) for row in rep)

    @classmethod
    def from_dict(cls, d):
        """
        Create an instance of `MinesGame` from a dictionary representation of
        the game.

        Parameters:
          d (dict): a dictionary with keys 'board', 'state', 'mask', and
                    'dimensions'.

        Returns:
          An instance of `MinesGame` with parameters as specified in the
          dictionary.

        Invariant:
          The four dictionary elements ('board', 'state', 'mask', and 'dimensions')
          are assumed to be sufficient and complete in establishing a current state
          of the game. This assumption is used in the test.py testing framework.
        """
        game = cls.__new__(cls)
        for i in ('dimensions', 'board', 'state', 'mask'):
            setattr(game, i, d[i])
        return game


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    doctest.testmod() #runs ALL doctests

    # Alternatively, can run the doctests JUST for specified
    # function/methods, e.g., for MinesGame.rendor or any other
    # function you might want.  This may be useful as you write/debug
    # individual doctests or functions.  Also, the verbose flag can be
    # set to True to see all test results, including those that pass.
    #
    #doctest.run_docstring_examples(MinesGame.render, globals(), verbose=False)
