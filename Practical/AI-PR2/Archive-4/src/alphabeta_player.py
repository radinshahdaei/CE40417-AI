from player import Player


class AlphaBetaPlayer(Player):
    def __init__(self, player_number, board, depth=3):
        super().__init__(player_number, board)
        self.depth = depth

    def get_next_move(self):
        return self.alphabeta(
            self.board.get_board_grid(), self.depth, -float("inf"), float("inf"), True
        )[1]

    def alphabeta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_game_over(board) != -1:
            # Return heuristic value if depth is 0 or game is over
            scores = self.board.get_scores(board)
            return scores[self.player_number] - scores[self.opponent_number], None

        if maximizing_player:
            max_value = -float("inf")
            best_move = None
            for move in self.generate_moves(board, self.player_number):
                new_board = self.apply_move(board, move, self.player_number)
                value, _ = self.alphabeta(new_board, depth - 1, alpha, beta, False)
                if value > max_value:
                    max_value = value
                    best_move = move
                alpha = max(alpha, max_value)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_value, best_move
        else:
            min_value = float("inf")
            best_move = None
            for move in self.generate_moves(board, self.opponent_number):
                new_board = self.apply_move(board, move, self.opponent_number)
                value, _ = self.alphabeta(new_board, depth - 1, alpha, beta, True)
                if value < min_value:
                    min_value = value
                    best_move = move
                beta = min(beta, min_value)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_value, best_move

    def generate_moves(self, board, player_number):
        moves = []
        for i in range(self.board.get_n()):
            for j in range(self.board.get_n()):
                if board[i][j] == player_number:
                    for direction in self.board.get_possible_directions(player_number):
                        move = (i, j), (i + direction[0], j + direction[1])
                        if self.board.is_move_valid(board, move, player_number):
                            moves.append(move)
        return moves

    def apply_move(self, board, move, player_number):
        new_board = [row.copy() for row in board]
        origin, destination = move
        new_board[origin[0]][origin[1]] = -1
        new_board[destination[0]][destination[1]] = player_number
        return new_board
