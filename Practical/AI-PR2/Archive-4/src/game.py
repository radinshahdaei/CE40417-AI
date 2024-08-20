import time

from board import Board
import visualizer


class Game:
    def __init__(self, first_player_class, second_player_class):
        self.first_player_class = first_player_class
        self.second_player_class = second_player_class

    def play(self, visualize=False, first_player_depth=None, second_player_depth=None):
        board = Board()
        black = self.first_player_class(board.black, board)
        white = self.second_player_class(board.white, board)
        if first_player_depth is not None:
            black = self.first_player_class(board.black, board, depth=first_player_depth)
        if second_player_depth is not None:
            white = self.second_player_class(board.white, board, depth=second_player_depth)

        sleep_time_when_game_ends = 0
        if visualize:
            visualizer.visualize_init(board)
        while True:
            black_move = black.get_next_move()
            if black_move:
                done = board.place_piece(black_move, board.black)
                if visualize:
                    visualizer.visualize(board)
                if done >= 0:
                    scores = board.get_scores(board.get_board_grid())
                    if visualize:
                        time.sleep(sleep_time_when_game_ends)
                        visualizer.end_visualization()
                    return scores

            white_move = white.get_next_move()
            if white_move:
                done = board.place_piece(white_move, board.white)
                if visualize:
                    visualizer.visualize(board)
                if done >= 0:
                    scores = board.get_scores(board.get_board_grid())
                    if visualize:
                        time.sleep(sleep_time_when_game_ends)
                        visualizer.end_visualization()
                    return scores

    def bulk_play(self, n, first_player_depth=None, second_player_depth=None):
        results = {'black': 0, 'white': 0}
        for _ in range(n):
            result = self.get_winner(self.play(False, first_player_depth, second_player_depth))
            results[result] += 1
        return results

    def get_winner(self, scores):
        if scores[0] > scores[1]:
            return 'black'
        if scores[0] < scores[1]:
            return 'white'

