import random
from ChessState import ChessState
# from evaluation import *
from first_evaluation import *
from second_evaluation import *

def generate_random_move(chess_state, turn):
    all_moves = []
    my_pieces = chess_state.white_pieces if turn == "White" else chess_state.black_pieces
    for piece in my_pieces:
        valid_moves = piece.get_valid_moves(chess_state)
        for move in valid_moves:
            all_moves.append((piece, move))
    
    if not all_moves:
        return None 

    return random.choice(all_moves)

def alpha_beta_engine(chess_state, depth, maximize, alpha=float("-inf"), beta=float("inf"), last_move=None, last_delta = None):
    turn = "White" if maximize else "Black"

    if depth == 0:
        # return (chess_state.score, None)
        return (evaluate_func(chess_state, turn), None)
    
    if maximize:
        best_value = float("-inf")
        best_move = None

        for piece in chess_state.white_pieces:
            moves = piece.get_valid_moves(chess_state)
            
            for move in moves:
                # delta = evaluate(chess_state, piece, move)
                # if last_delta is not None and last_delta == delta:
                #     delta = delta // 2
                # move_info = chess_state.make_move(piece, move, delta)
                move_info = chess_state.make_move(piece, move)
                value, _ = alpha_beta_engine(chess_state=chess_state, depth=depth-1, alpha=alpha, beta=beta, maximize=False,last_move=move_info)

                if value > best_value:
                    best_value = value
                    best_move = (piece, move)

                chess_state.undo_move(move_info=move_info)
                alpha = max(alpha, best_value)

                if beta <= alpha:
                    break
            
            if beta <= alpha:
                break

        return (best_value, best_move)

    else: 
        best_value = float("inf")
        best_move = None

        for piece in chess_state.black_pieces:
            moves = piece.get_valid_moves(chess_state)

            for move in moves:
                # delta = evaluate(chess_state, piece, move)
                # if last_delta is not None and last_delta == delta:
                #     delta = delta // 2
                # move_info = chess_state.make_move(piece, move, delta)
                move_info = chess_state.make_move(piece, move)
                value, _ = alpha_beta_engine(chess_state=chess_state, depth=depth-1, alpha=alpha, beta=beta, maximize=True,last_move=move_info)

                if value < best_value:
                    best_value = value
                    best_move = (piece, move)

                chess_state.undo_move(move_info=move_info)
                beta = min(beta, best_value)

                if beta <= alpha:
                    break  

            if beta <= alpha:
                break

        return (best_value, best_move)


def play_chess(chess_state, depth, agent_side):
    turn = "White"
    while True:
        if chess_state.is_checkmate(turn):
            winner = "Black" if turn=="White" else "White"
            yield "GAME_OVER", f"{winner} win"
            break

        draw_reason = chess_state.detect_draw(turn)
        if draw_reason:
            yield "GAME_OVER", draw_reason
            break

        if turn == agent_side:
            _, best = alpha_beta_engine(chess_state, depth,
                                        maximize=(turn=="White"))
            move_pair = best
        else:
            move_pair = generate_random_move(chess_state, turn)

        piece, move_dict = move_pair
        move_info = chess_state.make_move(piece, move_dict)

        chess_state.record_state(turn)

        yield "MOVE", move_info
        turn = "Black" if turn=="White" else "White"
