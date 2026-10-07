import chess
import pygame
from chessboard import chessmoves
import pygame_widgets
from pygame_widgets.button import Button 
class CHESSGUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("JUST_PLAY")
        self.clock = pygame.time.Clock()
        self.board = chess.Board()
        self.pieces_size = 70,70
        self.borad_size =  940,940
        self.square_size = 80
        self.offset = 5
        self.legal = chessmoves()
        self.selected = None
        self.turn = True
        self.show_sittings = False
        self.running = True
        self.screen = pygame.display.set_mode((self.borad_size))
        self.piece_image = {
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
        self.my_board = pygame.image.load("AI-CHESS/assates/Screenshot 2026-10-03 191504.png").convert_alpha()
        self.highlighting = pygame.image.load("AI-CHESS/assates/RedX_(3).png").convert_alpha()
        self.sittings_icon = pygame.image.load("AI-CHESS/assates/VirtualBox_6.1_–_vm_settings_16px_x4.png").convert_alpha()

    def screen_coordinates(self,square):# this is used to give the screen pos in bitboard form

        col = chess.square_file(square)
        row = chess.square_rank(square)

        x_coordinates =  self.offset + (col * self.square_size)# formula  offset + colume x squre_size 
        y_coordinates = self.offset + ((7 - row) * self.square_size)# formula  offset +  (7 - colume) x squre_size 

        return x_coordinates,y_coordinates #returns x and y coods for piece image placement 
    
    
    def move_from(self,x_mouse,y_mouse):#it is used to convert screen x and y into chess bitboard
        
          x_mouse_coordinates =  (x_mouse // self.square_size)# formula  colume // squre_size 
          y_mouse_coordinates = 7 - (y_mouse // self.square_size)# formula  7 - colume // squre_size 


          from_square = chess.square(x_mouse_coordinates,y_mouse_coordinates)
        
          return from_square
    
    def handal_checkes(self,mx,my):# this gets the screen coordinates when we right check on the screen 
        checked_square = self.move_from(mx,my) # then sends the coods to move_from() to get the bitboard pos

        if self.selected is None: # it sees if there is a selected square or not if there isn't any it moves forward
            piece = self.legal.board.piece_at(checked_square)#it checks if there is any piece there or not
            if piece is not None:
                self.selected = checked_square #makes that so that the  check we did on a piece gets selected to move 
            else:# does nothing if there is no piece when we check
                pass
        else: # if there is a piece selected (by doing the above)
            #get the chess name of both squres e.g(e2e4)
            fro_squre = chess.square_name(self.selected)
            to_squre = chess.square_name(checked_square)

            if fro_squre != to_squre:
                get_uni_move = fro_squre + to_squre # combines them to send them to (self.legal.chess_legal_moves(get_uni_move)) fuction which moves that piece 
                self.legal.chess_legal_moves(get_uni_move)

                self.selected = None #resets the value for next piece move
    
    
    
    def highlight(self,square):#used for highlighting the legal moves of the piese you select
        col = chess.square_file(square)
        row = chess.square_rank(square)

        x_coordinates =  25 + (col * self.square_size)# uses same formula as the sceen_coodensts 
        y_coordinates = 25 + ((7 - row) * self.square_size)

        return x_coordinates,y_coordinates#returns x and y coods for highlighting  of  pieces legal move placement 

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
    def check_botton(self):
        pygame.transform.scale(self.sittings_icon,(10,10))
        button = Button(
            self.screen, 900, 10, 30, 30, 
            text='',
            image=self.sittings_icon,
            inactiveColour=(0, 0, 0),  
            hoverColour=(125, 125, 125),     
            pressedColour=(0, 200, 20),     
            radius=25,                      
            onClick= self.sittings.sitting
            )
    def chessgui(self):# this is where the chess GUI starts
        while self.running:

            game_over = self.legal.is_terminal()
            if game_over is True:
                self.running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if mx < 640 and my < 640:
                        self.handal_checkes(mx,my)
                    
            self.screen.fill((0, 0, 0))
            t_board = pygame.transform.scale(self.my_board,(640,640))
            self.screen.blit(t_board,(0,0))
            
            for square in range(64):
                piece = self.legal.board.piece_at(square)
                if piece is not None:
                    symbol = piece.symbol()
                    if symbol in self.piece_image:
                        x, y = self.screen_coordinates(square)
                        pygame.transform.scale(self.piece_image[symbol],self.pieces_size)
                        self.screen.blit(self.piece_image[symbol], (x, y))


                if self.selected is not None:
                    for move in self.legal.board.legal_moves:
                        if move.from_square == self.selected:
                            target_square = move.to_square
                            x, y = self.highlight(target_square)
                            pygame.transform.scale(self.highlighting,self.pieces_size)
                            self.screen.blit(self.highlighting, (x, y))

            pygame_widgets.update(event) 
            pygame.display.flip()
            self.clock.tick(60)




if __name__ == "__main__":
    chessboard = CHESSGUI()
    chessboard.chessgui()