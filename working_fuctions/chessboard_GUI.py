import chess
import pygame
class CHESS:
#dataset
    def __init__(self):
        pass
#legal moves





    






class CHESSGUI:
    def __init__(self):
        self.board = chess.Board()
        self.pieces_size = 30,30
        self.borad_size =  640,640
        self.square_size = 80
        self.offset = 20
        self.pos = 0
        self.legal_move_bit = 0

    def chess_legal_moves(self,input):
        chess.Move(to_square=input)
        the_index = [move.to_square for move in self.board.legal_moves]
        print(the_index)
    
    def coordinates(self,square):
        col = chess.square_file(square)
        row = chess.square_rank(square)

        x_coordinates =  self.offset + (col * self.square_size)
        y_coordinates = self.offset + ((7 - row) * self.square_size)

        return x_coordinates,y_coordinates
    def mouse_check(self,x_mouse,y_mouse):
        
          x_mouse_coordinates =  (x_mouse // self.square_size)
          y_mouse_coordinates = 7 - (y_mouse // self.square_size)


          clecked_no = chess.square(x_mouse_coordinates,y_mouse_coordinates)
        
          return clecked_no
    def chessgui(self):
        
        pygame.init()
        screen = pygame.display.set_mode((self.borad_size))
        clock = pygame.time.Clock()
        running = True

        my_board = pygame.image.load("Screenshot 2026-10-03 191504.png").convert_alpha()
        my_pice = pygame.image.load("Download premium png of Pawn png chess piece clipart, 3D black graphic on transparent background about pawn, pawn chess piece, black pawn, chess piece, and chess pawn 6107211.jpg").convert_alpha()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    the_no = self.mouse_check(mx,my)
                    self.pos = the_no
            x, y = self.coordinates(self.pos)
                    

            screen.fill((0, 0, 0))
            t_my_board = pygame.transform.scale(my_board,self.borad_size)
            t_my_Pieces = pygame.transform.scale(my_pice,self.pieces_size)
            screen.blit(t_my_board,(0,0))
            screen.blit(t_my_Pieces,(x,y))
            pygame.display.flip()
            clock.tick(60)




    
chessboard = CHESSGUI()
chessboard.chessgui()



        