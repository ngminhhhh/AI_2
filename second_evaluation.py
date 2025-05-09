from ChessState import *

A8, H8, A1, H1 = 0, 7, 56, 63
piece_vals = {"P": 100, "N": 280, "B": 320, "R": 479, "Q": 929, "K": 60000}
pst = {
    'P': (   0,   0,   0,   0,   0,   0,   0,   0,
            78,  83,  86,  73, 102,  82,  85,  90,
             7,  29,  21,  44,  40,  31,  44,   7,
           -17,  16,  -2,  15,  14,   0,  15, -13,
           -26,   3,  10,   9,   6,   1,   0, -23,
           -22,   9,   5, -11, -10,  -2,   3, -19,
           -31,   8,  -7, -37, -36, -14,   3, -31,
             0,   0,   0,   0,   0,   0,   0,   0),
    'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
            -3,  -6, 100, -36,   4,  62,  -4, -14,
            10,  67,   1,  74,  73,  27,  62,  -2,
            24,  24,  45,  37,  33,  41,  25,  17,
            -1,   5,  31,  21,  22,  35,   2,   0,
           -18,  10,  13,  22,  18,  15,  11, -14,
           -23, -15,   2,   0,   2,   0, -23, -20,
           -74, -23, -26, -24, -19, -35, -22, -69),
    'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
           -11,  20,  35, -42, -39,  31,   2, -22,
            -9,  39, -32,  41,  52, -10,  28, -14,
            25,  17,  20,  34,  26,  25,  15,  10,
            13,  10,  17,  23,  17,  16,   0,   7,
            14,  25,  24,  15,   8,  25,  20,  15,
            19,  20,  11,   6,   7,   6,  20,  16,
            -7,   2, -15, -12, -14, -15, -10, -10),
    'R': (  35,  29,  33,   4,  37,  33,  56,  50,
            55,  29,  56,  67,  55,  62,  34,  60,
            19,  35,  28,  33,  45,  27,  25,  15,
             0,   5,  16,  13,  18,  -4,  -9,  -6,
           -28, -35, -16, -21, -13, -29, -46, -30,
           -42, -28, -42, -25, -25, -35, -26, -46,
           -53, -38, -31, -26, -29, -43, -44, -53,
           -30, -24, -18,   5,  -2, -18, -31, -32),
    'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
            14,  32,  60, -10,  20,  76,  57,  24,
            -2,  43,  32,  60,  72,  63,  43,   2,
             1, -16,  22,  17,  25,  20, -13,  -6,
           -14, -15,  -2,  -5,  -1, -10, -20, -22,
           -30,  -6, -13, -11, -16, -11, -16, -27,
           -36, -18,   0, -19, -15, -15, -21, -38,
           -39, -30, -31, -13, -31, -36, -34, -42),
    'K': (   4,  54,  47, -99, -99,  60,  83, -62,
           -32,  10,  55,  56,  56,  55,  10,   3,
           -62,  12, -57,  44, -67,  28,  37, -31,
           -55,  50,  11,  -4, -19,  13,   0, -49,
           -55, -43, -52, -28, -51, -47,  -8, -50,
           -47, -42, -43, -79, -64, -32, -29, -32,
            -4,   3, -14, -50, -57, -18,  13,   4,
            17,  30,  -3, -14,   6,  -1,  40,  18),
}


def evaluate(chess_state, piece, move):
    from_pos, to_pos = (piece.x, piece.y), move["new_pos"]
    p = chess_state.map_to_sym(piece.type, piece.color)

    # * Encode
    from_idx = (7 - from_pos[1]) * 8 + (from_pos[0])
    to_idx =  (7 - to_pos[1]) * 8 + (to_pos[0])

    score = pst[p.upper()][to_idx] - pst[p.upper()][from_idx]
    
    if move["captured"]:
        cap_sym = chess_state.map_to_sym(move["captured"].type, move["captured"].color)
        score += piece_vals[cap_sym.upper()]

    # * Basic score

    # * Capture
    idx = 63 - to_idx if p.islower() else to_idx
    score += pst[p.upper()][idx]

    # * Check
    op = "White" if piece.color == "Black" else "White"

    op_lst = chess_state.white_pieces if op == "White" else chess_state.black_pieces
    op_king = next(p for p in op_lst if p.type == "King")

    op_king_idx = (7 - op_king.y) * 8 + (op_king.x)

    if abs(to_idx - op_king_idx) < 2:
        pst_idx = to_idx if op == "White" else 63 - to_idx
        score += pst["K"][pst_idx]

    # * Castle
    if (p == "K" or p == 'k') and abs(from_idx - to_idx) == 2:
        is_white = p.isupper()
        original_rook = ((A1 if to_idx < from_idx else H1) if is_white else (A8 if to_idx < from_idx else H8))
        mid_square = (from_idx + to_idx) // 2

        add_idx = mid_square if is_white else 63 - mid_square
        sub_idx = original_rook if is_white else 63 - original_rook

        score += pst["R"][add_idx]
        score -= pst["R"][sub_idx]

    # * Pawn special
    if p == "P" or p == 'p':
        is_white = p.isupper()
        idx = to_idx if is_white else 63 - to_idx
        if move["type"] == "Promotion":
            score += pst["Q"][idx] - pst["P"][idx]
        # if to_pos == move.en_passant_prev:
        #     score += pst["P"][idx - 10]

    return score

