import numpy as np

from grid_filler.display.big_letters import BigLetters

class BigPrint:
    MIDDLE = '╠╬╣'
    TOP = '╔╦╗'
    BOTTOM = '╚╩╝'
    HORIZONTAL = '═'
    VERTICAL = '║'

    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.letter_height, self.letter_width = self.get_letter('A').shape
        self.rows, self.columns = grid.shape

        self.horizontal = self.HORIZONTAL * self.letter_width

    def get_letter(self, char: str) -> np.ndarray:
        """
        Small helper method to get a letter, with default
        return of blocker

        Implemented because BigLetters are too big, so
        a column either side is taken off
        """
        return getattr(BigLetters, char, BigLetters.SOLID)[:, 1:-1]

    def horizontal_bar(self, connectors: str) -> str:
        """
        Create a horizontal bar, either top middle or bottom
        """
        left, middle, right = connectors
        return left + middle.join([self.horizontal] * self.columns) + right

    def process_row(self, row: np.ndarray) -> str:
        """
        Convert a row of small letters to a row of big letters.

        Parameters
        ----------
        row: np.ndarray
            An array of characters/blocked cells

        Returns
        -------
        big_row: str
            A newline delimited string of big ascii text
            and grid lines
        """
        row = np.hstack([self.get_letter(char) for char in row])
        # Put the horizontal lines in
        indices = np.arange(0,
                            self.columns * self.letter_width + 1,
                            self.letter_width)
        row = np.insert(row, indices, self.VERTICAL, axis=1)
        return '\n'.join([''.join(line) for line in row])

    def print_grid(self):
        print(self.horizontal_bar(self.TOP))
        for row in self.grid[:-1]:
            print(self.process_row(row))
            print(self.horizontal_bar(self.MIDDLE))
        print(self.process_row(self.grid[-1]))
        print(self.horizontal_bar(self.BOTTOM))
            
        
        



grid = ('TENET'
        'O#U#A'
        'ADDLE'
        'S#G#L'
        'TREWS')

grid = np.array(list(grid)).reshape(5, 5)

x = BigPrint(grid)
x.print_grid()
