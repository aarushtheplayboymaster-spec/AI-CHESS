import torch
from torch.utils.data import Dataset
import chess.pgn
import numpy as np
import random

class CHESS_DATASET_LODEAR(Dataset):
    def __init__(self,png_path):
        self.png_path = png_path
        self.game_offset = []
        with open(self.png_path,"r") as f:
            while True:
                offset = f.tell()
                game = chess.pgn.read_game(f)
                if game is None:
                    break
                
                # FIX: Check if the game actually has moves before saving its offset!
                # This guarantees zero empty games ever enter our training pipeline.
                try:
                    moves_list = list(game.mainline_moves())
                    if len(moves_list) > 0:
                        self.game_offset.append(offset)
                        count += 1
                        if count % 1000 == 0:
                            print(f"Indexed {count} games so far...")
                except Exception:
                    continue
    def __len__(self):
        game_offset = len(self.game_offset)
        return game_offset
    def board_to_tensor(self,board):
        board3d = np.zeros((19,8,8), dtype=np.int8)
        for piece_type in chess.PIECE_TYPES:
            for square in board.pieces(piece_type, chess.WHITE):
                idx = np.unravel_index(square, (8, 8))
                board3d[piece_type - 1][7 - idx[0]][idx[1]] = 1
            for square in board.pieces(piece_type, chess.BLACK):
                idx = np.unravel_index(square, (8, 8))
                board3d[piece_type + 5][7 - idx[0]][idx[1]] = 1
        if board.turn == chess.WHITE:
            board3d[12, :, :] = 1
        else:
            board3d[13, :, :] = 1

        return torch.tensor(board3d, dtype=torch.float32)

    def __getitem__(self,idx):
        idx = idx % len(self.game_offset)
        offset = self.game_offset[idx]
        
        with open(self.png_path, 'r') as f:
            f.seek(offset)
            game = chess.pgn.read_game(f)
            
        # Absolute failsafe if game read fails
        if game is None:
            return torch.zeros((19, 8, 8), dtype=torch.float32), torch.tensor(0, dtype=torch.long), torch.tensor(0.0, dtype=torch.float32)
            
        result = game.headers.get('Result', '*')
        if result == "1-0":
            board_result = 1.0
        elif result == "0-1":
            board_result = -1.0
        else:
            board_result = 0.0
            
        positions = []
        board = game.board()
        for move in game.mainline_moves():
            state_tensor = self.board_to_tensor(board)
            policy_tensor_cul = (move.from_square * 64) + move.to_square
            policy_tensor = torch.tensor(policy_tensor_cul, dtype=torch.long)
            
            positions.append((
                state_tensor, 
                policy_tensor, 
                torch.tensor(board_result, dtype=torch.float32)
            ))
            board.push(move)
            
        # If positions list somehow ended up empty, return a safe dummy tensor instead of []
        if len(positions) == 0:
            return torch.zeros((19, 8, 8), dtype=torch.float32), torch.tensor(0, dtype=torch.long), torch.tensor(board_result, dtype=torch.float32)
            
        return random.choice(positions)

if __name__ == "__main__":
    dataset = CHESS_DATASET_LODEAR("AI-CHESS/assates/lichess_db_standard_rated_2013-01.pgn")
    print(f"Total games indexed: {len(dataset)}")
    s, p, v = dataset[0]
    print("Test load successful! Shapes:", s.shape, p.shape, v.shape)
    
