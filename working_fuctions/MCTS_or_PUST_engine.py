import math
from .NET import ChessNet
import torch
#MCTS engine
class PUCT:
    def __init__(self,board, parent = None,move = None,prior_prob=1.0):
        self.state = board
        self.parent = parent
        self.move = move
        self.children = []
        self.number_of_wins = 0
        self.number_of_visite = 0
        self.untried_moves = list(self.state.board.legal_moves)
        self.prior_prob = prior_prob

#this calculates the best node to visite
    def get_PUCT_score(self,exploration_constant=2.5):
        if self.number_of_visite == 0:
            return float('inf')
        exploitation = self.number_of_wins / self.number_of_visite

        exploration = exploration_constant * self.prior_prob * math.sqrt(math.log(self.parent.number_of_visite ) / (1 + self.number_of_visite))
        return exploitation + exploration
        
#this uses UCB1_score and choose the best node
    def select(self):
        current_node = self
        while not current_node.untried_moves and not current_node.state.is_terminal():
            current_node = max(current_node.children,key=lambda child: child.get_PUCT_score())
        return current_node
#when select() find that there are untried moves it makes the node, child_node and appends them in childern   
    def expand(self,model):
        if self.untried_moves:
            move = self.untried_moves.pop()
            new_board = self.state.simulate_move(move)

            action_index = (move.from_square * 64) + move.to_square
            tensor4d = self.state.to_tensor().unsqueeze(0)
            with torch.no_grad():
                policy_head, _ = model(tensor4d)
                probs = torch.softmax(policy_head, dim=1)
                prior = probs[0, action_index].item()
            child = PUCT(board=new_board,parent=self,move=move,prior_prob=prior)
            self.children.append(child)
            return child
    def board_value(self,model):
        tensor3d = self.state.to_tensor()
        tensor4d = tensor3d.unsqueeze(0)
        with torch.no_grad():
            _ , value_head = model(tensor4d)
        return value_head.item()
    def backtrack(self,result):
        current_node = self
        while current_node is not None:
            current_node.number_of_visite += 1
            current_node.number_of_wins += result
            current_node = current_node.parent
    def puct_search(self,loop_runs=1000):
        model = ChessNet()
        model.load_state_dict(torch.load("check_point_chess_model_weights.pt"))
        model.eval()
        for _ in range(loop_runs):
            node = self.select()
            if node.untried_moves and not node.state.is_terminal():
                node = node.expand(model) 
            result = node.board_value(model)
            node.backtrack(result)
        best_path = max(self.children,key=lambda child: child.number_of_visite)
        return best_path.move




