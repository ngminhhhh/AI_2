from ChessState import *

DEV_KNIGHT_BISHOP = 10  
DEV_ROOK            = 5   

CENTER_FULL    = 15  
CENTER_HALF    = 7   

MOBILITY_WEIGHT = {
    'Pawn':   0,   
    'Knight': 1,   
    'Bishop': 1,   
    'Rook':   0.5, 
    'Queen':  0.2, 
    'King':   0
}

KING_THREAT_WEIGHT = -2  
KING_SHIELD_WEIGHT =  1  

TRAPPED_PENALTY = -5  

OUTPOST_BONUS = 8  

ISOLATED_PENALTY = -5  
DOUBLED_PENALTY  = -5  

PASSED_BASE    = 10  
PASSED_PER_RANK= 2   

EG_KING_MOBILITY_MULT = 2  

CONTEMPT_VALUE = 10  

def is_pawn_control(chess_state, r, c, color):
    if color == "White":
        offsets = [(1, -1), (1, 1)]
    else:
        offsets = [(-1, -1), (-1, 1)]

    for dr, dc in offsets:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            p = chess_state.board[nr][nc]
            if p and p.type == "Pawn" and p.color == color:
                return True
    return False

def is_passed_pawn(chess_state, pawn):
    f = pawn.x
    r = pawn.y
    if pawn.color == 'White':
        for pb in chess_state.black_pieces:
            if pb.type == "Pawn" and abs(pb.x - f) <= 1 and pb.y < r:
                return False
            
        return True
    else:
        for pb in chess_state.white_pieces:
            if pb.type == "Pawn" and abs(pb.x - f) <= 1 and pb.y > r:
                return False
            
        return True
        
def development_bonus(chess_state, turn):
    mg_bonus = 0
    lst = chess_state.white_pieces if turn == "White" else chess_state.black_pieces

    init_positions = {
        'White': {'Knight': [(7,1),(7,6)], 'Bishop': [(7,2),(7,5)], 'Rook': [(7,0),(7,7)]},
        'Black': {'Knight': [(0,1),(0,6)], 'Bishop': [(0,2),(0,5)], 'Rook': [(0,0),(0,7)]}
    }

    for piece in lst:
        if piece.type in init_positions[turn]:
            if (piece.x, piece.y) not in init_positions[turn][piece.type]:
                if piece.type in ("Knight", "Bishop"):
                    mg_bonus += DEV_KNIGHT_BISHOP  
                else:
                    mg_bonus += DEV_ROOK             

    return mg_bonus if turn == "White" else -mg_bonus

def center_control_bonus(chess_state, turn):
    mg_bonus = 0
    center_squares = [(4,4),(4,3),(3,4),(3,3)]
    half_center    = [(5,2),(5,5),(2,2),(2,5)]

    lst = chess_state.white_pieces if turn == "White" else chess_state.black_pieces
    for piece in lst:
        if (piece.x, piece.y) in center_squares:
            mg_bonus += CENTER_FULL      
        elif (piece.x, piece.y) in half_center:
            mg_bonus += CENTER_HALF      

    return mg_bonus if turn == "White" else -mg_bonus


def mobility_bonus(chess_state, turn):
    mobility_point = 0
    lst = chess_state.white_pieces if turn == "White" else chess_state.black_pieces
    for piece in lst:
        moves = piece.get_valid_moves(chess_state)
        mobility_point += MOBILITY_WEIGHT[piece.type] * len(moves)
    return mobility_point


