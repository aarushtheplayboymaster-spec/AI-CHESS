import chess
import chess.svg
import random
class CHESSBOARD_GUI:
    def __init__(self):
        self.board = chess.Board()
        self.gameisruning = True
    def chessbord(self):
        svg_data = chess.svg.board(board=self.board, size=400)
        with open("starting_board.svg", "w") as f:
            f.write(svg_data)
    def is_game_over(self):
        if self.board.is_game_over(claim_draw=True):
            self.gameisruning = False
    def AI_controle(self):
        self.chessbord()
        while self.gameisruning:
            legal_moves = list(self.board.legal_moves)
            moves = random.choice(legal_moves)
            self.board.push(moves)
            self.is_game_over()
            self.chessbord()
if __name__ == "__main__":
    boarde = CHESSBOARD_GUI()
    boarde.AI_controle()