import pygame
from pygame.locals import *
import json
import numpy as np

class ChessGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

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

        # Set the font for the text
        self.font = pygame.font.Font(None, 36)

        # Create the chess board
        self.board = [[0 for x in range(8)] for y in range(8)]
        self.board_piece_pos = [[0 for x in range(8)] for y in range(8)]

        # Set up other game-related variables
        self.clock = pygame.time.Clock()
        self.running = True

        # Load piece file dictionary
        self.piece_file_dict = None
        with open('piece_dict.json') as f:
            self.piece_file_dict = json.load(f)

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

    def init(self):
        # Draw the chess board
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    self.board[row][col] = self.GREEN
                else:
                    self.board[row][col] = self.L_GREEN

    def make_UI_and_place_piece(self):

        for row in range(8):
            for col in range(8):
                pygame.draw.rect(
                    self.screen, self.board[row][col], [col * self.WIDTH / 8, row * self.HEIGHT / 8, self.WIDTH / 8, self.HEIGHT / 8]
                )

        # Placing the pieces on the chess board
        row_, col_ = 0, 0
        for i in self.PIECE_INFO:
            if i == '/':
                row_ += 1
            elif i in '12345678'.split():
                col_ += int(i)
            else:
                piece_img = pygame.image.load(self.piece_file_dict[i])
                img_copy = piece_img.copy()
                alpha = 255
                img_copy.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
                img_width = piece_img.get_width()
                self.screen.blit(
                    img_copy,
                    (
                        col_ * self.WIDTH / 8 + self.WIDTH / 16 - self.IMG_SIZE / 2,
                        row_ * self.HEIGHT / 8 + self.HEIGHT / 16 - self.IMG_SIZE / 2,
                    ),
                )
                self.board_piece_pos[row_][col_] = i
                col_ += 1
                if col_ >= 8:
                    col_ = 0

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
        if piece!= 0:
            rect = (
                    self.BOARD_POS[0] + x * self.WIDTH / 8,
                    self.BOARD_POS[1] + y * self.HEIGHT / 8,
                    self.WIDTH / 8,
                    self.HEIGHT / 8,
                )
            pygame.draw.rect(self.screen, (255, 0, 0, 50), rect, 2)

    def draw_dragging_cursor(self, screen, board, selected_piece):
        if selected_piece:
            piece, x, y = self.get_square_under_mouse()
            # print(x,y)
            if x is not None:
                rect = (
                    self.BOARD_POS[0] + x * self.WIDTH / 8,
                    self.BOARD_POS[1] + y * self.HEIGHT / 8,
                    self.WIDTH / 8,
                    self.HEIGHT / 8,
                )
                pygame.draw.rect(self.screen, (0, 250, 0, 50), rect, 2)
            pygame.draw.line(screen, 
                            pygame.Color('red'),
                            (self.BOARD_POS[0] + selected_piece[1] * self.WIDTH / 8 +self.WIDTH/16,self.BOARD_POS[0] + selected_piece[2] * self.WIDTH / 8 +self.WIDTH/16), 
                            (rect[0]+self.WIDTH/16, rect[1]+self.WIDTH/16),
                            5)

            



    def run(self):
        selected_piece = None
        drop_pos = None
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == MOUSEBUTTONDOWN:
                    # if piece != 0:
                    #     selected_piece = (piece, x, y)
                    piece, x, y = self.get_square_under_mouse()
                    if piece!=0:
                        selected_piece = (piece, x, y)
                        # print(selected_piece)
                    

                elif event.type == MOUSEBUTTONUP:
                    pass
                            
                
                elif event.type == MOUSEMOTION:
                    pass

            # piece, x, y = self.get_square_under_mouse()
            self.screen.fill(self.WHITE)
            self.make_UI_and_place_piece()
            if selected_piece:
                self.draw_selected(self.screen, selected_piece[0], selected_piece[1], selected_piece[2])
                self.draw_dragging_cursor(self.screen, self.board_piece_pos, selected_piece)

            

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    chess_game = ChessGame()
    chess_game.run()
