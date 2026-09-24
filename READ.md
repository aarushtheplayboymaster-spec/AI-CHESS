AS, you can already see and tell that this is a AI chess board(and my first AI projest)
and it is really simple project to be honest the only two thing that are going to to hard are MCTS search and whell the neural network which the main reason
I have build this whole thing in first place.

1) strcture

chessboard.py #gives legal move,simulates moves,gives hectes,gives terminal state

chessboard_GUI.py #displays the whole game

NET.py #the AI model calculates the moves and gives  P(policy e.g which move is best) V(value e.g +1.0,-1.0,0.0)

MCTS.py #it usesg the intution and values from AI to use them in its simulation fuction instant of random move then it provides the best the best move to play


MAIN.py #run everything and does navigation 


2) neural network(usesg supervised learning,pytorch)

















