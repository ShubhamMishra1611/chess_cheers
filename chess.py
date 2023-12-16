import pygame
from pygame.locals import *
import json
import numpy as np
import chess_initial
from chess_piece import rook, bishop, knight, pawn, queen, king, chess_piece
import copy

class ChessGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        self.white_or_black = 1 # 0 : white and 1 : black

        # Set the dimensions of the board
        self.WIDTH = 800
        self.HEIGHT = 800
        self.IMG_SIZE = 60
        self.BOARD_POS = (0, 0)

        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.GREEN = (115, 144, 83)
        self.L_GREEN = (230, 231, 202)
        self.BLUE = (0, 0, 223)
        self.RED = (223, 15, 0)

        self.player_side = 0 # 0 : white and 1 : black
        self.king_check = [False, 0, 0]

        # Set the font for the text
        self.font = pygame.font.Font(None, 36)

        # Create the chess board
        self.board = [[0 for x in range(8)] for y in range(8)]
        # self.board_piece_pos = [[0 for x in range(8)] for y in range(8)]
        # self.board_piece_pos = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
        #                         ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
        #                         [0, 0, 0, 0, 0, 0, 0, 0], 
        #                         [0, 0, 0, 0, 0, 0, 0, 0], 
        #                         [0, 0, 0, 0, 0, 0, 0, 0], 
        #                         [0, 0, 0, 0, 0, 0, 0, 0], 
        #                         ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
        #                         ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        self.board_piece_pos = self.get_pieces()
        

        # Set up other game-related variables
        self.clock = pygame.time.Clock()
        self.running = True

        # Load piece file dictionary
        # self.piece_file_dict = None
        # with open('piece_dict.json') as f:
        #     self.piece_file_dict = json.load(f)
        # self.piece_file_dict = self.piece_file_dict[str(self.player_side)]

        # Set the side the user is playing
        self.USER_SIDE = 0  # {0: White, 1: Black}

        # Set up piece information
        self.PIECE_INFO = 'rnbqkbnr/pppppppp/////PPPPPPPP/RNBQKBNR'
        self.chess = np.zeros((8, 8), dtype=np.int8)

        # Set up the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess Board")

        # Initialize the chess game
        self.init()
        self.make_UI_and_place_piece()

    def get_pieces(self)->list[list[chess_piece]]:
        # return chess_initial.board_white
        if self.player_side == 0:
            return chess_initial.board_white
        else:
            return chess_initial.board_black

    def init(self):
        # Draw the chess board
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    self.board[row][col] = self.GREEN
                else:
                    self.board[row][col] = self.L_GREEN

    def make_UI_and_place_piece(self):
        # make the board
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(
                    self.screen, self.board[row][col], 
                    [
                        col * self.WIDTH / 8, 
                        row * self.HEIGHT / 8, 
                        self.WIDTH / 8, 
                        self.HEIGHT / 8
                    ]
                )

        for row in range(8):
            for col in range(8):
                target_piece = self.board_piece_pos[row][col]
                if target_piece!=None:
                    piece_img = pygame.image.load(target_piece.img_file)
                    img_copy = piece_img.copy()
                    alpha = 255
                    img_copy.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
                    self.screen.blit(
                        img_copy,
                        (
                            col * self.WIDTH / 8 + self.WIDTH / 16 - self.IMG_SIZE / 2,
                            row * self.HEIGHT / 8 + self.HEIGHT / 16 - self.IMG_SIZE / 2,
                        ),
                    )



        pygame.display.flip()

    def get_square_under_mouse(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        x, y = [int(v // (self.WIDTH / 8)) for v in mouse_pos]
        try:
            if x >= 0 and y >= 0:
                return self.board_piece_pos[y][x], x, y
        except IndexError:
            pass
        return None, None, None
    
    def draw_selected(self, screen, piece, x, y):
        if piece!= None:
            rect = (
                    self.BOARD_POS[0] + x * self.WIDTH / 8,
                    self.BOARD_POS[1] + y * self.HEIGHT / 8,
                    self.WIDTH / 8,
                    self.HEIGHT / 8,
                )
            pygame.draw.rect(self.screen, (255, 0, 0, 50), rect, 5)

    def draw_dragging_cursor(self, screen, board, selected_piece):
        if selected_piece:
            piece, x, y = self.get_square_under_mouse()
            if x is not None :
                if x != selected_piece[1] or  y!=selected_piece[2]: 
                    rect = (
                        self.BOARD_POS[0] + x * self.WIDTH / 8,
                        self.BOARD_POS[1] + y * self.HEIGHT / 8,
                        self.WIDTH / 8,
                        self.HEIGHT / 8,
                    )
                    pygame.draw.rect(self.screen, (0, 250, 0, 50), rect, 5)
                    pygame.draw.line(screen, 
                                    pygame.Color('red'),
                                    (self.BOARD_POS[0] + selected_piece[1] * self.WIDTH / 8 +self.WIDTH/16,self.BOARD_POS[0] + selected_piece[2] * self.WIDTH / 8 +self.WIDTH/16), 
                                    (rect[0]+self.WIDTH/16, rect[1]+self.WIDTH/16),
                                    5)

    def recommend_valid_moves(self, screen, selected_piece, look_for_check = True, board = None):
        # this function will return x, y of valid moves
        # TODO: Update all moves to check if king is in check
        if selected_piece is None:
            return None
        
        if board == None:
            board = self.board_piece_pos

        piece, x, y = selected_piece
        moves = [] # see what is moves it is nothing but a list of valid moves. Now question is what is move, it is nothing
                   # but a tuple of (x, y, 1|0) x and y are coordinate while 1|0 determine if this moves takes n takes n takes n takes
        all_moves = piece.valid_moves(x, y)
        if piece.name in ['rook', 'bishop', 'queen']: 
            # these guys are just awesome         
            for direction in all_moves:
                for j, i in direction:
                    if board[j][i] == None:
                        moves.append((i, j, 0))
                    elif board[j][i].color != piece.color:
                        moves.append((i, j, 1))
                        break
                    elif board[j][i].color == piece.color:
                        break

        elif piece.name == 'knight':
            # knight is weird, he will fork you
            
            for j, i in all_moves:
                if 0 <= i < 8 and 0 <= j < 8:
                    target_piece = board[j][i] 
                    if target_piece == None:
                        moves.append((i, j, 0))
                    elif target_piece.color != piece.color:
                        moves.append((i, j, 1))

        elif piece.name == 'king':
            # king is the weakest guy, you lose him, you lose it.
            # anyways so make the guy move everywhere and see where he can go, I will leave checkmate and castle for now
            # TODO: look for checkmate and castle
            for j, i in all_moves:
                if 0 <= i < 8 and 0 <= j < 8:
                    target_piece = board[j][i] 
                    if target_piece == None:
                        moves.append((i, j, 0))
                    elif target_piece.color != piece.color:
                        moves.append((i, j, 1))
        elif piece.name == 'pawn':
            # since this stupid piece only moves in one direction then lets look if it is black or white

            #  player    color    direction
            # 0 0 -1
            # 0 1 1
            # 1 0 1
            # 1 1 -1
            # direction is -1 when piece color and player color is same
            # direction is 1 when piece color and player color is different
            if piece.color == self.player_side:
                direction = -1
            else:
                direction = 1
            piece.direction = direction
            
            if board[y+direction][x] == None: # my soldiers move forward
                moves.append((x, y+direction, 0))
                if (direction == -1 and y == 6) or (direction == 1 and y == 1): 
                    if board[y+2*direction][x] == None: # my soldier rage
                        moves.append((x, y+2*direction, 0))

            for dx in [-1, 1]:
                new_x = x+dx
                new_y = y+direction
                
                if 0<=new_x <8 and 0<=new_y<8:
                    target_piece = board[new_y][new_x]
                    if target_piece!=None and target_piece.color!=piece.color:
                        moves.append((new_x, new_y, 1))
        if look_for_check == True:
            moves_copy = copy.deepcopy(moves)
            # take each move
            # now get the moves for opposite side piece
            # check if any move of there has our king in attack
            for move in moves:
                copy_board = copy.deepcopy(self.board_piece_pos)
            
                copy_board[move[1]][move[0]] = piece
                copy_board[y][x] = None
                for j in range(8):
                    for i in range(8):
                        oppo_piece = copy_board[j][i]
                        if oppo_piece is None:
                            continue
                        if oppo_piece.color != piece.color:
                            possible_moves = self.recommend_valid_moves(self.screen, (oppo_piece, i, j), False, copy_board)
                            for new_moves in possible_moves:
                                if new_moves[2] == 1:
                                    target_cell = copy_board[new_moves[1]][new_moves[0]]
                                    if target_cell.name == 'king':
                                        moves_copy.remove(move)
            return moves_copy 
        return moves
        # TODO: en passant 

    def draw_valid_moves(self, moves):
        if moves is not None:
            for x, y, i in moves:
                pygame.draw.circle(
                    self.screen,
                    self.BLUE if i == 0 else self.RED,
                    (
                        self.BOARD_POS[0] + x * self.WIDTH / 8 + self.WIDTH / 16, 
                        self.BOARD_POS[1] + y * self.HEIGHT / 8 + self.HEIGHT / 16
                    ),
                    10
                )


    def make_king_check_rect(self, x, y):
        pygame.draw.rect(
            self.screen,
            self.BLACK,
            (
                x,
                y,
                self.WIDTH / 8,
                self.HEIGHT / 8,
            ),
            10
        )


      
    def check_king_check(self, color:0|1):
        for j in range(8):
            for i in range(8):
                oppo_piece = self.board_piece_pos[j][i]
                if oppo_piece is None:
                    continue
                if oppo_piece.color != color:
                    possible_moves = self.recommend_valid_moves(self.screen, (oppo_piece, i, j), False)
                    for new_moves in possible_moves:
                        if new_moves[2] == 1:
                            target_cell = self.board_piece_pos[new_moves[1]][new_moves[0]]
                            if target_cell.name == 'king':
                                target_cell.in_check = True
                                return (True, new_moves[0]*self.WIDTH/8, new_moves[1]*self.HEIGHT/8)
        return (False, 0, 0)
                        

    def run(self):
        selected_piece = None
        moves = None
        while self.running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == MOUSEBUTTONUP:
                    _, cur_x, cur_y = self.get_square_under_mouse()
                    if selected_piece:
                        piece, x, y = selected_piece
                        if x != cur_x or  y!=cur_y:
                            self.board_piece_pos[cur_y][cur_x] = piece
                            print(f'{piece.name} from ({x}, {y}) to ({cur_x}, {cur_y})')
                            print("Now it is turn of ", self.white_or_black)
                            self.white_or_black = (self.white_or_black + 1) % 2
                            # moves = self.recommend_valid_moves(self.screen, (piece, cur_x, cur_y))
                            # # print("possible moves are : ", moves)
                            # for move in moves:
                            #     if move[2]==1:
                            #         target_cell = self.board_piece_pos[move[1]][move[0]]
                            #         # print("target cell is :", target_cell)
                            #         if target_cell.name == 'king':
                            #             target_cell.in_check = True
                            #             print(target_cell.color, target_cell.in_check)
                            #             break
                            # moves = None
                            self.board_piece_pos[y][x] = None
                            selected_piece = None
                        else:
                            pass

                elif event.type == MOUSEBUTTONDOWN:
                    piece, x, y = self.get_square_under_mouse()
                    if piece!=None and selected_piece is None:
                        selected_piece = (piece, x, y)
                        moves = self.recommend_valid_moves(self.screen, selected_piece)
                        # print(moves)
                    elif selected_piece is not None:
                        # check if selected cell comes in valid move
                        valid_move_or_not = lambda x, y: any(t[0]==x and t[1]==y for t in moves)
                        # checking_check = self.check_king_check(piece)
                        # if not checking_check: # this means this move will cause own king to go in check hence invalid move
                        #     selected_piece = None
                        # if checking_check is None:
                        #     pass
                        if not valid_move_or_not(x, y):
                            selected_piece = None
                        else:
                            if selected_piece[0].name == 'pawn':
                                if (selected_piece[0].direction == 1 and y == 7) or (selected_piece[0].direction == -1 and y == 0):
                                    self.board_piece_pos[y][x] = queen(selected_piece[0].color)
                                    self.board_piece_pos[selected_piece[2]][selected_piece[1]] = None
                                    selected_piece = None
                            # pass
                        # if not (x!=selected_piece[1] or y!=selected_piece[2]):
                        #     selected_piece = None
                        # else:
                        #     if selected_piece[0].name == 'pawn': # checking for promotion
                        #         if (selected_piece[0].direction == 1 and y == 7) or (selected_piece[0].direction == -1 and y == 0):
                        #             self.board_piece_pos[y][x] = queen(selected_piece[0].color)
                        #             self.board_piece_pos[selected_piece[2]][selected_piece[1]] = None
                        #             selected_piece = None
                            
                
                elif event.type == MOUSEMOTION:
                    pass

            self.screen.fill(self.WHITE)
            self.make_UI_and_place_piece()
            check_check = self.check_king_check((self.white_or_black+1)%2)
            if check_check[0]:
                self.make_king_check_rect(check_check[1], check_check[2])
            if selected_piece:
                self.draw_selected(self.screen, selected_piece[0], selected_piece[1], selected_piece[2])
                self.draw_dragging_cursor(self.screen, self.board_piece_pos, selected_piece)
                self.draw_valid_moves(moves)
            else:
                _, x, y = self.get_square_under_mouse()
                if x is not None :
                    rect = (
                        self.BOARD_POS[0] + x * self.WIDTH / 8,
                        self.BOARD_POS[1] + y * self.HEIGHT / 8,
                        self.WIDTH / 8,
                        self.HEIGHT / 8,
                    )
                    pygame.draw.rect(self.screen, (0, 250, 0, 50), rect, 5)

            

            pygame.display.flip()
            self.clock.tick(1000)

        pygame.quit()


if __name__ == "__main__":
    chess_game = ChessGame()
    chess_game.run()
