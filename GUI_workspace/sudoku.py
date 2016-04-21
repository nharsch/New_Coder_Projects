import argparse
from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

BOARDS = ['debug', 'n00b', 'l33t', 'error'] # Available sudoku boards
MARGIN = 20 # Pixels around the board
SIDE = 50 # Width of every board cell
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9 # Width and height of the whole board

class SudokuError(Exception):
    """
    An application specific error.
    """
    pass

class SudokuBoard(object):
    """
    Sudoku Board representation
    """
    def __init__(self, board_file):
        self.board = board_file

    # TODO: make this more concise
    def __create_board(self, board_file):
        # create an initial matrix, or a list of a list
        board = []

        # iterate over each line
        for line in board_file:
            line = line.strip()

            # line not 9 chars?
            if len(line) != 9:
                # reinit board if error
                board = []
                raise SudokuError(
                    "Each line in the sudoku puzzle must be 9 chars long."
                )

            # create a list for the line
            board.append([])

            # then iterate over each char
            for c in line:
                # Raise an error if the char is not an integer
                if not c.isdigit():
                    raise SudokuError(
                        "Valid chararcters for a sudoku puzzle must be in 0-9"
                    )
                # Add to the latest line in board 
                board[-1].append(int(c))

        # Raise an error if there are not 9 lines
        if len(board) != 9:
            raise SudokuError("Each sudoku puzzle must be 9 lines long")

        # Return the constructed board
        return board

class SudokuGame(object):
    """
    A sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    """
    def __init__(self, board_file):
        self.board_file = board_file
        self.start_puzzle = SudokuBoard(board_file).board

    def start(self):
        self.game_over = False
        # create a play state puzzle
        self.puzzle = []
        for i in xrange(9):
            self.puzzle.append([])
            for j in xrange(9):
                self.puzzle[i].append(self.start_puzzle[i][j])

    def check_win(self):
        for row in xrange(9):
            if not self.__check_row(row):
                return False
        for column in xrange(9):
            if not self.__check_column(column):
                return False
        for row in xrange(3):
            for column in xrange(3):
                if not self.__check_square(row, column):
                    return False
        self.game_over = True
        return True
    
    def __check_block(self, block):
        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])

    def __check_column(self, column):
            return self.__check_block(
                [self.puzzle[row][column] for row in xrange(9)]
            )

    def __check_square(self, row, column):
        return self.__check_block(
            # one hell of a list exp
            [
                self.puzzle[r][c]
                for r in xrange(row * 3, (row + 1) * 3)
                for c in xrange(column * 3, (column + 1) * 3)
            ]
        )
