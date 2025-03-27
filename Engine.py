import random
from Piece import *

def generate_random_move(board, my_pieces, opponent_pieces):
    all_moves = []
    
    for piece in my_pieces:
        valid_moves = piece.get_valid_moves(board, my_pieces, opponent_pieces)
        for nx, ny in valid_moves:
            all_moves.append((piece, nx, ny))
    
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
        col = 7 - col

    return piece_square[piece.type][row][col]


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

    return score


def alpha_beta_engine(board, my_pieces, opponent_pieces, depth, maximize, alpha=float("-inf"), beta=float("inf")):
    if depth == 0:
        return (evaluate_func(board, my_pieces, opponent_pieces), None)
    
    if maximize:
        best_value = float("-inf")
        best_move = None

        for piece in my_pieces:
            moves = piece.get_valid_moves(board, my_pieces, opponent_pieces)
            
            for nx, ny in moves:
                move_info = make_move(board=board, piece=piece, nx=nx, ny=ny, opponent_pieces=opponent_pieces)
                value, _ = alpha_beta_engine(board=board, my_pieces=my_pieces, opponent_pieces=opponent_pieces, 
                                               depth=depth-1, alpha=alpha, beta=beta, maximize=False)

                if value > best_value:
                    best_value = value
                    best_move = (piece, nx, ny)

                undo_move(board=board, opponent_pieces=opponent_pieces, move_info=move_info)
                alpha = max(alpha, best_value)

                if beta <= alpha:
                    break
            
            if beta <= alpha:
                break

        return (best_value, best_move)

    else: 
        best_value = float("inf")
        best_move = None

        for piece in opponent_pieces:
            moves = piece.get_valid_moves(board, opponent_pieces, my_pieces)

            for (nx, ny) in moves:
                move_info = make_move(board, piece, nx, ny, my_pieces)
                value, _ = alpha_beta_engine(board=board, my_pieces=my_pieces, opponent_pieces=opponent_pieces, 
                                               depth=depth-1, alpha=alpha, beta=beta, maximize=True)

                if value < best_value:
                    best_value = value
                    best_move = (piece, nx, ny)

                undo_move(board, my_pieces, move_info)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break  

            if beta <= alpha:
                break
        return (best_value, best_move)


def play_chess(board, white_pieces, black_pieces, depth, turn):
    if turn == "White":
        if is_checkmate(board=board, my_pieces=white_pieces, opponent_pieces=black_pieces):
            print("Black win")
            return
        
        _, move = alpha_beta_engine(board=board, my_pieces=white_pieces, opponent_pieces=black_pieces, depth=depth, maximize=True)

        if move is None:
            print("Stalemate")
            return

        moving_piece, nx, ny = move

        move_info = make_move(board=board, piece=moving_piece, nx=nx, ny=ny, opponent_pieces=black_pieces)

        print(f"White turn: {move_info}")

        play_chess(board=board, white_pieces=white_pieces, black_pieces=black_pieces, depth=depth, turn="Black")

    else:
        if is_checkmate(board=board, my_pieces=white_pieces, opponent_pieces=black_pieces):
            print("White win")
            return
        
        move = generate_random_move(board=board, my_pieces=black_pieces, opponent_pieces=white_pieces)

        if move is None:
            print("Stalemate")
            return

        moving_piece, nx, ny = move

        move_info = make_move(board=board, piece=moving_piece, nx=nx, ny=ny, opponent_pieces=white_pieces)

        print(f"Black turn: {move_info}")

        play_chess(board=board, white_pieces=white_pieces, black_pieces=black_pieces, depth=depth, turn="White")
