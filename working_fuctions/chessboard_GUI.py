import chess
import pygame
from chessboard import chessmoves
import pygame_widgets
from pygame_widgets.button import Button 
from pygame_widgets.dropdown import Dropdown
import time
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
        self.flip_board = False
        self.running = True
        self.pawn_promotion = False
        self.pending_move = None
        self.screen = pygame.display.set_mode((self.borad_size))
        self.flip_botton()
        self.white_timer = 600.0
        self.black_timer = 600.0
        self.wmin = 10
        self.bmin = 10
        self.wsec = 00
        self.bsec = 00
        self.is_game_started = False
        self.setting_is_active = True
        self.sitting_on = False
        self.is_game_overed = False
        self.lost_by_time = False
        self.who_won_by_time = None
        self.player_is_resigning = False
        self.resign_button()


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
        self.white_board = pygame.image.load("AI-CHESS/assates/Screenshot 2026-10-03 191504.png").convert_alpha()
        self.black_board = pygame.image.load("AI-CHESS/assates/Screenshot 2026-10-09 233024.png").convert_alpha()
        self.highlighting = pygame.image.load("AI-CHESS/assates/RedX_(3).png").convert_alpha()
        self.sittings_icon = pygame.image.load("AI-CHESS/assates/VirtualBox_6.1_–_vm_settings_disabled_16px_x4.png").convert_alpha()
        pygame.transform.scale(self.sittings_icon,(10,10))
        self.sittings_button()

    def white_screen_coordinates(self,square):# this is used to give the screen pos in bitboard form

        col = chess.square_file(square)
        row = chess.square_rank(square)

        x_coordinates =  self.offset + (col * self.square_size)# formula  offset + colume x squre_size 
        y_coordinates = self.offset + ((7 - row) * self.square_size)# formula  offset +  (7 - colume) x squre_size 

        return x_coordinates,y_coordinates #returns x and y coods for piece image placement 
    
    def black_screen_coordinates(self,square):# this is used to give the screen pos in bitboard form

        col = chess.square_file(square)
        row = chess.square_rank(square)

        x_coordinates =  self.offset + ((7- col) * self.square_size)# formula  offset + colume x squre_size 
        y_coordinates = self.offset + (row * self.square_size)# formula  offset +  (7 - colume) x squre_size 

        return x_coordinates,y_coordinates #returns x and y coods for piece image placement 
    
    
    def white_move_from(self,x_mouse,y_mouse):#it is used to convert screen x and y into chess bitboard
        
          x_mouse_coordinates =  (x_mouse // self.square_size)# formula  colume // squre_size 
          y_mouse_coordinates = 7 - (y_mouse // self.square_size)# formula  7 - colume // squre_size 


          from_square = chess.square(x_mouse_coordinates,y_mouse_coordinates)
        
          return from_square
    
    def black_move_from(self,x_mouse,y_mouse):#it is used to convert screen x and y into chess bitboard
        
          x_mouse_coordinates =  7 - (x_mouse // self.square_size)# formula  colume // squre_size 
          y_mouse_coordinates = (y_mouse // self.square_size)# formula  7 - colume // squre_size 


          from_square = chess.square(x_mouse_coordinates,y_mouse_coordinates)
        
          return from_square
    
    def handal_checkes(self,mx,my):# this gets the screen coordinates when we right check on the screen 
        if self.flip_board == False:
        
            checked_square = self.white_move_from(mx,my) # then sends the coods to move_from() to get the bitboard pos
            if self.selected is None: # it sees if there is a selected square or not if there isn't any it moves forward
                piece = self.legal.board.piece_at(checked_square) #it checks if there is any piece there or not
                if piece is not None:
                    self.selected = checked_square #makes that so that the  check we did on a piece gets selected to move 
                else:# does nothing if there is no piece when we check
                    pass
            else: # if there is a piece selected (by doing the above)
                #get the chess name of both squres e.g(e2e4)
                fro_squre = chess.square_name(self.selected)
                to_squre = chess.square_name(checked_square)
                if fro_squre != to_squre:
                    pieces = self.legal.board.piece_at(self.selected)
                    if pieces and pieces.piece_type == chess.PAWN:
                        target_rank = chess.square_rank(checked_square)
                        if pieces.color == chess.WHITE and target_rank == 7:
                            self.pawn_promotion = True
                            self.its_white = True
                        if pieces.color == chess.BLACK and target_rank == 0:
                            self.pawn_promotion = True
                            self.its_white = False
                    if self.pawn_promotion == True:
                        self.pending_move = fro_squre + to_squre # combines them to send them to (self.legal.chess_legal_moves(get_uni_move)) fuction which moves that piece 
                    else:
                        get_uni_move = fro_squre + to_squre 
                        self.legal.chess_legal_moves(get_uni_move)
                self.selected = None #resets the value for next piece move
            
        elif self.flip_board == True:
            checked_square = self.black_move_from(mx,my)

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
                    pieces = self.legal.board.piece_at(self.selected)
                    if pieces and pieces.piece_type == chess.PAWN:
                        target_rank = chess.square_rank(checked_square)
                        if pieces.color == chess.WHITE and target_rank == 7:
                            self.pawn_promotion = True
                            self.its_white = True
                        if pieces.color == chess.BLACK and target_rank == 0:
                            self.pawn_promotion = True
                            self.its_white = False
                    if self.pawn_promotion == True:
                        self.pending_move = fro_squre + to_squre # combines them to send them to (self.legal.chess_legal_moves(get_uni_move)) fuction which moves that piece 
                    else: 
                        get_uni_move = fro_squre + to_squre # combines them to send them to (self.legal.chess_legal_moves(get_uni_move)) fuction which moves that piece 
                        self.legal.chess_legal_moves(get_uni_move)

                    self.selected = None #resets the value for next piece move
    
    
    
    def white_highlight(self,square):#used for highlighting the legal moves of the piese you select
        col = chess.square_file(square)
        row = chess.square_rank(square)

        x_coordinates =  25 + (col * self.square_size)# uses same formula as the sceen_coodensts 
        y_coordinates = 25 + ((7 - row) * self.square_size)

        return x_coordinates,y_coordinates#returns x and y coods for highlighting  of  pieces legal move placement 
    def black_highlight(self,square):#used for highlighting the legal moves of the piese you select
        col = chess.square_file(square)
        row = chess.square_rank(square)

        x_coordinates =  25 + ((7 - col) * self.square_size)# uses same formula as the sceen_coodensts 
        y_coordinates = 25 + (row * self.square_size)

        return x_coordinates,y_coordinates#returns x and y coods for highlighting  of  pieces legal move placement t 

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
    def flip_botton(self):
        self.filp_the_board = Button(
            self.screen, 670, 10, 30, 30, 
            text='',
            image=pygame.image.load('AI-CHESS/assates/Farm-Fresh_transform_flip.png').convert_alpha(),
            inactiveColour=(0, 0, 0),  
            hoverColour=(125, 125, 125),     
            pressedColour=(0, 200, 20),     
            radius=25,
            onClick= self.fliping_board
        )
    def resign_button(self):
        self.resign_the_game = Button(
            self.screen, 670, 50, 50, 50, 
            text='',
            image=pygame.image.load('AI-CHESS/assates/Screenshot 2026-10-18 202440.png').convert_alpha(),
            inactiveColour=(0, 0, 0),  
            hoverColour=(125, 125, 125),     
            pressedColour=(0, 200, 20),     
            radius=25,
            onClick= self.resigning
        )
    def resigning(self):
        if self.is_game_started == True:
            self.player_is_resigning = not self.player_is_resigning
            self.is_game_overed = True


    def fliping_board(self):
        if self.is_game_started == False:
            self.flip_board = not self.flip_board

    def showing_sittings(self):
        self.show_sittings = not self.show_sittings
    def promote_pawn(self,the_piece_type):
        if the_piece_type != 'c':
            self.legal.chess_legal_moves(self.pending_move + the_piece_type)
        self.pawn_promotion = False
        self.pending_move = None
        self.Queen_promotion.hide()
        self.Knight_promotion.hide()
        self.Bishop_promotion.hide()
        self.Rook_promotion.hide()
        self.close_buttons.hide()
        
    def pawn_promotion_botton(self,mx,my):
        self.Queen_promotion = Button(
            self.screen, mx, (my), 60, 60, 
            text='',
            image=self.piece_image['Q' if self.its_white == True else 'q'],
            inactiveColour=(0, 0, 0),  
            hoverColour=(125, 125, 125),     
            pressedColour=(0, 200, 20),     
            radius=0,                      
            onClick= lambda : self.promote_pawn(the_piece_type = 'q')
        )
        self.Knight_promotion = Button(
            self.screen, mx, (my+60), 60, 60, 
            text='',
            image=self.piece_image['N' if self.its_white == True else 'n'],
            inactiveColour=(0, 0, 0),  
            hoverColour=(125, 125, 125),     
            pressedColour=(0, 200, 20),     
            radius=0,                      
            onClick= lambda : self.promote_pawn(the_piece_type = 'n')
        )
        self.Bishop_promotion = Button(
            self.screen, mx, (my+60*2), 60, 60, 
            text='',
            image=self.piece_image['B' if self.its_white == True else 'b'],
            inactiveColour=(0, 0, 0),  
            hoverColour=(125, 125, 125),     
            pressedColour=(0, 200, 20),     
            radius=0,                      
            onClick= lambda : self.promote_pawn(the_piece_type = 'b')
        )
        self.Rook_promotion = Button(
            self.screen, mx, (my+60*3), 60, 60, 
            text='',
            image=self.piece_image['R' if self.its_white == True else 'r'],
            inactiveColour=(0, 0, 0),  
            hoverColour=(125, 125, 125),     
            pressedColour=(0, 200, 20),     
            radius=0,                      
            onClick= lambda : self.promote_pawn(the_piece_type = 'r')
        )
        self.close_buttons = Button(
            self.screen, mx, (my+60*4), 60, 40, 
            text='',
            image=self.highlighting,
            inactiveColour=(0, 0, 0),  
            hoverColour=(125, 125, 125),     
            pressedColour=(0, 200, 20),     
            radius=0,                      
            onClick=  lambda : self.promote_pawn(the_piece_type = 'c')
        )
    def game_timer(self,time_paused):
        if self.is_game_started == True and self.is_game_overed == False:
            if self.legal.board.turn == chess.WHITE:
                self.white_timer -= time_paused
                self.wmin = int(self.white_timer) // 60
                self.wsec = int(self.white_timer) % 60
            elif self.legal.board.turn == chess.BLACK:
                self.black_timer -= time_paused
                self.bmin = int(self.black_timer) // 60
                self.bsec = int(self.black_timer) % 60
            self.start_time = time.perf_counter()
        if self.flip_board == False:
            font = pygame.font.SysFont("Arial", 36, bold=True, italic=False)
            white_text_surface = font.render(f"{self.wmin:02d}:{self.wsec:02d}", True, (0, 0, 0)) 
            white_text_rect = white_text_surface.get_rect()
            white_text_rect.center = (680 + 150 // 2, 500 + 60 // 2)
            pygame.draw.rect(self.screen,(255, 255, 255),(680,500,150,60))
            self.screen.blit(white_text_surface,white_text_rect)
            black_text_surface = font.render(f"{self.bmin:02d}:{self.bsec:02d}", True, (255, 255, 255)) 
            black_text_rect = black_text_surface.get_rect()
            black_text_rect.center = (680 + 150 // 2, 300 + 60 // 2)
            pygame.draw.rect(self.screen,(38, 36, 33),(680,300,150,60))
            self.screen.blit(black_text_surface,black_text_rect)
        elif self.flip_board == True:
            font = pygame.font.SysFont("Arial", 36, bold=True, italic=False)
            white_text_surface = font.render(f"{self.wmin:02d}:{self.wsec:02d}", True, (0, 0, 0)) 
            white_text_rect = white_text_surface.get_rect()
            white_text_rect.center = (680 + 150 // 2, 300 + 60 // 2)
            pygame.draw.rect(self.screen,(255, 255, 255),(680,300,150,60))
            self.screen.blit(white_text_surface,white_text_rect)
            black_text_surface = font.render(f"{self.bmin:02d}:{self.bsec:02d}", True, (255, 255, 255)) 
            black_text_rect = black_text_surface.get_rect()
            black_text_rect.center = (680 + 150 // 2, 500 + 60 // 2)
            pygame.draw.rect(self.screen,(38, 36, 33),(680,500,150,60))
            self.screen.blit(black_text_surface,black_text_rect)
    def fake_game_timer(self):
        if self.flip_board == False:
            font = pygame.font.SysFont("Arial", 36, bold=True, italic=False)
            white_text_surface = font.render(f"{self.wmin:02d}:{self.wsec:02d}", True, (0, 0, 0)) 
            white_text_rect = white_text_surface.get_rect()
            white_text_rect.center = (680 + 150 // 2, 500 + 60 // 2)
            pygame.draw.rect(self.screen,(255, 255, 255),(680,500,150,60))
            self.screen.blit(white_text_surface,white_text_rect)
            black_text_surface = font.render(f"{self.bmin:02d}:{self.bsec:02d}", True, (255, 255, 255)) 
            black_text_rect = black_text_surface.get_rect()
            black_text_rect.center = (680 + 150 // 2, 300 + 60 // 2)
            pygame.draw.rect(self.screen,(38, 36, 33),(680,300,150,60))
            self.screen.blit(black_text_surface,black_text_rect)
        elif self.flip_board == True:
            font = pygame.font.SysFont("Arial", 36, bold=True, italic=False)
            white_text_surface = font.render(f"{self.wmin:02d}:{self.wsec:02d}", True, (0, 0, 0)) 
            white_text_rect = white_text_surface.get_rect()
            white_text_rect.center = (680 + 150 // 2, 300 + 60 // 2)
            pygame.draw.rect(self.screen,(255, 255, 255),(680,300,150,60))
            self.screen.blit(white_text_surface,white_text_rect)
            black_text_surface = font.render(f"{self.bmin:02d}:{self.bsec:02d}", True, (255, 255, 255)) 
            black_text_rect = black_text_surface.get_rect()
            black_text_rect.center = (680 + 150 // 2, 500 + 60 // 2)
            pygame.draw.rect(self.screen,(38, 36, 33),(680,500,150,60))
            self.screen.blit(black_text_surface,black_text_rect)
    
    def the_game_is_on(self):
        if self.is_game_started == False and self.is_game_overed == False:
            pygame.draw.rect(self.screen,(0, 0, 0),(159,220,320,200))
            font = pygame.font.SysFont("Arial", 36, bold=True, italic=False)
            
            self.play_game = Button(
                self.screen, 220, 290, 200, 70,
                text="PLAY AI",
                font = font,
                textColour = (255,255,255),
                fontSize=30,
                inactiveColour=(50, 205, 50),
                hoverColour=(0, 128, 0),
                pressedColour=(0, 200, 20),
                radius=0,
                onClick=  self.the_game_state
            )

    def the_game_state(self):
        self.is_game_started = not self.is_game_started
        self.start_time = time.perf_counter()
        self.play_game.hide()
    def sittings_button(self):
        if self.is_game_started == False:
            self.setting = Button(
                self.screen, 878, 10, 70, 70, 
                text='',
                image=self.sittings_icon,
                inactiveColour=(48, 46, 43),  
                hoverColour=(125, 125, 125),     
                pressedColour=(0, 200, 20),     
                radius=0,                      
                onClick=  self.sitting_is_active
            )
    def sitting_is_active(self):
        if self.is_game_started == False:
            self.sitting_on = not self.sitting_on
    def sitting_panal(self):
        if self.sitting_on == True:
            pygame.draw.rect(self.screen,(38, 36, 33),(300,300,320,300)) 
    def game_over(self):
        if self.is_game_overed == True and self.lost_by_time == False and self.player_is_resigning == False:
            game_result = self.legal.board.outcome()
            if game_result.winner == chess.WHITE:
                how_it_ended = game_result.termination.name
                pygame.draw.rect(self.screen,(38, 36, 33),(159,180,320,280)) 
                pygame.draw.rect(self.screen,(0, 0, 0),(159,180,320,100)) 
                font = pygame.font.SysFont("Arial", 36, bold=True, italic=False)
                winning_text = font.render("white has won by",True,(255,255,255))
                winning_text_about = font.render(f'{how_it_ended}',True,(255,255,255))
                self.screen.blit(winning_text, (220,180))
                self.screen.blit(winning_text_about, (240,230))
                self.resit = Button(
                    self.screen, 220, 305, 200, 70,
                    text="REMACH",
                    font = font,
                    textColour = (255,255,255),
                    fontSize=30,
                    inactiveColour=(50, 205, 50),
                    hoverColour=(0, 128, 0),
                    pressedColour=(0, 200, 20),
                    radius=0,
                    onClick=  self.game_reset
                )
            elif game_result.winner == chess.BLACK:
                how_it_ended = game_result.termination.name
                pygame.draw.rect(self.screen,(38, 36, 33),(159,180,320,280)) 
                pygame.draw.rect(self.screen,(255, 255, 255),(159,180,320,100)) 
                font = pygame.font.SysFont("Arial", 36, bold=True, italic=False)
                winning_text = font.render("black has won by",True,(0,0,0))
                winning_text_about = font.render(f'{how_it_ended}',True,(0,0,0))
                self.screen.blit(winning_text, (220,180))
                self.screen.blit(winning_text_about, (240,230))
                self.resit = Button(
                    self.screen, 220, 305, 200, 70,
                    text="REMACH",
                    font = font,
                    textColour = (255,255,255),
                    fontSize=30,
                    inactiveColour=(50, 205, 50),
                    hoverColour=(0, 128, 0),
                    pressedColour=(0, 200, 20),
                    radius=0,
                    onClick=  self.game_reset
                )

            else:
                how_it_ended = game_result.termination.name
                pygame.draw.rect(self.screen,(38, 36, 33),(159,180,320,280)) 
                pygame.draw.rect(self.screen,(255, 255, 255),(159,180,320,100)) 
                font = pygame.font.SysFont("Arial", 36, bold=True, italic=False)
                winning_text = font.render("IT WAS A STALMATE",True,(0,0,0))
                winning_text_about = font.render(f'{how_it_ended}',True,(0,0,0))
                self.screen.blit(winning_text, (220,180))
                self.screen.blit(winning_text_about, (240,230))
                self.resit = Button(
                    self.screen, 220, 305, 200, 70,
                    text="REMACH",
                    font = font,
                    textColour = (255,255,255),
                    fontSize=30,
                    inactiveColour=(50, 205, 50),
                    hoverColour=(0, 128, 0),
                    pressedColour=(0, 200, 20),
                    radius=0,
                    onClick=  self.game_reset
                )
    def game_over_by_time(self):
        if self.is_game_overed == True and self.player_is_resigning == False:
            if self.who_won_by_time == 'BLACK':
                pygame.draw.rect(self.screen,(38, 36, 33),(159,180,320,280)) 
                pygame.draw.rect(self.screen,(255, 255, 255),(159,180,320,100)) 
                font = pygame.font.SysFont("Arial", 36, bold=True, italic=False)
                winning_text = font.render("black won",True,(0,0,0))
                winning_text_about = font.render('by time',True,(0,0,0))
                self.screen.blit(winning_text, (220,180))
                self.screen.blit(winning_text_about, (240,230))
                self.resit = Button(
                    self.screen, 220, 305, 200, 70,
                    text="REMACH",
                    font = font,
                    textColour = (255,255,255),
                    fontSize=30,
                    inactiveColour=(50, 205, 50),
                    hoverColour=(0, 128, 0),
                    pressedColour=(0, 200, 20),
                    radius=0,
                    onClick=  self.game_reset
                )
            elif self.who_won_by_time == 'WHITE':
                pygame.draw.rect(self.screen,(38, 36, 33),(159,180,320,280)) 
                pygame.draw.rect(self.screen,(255, 255, 255),(159,180,320,100)) 
                font = pygame.font.SysFont("Arial", 36, bold=True, italic=False)
                winning_text = font.render("white won",True,(0,0,0))
                winning_text_about = font.render('by time',True,(0,0,0))
                self.screen.blit(winning_text, (220,180))
                self.screen.blit(winning_text_about, (240,230))
                self.resit = Button(
                    self.screen, 220, 305, 200, 70,
                    text="REMACH",
                    font = font,
                    textColour = (255,255,255),
                    fontSize=30,
                    inactiveColour=(50, 205, 50),
                    hoverColour=(0, 128, 0),
                    pressedColour=(0, 200, 20),
                    radius=0,
                    onClick=  self.game_reset
                )
    def palyer_wants_to_resign(self):
        if self.player_is_resigning == True and self.is_game_overed == True:
            if self.flip_board == False:
                pygame.draw.rect(self.screen,(38, 36, 33),(159,180,320,280)) 
                pygame.draw.rect(self.screen,(255, 255, 255),(159,180,320,100)) 
                font = pygame.font.SysFont("Arial", 36, bold=True, italic=False)
                winning_text = font.render("black won becouse",True,(0,0,0))
                winning_text_about = font.render('white resigned',True,(0,0,0))
                self.screen.blit(winning_text, (220,180))
                self.screen.blit(winning_text_about, (240,230))
                self.resit = Button(
                    self.screen, 220, 305, 200, 70,
                    text="REMACH",
                    font = font,
                    textColour = (255,255,255),
                    fontSize=30,
                    inactiveColour=(50, 205, 50),
                    hoverColour=(0, 128, 0),
                    pressedColour=(0, 200, 20),
                    radius=0,
                    onClick=  self.game_reset
                )
            elif self.flip_board == True:
                pygame.draw.rect(self.screen,(38, 36, 33),(159,180,320,280)) 
                pygame.draw.rect(self.screen,(255, 255, 255),(159,180,320,100)) 
                font = pygame.font.SysFont("Arial", 36, bold=True, italic=False)
                winning_text = font.render("white won becouse",True,(0,0,0))
                winning_text_about = font.render('black resigned',True,(0,0,0))
                self.screen.blit(winning_text, (220,180))
                self.screen.blit(winning_text_about, (240,230))
                self.resit = Button(
                    self.screen, 220, 305, 200, 70,
                    text="REMACH",
                    font = font,
                    textColour = (255,255,255),
                    fontSize=30,
                    inactiveColour=(50, 205, 50),
                    hoverColour=(0, 128, 0),
                    pressedColour=(0, 200, 20),
                    radius=0,
                    onClick=  self.game_reset
                )
    def game_reset(self):
        self.legal.board = chess.Board()
        self.is_game_overed =  False
        self.is_game_started = False
        self.player_is_resigning = False
        self.white_timer = 600.0
        self.black_timer = 600.0
        self.wmin = 10
        self.bmin = 10
        self.wsec = 00
        self.bsec = 00
        self.resit.hide()

        

    def chessgui(self):# this is where the chess GUI starts
        while self.running:
            # this handals is sameone has won or not
            game_over = self.legal.is_terminal()
            if game_over is True:
                self.is_game_overed = True
                self.is_game_started = False

            elif self.white_timer <= 0:
                self.who_won_by_time = 'BLACK'
                self.is_game_overed = True
                self.lost_by_time = True
                self.is_game_started = False
            elif self.black_timer <= 0:
                self.who_won_by_time = 'WHITE'
                self.lost_by_time = True
                self.is_game_overed = True
                
                self.is_game_started = False

            # this handal the window events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:#quiting the game
                    self.running = False
                if self.is_game_started == True:
                    if event.type == pygame.MOUSEBUTTONDOWN:#check on the screen
                        mx, my = event.pos #gets the screen coods
                        if self.pawn_promotion and self.pending_move is not None:
                            pass
                        else:
                            if mx < 640 and my < 640: #sees of the check was inside of the board 
                                self.handal_checkes(mx,my)#give the coods to handal_checkes() to move a piece 
                                if self.pawn_promotion == True and self.pending_move is not None:
                                    self.pawn_promotion_botton(mx,my)
                
            #this fills the windows background
            self.screen.fill((48, 46, 43))
            self.filp_the_board.show()
            if self.is_game_started == True:
                current = time.perf_counter()
                elapsed = current - self.start_time
                self.game_timer(elapsed)
            else:
                self.fake_game_timer()
            
            self.sittings_button


            if self.flip_board == False:
                resized_white_board = pygame.transform.scale(self.white_board,(640,640))
                self.screen.blit(resized_white_board,(0,0))
                self.the_game_is_on()
                for square in range(64):
                    #this prints all the piece to there places in order
                    piece = self.legal.board.piece_at(square)
                    if piece is not None:
                        symbol = piece.symbol()
                        if symbol in self.piece_image:
                            x, y = self.white_screen_coordinates(square)
                            pygame.transform.scale(self.piece_image[symbol],self.pieces_size)
                            self.screen.blit(self.piece_image[symbol], (x, y))
                    #where this prints all the highlighting moves that you can play when you select a piece 
                    if self.selected is not None:
                        for move in self.legal.board.legal_moves:
                            if move.from_square == self.selected:
                                target_square = move.to_square
                                x, y = self.white_highlight(target_square)
                                pygame.transform.scale(self.highlighting,self.pieces_size)
                                self.screen.blit(self.highlighting, (x, y))
                self.game_over_by_time()
                self.palyer_wants_to_resign()
                self.game_over()


            elif self.flip_board == True:
                resized_black_board = pygame.transform.scale(self.black_board,(640,640))
                self.screen.blit(resized_black_board,(0,0))
                self.the_game_is_on()
                for square in range(64):
                     #this prints all the piece to there places in order
                     piece = self.legal.board.piece_at(square)
                     if piece is not None:
                        symbol = piece.symbol()
                        if symbol in self.piece_image:
                            x, y = self.black_screen_coordinates(square)
                            pygame.transform.scale(self.piece_image[symbol],self.pieces_size)
                            self.screen.blit(self.piece_image[symbol], (x, y))
                    #where this prints all the highlighting moves that you can play when you select a piece 
                     if self.selected is not None:
                        for move in self.legal.board.legal_moves:
                            if move.from_square == self.selected:
                                target_square = move.to_square
                                x, y = self.black_highlight(target_square)
                                pygame.transform.scale(self.highlighting,self.pieces_size)
                                self.screen.blit(self.highlighting, (x, y))
                self.game_over()
                self.palyer_wants_to_resign()
                self.game_over()


            pygame_widgets.update(event) 
            #if self.sitting_on == True:
            #    pygame.draw.rect(self.screen,(38, 36, 33),(300,300,320,300))
            
            self.sitting_panal()
           
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    chessboard = CHESSGUI()
    chessboard.chessgui()