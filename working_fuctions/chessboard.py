import chess
import pygame
import random
class chessGUI:
    def __init__(self):
        self.board = chess.Board()
    def chess_legal_moves(self,player):
        self.board.push_san(player)
        legal_moves = [self.board.san(move) for move in self.board.legal_moves]   
        return legal_moves
    def chessmoves(self):
        player = str(input("enter your legal move: "))
        move = self.chess_legal_moves(player)
        print(move)
        AI = str(random.choice(move))
        move = self.chess_legal_moves(AI)
        print(move)
    def chessGUI(self):
        pygame.init()
        screen = pygame.display.set_mode((1000, 600))
        clock = pygame.time.Clock()
        my_image = pygame.image.load("starting_board.svg").convert_alpha()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))
            screen.blit(my_image,(10,60))
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

game = chessGUI()
game.chessGUI()



        
       


