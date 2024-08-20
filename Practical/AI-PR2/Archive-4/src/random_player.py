from player import Player
import random


class RandomPlayer(Player):
    def get_next_move(self):
        moves = []
        range_n = 0, self.board.get_n()
        step = 1
        if self.player_number == 0:
            range_n = self.board.get_n() - 1, -1
            step = -1
        for i in range(range_n[0], range_n[1], step):
            for j in range(range_n[0], range_n[1], step):
                if self.board.get_board_grid()[i][j] == self.player_number:
                    for direction in self.board.get_possible_directions(self.player_number):
                        move = (i, j), (i + direction[0], j + direction[1])
                        self.board.start_imagination()
                        if self.board.is_move_valid(self.board.get_imaginary_board(), move, self.player_number):
                            moves.append(move)
        return random.choice(moves)
