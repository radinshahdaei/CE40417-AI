import numpy as np


class Board:
    def __init__(self, n=6):
        self.__colors = ["black", "white"]
        self.__board_grid = np.full((n, n), -1)
        self.__n = n
        self.white_directions = [(-1, 0), (-1, 1), (-1, -1)]
        self.black_directions = [(1, 0), (1, 1), (1, -1)]
        self.black = 0
        self.white = 1
        self.__board_grid[:2, :] = self.black  # Set first two rows to 0 for black
        self.__board_grid[-2:, :] = self.white  # Set last two rows to 1 for white
        self.imaginary_board_grid = None

    def get_possible_directions(self, color):
        if color == self.black:
            return self.black_directions
        return self.white_directions

    def get_board_grid(self):
        """ Return the 2D list representing the board."""
        return np.copy(self.__board_grid)

    def get_n(self):
        """ Return the dimension of the board."""
        return self.__n

    def get_color(self, i, j):
        """ Given the coordinates (i, j) number,
            return the color of the piece placed there."""

        if self.__board_grid[i][j] not in [0, 1]:
            return None
        return self.__colors[self.__board_grid[i][j]]

    def is_move_valid(self, board, move, player_number):
        """ Given the player number and an origin and a destination position (i, j)
            return True if the position is a valid move for the color.
            return False otherwise."""
        origin, destination = move
        black_move = player_number == self.black

        is_inside = True if 0 <= origin[0] < self.__n and \
                            0 <= origin[1] < self.__n and \
                            0 <= destination[0] < self.__n and \
                            0 <= destination[1] < self.__n \
            else False

        if not is_inside:
            return False

        if black_move:
            integrity = True if board[origin[0]][origin[1]] == self.black and \
                                board[destination[0]][destination[1]] != self.black else False
        else:
            integrity = True if board[origin[0]][origin[1]] == self.white and \
                                board[destination[0]][destination[1]] != self.white else False

        if not integrity:
            return False

        if origin[1] == destination[1]:
            if board[destination[0]][destination[1]] == self.white or \
                    board[destination[0]][destination[1]] == self.black:
                return False

        return True

    def place_piece(self, move, player_number):
        """ Given the player number, place a piece with its color in position (i, j).
                Upon success, return the count of overturned pieces plus one. Return 0 otherwise."""
        origin, destination = move
        black_move = player_number == self.black

        if black_move:
            self.__board_grid[origin[0]][origin[1]] = -1
            self.__board_grid[destination[0]][destination[1]] = self.black
        else:
            self.__board_grid[origin[0]][origin[1]] = -1
            self.__board_grid[destination[0]][destination[1]] = self.white

        return self.is_game_over(self.__board_grid)

    def start_imagination(self):
        """ Prepare a copy of the board to test moves without a real impact."""
        self.imaginary_board_grid = np.copy(self.__board_grid)

    def get_imaginary_board(self):
        return self.imaginary_board_grid

    def place_piece_imaginary(self, move, player_number):
        """ Given the player number, place a piece with its color in position (i, j).
                Upon success, return the count of overturned pieces plus one. Return 0 otherwise."""
        origin, destination = move
        black_move = player_number == self.black

        if black_move:
            self.imaginary_board_grid[origin[0]][origin[1]] = -1
            self.imaginary_board_grid[destination[0]][destination[1]] = self.black
        else:
            self.imaginary_board_grid[origin[0]][origin[1]] = -1
            self.imaginary_board_grid[destination[0]][destination[1]] = self.white

        return self.get_scores(self.imaginary_board_grid), self.is_game_over(self.imaginary_board_grid)

    def get_scores(self, board):
        """ Return the scores of the game for both players."""
        scores = {0: 0, 1: 0}
        for row in range(self.__n):
            for col in range(self.__n):
                if board[row][col] == self.black:
                    scores[self.black] += 1 + (1.0 ** row) * row
                elif board[row][col] == self.white:
                    scores[self.white] += 1 + (1.0 ** (self.__n - row - 1)) * (self.__n - row - 1)
        scores[self.black] += self.winning_score(board, self.black)
        scores[self.white] += self.winning_score(board, self.white)
        return scores

    def winning_score(self, board, color):
        winning_value = 200
        if color == self.black:
            if self.is_game_over(board) == self.black:
                return winning_value
            elif self.is_game_over(board) == self.white:
                return -winning_value
            else:
                return 0

        if self.is_game_over(board) == self.white:
            return winning_value
        elif self.is_game_over(board) == self.black:
            return -winning_value
        else:
            return 0

    def is_game_over(self, board):
        for wp in board[self.__n - 1]:
            if wp == self.black:
                return self.black
        for bp in board[0]:
            if bp == self.white:
                return self.white

        counts = {self.white: 0, self.black: 0}
        for row in board:
            for cell in row:
                if cell == self.white:
                    counts[self.white] += 1
                elif cell == self.black:
                    counts[self.black] += 1
        if counts[self.white] == 0:
            return self.black
        elif counts[self.black] == 0:
            return self.white
        return -1

    def __str__(self):
        s = []
        for row in self.__board_grid:
            s.append(" ".join(map(str, row)))
        return "\n".join(s)
