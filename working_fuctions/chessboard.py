import chess
import torch
import numpy as np
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
    def simulate_move(self,move):
        fack_board = self.board.copy()
        fack_board.push(move)

        fack_wapper = chessmoves()
        fack_wapper.board = fack_board
        return fack_wapper
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
        board3d = np.zeros((19,8,8), dtype=np.int8)
        for piece_type in chess.PIECE_TYPES:
            for square in self.board.pieces(piece_type, chess.WHITE):
                idx = np.unravel_index(square, (8, 8))
                board3d[piece_type - 1][7 - idx[0]][idx[1]] = 1
            for square in self.board.pieces(piece_type, chess.BLACK):
                idx = np.unravel_index(square, (8, 8))
                board3d[piece_type + 5][7 - idx[0]][idx[1]] = 1
        if self.board.turn == chess.WHITE:
            board3d[12, :, :] = 1
        else:
            board3d[13, :, :] = 1
        
        return torch.tensor(board3d, dtype=torch.float32)
if __name__ == "__main__":
    test_board = chessmoves()
    print("Board initialized successfully!")