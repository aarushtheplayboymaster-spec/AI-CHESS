import random
import math
#MCTS engine
class MCTS:
    def __init__(self,board, parent = None,move = None):
        self.state = board
        self.parent = parent
        self.move = move
        self.children = []
        self.number_of_wins = 0
        self.number_of_visite = 0
        self.untried_moves = board.get_legal_moves()

#this calculates the best node to visite
    def get_UCB1_score(self,exploration_constant=1.414):
        if self.number_of_visite == 0:
            return float('inf')
        
        exploitation = self.number_of_wins / self.number_of_visite
        exploration = exploration_constant * math.sqrt(math.log(self.parent.number_of_visite ) / self.number_of_visite)
        return exploitation + exploration
#this uses UCB1_score and choose the best node
    def select(self):
        current_node = self
        while not current_node.untried_moves and not current_node.state.game_is_over():
            current_node = max(current_node.children,key=lambda child: child.get_UCB1_score())
        return current_node
#when select() find that there are untried moves it makes the node, child_node and appends them in childern   
    def expand(self):
        if self.untried_moves:
            move = self.untried_moves.pop()
            new_board = self.state.simulat_moves(move)
            child = MCTS(board=new_board,parent=self,move=move)
            self.children.append(child)
            return child
    def simulate(self):
        current_board = self.state
        while not current_board.game_is_over():
            right_move = current_board.get_legal_moves()
            random_move = random.choice(right_move)
            current_board = current_board.simulat_moves(random_move)
        return current_board.hecuristic()
    def backtrack(self,result):
        current_node = self
        while current_node is not None:
            current_node.number_of_visite += 1
            current_node.number_of_wins += result
            current_node = current_node.parent
    def mcts_search(self,loop_runs=1000):
        for _ in range(loop_runs):
            node = self.select()
            if node.untried_moves and not node.state.game_is_over():
                node = node.expand() 
            result = node.simulate()
            node.backtrack(result)
        best_path = max(self.children,key=lambda child: child.number_of_visite)
        return best_path.move




