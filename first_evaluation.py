from ChessState import *

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

def threat_bonus(chess_state, turn):
    my_pieces = chess_state.white_pieces if turn == "White" else chess_state.black_pieces
    bonus = 0.0

    for piece in my_pieces:
        possible_moves = piece.get_legal_moves(chess_state)

        for move in possible_moves:
            nx, ny = move["new_pos"]
            occupant = chess_state.board[nx][ny]
            if occupant is not None and occupant.color != piece.color:
                if occupant.type == "King":
                    bonus += 2.0
                else:
                    bonus += occupant.point * 0.3 
    return bonus

def king_safety_bonus(chess_state, turn):
    my_pieces = chess_state.white_pieces if turn == "White" else chess_state.black_pieces
    op_turn = "White" if turn == "Black" else turn
    king = [piece for piece in my_pieces if piece.type == "King"][0]
    bonus = 0.0
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    
    for dx, dy in directions:
        nx, ny = king.x + dx, king.y + dy
        if king.is_in_bound(nx, ny):
            occupant = chess_state.board[nx][ny]
            if occupant is not None:
                if occupant.color == king.color:
                    bonus += 0.5  
                else:
                    bonus -= 0.5  
            else:
                if chess_state.is_attacked(nx, ny, op_turn):
                    bonus -= 0.3
                else:
                    bonus += 0.2
    
    if king.is_castle:
        bonus += 1.0  
    
    return bonus


def evaluate_func(chess_state, turn):
    my_pieces = chess_state.white_pieces if turn == "White" else chess_state.black_pieces
    opponent_pieces = chess_state.white_pieces if turn == "Black" else chess_state.black_pieces
    op_turn = "White" if turn == "Black" else turn

    if chess_state.is_checkmate("White"):
        return float('-inf')

    if chess_state.is_checkmate("Black"):
        return float('inf')

    score = 0

    for piece in my_pieces:
        score += piece.point + piece_square_table(piece)

    for piece in opponent_pieces:
        score -= piece.point + piece_square_table(piece)

    my_threat_bonus = threat_bonus(chess_state, turn)
    opp_threat_bonus = threat_bonus(chess_state, turn)

    score += (my_threat_bonus - opp_threat_bonus)
    
    score += king_safety_bonus(chess_state, turn)
    score -= king_safety_bonus(chess_state, turn)

    return score