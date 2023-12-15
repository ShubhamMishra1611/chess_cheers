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
        self.BLUE = (0, 0, 223)
        self.RED = (223, 15, 0)

        self.player_side = 0 # 0 : white and 1 : black

        # Set the font for the text
        self.font = pygame.font.Font(None, 36)

        # Create the chess board
        self.board = [[0 for x in range(8)] for y in range(8)]
        # self.board_piece_pos = [[0 for x in range(8)] for y in range(8)]
        self.board_piece_pos = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
                                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
                                [0, 0, 0, 0, 0, 0, 0, 0], 
                                [0, 0, 0, 0, 0, 0, 0, 0], 
                                [0, 0, 0, 0, 'k', 0, 0, 0], 
                                [0, 0, 0, 0, 0, 0, 0, 0], 
                                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
                                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        

        # Set up other game-related variables
        self.clock = pygame.time.Clock()
        self.running = True

        # Load piece file dictionary
        self.piece_file_dict = None
        with open('piece_dict.json') as f:
            self.piece_file_dict = json.load(f)
        self.piece_file_dict = self.piece_file_dict[str(self.player_side)]

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
                if self.board_piece_pos[row][col]!=0:
                    piece_img = pygame.image.load(self.piece_file_dict[self.board_piece_pos[row][col]])
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
        if piece!= 0:
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

    def recommend_valid_moves(self, screen, selected_piece):
        # this function will return x, y of valid moves
        if selected_piece is None:
            return None

        piece, x, y = selected_piece
        moves = [] # see what is moves it is nothing but a list of valid moves. Now question is what is move, it is nothing
                   # but a tuple of (x, y, 1|0) x and y are coordinate while 1|0 determine if this moves takes and takes and takes and takes
        if piece.upper() == 'R':
            # rook is very simple so yeah
            # move it to the right
            for i in range(x+1, 8):
                if self.board_piece_pos[y][i] == 0:
                    moves.append((i, y, 0))
                elif self.board_piece_pos[y][i].isupper() != piece.isupper(): # riding on enemy 😏
                    moves.append((i, y, 1))
                    break
                elif self.board_piece_pos[y][i].isupper() == piece.isupper():
                    break
            # move it to the left
            for i in range(x-1, -1, -1):
                if self.board_piece_pos[y][i] == 0:
                    moves.append((i, y, 0))
                elif self.board_piece_pos[y][i].isupper() != piece.isupper(): 
                    moves.append((i, y, 1))
                    break
                elif self.board_piece_pos[y][i].isupper() == piece.isupper():
                    break
            # move it to the top
            for i in range(y+1, 8):
                if self.board_piece_pos[i][x] == 0:
                    moves.append((x, i, 0))
                elif self.board_piece_pos[i][x].isupper() != piece.isupper():
                    moves.append((x, i, 1))
                    break
                elif self.board_piece_pos[i][x].isupper() == piece.isupper():
                    break
            # move it to the bottom
            for i in range(y-1, -1, -1):
                if self.board_piece_pos[i][x] == 0:
                    moves.append((x, i, 0))
                elif self.board_piece_pos[i][x].isupper() != piece.isupper():
                    moves.append((x, i, 1))
                    break
                elif self.board_piece_pos[i][x].isupper() == piece.isupper():
                    break
            return moves
        elif piece.upper() == 'B':
            pass
        elif piece.upper() == 'N':
            pass
        elif piece.upper() == 'K':
            # king is the weakest guy, you lose him, you lose it.
            # anyways so make the guy move everywhere and see where he can go, I will leave checkmate and castle for now
            # TODO: look for checkmate and castle
            moves_pos = [
                [y+1, x],
                [y+1, x+1],
                [y+1, x-1],
                [y-1, x],
                [y-1, x+1],
                [y-1, x-1],
                [y, x-1],
                [y, x+1],
            ]
            for move in moves_pos:
                if self.board_piece_pos[move[0]][move[1]] == 0:
                    moves.append((move[1], move[0], 0))
                elif self.board_piece_pos[move[0]][move[1]].isupper() != piece.isupper():
                    moves.append((move[1], move[0], 1))
                elif self.board_piece_pos[move[0]][move[1]].isupper() == piece.isupper():
                    continue
            return moves
        elif piece.upper() == 'Q':
            pass
        elif piece.upper() == 'P':
            # implement only simple front move

            pass
        return None

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

    def run(self):
        selected_piece = None
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
                            self.board_piece_pos[y][x] = 0
                            selected_piece = None
                        else:
                            pass
                elif event.type == MOUSEBUTTONDOWN:
                    piece, x, y = self.get_square_under_mouse()
                    if piece!=0 and selected_piece is None:
                        selected_piece = (piece, x, y)
                    elif selected_piece is not None: 
                        if not (x!=selected_piece[1] or y!=selected_piece[2]):
                            selected_piece = None
                            
                
                elif event.type == MOUSEMOTION:
                    pass

            self.screen.fill(self.WHITE)
            self.make_UI_and_place_piece()
            if selected_piece:
                self.draw_selected(self.screen, selected_piece[0], selected_piece[1], selected_piece[2])
                self.draw_dragging_cursor(self.screen, self.board_piece_pos, selected_piece)
                moves = self.recommend_valid_moves(self.screen, selected_piece)
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
