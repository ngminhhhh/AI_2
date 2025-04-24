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
    
    white_side_btn = pygame.Rect(BOARD_WIDTH + PANEL_MARGIN , HEIGHT // 2 - start_btn_height, start_btn_width, start_btn_height)
    black_side_btn = pygame.Rect(BOARD_WIDTH + PANEL_MARGIN , HEIGHT // 2 + start_btn_height, start_btn_width, start_btn_height)

    level_easy_btn = pygame.Rect(BOARD_WIDTH + PANEL_MARGIN , HEIGHT // 2 - 2 * start_btn_height, start_btn_width, start_btn_height)
    level_medium_btn = pygame.Rect(BOARD_WIDTH + PANEL_MARGIN , HEIGHT // 2, start_btn_width, start_btn_height)
    level_hard_btn = pygame.Rect(BOARD_WIDTH + PANEL_MARGIN , HEIGHT // 2 + 2 * start_btn_height, start_btn_width, start_btn_height)

    restart_btn = pygame.Rect(BOARD_WIDTH + PANEL_MARGIN , (HEIGHT - start_btn_height) // 2, start_btn_width, start_btn_height)    

    started  = False

    return {
        'screen'       : screen,
        'clock'        : clock,
        'font'         : font,
        'white_pieces' : white_pieces,
        'black_pieces' : black_pieces,
        'board'        : board,
        'start_btn_rect': btn_rect,
        'white_side_btn': white_side_btn,
        'black_side_btn': black_side_btn,
        'level_easy_btn': level_easy_btn,
        'level_medium_btn': level_medium_btn,
        'level_hard_btn': level_hard_btn,
        'restart_btn': restart_btn,
        'started'      : started
    }

def draw_piece(screen, pieces):
    for p in pieces:
        px = p.x * SQUARE_SIZE + MARGIN
        py = p.y * SQUARE_SIZE + MARGIN
        screen.blit(p.piece_image, (px, py))

def draw_button(screen, mx, my, btn, font, text):
    color = BTN_HOVER if btn.collidepoint(mx, my) else BTN_COLOR
    pygame.draw.rect(screen, color, btn)
    txt = font.render(text, True, TEXT_COL)
    screen.blit(txt, (btn.x + (start_btn_width - txt.get_width()) // 2, btn.y + (start_btn_height - txt.get_height()) // 2))

def run():
    ctx = init()

    screen       = ctx['screen']
    clock        = ctx['clock']
    font         = ctx['font']
    white_pieces = ctx['white_pieces']
    black_pieces = ctx['black_pieces']
    board        = ctx['board']
    start_btn_rect     = ctx['start_btn_rect']
    started      = ctx['started']
    white_side_btn = ctx['white_side_btn']
    black_side_btn = ctx['black_side_btn']

    level_easy_btn = ctx['level_easy_btn']
    level_medium_btn = ctx['level_medium_btn']
    level_hard_btn = ctx['level_hard_btn']

    restart_btn = ctx["restart_btn"]

    move_delay = 500
    last_move_time = 0
    game_over_msg = None

    running = True

    # * Flag
    begin_state = True
    choose_side_state = False
    choose_level_state = False
    started = False
    restart_state = False

    # * Params
    side = None 
    depth = 0

    # * Handle double click
    last_click_time = 0
    CLICK_COOLDOWN = 200  # ms

    while running:
        mx, my = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                now = pygame.time.get_ticks()
                if now - last_click_time < CLICK_COOLDOWN:
                    continue

                last_click_time = now

                if start_btn_rect.collidepoint(mx, my) and begin_state:
                    begin_state = False
                    choose_side_state = True
                    continue
                
                if choose_side_state:
                    for btn, name in [(white_side_btn, "White"), (black_side_btn, "Black")]:
                        if btn.collidepoint(mx, my):
                            side = name
                            choose_side_state = False
                            choose_level_state = True
                            break

                if choose_level_state:
                    for btn, level in [(level_easy_btn, 1), (level_medium_btn, 2), (level_hard_btn, 3)]:
                        if btn.collidepoint(mx, my):
                            depth = level
                            choose_level_state = False
                            started = True

                            stepper = play_chess(board,
                                    white_pieces,
                                    black_pieces,
                                    depth,
                                    side)
                            
                            last_move_time = pygame.time.get_ticks()
                    
                if restart_state and restart_btn.collidepoint(mx, my):
                    restart_state = False
                    begin_state = True

                    side = None
                    depth = 0

                    restart_all()
                    white_pieces, black_pieces, board   = init_piece(load_piece_images())


        # * Engine render
        if started and pygame.time.get_ticks() - last_move_time >= move_delay:
            try:
                tag, payload = next(stepper)
                if tag == "MOVE":
                    pass
                elif tag == "GAME_OVER":
                    game_over_msg = payload
                    started = False
                    restart_state = True

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

        # * Draw start button
        if begin_state:
            draw_button(screen, mx, my, start_btn_rect, font, "Start")
        
        # * Draw choose side button
        if choose_side_state:
            draw_button(screen, mx, my, white_side_btn, font, "White")
            draw_button(screen, mx, my, black_side_btn, font, "Black")

        # * Draw choose level button
        if choose_level_state:
            draw_button(screen, mx, my, level_easy_btn, font, "Easy")
            draw_button(screen, mx, my, level_medium_btn, font, "Medium")
            draw_button(screen, mx, my, level_hard_btn, font, "Hard")

        # * Draw message and restart button
        if restart_state:
            txt = font.render(game_over_msg, True, TEXT_COL)

            x = BOARD_WIDTH + (PANEL_WIDTH - txt.get_width()) // 2
            y = restart_btn.y - 100  
            
            screen.blit(txt, (x, y))
            draw_button(screen, mx, my, restart_btn, font, "Restart")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()