def pawn_shield_bonus(king, chess_state):
    r, c = king.y, king.x
    shield = 0
    if king.color == 'white':
        directions = [( -1, 0), (-1, -1), (-1, 1)]
    else:
        directions = [( 1, 0), (1, -1), (1, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            p = chess_state.board[nr][nc]
            if p and p.type == "Pawn" and p.color == king.color:
                shield += 1

    return shield

def king_safety_bonus(chess_state, turn):
    threat = 0
    my_lst = chess_state.white_pieces if turn == "White" else chess_state.black_pieces
    op_lst = chess_state.white_pieces if turn == "Black" else chess_state.black_pieces

    my_king = next((p for p in my_lst if p.type == "King"), None)
    for piece in op_lst:
        moves = piece.get_legal_moves(chess_state)
        if (my_king.x, my_king.y) in moves:
            threat += 1

    shield = pawn_shield_bonus(my_king, chess_state)
    return threat * KING_THREAT_WEIGHT, shield * KING_SHIELD_WEIGHT  


def trapped_minus(chess_state, turn):
    minus = 0
    lst = chess_state.white_pieces if turn == "White" else chess_state.black_pieces
    for piece in lst:
        if len(piece.get_valid_moves(chess_state)) == 0:
            minus += TRAPPED_PENALTY  
    return minus


def outposts_bonus(chess_state, turn):
    bonus = 0
    op_turn = "Black" if turn == "White" else turn
    lst = chess_state.white_pieces if turn == "White" else chess_state.black_pieces
    for piece in lst:
        if piece.type in ["Knight", "Bishop"]:
            if is_pawn_control(chess_state, piece.x, piece.y, turn) \
               and not is_pawn_control(chess_state, piece.x, piece.y, op_turn):
                bonus += OUTPOST_BONUS  
    return bonus

def pawn_structure_point(chess_state, turn):
    point = 0
    pawn_file = {f:0 for f in range(8)}
    my_lst = chess_state.white_pieces if turn == "White" else chess_state.black_pieces
    for piece in my_lst:
        if piece.type == "Pawn": pawn_file[piece.x] += 1
    for f,count in pawn_file.items():
        if count == 1:
            point -= ISOLATED_PENALTY  
        elif count > 1:
            point -= DOUBLED_PENALTY * (count-1)  
    return point


def passed_pawn_bonus(chess_state, turn):
    bonus = 0
    lst = chess_state.white_pieces if turn == "White" else chess_state.black_pieces
    for piece in lst:
        if piece.type == "Pawn" and is_passed_pawn(chess_state, piece):
            rank = 7-piece.y if turn=="White" else piece.y
            bonus += PASSED_BASE + PASSED_PER_RANK * rank  
    return bonus


def endgame_king_mobility(chess_state, turn):
    lst = chess_state.white_pieces if turn == "White" else chess_state.black_pieces
    king = next((p for p in lst if p.type == "King"), None)
    dist = 14 - abs(king.y-3.5) + abs(king.x-3.5)
    return int(dist * EG_KING_MOBILITY_MULT)  


def tactical_factors(chess_state, turn):
    # scaled piece values inside tactical context:
    PIECE_VALUES = {
        'Pawn':   100,   
        'Knight': 320,   
        'Bishop': 330,   
        'Rook':   500,   
        'Queen':  900,   
        'King':   10000  
    }
    raw = 0
    opp = 'Black' if turn=='White' else 'White'
    own_list = chess_state.white_pieces if turn=='White' else chess_state.black_pieces
    for p in own_list:
        for move in p.get_legal_moves(chess_state):
            if move['type'] not in ('normal','capture'): continue
            mi = chess_state.make_move(p, move)
            tx, ty = mi.to_pos
            if mi.captured:
                gain = PIECE_VALUES[mi.captured.type] - PIECE_VALUES[p.type]
                raw += gain * 10  # adjusted capture weight
                if chess_state.is_in_check(opp): raw += 5   # adjusted check-on-capture
                if chess_state.is_attacked(tx,ty,opp): raw -= 5  # adjusted attacked penalty
            elif chess_state.is_in_check(opp):
                if not chess_state.is_attacked(tx,ty,opp): raw += 2  # adjusted check bonus
                else: raw -= 1  
            chess_state.undo_move(mi)
    return raw if turn=='White' else -raw

def evaluate(chess_state, turn):
    phase_score = {
        "Knight" : 1,
        "Bishop" : 1,
        "Rook"   : 2,
        "Queen"  : 4,
        "Pawn"   : 0,
        "King"   : 0
    }

    MAX_PHASE = 2 * phase_score["Knight"] * 2 + 2 * phase_score["Bishop"] * 2 + 2 * phase_score["Rook"] * 2 + 2 * phase_score["Queen"] * 1

    mg_score = 0 # middle game score
    eg_score = 0 # end game score

    phase = 0

    for piece in chess_state.white_pieces + chess_state.black_pieces:
        phase += phase_score[piece.type]

    phase = max(0, min(phase, MAX_PHASE))

    mg_phase_factor = phase / MAX_PHASE
    eg_phase_factor = 1 - mg_phase_factor

    mg_score += development_bonus(chess_state, "White") + development_bonus(chess_state, "Black")  # * Development bonus
    mg_score += center_control_bonus(chess_state, "White") + center_control_bonus(chess_state, "Black") # * center control bonus
    mg_score += 5 * (mobility_bonus(chess_state, "White") - mobility_bonus(chess_state, "Black")) 

    # * King safety and shield bonus
    white_threat, white_shield = king_safety_bonus(chess_state, "White")
    black_threat, black_shied = king_safety_bonus(chess_state, "Black")

    mg_score = mg_score + 5 * (white_threat - black_threat) + 2 * (white_shield - black_shied)

    # * Trapped pieces minus
    mg_score = mg_score + trapped_minus(chess_state, "White") - trapped_minus(chess_state, "Black")

    # * Outpost bonus
    mg_score = mg_score + outposts_bonus(chess_state, "White") - outposts_bonus(chess_state, "Black")

    # * Pawn structure point
    mg_score = mg_score + pawn_structure_point(chess_state, "White") - pawn_structure_point(chess_state, "Black")

    # * Passed pawn bonus
    mg_score = mg_score + passed_pawn_bonus(chess_state, "White") - passed_pawn_bonus(chess_state, "Black")

    if phase < MAX_PHASE * 0.3:
        eg_score = eg_score + endgame_king_mobility(chess_state, "White") - endgame_king_mobility(chess_state, "Black")

    # * Tactical factor bonus
    mg_score += tactical_factors(chess_state, turn)

    # * Contempt factor
    if len(chess_state.white_pieces) + len(chess_state.black_pieces) <= 4:
        mg_score += CONTEMPT_VALUE if mg_score < 0 else -CONTEMPT_VALUE
    
    score = mg_score * mg_phase_factor + eg_score * eg_phase_factor

    return int(score)