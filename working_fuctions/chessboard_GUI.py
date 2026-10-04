import chess
import pygame

class CHESSGUI:
    def __init__(self):
        self.board = chess.Board()
        self.pieces_size = 70,70
        self.borad_size =  640,640
        self.square_size = 80
        self.offset = 5
        self.w_pawn1_pos = 8
        self.w_pawn2_pos = 9
        self.w_pawn3_pos = 10
        self.w_pawn4_pos = 11
        self.w_pawn5_pos = 12
        self.w_pawn6_pos = 13
        self.w_pawn7_pos = 14
        self.w_pawn8_pos = 15

        self.b_pawn1_pos = 48
        self.b_pawn2_pos = 49
        self.b_pawn3_pos = 50
        self.b_pawn4_pos = 51
        self.b_pawn5_pos = 52
        self.b_pawn6_pos = 53
        self.b_pawn7_pos = 54
        self.b_pawn8_pos = 55




        self.selected = None


    def chess_legal_moves(self,input):
        move = chess.Move.from_uci(input)
        if move in self.board.legal_moves:
            self.board.push(move)
            to_move = move.to_square
            return to_move
        return None
    
    def screen_coordinates(self,square):

        col = chess.square_file(square)
        row = chess.square_rank(square)

        x_coordinates =  self.offset + (col * self.square_size)
        y_coordinates = self.offset + ((7 - row) * self.square_size)

        return x_coordinates,y_coordinates
    
    def move_from(self,x_mouse,y_mouse):
        
          x_mouse_coordinates =  (x_mouse // self.square_size)
          y_mouse_coordinates = 7 - (y_mouse // self.square_size)


          from_square = chess.square(x_mouse_coordinates,y_mouse_coordinates)
        
          return from_square
    
    def handal_checkes(self,mx,my):
        checked_square = self.move_from(mx,my)
        if self.selected is None:
            piece = self.board.piece_at(checked_square)
            if piece is not None:
                self.selected = checked_square
            else:
                print("there is no piece stupid")
        else:
            fro_squre = chess.square_name(self.selected)
            to_squre = chess.square_name(checked_square)
            get_uni_move = fro_squre + to_squre
            to_move = self.chess_legal_moves(get_uni_move)
            self.selected = None
            return to_move







    
    def chessgui(self):
        
        pygame.init()
        screen = pygame.display.set_mode((self.borad_size))
        clock = pygame.time.Clock()
        running = True

        my_board = pygame.image.load("Screenshot 2026-10-03 191504.png").convert_alpha()
        w_pawn1 = pygame.image.load("Chess_plt60.png").convert_alpha()
        w_pawn2 = pygame.image.load("Chess_plt60.png").convert_alpha()
        w_pawn3 = pygame.image.load("Chess_plt60.png").convert_alpha()
        w_pawn4 = pygame.image.load("Chess_plt60.png").convert_alpha()
        w_pawn5 = pygame.image.load("Chess_plt60.png").convert_alpha()
        w_pawn6 = pygame.image.load("Chess_plt60.png").convert_alpha()
        w_pawn7 = pygame.image.load("Chess_plt60.png").convert_alpha()
        w_pawn8 = pygame.image.load("Chess_plt60.png").convert_alpha()

        b_pawn1 = pygame.image.load("Chess_pdt60.png").convert_alpha()
        b_pawn2 = pygame.image.load("Chess_pdt60.png").convert_alpha()
        b_pawn3 = pygame.image.load("Chess_pdt60.png").convert_alpha()
        b_pawn4 = pygame.image.load("Chess_pdt60.png").convert_alpha()
        b_pawn5 = pygame.image.load("Chess_pdt60.png").convert_alpha()
        b_pawn6 = pygame.image.load("Chess_pdt60.png").convert_alpha()
        b_pawn7 = pygame.image.load("Chess_pdt60.png").convert_alpha()
        b_pawn8 = pygame.image.load("Chess_pdt60.png").convert_alpha()




        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    to_move = self.handal_checkes(mx,my)
                    if to_move is not None:
                        self.w_pawn1_pos = to_move


            w_pawn1_x, w_pawn1_y = self.screen_coordinates(self.w_pawn1_pos)
            w_pawn2_x, w_pawn2_y = self.screen_coordinates(self.w_pawn2_pos)
            w_pawn3_x, w_pawn3_y = self.screen_coordinates(self.w_pawn3_pos)
            w_pawn4_x, w_pawn4_y = self.screen_coordinates(self.w_pawn4_pos)
            w_pawn5_x, w_pawn5_y = self.screen_coordinates(self.w_pawn5_pos)
            w_pawn6_x, w_pawn6_y = self.screen_coordinates(self.w_pawn6_pos)
            w_pawn7_x, w_pawn7_y = self.screen_coordinates(self.w_pawn7_pos)
            w_pawn8_x, w_pawn8_y = self.screen_coordinates(self.w_pawn8_pos)


            b_pawn1_x, b_pawn1_y = self.screen_coordinates(self.b_pawn1_pos)
            b_pawn2_x, b_pawn2_y = self.screen_coordinates(self.b_pawn2_pos)
            b_pawn3_x, b_pawn3_y = self.screen_coordinates(self.b_pawn3_pos)
            b_pawn4_x, b_pawn4_y = self.screen_coordinates(self.b_pawn4_pos)
            b_pawn5_x, b_pawn5_y = self.screen_coordinates(self.b_pawn5_pos)
            b_pawn6_x, b_pawn6_y = self.screen_coordinates(self.b_pawn6_pos)
            b_pawn7_x, b_pawn7_y = self.screen_coordinates(self.b_pawn7_pos)
            b_pawn8_x, b_pawn8_y = self.screen_coordinates(self.b_pawn8_pos)



                    

            screen.fill((0, 0, 0))
            t_my_board = pygame.transform.scale(my_board,self.borad_size)
            w_size_of_pawn1 = pygame.transform.scale(w_pawn1,self.pieces_size)
            w_size_of_pawn2 = pygame.transform.scale(w_pawn2,self.pieces_size)
            w_size_of_pawn3 = pygame.transform.scale(w_pawn3,self.pieces_size)
            w_size_of_pawn4 = pygame.transform.scale(w_pawn4,self.pieces_size)
            w_size_of_pawn5 = pygame.transform.scale(w_pawn5,self.pieces_size)
            w_size_of_pawn6 = pygame.transform.scale(w_pawn6,self.pieces_size)
            w_size_of_pawn7 = pygame.transform.scale(w_pawn7,self.pieces_size)
            w_size_of_pawn8 = pygame.transform.scale(w_pawn8,self.pieces_size)

            b_size_of_pawn1 = pygame.transform.scale(b_pawn1,self.pieces_size)
            b_size_of_pawn2 = pygame.transform.scale(b_pawn2,self.pieces_size)
            b_size_of_pawn3 = pygame.transform.scale(b_pawn3,self.pieces_size)
            b_size_of_pawn4 = pygame.transform.scale(b_pawn4,self.pieces_size)
            b_size_of_pawn5 = pygame.transform.scale(b_pawn5,self.pieces_size)
            b_size_of_pawn6 = pygame.transform.scale(b_pawn6,self.pieces_size)
            b_size_of_pawn7 = pygame.transform.scale(b_pawn7,self.pieces_size)
            b_size_of_pawn8 = pygame.transform.scale(b_pawn8,self.pieces_size)

            screen.blit(t_my_board,(0,0))
            screen.blit(w_size_of_pawn1,(w_pawn1_x,w_pawn1_y))
            screen.blit(w_size_of_pawn2,(w_pawn2_x,w_pawn2_y))
            screen.blit(w_size_of_pawn3,(w_pawn3_x,w_pawn3_y))
            screen.blit(w_size_of_pawn4,(w_pawn4_x,w_pawn4_y))
            screen.blit(w_size_of_pawn5,(w_pawn5_x,w_pawn5_y))
            screen.blit(w_size_of_pawn6,(w_pawn6_x,w_pawn6_y))
            screen.blit(w_size_of_pawn7,(w_pawn7_x,w_pawn7_y))
            screen.blit(w_size_of_pawn8,(w_pawn8_x,w_pawn8_y))

            screen.blit(b_size_of_pawn1,(b_pawn1_x,b_pawn1_y))
            screen.blit(b_size_of_pawn2,(b_pawn2_x,b_pawn2_y))
            screen.blit(b_size_of_pawn3,(b_pawn3_x,b_pawn3_y))
            screen.blit(b_size_of_pawn4,(b_pawn4_x,b_pawn4_y))
            screen.blit(b_size_of_pawn5,(b_pawn5_x,b_pawn5_y))
            screen.blit(b_size_of_pawn6,(b_pawn6_x,b_pawn6_y))
            screen.blit(b_size_of_pawn7,(b_pawn7_x,b_pawn7_y))
            screen.blit(b_size_of_pawn8,(b_pawn8_x,b_pawn8_y))
            pygame.display.flip()
            clock.tick(60)




    
chessboard = CHESSGUI()
chessboard.chessgui()



        