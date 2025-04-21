from Engine import *
import pygame

# * Configuration 
SQUARE_SIZE     = 80
NUM_SQUARES     = 8
BOARD_WIDTH     = SQUARE_SIZE * NUM_SQUARES
BOARD_HEIGHT    = SQUARE_SIZE * NUM_SQUARES

PANEL_WIDTH     = 400
PANEL_MARGIN    = 0.1 * PANEL_WIDTH

WIDTH, HEIGHT   = BOARD_WIDTH + PANEL_WIDTH, BOARD_HEIGHT

# - Color
WHITE     = (234, 234, 210)
BLACK     = (75, 114, 153)
PANEL_BG  = (50, 50, 50)
BTN_COLOR = (100, 200, 100)
BTN_HOVER = (120, 220, 120)
TEXT_COL  = (255, 255, 255)

PIECE_SCALE = 0.7
PIECE_SIZE  = int(SQUARE_SIZE * PIECE_SCALE)
MARGIN      = (SQUARE_SIZE - PIECE_SIZE) // 2

start_btn_width = PANEL_WIDTH - PANEL_MARGIN * 2
start_btn_height = 50

BOX_WIDTH = 500
BOX_HEIGHT = 300

def load_piece_images():
    images = {}
    pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['white', 'black']

    for color in colors:
        for piece in pieces:
            image_path = f"assets/chess_pieces/{color}_{piece}.png"
            img = pygame.image.load(image_path).convert_alpha()

            images[f"{color}_{piece}"] = pygame.transform.smoothscale(img, (PIECE_SIZE, PIECE_SIZE))

    return images

def init():
    pygame.init()

    screen  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    clock   = pygame.time.Clock()

    font    = pygame.font.SysFont('Ubuntu', 24)

    piece_images    = load_piece_images()
    white_pieces, black_pieces, board   = init_piece(piece_images)

    btn_rect = pygame.Rect(BOARD_WIDTH + PANEL_MARGIN , (HEIGHT - start_btn_height) // 2, start_btn_width, start_btn_height)
    started  = False

    return {
        'screen'       : screen,
        'clock'        : clock,
        'font'         : font,
        'white_pieces' : white_pieces,
        'black_pieces' : black_pieces,
        'board'        : board,
        'btn_rect'     : btn_rect,
        'started'      : started
    }

def draw_piece(screen, pieces):
    for p in pieces:
        px = p.x * SQUARE_SIZE + MARGIN
        py = p.y * SQUARE_SIZE + MARGIN
        screen.blit(p.piece_image, (px, py))

def run():
    ctx = init()

    screen       = ctx['screen']
    clock        = ctx['clock']
    font         = ctx['font']
    white_pieces = ctx['white_pieces']
    black_pieces = ctx['black_pieces']
    board        = ctx['board']
    btn_rect     = ctx['btn_rect']
    started      = ctx['started']

    move_delay = 500
    last_move_time = 0
    game_over_msg = None

    running = True

    while running:
        mx, my = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if btn_rect.collidepoint(mx, my) and not started:
                    started = True

                    stepper = play_chess(board,
                            white_pieces,
                            black_pieces,
                            depth=2)
                    
                    last_move_time = pygame.time.get_ticks()

                    print("On click")

        # * Engine render
        if started and pygame.time.get_ticks() - last_move_time >= move_delay:
            try:
                tag, payload = next(stepper)
                if tag == "MOVE":
                    pass
                elif tag == "GAME_OVER":
                    game_over_msg = payload
                    started = False

                last_move_time = pygame.time.get_ticks()

            except StopIteration:
                started = False

        # * Draw board
        for r in range(NUM_SQUARES):
            for c in range(NUM_SQUARES):
                color = WHITE if (r + c) % 2 == 0 else BLACK
                rect = (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, color, rect)

        # * Draw chess piece
        draw_piece(screen, white_pieces)
        draw_piece(screen, black_pieces)

        # * Draw sidebar
        pygame.draw.rect(screen, PANEL_BG, (BOARD_WIDTH, 0, PANEL_WIDTH, HEIGHT))
        title_surf = font.render("CHESS info", True, TEXT_COL)
        screen.blit(title_surf, (BOARD_WIDTH + 30, 10))

        # * Draw start button
        btn_color = BTN_HOVER if btn_rect.collidepoint(mx, my) else BTN_COLOR
        pygame.draw.rect(screen, btn_color, btn_rect)

        txt = font.render("Start", True, TEXT_COL)
        screen.blit(txt, (btn_rect.x + (start_btn_width - txt.get_width()) // 2, btn_rect.y + (start_btn_height - txt.get_height()) // 2))

        if game_over_msg:
            box = pygame.Rect((WIDTH - BOX_WIDTH) // 2 , (HEIGHT - BOX_HEIGHT) // 2, BOX_WIDTH, BOX_HEIGHT)
            pygame.draw.rect(screen, PANEL_BG, box)
            txt_info = font.render(payload, True, TEXT_COL)
            screen.blit(txt_info, (box.x + (BOX_WIDTH - txt_info.get_width()) // 2, box.y + (BOX_HEIGHT - txt_info.get_height()) // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()