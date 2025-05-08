from Piece import *

piece_values = {
    'King': 0,   
    'Queen': 900,
    'Rook': 500,
    'Bishop': 330,
    'Knight': 320,
    'Pawn': 100
}

def threat_bonus(board, my_pieces, opponent_pieces):
    bonus = 0.0

    for piece in my_pieces:
        possible_moves = piece.get_legal_moves(board, my_pieces, opponent_pieces)

        for move in possible_moves:
            nx, ny = move["new_pos"]
            occupant = board[nx][ny]
            if occupant is not None and occupant.color != piece.color:
                if occupant.type == "King":
                    bonus += 5
                else:
                    bonus += occupant.point 
    return bonus

def evaluate_opening(board, white_pieces, black_pieces):
    score = 0

    for piece in white_pieces:
        score += piece_values[piece.type]
    for piece in black_pieces:
        score -= piece_values[piece.type]

    starting_squares_white = {'Knight': [(7,1),(7,6)], 'Bishop': [(7,2),(7,5)]}
    starting_squares_black = {'Knight': [(0,1),(0,6)], 'Bishop': [(0,2),(0,5)]}
    develop_bonus = 20 

    for piece in white_pieces:
        if piece.type in ['Knight','Bishop'] and (piece.x, piece.y) not in starting_squares_white[piece.type]:
            score += develop_bonus
    for piece in black_pieces:
        if piece.type in ['Knight','Bishop'] and (piece.x, piece.y) not in starting_squares_black[piece.type]:
            score -= develop_bonus

    center_squares = [(3,3),(3,4),(4,3),(4,4)]
    center_control_bonus = 10
    for piece in white_pieces:
        if (piece.x, piece.y) in center_squares:
            score += center_control_bonus
    for piece in black_pieces:
        if (piece.x, piece.y) in center_squares:
            score -= center_control_bonus

    castle_bonus = 30
    white_king = next(p for p in white_pieces if p.type == 'King')
    black_king = next(p for p in black_pieces if p.type == 'King')

    if getattr(white_king, 'is_castle', False):
        score += castle_bonus
    if getattr(black_king, 'is_castle', False):

        score -= castle_bonus
    return score

def get_surrounding_squares(pos, board_size=8):
    x, y = pos
    neighbors = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < board_size and 0 <= ny < board_size:
                neighbors.append((nx, ny))
    return neighbors

def evaluate_middlegame(board, white_pieces, black_pieces):
    score = 0

    for piece in white_pieces:
        score += piece_values[piece.type]
    for piece in black_pieces:
        score -= piece_values[piece.type]

    mobility_weights = {'Queen': 2, 'Rook': 2, 'Bishop': 1, 'Knight': 1, 'Pawn': 0.5, 'King': 0} 

    for piece in white_pieces:
        moves = piece.get_legal_moves(board, white_pieces, black_pieces)
        score += len(moves) * mobility_weights.get(piece.type, 1)
    for piece in black_pieces:
        moves = piece.get_legal_moves(board, black_pieces, white_pieces)
        score -= len(moves) * mobility_weights.get(piece.type, 1)

    white_king = next(p for p in white_pieces if p.type == 'King')
    black_king = next(p for p in black_pieces if p.type == 'King')
 
    king_safety_penalty = 20

    white_king_square = (white_king.x, white_king.y)
    white_king_neighbors = get_surrounding_squares(white_king_square)

    pawns_near_white_king = sum(1 for p in white_pieces 
                                 if p.type == 'Pawn' and (p.x, p.y) in white_king_neighbors)
 
    if pawns_near_white_king < 2:
        score -= king_safety_penalty * (2 - pawns_near_white_king)


    black_king_square = (black_king.x, black_king.y)
    black_king_neighbors = get_surrounding_squares(black_king_square)
    pawns_near_black_king = sum(1 for p in black_pieces 
                                 if p.type == 'Pawn' and (p.x, p.y) in black_king_neighbors)
    if pawns_near_black_king < 2:
        score += king_safety_penalty * (2 - pawns_near_black_king)

    return score


