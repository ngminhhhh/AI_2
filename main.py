from Engine import *
import pygame

SQUARE_SIZE = 80
NUM_SQUARES = 8

WIDTH = SQUARE_SIZE * NUM_SQUARES
HEIGHT = SQUARE_SIZE * NUM_SQUARES

def load_piece_images():
    images = {}
    pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['white', 'black']

    for color in colors:
        for piece in pieces:
            image_path = f"assets/chess_pieces/{color}_{piece}.png"
            image = pygame.image.load(image_path).convert_alpha()

            image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
            images[f"{color}_{piece}"] = image

    return images

def draw_board(screen):
    WHITE_COLOR = (234, 234, 210)
    BLACK_COLOR = (75, 114, 153)

    for row in range(NUM_SQUARES):
        for col in range(NUM_SQUARES):
            rect_x = col * SQUARE_SIZE
            rect_y = row * SQUARE_SIZE

            if (row + col) % 2 == 0:
                color = WHITE_COLOR
            else:
                color = BLACK_COLOR

            rect = pygame.Rect(rect_x, rect_y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

def init():
    images = load_piece_images()

    white_pieces, black_pieces, board = init_piece(piece_images=images)

    return white_pieces, black_pieces, board

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    white_pieces, black_pieces, board = init()

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            draw_board(screen)

            pygame.display.flip()

            clock.tick(60)

    pygame.quit()


    # play_chess(board=board, white_pieces=white_pieces, black_pieces=black_pieces, depth=1)



