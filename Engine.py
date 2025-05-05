import random
from Piece import *
from evaluation import *

def generate_random_move(board, my_pieces, opponent_pieces):
    all_moves = []
    
    for piece in my_pieces:
        valid_moves = piece.get_valid_moves(board, my_pieces, opponent_pieces)
        for move in valid_moves:
            all_moves.append((piece, move))
    
    if not all_moves:
        return None 

    return random.choice(all_moves)

def piece_square_table(piece):
    piece_square = {
        "King": [
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [ 2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
            [ 2.0,  3.0,  0.0,  0.0,  0.0,  0.0,  3.0,  2.0]
        ],
        "Queen": [
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.5,  0.5, -1.0],
            [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ],
        "Rook": [
            [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0, -0.5,  0.0],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [ 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
        ],
        "Bishop": [
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
            [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
            [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
            [-1.0,  0.5,  1.0,  0.5,  0.5,  1.0,  0.5, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
        ],
        "Knight": [
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
            [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
            [-3.0,  0.5,  2.0,  2.5,  2.5,  2.0,  0.5, -3.0],
            [-3.0,  0.5,  2.0,  2.5,  2.5,  2.0,  0.5, -3.0],
            [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
            [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
        ],
        "Pawn": [
            [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [ 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
            [ 1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
            [ 0.5,  0.5,  1.5,  2.5,  2.5,  1.5,  0.5,  0.5],
            [ 0.0,  0.0,  2.0,  2.5,  2.5,  2.0,  0.0,  0.0],
            [ 0.5, -0.5,  1.0,  0.0,  0.0,  1.0, -0.5,  0.5],
            [ 0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0,  0.5],
            [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
        ]
    }

    row, col = piece.x, piece.y

    if piece.color == 'Black':
        row = 7 - row

    return piece_square[piece.type][row][col]

# def threat_bonus(board, my_pieces, opponent_pieces):
#     bonus = 0.0

#     for piece in my_pieces:
#         possible_moves = piece.get_legal_moves(board, my_pieces, opponent_pieces)

#         for move in possible_moves:
#             nx, ny = move["new_pos"]
#             occupant = board[nx][ny]
#             if occupant is not None and occupant.color != piece.color:
#                 if occupant.type == "King":
#                     bonus += 2.0
#                 else:
#                     bonus += occupant.point * 0.3 
#     return bonus

def king_safety_bonus(board, my_pieces, opponent_pieces):
    king = [piece for piece in my_pieces if piece.type == "King"][0]
    bonus = 0.0
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    
    for dx, dy in directions:
        nx, ny = king.x + dx, king.y + dy
        if king.is_in_bound(nx, ny):
            occupant = board[nx][ny]
            if occupant is not None:
                if occupant.color == king.color:
                    bonus += 0.5  
                else:
                    bonus -= 0.5  
            else:
                if is_attacked_square(board, nx, ny, my_pieces, opponent_pieces):
                    bonus -= 0.3
                else:
                    bonus += 0.2
    
    if king.is_castle:
        bonus += 1.0  
    
    return bonus


def evaluate_func(board, my_pieces, opponent_pieces):
    if is_checkmate(board=board, my_pieces=my_pieces, opponent_pieces=opponent_pieces):
        return float('-inf')

    if is_checkmate(board=board, my_pieces=opponent_pieces, opponent_pieces=my_pieces):
        return float('inf')

    score = 0

    for piece in my_pieces:
        score += piece.point + piece_square_table(piece)

    for piece in opponent_pieces:
        score -= piece.point + piece_square_table(piece)

    my_threat_bonus = threat_bonus(board, my_pieces, opponent_pieces)
    opp_threat_bonus = threat_bonus(board, opponent_pieces, my_pieces)

    score += (my_threat_bonus - opp_threat_bonus)
    
    score += king_safety_bonus(board, my_pieces, opponent_pieces)
    score -= king_safety_bonus(board, opponent_pieces, my_pieces)

    return score

def alpha_beta_engine(board, white_pieces, black_pieces, depth, maximize, alpha=float("-inf"), beta=float("inf")):
    turn = "white" if maximize else "black"

    if depth == 0:
        return (evaluate_position(board, white_pieces, black_pieces, turn), None)
    
    if maximize:
        best_value = float("-inf")
        best_move = None

        for piece in white_pieces:
            moves = piece.get_valid_moves(board, white_pieces, black_pieces)
            
            for move in moves:
                move_info = make_move(board=board, piece=piece, move=move, opponent_pieces=black_pieces)
                value, _ = alpha_beta_engine(board=board, white_pieces=white_pieces, black_pieces=black_pieces, 
                                               depth=depth-1, alpha=alpha, beta=beta, maximize=False)

                if value > best_value:
                    best_value = value
                    best_move = (piece, move)

                undo_move(board=board, opponent_pieces=black_pieces, move_info=move_info)
                alpha = max(alpha, best_value)

                if beta <= alpha:
                    break
            
            if beta <= alpha:
                break

        return (best_value, best_move)

    else: 
        best_value = float("inf")
        best_move = None

        for piece in black_pieces:
            moves = piece.get_valid_moves(board, black_pieces, white_pieces)

            for move in moves:
                move_info = make_move(board, piece, move, white_pieces)
                value, _ = alpha_beta_engine(board=board, white_pieces=white_pieces, black_pieces=black_pieces, 
                                               depth=depth-1, alpha=alpha, beta=beta, maximize=True)

                if value < best_value:
                    best_value = value
                    best_move = (piece, move)

                undo_move(board, white_pieces, move_info)
                beta = min(beta, best_value)

                if beta <= alpha:
                    break  

            if beta <= alpha:
                break
        return (best_value, best_move)


def play_chess(board, white_pieces, black_pieces, depth, agent_side):
    turn = "White"
    while True:
        my_pieces, opp_pieces = (white_pieces, black_pieces) if turn=="White" else (black_pieces, white_pieces)
        if is_checkmate(board, my_pieces, opp_pieces):
            winner = "Black" if turn=="White" else "White"
            yield "GAME_OVER", f"{winner} win"
            break

        draw_reason = detect_draw(board, white_pieces, black_pieces, turn)
        if draw_reason:
            yield "GAME_OVER", draw_reason
            break

        if turn == agent_side:
            _, best = alpha_beta_engine(board, white_pieces, black_pieces, depth,
                                        maximize=(turn=="White"))
            move_pair = best
        else:
            move_pair = generate_random_move(board, my_pieces, opp_pieces)

        piece, move_dict = move_pair
        move_info = make_move(board, piece, move_dict, opp_pieces)

        record_state(board, EN_PASSANT_SQUARE, derive_castling_array(white_pieces, black_pieces))

        yield "MOVE", move_info
        turn = "Black" if turn=="White" else "White"