def evaluate_endgame(board, white_pieces, black_pieces):
    score = 0
    endgame_values = {'King': 200, 'Queen': 900, 'Rook': 500, 'Bishop': 330, 'Knight': 320, 'Pawn': 100}

    for piece in white_pieces:
        score += endgame_values[piece.type]
    for piece in black_pieces:
        score -= endgame_values[piece.type]

    def distance_to_center(pos):
        center = (3.5, 3.5)
        return abs(pos[0] - center[0]) + abs(pos[1] - center[1])
    white_king = next(p for p in white_pieces if p.type == 'King')
    black_king = next(p for p in black_pieces if p.type == 'King')

    king_center_bonus = 10
    score += (30 - 5 * distance_to_center((white_king.x, white_king.y)))  
    score -= (30 - 5 * distance_to_center((black_king.x, black_king.y)))

    def is_passed_pawn(pawn, white_pieces, black_pieces):
        px, py = pawn.x, pawn.y
        if pawn.color == 'white':
            for bp in black_pieces:
                if bp.type == 'Pawn':
                    bx, by = (bp.x, bp.y)
                    if bx >= px:  
                        continue
                    if abs(by - py) <= 1:
                        return False
            return True
        else:  
            for wp in white_pieces:
                if wp.type == 'Pawn':
                    wx, wy = (wp.x, wp.y)
                    if wx <= px:
                        continue
                    if abs(wy - py) <= 1:
                        return False
            return True
        
    for pawn in [p for p in white_pieces if p.type == 'Pawn']:
        if is_passed_pawn(pawn, white_pieces, black_pieces):
            rank = pawn.x

            bonus = 50 + (rank * 10)  
            score += bonus
    for pawn in [p for p in black_pieces if p.type == 'Pawn']:
        if is_passed_pawn(pawn, white_pieces, black_pieces):
            rank = pawn.x
            bonus = 50 + ((7 - rank) * 10) 
            score -= bonus

    if len([p for p in white_pieces if p.type != 'King']) == 0 and len([p for p in black_pieces if p.type != 'King']) == 0:
        return 0  

    return score


def determine_game_phase(white_pieces, black_pieces):
    total_material = 0
    for piece in white_pieces + black_pieces:
        total_material += piece_values.get(piece.type, 0)
    
    if total_material > 3000:
        return 'opening'
    elif total_material > 1500:
        return 'middlegame'
    else:
        return 'endgame'


def evaluate_position(board, white_pieces, black_pieces, turn):
    if turn.lower() == "white":
        my_pieces = white_pieces
        opponent_pieces = black_pieces
    else:
        my_pieces = black_pieces
        opponent_pieces = white_pieces

    if is_checkmate(board, opponent_pieces, my_pieces):
        return 10000
    
    if is_checkmate(board, my_pieces, opponent_pieces):
        return -10000

    all_moves = []
    for piece in my_pieces:
        moves = piece.get_legal_moves(board, white_pieces, black_pieces)
        if moves:
            all_moves.extend(moves)
    if not all_moves:
        return 0
    

    white_non_king = [p for p in white_pieces if p.type != "King"]
    black_non_king = [p for p in black_pieces if p.type != "King"]

    no_pawns = all(p.type != "Pawn" for p in white_non_king + black_non_king)
    if no_pawns:
        if (len(white_non_king) <= 1 and len(black_non_king) <= 1):
            if not any(p.type in ("Queen", "Rook") for p in white_non_king + black_non_king):
                return 0

        if len(white_non_king) == 2 and len(black_non_king) == 0:
            piece_types = sorted(p.type for p in white_non_king)
            if piece_types == ["Knight", "Knight"]:
                return 0
        if len(black_non_king) == 2 and len(white_non_king) == 0:
            piece_types = sorted(p.type for p in black_non_king)
            if piece_types == ["Knight", "Knight"]:
                return 0
    
    total_pieces = len(white_pieces) + len(black_pieces)
    if total_pieces > 26:
        score = evaluate_opening(board, white_pieces, black_pieces)
    elif total_pieces > 14:
        score = evaluate_middlegame(board, white_pieces, black_pieces)
    else:
        score = evaluate_endgame(board, white_pieces, black_pieces)
    
    return score + threat_bonus(board, my_pieces, opponent_pieces)
