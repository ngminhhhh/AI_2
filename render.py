# Importing Modules 
import pygame
import requests
import rembg
from io import BytesIO

# Initialising pygame module
pygame.init()

# Setting Width and height of the Chess Game screen
WIDTH = 1000
HEIGHT = 900

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Chess Game')

font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)

timer = pygame.time.Clock()
fps = 60

# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = []
captured_pieces_black = []

# En passant globals: 
# en_passant_target: ô mà nước bắt tốt qua đường có thể thực hiện
# en_passant_piece: thông tin về con tốt vừa di chuyển 2 ô (tuple: (color, index))
en_passant_target = None
en_passant_piece = None

# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []

black_queen = pygame.image.load('assets/chess_pieces/black_queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))

black_king = pygame.image.load('assets/chess_pieces/black_king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))

black_rook = pygame.image.load('assets/chess_pieces/black_rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))

black_bishop = pygame.image.load('assets/chess_pieces/black_bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))

black_knight = pygame.image.load('assets/chess_pieces/black_knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))

black_pawn = pygame.image.load('assets/chess_pieces/black_pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))

white_queen = pygame.image.load('assets/chess_pieces/white_queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))

white_king = pygame.image.load('assets/chess_pieces/white_king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))

white_rook = pygame.image.load('assets/chess_pieces/white_rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))

white_bishop = pygame.image.load('assets/chess_pieces/white_bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))

white_knight = pygame.image.load('assets/chess_pieces/white_knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))

white_pawn = pygame.image.load('assets/chess_pieces/white_pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

white_images = [white_pawn, white_queen, white_king,
                white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]

black_images = [black_pawn, black_queen, black_king,
                black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small,
                      black_knight_small, black_rook_small, black_bishop_small]

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# check variables/ flashing counter
counter = 0
winner = ''
game_over = False


# draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [
                             600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [
                             700 - (column * 200), row * 100, 100, 100])
    pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
    pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
    pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
    status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                   'Black: Select a Piece to Move!', 'Black: Select a Destination!']
    screen.blit(big_font.render(
        status_text[turn_step], True, 'black'), (20, 820))
    for i in range(9):
        pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
        pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
    screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))


# draw pieces onto board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(
                white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[i]
                                              [0] * 100 + 10, white_locations[i][1] * 100 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(
                black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i]
                                              [0] * 100 + 10, black_locations[i][1] * 100 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                                                  100, 100], 2)


# check functions for each piece remain unchanged ...
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list

def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0),
               (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for dx, dy in targets:
        target = (position[0] + dx, position[1] + dy)
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    moves_list.extend(second_list)
    return moves_list

def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # 4 hướng: up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x, y = 1, -1
        elif i == 1:
            x, y = -1, -1
        elif i == 2:
            x, y = 1, 1
        else:
            x, y = -1, 1
        while path:
            new_pos = (position[0] + chain * x, position[1] + chain * y)
            if new_pos not in friends_list and 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                moves_list.append(new_pos)
                if new_pos in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x, y = 0, 1
        elif i == 1:
            x, y = 0, -1
        elif i == 2:
            x, y = 1, 0
        else:
            x, y = -1, 0
        while path:
            new_pos = (position[0] + chain * x, position[1] + chain * y)
            if new_pos not in friends_list and 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                moves_list.append(new_pos)
                if new_pos in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_pawn(position, color):
    global en_passant_target  # Đưa lệnh này lên đầu hàm
    moves_list = []
    # Lấy các vị trí xung quanh theo hướng di chuyển của tốt
    if color == 'white':
        # Di chuyển thẳng
        if (position[0], position[1] + 1) not in white_locations and \
           (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations and \
           (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        # Bắt đối phương
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        # En passant: nếu có nước en passant (đối với black vừa di chuyển 2 ô)
        if en_passant_target is not None:
            if (position[0] + 1, position[1] + 1) == en_passant_target:
                moves_list.append(en_passant_target)
            if (position[0] - 1, position[1] + 1) == en_passant_target:
                moves_list.append(en_passant_target)
    else:
        # Black di chuyển ngược lại
        if (position[0], position[1] - 1) not in white_locations and \
           (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
           (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        # Bắt đối phương
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        # En passant: nếu có nước en passant (đối với white vừa di chuyển 2 ô)
        if en_passant_target is not None:
            if (position[0] + 1, position[1] - 1) == en_passant_target:
                moves_list.append(en_passant_target)
            if (position[0] - 1, position[1] - 1) == en_passant_target:
                moves_list.append(en_passant_target)
    return moves_list

def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    targets = [(1, 2), (1, -2), (2, 1), (2, -1),
               (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for dx, dy in targets:
        target = (position[0] + dx, position[1] + dy)
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for move in moves:
        pygame.draw.circle(
            screen, color, (move[0] * 100 + 50, move[1] * 100 + 50), 5)

def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))

def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for options in black_options:
                if king_location in options:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [king_location[0] * 100 + 1,
                                                               king_location[1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for options in white_options:
                if king_location in options:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [king_location[0] * 100 + 1,
                                                                king_location[1] * 100 + 1, 100, 100], 5)
def handle_piece_capture(attacking_locations, attacking_pieces, defending_locations, defending_pieces, click_coords):
    # Check if the destination square is occupied by an opponent's piece
    if click_coords in defending_locations:
        # Find the index of the captured piece
        captured_index = defending_locations.index(click_coords)
        
        # Remove the captured piece
        captured_piece = defending_pieces.pop(captured_index)
        defending_locations.pop(captured_index)
        
        # Add to captured pieces list (for display)
        if attacking_pieces == white_pieces:
            captured_pieces_white.append(captured_piece)
        else:
            captured_pieces_black.append(captured_piece)
    
    return defending_pieces, defending_locations
def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(
        f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render('Press ENTER to Restart!',
                            True, 'white'), (210, 240))

def is_in_check(king_location, attacking_options):
    """Check if the king is under attack"""
    for options in attacking_options:
        if king_location in options:
            return True
    return False

def is_checkmate(pieces, locations, options, king_color):
    """
    Determine if the current position is a checkmate
    
    Args:
    - pieces: list of pieces for the player being checked
    - locations: list of piece locations
    - options: list of possible moves for all pieces
    - king_color: color of the king being checked ('white' or 'black')
    
    Returns:
    - Boolean indicating if it's a checkmate
    """
    # Find the king's location and index
    if king_color == 'white':
        king_index = pieces.index('king')
        king_location = locations[king_index]
        friendly_options = options
        enemy_options = black_options
    else:
        king_index = pieces.index('king')
        king_location = locations[king_index]
        friendly_options = options
        enemy_options = white_options
    
    # First, check if the king is in check
    if not is_in_check(king_location, enemy_options):
        return False
    
    # Check if king can move out of check
    king_moves = check_king(king_location, king_color)
    for move in king_moves:
        # Temporarily move the king
        original_king_location = locations[king_index]
        locations[king_index] = move
        
        # Recheck if this move gets the king out of check
        temporary_options = check_options(pieces, locations, king_color)
        if not is_in_check(move, enemy_options):
            # Restore original location
            locations[king_index] = original_king_location
            return False
        
        # Restore original location
        locations[king_index] = original_king_location
    
    # Check if any piece can block the check or capture the attacking piece
    for i in range(len(pieces)):
        # Skip the king
        if pieces[i] == 'king':
            continue
        
        # Get possible moves for this piece
        piece_moves = friendly_options[i]
        
        for move in piece_moves:
            # Temporarily move the piece
            original_piece_location = locations[i]
            locations[i] = move
            
            # Temporarily remove any captured piece
            captured_index = -1
            captured_piece = None
            if move in (white_locations if king_color == 'black' else black_locations):
                captured_index = (white_locations if king_color == 'black' else black_locations).index(move)
                captured_piece = (white_pieces if king_color == 'black' else black_pieces)[captured_index]
                (white_locations if king_color == 'black' else black_locations).pop(captured_index)
                (white_pieces if king_color == 'black' else black_pieces).pop(captured_index)
            
            # Recheck options and check status
            temporary_options = check_options(pieces, locations, king_color)
            if not is_in_check(king_location, enemy_options):
                # Restore locations and pieces
                locations[i] = original_piece_location
                if captured_piece:
                    (white_locations if king_color == 'black' else black_locations).insert(captured_index, move)
                    (white_pieces if king_color == 'black' else black_pieces).insert(captured_index, captured_piece)
                return False
            
            # Restore locations and pieces
            locations[i] = original_piece_location
            if captured_piece:
                (white_locations if king_color == 'black' else black_locations).insert(captured_index, move)
                (white_pieces if king_color == 'black' else black_pieces).insert(captured_index, captured_piece)
    
    # If no moves can get out of check, it's a checkmate
    return True

black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            # Xử lý cho lượt trắng
            if turn_step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    original = white_locations[selection]
                    white_locations[selection] = click_coords

                    # Capture opponent's piece
                    if click_coords in black_locations:
                        capture_index = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[capture_index])
                        black_pieces.pop(capture_index)
                        black_locations.pop(capture_index)

                    # Nếu di chuyển en passant (nước đi trùng với en_passant_target)
                    if white_pieces[selection] == 'pawn' and en_passant_target == click_coords:
                        # Khi trắng bắt en passant, quân địch nằm bên dưới ô đích (vì pawn đen di chuyển lên)
                        captured_square = (click_coords[0], click_coords[1] - 1)
                        if captured_square in black_locations:
                            idx = black_locations.index(captured_square)
                            captured_pieces_white.append(black_pieces[idx])
                            black_pieces.pop(idx)
                            black_locations.pop(idx)
                    # Kiểm tra double move để cho en passant (cho quân tốt trắng: bắt đầu từ hàng 1 đến hàng 3)
                    if white_pieces[selection] == 'pawn' and original[1] == 1 and click_coords[1] - original[1] == 2:
                        en_passant_target = (original[0], original[1] + 1)  # ô trung gian
                        en_passant_piece = ('white', selection)
                    else:
                        en_passant_target = None
                        en_passant_piece = None

                    # Phong hậu: nếu con tốt đến hàng cuối (với trắng là hàng 7)
                    if white_pieces[selection] == 'pawn' and click_coords[1] == 7:
                        white_pieces[selection] = 'queen'
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    
                    # Check for checkmate
                    if is_checkmate(black_pieces, black_locations, black_options, 'black'):
                        winner = 'white'
                        game_over = True
                    
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            # Xử lý cho lượt đen
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    original = black_locations[selection]
                    black_locations[selection] = click_coords

                    # Capture opponent's piece
                    if click_coords in white_locations:
                        capture_index = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[capture_index])
                        white_pieces.pop(capture_index)
                        white_locations.pop(capture_index)

                    # Nếu di chuyển en passant (nước đi trùng với en_passant_target)
                    if black_pieces[selection] == 'pawn' and en_passant_target == click_coords:
                        # Khi đen bắt en passant, quân địch nằm bên trên ô đích (vì pawn trắng di chuyển xuống)
                        captured_square = (click_coords[0], click_coords[1] + 1)
                        if captured_square in white_locations:
                            idx = white_locations.index(captured_square)
                            captured_pieces_black.append(white_pieces[idx])
                            white_pieces.pop(idx)
                            white_locations.pop(idx)
                    # Kiểm tra double move cho pawn đen (bắt đầu từ hàng 6 đến hàng 4)
                    if black_pieces[selection] == 'pawn' and original[1] == 6 and original[1] - click_coords[1] == 2:
                        en_passant_target = (original[0], original[1] - 1)
                        en_passant_piece = ('black', selection)
                    else:
                        en_passant_target = None
                        en_passant_piece = None

                    # Phong hậu: nếu con tốt đến hàng cuối (với đen là hàng 0)
                    if black_pieces[selection] == 'pawn' and click_coords[1] == 0:
                        black_pieces[selection] = 'queen'
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    
                    # Check for checkmate
                    if is_checkmate(white_pieces, white_locations, white_options, 'white'):
                        winner = 'black'
                        game_over = True
                    
                    turn_step = 0
                    selection = 100
                    valid_moves = []

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                en_passant_target = None
                en_passant_piece = None
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()

pygame.quit()
