import chess
class chessmoves:
    def __init__(self):
        self.board = chess.Board()
    def chess_legal_moves(self,input):
        move = chess.Move.from_uci(input)
        if move in self.board.legal_moves:
            self.board.push(move)
            return move
        return None
    def simulate_move(self):
        pass
    def is_terminal(self):
        is_terminal = self.board.is_game_over()
        return is_terminal
    def winning(self):
        is_game_over = self.is_terminal()
        if is_game_over == True:
            outcome = self.board.outcome()
            if outcome.winner == chess.WHITE:
                return 1
            elif outcome.winner == chess.BLACK:
                return -1
            else:
                return 0
    def to_tensor(self):
        pass
if __name__ == "__main__":
    test_board = chessmoves()
    print("Board initialized successfully!")