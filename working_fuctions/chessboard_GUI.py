import chess
import pygame
from chessboard import chessmoves
class CHESSGUI:
    def __init__(self):
        self.board = chess.Board()
        self.pieces_size = 70,70
        self.borad_size =  940,940
        self.square_size = 80
        self.offset = 5
        self.legal = chessmoves()
        self.selected = None
        self.selected_piece_key = None
        self.turn = True

    def screen_coordinates(self,square):

        col = chess.square_file(square)
        row = chess.square_rank(square)

        x_coordinates =  self.offset + (col * self.square_size)
        y_coordinates = self.offset + ((7 - row) * self.square_size)

        return x_coordinates,y_coordinates
    def highlight(self,square):
        col = chess.square_file(square)
        row = chess.square_rank(square)

        x_coordinates =  25 + (col * self.square_size)
        y_coordinates = 25 + ((7 - row) * self.square_size)

        return x_coordinates,y_coordinates

    
    def move_from(self,x_mouse,y_mouse):
        
          x_mouse_coordinates =  (x_mouse // self.square_size)
          y_mouse_coordinates = 7 - (y_mouse // self.square_size)


          from_square = chess.square(x_mouse_coordinates,y_mouse_coordinates)
        
          return from_square
    
    def handal_checkes(self,mx,my):
        checked_square = self.move_from(mx,my)
        if self.selected is None:
            piece = self.legal.board.piece_at(checked_square)
            if piece is not None:
                self.selected = checked_square
            else:
                print("there is no piece stupid")
        else:
            fro_squre = chess.square_name(self.selected)
            to_squre = chess.square_name(checked_square)
            if fro_squre != to_squre:
                get_uni_move = fro_squre + to_squre
                self.legal.chess_legal_moves(get_uni_move)
                self.selected = None

    def chess_engine(self):
        if self.turn == False:
            checked_square = 47
            selected = 55
            fro_squre = chess.square_name(selected)
            to_squre = chess.square_name(checked_square)
            if fro_squre != to_squre:
                get_uni_move = fro_squre + to_squre
                self.legal.chess_legal_moves(get_uni_move)
                self.turn = True
    def chessgui(self):

        pygame.init()
        screen = pygame.display.set_mode((self.borad_size))
        pygame.display.set_caption("JUST_PLAY")
        clock = pygame.time.Clock()
        running = True

        my_board = pygame.image.load("AI-CHESS/assates/Screenshot 2026-10-03 191504.png").convert_alpha()
        highlighting = pygame.image.load("AI-CHESS/assates/RedX_(3).png").convert_alpha()
        piece_image = {
        "P":pygame.image.load("AI-CHESS/assates/Chess_plt60.png").convert_alpha(),
        "p":pygame.image.load("AI-CHESS/assates/Chess_pdt60.png").convert_alpha(),
        "R":pygame.image.load("AI-CHESS/assates/Chess_rlt60.png").convert_alpha(),
        "r":pygame.image.load("AI-CHESS/assates/Chess_rdt60.png").convert_alpha(),
        "B":pygame.image.load("AI-CHESS/assates/Chess_blt60.png").convert_alpha(),
        "b":pygame.image.load("AI-CHESS/assates/Chess_bdt60.png").convert_alpha(),
        "N":pygame.image.load("AI-CHESS/assates/Chess_nlt60.png").convert_alpha(),
        "n":pygame.image.load("AI-CHESS/assates/Chess_ndt60.png").convert_alpha(),
        "K":pygame.image.load("AI-CHESS/assates/Chess_klt60.png").convert_alpha(),
        "k":pygame.image.load("AI-CHESS/assates/Chess_kdt60.png").convert_alpha(),
        "Q":pygame.image.load("AI-CHESS/assates/Chess_qlt60.png").convert_alpha(),
        "q":pygame.image.load("AI-CHESS/assates/Chess_qdt60.png").convert_alpha()
      
        }
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    self.handal_checkes(mx,my)




            screen.fill((0, 0, 0))
            t_my_board = pygame.transform.scale(my_board,(640,640))



            screen.blit(t_my_board,(0,0))

            for square in range(64):
                piece = self.legal.board.piece_at(square)
                if piece is not None:
                    symbol = piece.symbol()
                    if symbol in piece_image:
                        x, y = self.screen_coordinates(square)
                        pygame.transform.scale(piece_image[symbol],self.pieces_size)
                        screen.blit(piece_image[symbol], (x, y))


                if self.selected is not None:
                    for move in self.legal.board.legal_moves:
                        if move.from_square == self.selected:
                            target_square = move.to_square
                            x, y = self.highlight(target_square)
                            pygame.transform.scale(highlighting,self.pieces_size)
                            screen.blit(highlighting, (x, y))








            pygame.display.flip()
            clock.tick(60)




if __name__ == "__main__":
    chessboard = CHESSGUI()
    chessboard.chessgui()