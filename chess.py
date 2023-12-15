import pygame
import numpy as np
import json
from PIL import Image
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (115,144,83)
L_GREEN = (230,231,202)

# Set the dimensions of the board
WIDTH = 800
HEIGHT = 800
IMG_SIZE = 60
BOARD_POS = (0, 0)

#Defining which side user is playing
USER_SIDE = 0 # {0: White, 1:Black}
# I will use string for representing piece position information, 
# Capital letters are for white and small are for black
# numbers denote skipping between piece in row
# / denotes skip to next row
# Piece code: R-rook, B-bishop, N-knight, Q-Queen, K-king, P-pawn
PIECE_INFO = 'rnbqkbnr/pppppppp/////PPPPPPPP/RNBQKBNR'
chess = np.zeros((8,8), dtype = np.int8)

# Initialize Pygame
pygame.init()

# Set the size of the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title of the window
pygame.display.set_caption("Chess Board")

# Set the font for the text
font = pygame.font.Font(None, 36)

# Create the chess board
board = [[0 for x in range(8)] for y in range(8)]
board_piece_pos = [[0 for x in range(8)] for y in range(8)]
for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            board[row][col] = GREEN
        else:
            board[row][col] = L_GREEN

# Draw the chess board
for row in range(8):
    for col in range(8):
        pygame.draw.rect(screen, board[row][col], [col * WIDTH/8, row * HEIGHT/8, WIDTH/8, HEIGHT/8])

def get_square_under_mouse(board):
    mouse_pos =  pygame.Vector2(pygame.mouse.get_pos())
    x, y = [int(v//(WIDTH/8)) for v in mouse_pos]
    print(x,y)
    try:
        if x>=0 and y>=0: return (board[y][x], x, y)
    except IndexError: pass
    return None, None, None


str_idx = 0
row_, col_ = 0, 0
piece_file_dict = None
f = open('piece_dict.json')
piece_file_dict = json.load(f)
f.close()
# placing the pieces on the chess board
for i in PIECE_INFO:
    if i == '/':
        row_+=1
    elif i in '12345678'.split():
        col_+=int(i)
    else:
        piece_img = pygame.image.load(piece_file_dict[i])
        img_copy = piece_img.copy()
        alpha = 255
        img_copy.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        img_width = piece_img.get_width()
        screen.blit(img_copy, (col_ * WIDTH/8 + WIDTH/16 - IMG_SIZE/2, row_ * HEIGHT/8 + HEIGHT/16 - IMG_SIZE/2))
        board_piece_pos[row_][col_] = i
        col_ += 1
        if col_ >=8:
            col_ = 0

clock = pygame.time.Clock()
# Update the screen
pygame.display.flip()

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == MOUSEBUTTONUP:
            # print("it way down")
            pass

        elif event.type == MOUSEBUTTONUP:
            pass# print("Button up")
        
        elif event.type == MOUSEMOTION:
            pass #print("moving")
    piece, x, y = get_square_under_mouse(board_piece_pos)
    screen.fill((255, 255, 255))
    for row in range(8):
        for col in range(8):
            pygame.draw.rect(screen, board[row][col], [col * WIDTH/8, row * HEIGHT/8, WIDTH/8, HEIGHT/8])

    if x!= None:
        rect = (BOARD_POS[0]+x*WIDTH/8, BOARD_POS[1]+y*HEIGHT/8, WIDTH/8, HEIGHT/8)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)
        # print(f'{piece}, {x}, {y}')
    pygame.display.flip()
    clock.tick(60)
    # screen.blit(screen, (0,0))


# Quit Pygame   
pygame.quit()
