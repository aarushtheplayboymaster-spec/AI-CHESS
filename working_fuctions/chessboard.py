import chess
class chessmoves:
    def __init__(self):
        self.board = chess.Board()
    def chess_legal_moves(self,input):
        move = chess.Move.from_uci(input)
        if move in self.board.legal_moves:
            self.board.push(move)
            self.board.move_stack
            return move
        return None
    def temp_san_board(self):
        temp_board = chess.Board()
        san_moves = []
        for move in self.board.move_stack:
            san_moves.append(temp_board.san(move))
            temp_board.push(move)
        return san_moves
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