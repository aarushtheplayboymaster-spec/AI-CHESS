import chess
import chess.svg

# 1. Setup the board and play a few moves
board = chess.Board()
board.push_san("e4")  # White moves pawn to e4
board.push_san("e5")  # Black responds with e5
board.push_san("Nf3") # White brings out the Knight

# 2. Render the board to SVG code
# 'size' sets the width/height in pixels
svg_output = chess.svg.board(board, size=400)

# 3. Save the SVG data to a file
with open("chessboard.svg", "w") as f:
    f.write(svg_output)
