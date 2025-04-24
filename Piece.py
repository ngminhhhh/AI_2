from abc import ABC, abstractmethod
from collections import Counter

EN_PASSANT_SQUARE = None

def map_to_block(pos, board_size=8):
    x, y = pos 
    return chr(x + 65) + str(board_size - y)

def init_piece(piece_images, board_size = 8):
    white_pieces = [
        Rook(0, 7, "White", piece_images["white_rook"]),
        Knight(1, 7, "White", piece_images["white_knight"]),
        Bishop(2, 7, "White", piece_images["white_bishop"]),
        Queen(3, 7, "White", piece_images["white_queen"]),
        King(4, 7, "White", piece_images["white_king"]),
        Bishop(5, 7, "White", piece_images["white_bishop"]),  
        Knight(6, 7, "White", piece_images["white_knight"]),  
        Rook(7, 7, "White", piece_images["white_rook"])
    ]
    
    for x in range(board_size):
        white_pieces.append(Pawn(x, 6, "White", piece_images["white_pawn"]))
    
    black_pieces = [
        Rook(0, 0, "Black", piece_images["black_rook"]),
        Knight(1, 0, "Black", piece_images["black_knight"]),
        Bishop(2, 0, "Black", piece_images["black_bishop"]),
        Queen(3, 0, "Black", piece_images["black_queen"]),
        King(4, 0, "Black", piece_images["black_king"]),
        Bishop(5, 0, "Black", piece_images["black_bishop"]),  
        Knight(6, 0, "Black", piece_images["black_knight"]),  
        Rook(7, 0, "Black", piece_images["black_rook"])
    ]

    for x in range(board_size):
        black_pieces.append(Pawn(x, 1, "Black", piece_images["black_pawn"]))

    board = [[None for _ in range(board_size)] for _ in range(board_size)]

    for piece in white_pieces:
        board[piece.x][piece.y] = piece

    for piece in black_pieces:
        board[piece.x][piece.y] = piece

    return white_pieces, black_pieces, board


# * Function to check checkmate and stalemate
def is_attacked_square(board, nx, ny, my_pieces, opponent_pieces):
    for piece in opponent_pieces:
        moves = piece.get_legal_moves(board, my_pieces, opponent_pieces)

        for move in moves:
            if move["type"] == "normal":
                x, y = move["new_pos"]
                if x == nx and y == ny:
                    return True

    return False

def is_check(board, my_pieces, opponent_pieces):
    my_king = [piece for piece in my_pieces if piece.type == "King"][0]

    return is_attacked_square(board, my_king.x, my_king.y, my_pieces, opponent_pieces)

def is_checkmate(board, my_pieces, opponent_pieces):
    if not is_check(board, my_pieces, opponent_pieces):
        return False
    
    moves = []
    for piece in my_pieces:
        moves += piece.get_valid_moves(board, my_pieces, opponent_pieces)

    return len(moves) == 0

# * Threefold repetition
state_counter = Counter()

def map_to_sym(type):
    if type == "Knight":
        return "N"
    return type[0]

def derive_castling_array(white_pieces, black_pieces):
    rights_white, rights_black = [], []

    # * White
    wking = next(p for p in white_pieces if p.type=="King")
    if wking.is_first_move:
        for rook_pos, flag in [((7,7),"K"), ((0,7),"Q")]:
            rook = next((r for r in white_pieces if r.type=="Rook" and (r.x,r.y)==rook_pos), None)
            if rook and rook.is_first_move:
                rights_white.append(flag)

    # * Black
    bking = next(p for p in black_pieces if p.type=="King")
    if bking.is_first_move:
        for rook_pos, flag in [((7,0),"k"), ((0,0),"q")]:
            rook = next((r for r in black_pieces if r.type=="Rook" and (r.x,r.y)==rook_pos), None)
            if rook and rook.is_first_move:
                rights_black.append(flag)

    return [rights_white, rights_black]

def encode_state(board, en_passant, castling_rights):
    # * Board
    rows = []
    for y in range(7, -1, -1):
        empty = 0
        row = ""

        for x in range(8):
            p = board[x][y]

            if p is not None:
                if empty:
                    row += str(empty)
                    empty = 0
                sym = map_to_sym(p.type)
                row += sym.upper() if p.color == "White" else sym.lower()
            else:
                empty = 1
        
        row += str(empty) if empty else ""
        rows.append(row)

    board_fen = "/".join(rows)

    # * Castle Right
    rights_white, rights_black = castling_rights
    castle_field = "".join(rights_white + rights_black) or "-"

    # * En passant
    ep = map_to_block(en_passant) if en_passant else "-"

    return f"{board_fen} {castle_field} {ep}"

def record_state(board, en_passant, castling_rights):
    key = encode_state(board, en_passant, castling_rights)
    state_counter[key] += 1

    return state_counter[key]

# * Insufficient material
def is_insufficient_material(pieces):
    num_kings   = sum(1 for p in pieces if p.type == "King")
    num_knights = sum(1 for p in pieces if p.type == "Knight")
    num_bishops = sum(1 for p in pieces if p.type == "Bishop")
    total_pieces = len(pieces)

    # King vs King
    if total_pieces == 2 and num_kings == 2:
        return True

    # King + Knight vs King
    if total_pieces == 3 and num_kings == 2 and num_knights == 1:
        return True

    # King + Bishop vs King
    if total_pieces == 3 and num_kings == 2 and num_bishops == 1:
        return True

    return False

# * Stalemate
def is_stalemate(board, my_pieces, opponent_pieces):
    if is_check(board, my_pieces, opponent_pieces):
        return False
    
    for piece in my_pieces:
        if piece.get_valid_moves(board, my_pieces, opponent_pieces):
            return False
        
    return True
    

def detect_draw(board, white_pieces, black_pieces, turn):
    # * Threefold repetition
    state = encode_state(board, EN_PASSANT_SQUARE, derive_castling_array(white_pieces, black_pieces))
    count = state_counter[state]

    if count >= 3:
        return "Draw by threefold repetition"
    
    # * Insufficient material
    if is_insufficient_material(white_pieces+black_pieces):
        return "Draw by Insufficient material"
    
    if turn == "White":
        if is_stalemate(board, white_pieces, black_pieces):
            return "Draw by Stalemate"
    else:
        if is_stalemate(board, black_pieces, white_pieces):
            return "Draw by Stalemate"
    
    return None

def make_move(board, piece, move, opponent_pieces):
    move_type = move['type']
    move_info = None
    global EN_PASSANT_SQUARE
    old_en_passant = EN_PASSANT_SQUARE

    if move_type == "normal":
        nx, ny = move["new_pos"]
        captured = move["captured"]

        if piece.type == "Pawn":
            if abs(ny - piece.y) == 2:
                EN_PASSANT_SQUARE = (nx, (piece.y + ny) // 2)
            else:
                EN_PASSANT_SQUARE = None
        else:
            EN_PASSANT_SQUARE = None

        move_info = NormalMoveInfo(old_en_passant, piece, piece.is_first_move, piece.x, piece.y, nx, ny, captured)

        if captured is not None:
            opponent_pieces.remove(captured)

        board[piece.x][piece.y] = None
        board[nx][ny] = piece
        piece.is_first_move = False

        piece.moves(nx, ny)
    
    elif move_type == "castle":
        rook = move["rook"]
        king_nx, king_ny = move["new_pos"]
        rook_nx, rook_ny = move["rook_new_pos"]

        move_info = CastleMoveInfo(old_en_passant, piece, rook, piece.is_first_move, rook.is_first_move, 
                                   (piece.x, piece.y), (rook.x, rook.y), (king_nx, king_ny), (rook_nx, rook_ny))

        board[piece.x][piece.y] = None
        board[rook.x][rook.y] = None

        board[king_nx][king_ny] = piece
        board[rook_nx][rook_ny] = rook

        piece.is_first_move = False
        rook.is_first_move = False

        piece.moves(king_nx, king_ny)
        rook.moves(rook_nx, rook_ny)
    
        piece.is_castle = True
        EN_PASSANT_SQUARE = None

    elif move_type == "en_passant":
        nx, ny = move["new_pos"]
        captured = move["captured"]

        move_info = NormalMoveInfo(old_en_passant, piece, piece.is_first_move, piece.x, piece.y, nx, ny, captured, "en_passant")

        opponent_pieces.remove(captured)

        board[piece.x][piece.y] = None
        board[nx][ny] = piece
        piece.is_first_move = False
        
        piece.moves(nx, ny)
        EN_PASSANT_SQUARE = None

    return move_info

def undo_move(board, opponent_pieces, move_info):
    global EN_PASSANT_SQUARE

    EN_PASSANT_SQUARE = move_info.en_passant_pos

    if move_info.type in ["normal", "en_passant"]:
        piece = move_info.piece
        old_x = move_info.old_x
        old_y = move_info.old_y
        new_x = move_info.new_x
        new_y = move_info.new_y
        captured_piece = move_info.captured_piece

        board[old_x][old_y] = piece
        board[new_x][new_y] = None

        if move_info.type == "en_passant":
            board[new_x][old_y] = captured_piece
        else:
            board[new_x][new_y] = captured_piece

        piece.moves(old_x, old_y)
        piece.is_first_move = move_info.piece_is_first_move

        if captured_piece is not None:
            opponent_pieces.append(captured_piece)

    elif move_info.type == "castle":
        king = move_info.king
        rook = move_info.rook

        king_old_x, king_old_y = move_info.king_old_pos
        rook_old_x, rook_old_y = move_info.rook_old_pos

        king_is_first_move, rook_is_first_move = move_info.king_is_first_move, move_info.rook_is_first_move

        board[king.x][king.y] = None
        board[rook.x][rook.y] = None

        board[king_old_x][king_old_y] = king
        board[rook_old_x][rook_old_y] = rook

        king.is_first_move = king_is_first_move
        rook.is_first_move = rook_is_first_move

        king.moves(king_old_x, king_old_y)
        rook.moves(rook_old_x, rook_old_y)

        king.is_castle = False

class MoveInfo(ABC):
    def __init__(self, en_passant_pos):
        self.type = None
        self.en_passant_pos = en_passant_pos

class NormalMoveInfo(MoveInfo):
    def __init__(self,en_passant_pos, piece, piece_is_first_move, old_x, old_y, new_x, new_y, captured_piece, move_type = "normal"):
        super().__init__(en_passant_pos)
        self.piece = piece
        self.piece_is_first_move = piece_is_first_move
        self.old_x = old_x
        self.old_y = old_y
        self.new_x = new_x
        self.new_y = new_y
        self.captured_piece = captured_piece
        
        self.type = move_type

    def __repr__(self):
        return f"{self.piece.type} from {map_to_block((self.old_x, self.old_y))} to {map_to_block((self.new_x, self.new_y))}, capture {self.captured_piece}"

class CastleMoveInfo(MoveInfo):
    def __init__(self,en_passant_pos, king, rook, king_is_first_move, rook_is_first_move, 
                 king_old_pos, rook_old_pos, king_new_pos, rook_new_pos):
        super().__init__(en_passant_pos)
        self.type = "castle"

        self.king = king
        self.rook = rook
        self.king_is_first_move = king_is_first_move
        self.rook_is_first_move = rook_is_first_move
        self.king_new_pos = king_new_pos
        self.rook_new_pos = rook_new_pos
        self.rook_old_pos = rook_old_pos
        self.king_old_pos = king_old_pos

    def __repr__(self):
        return f"Castle King to {map_to_block(self.king_new_pos)}"

class Piece(ABC):
    def __init__(self, x, y, color, image, board_size = 8):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.board_size = board_size
        self.is_first_move = True
        self.piece_image = image

    def __repr__(self):
        return f"{self.type}"

    def is_in_bound(self, nx, ny):
        return 0 <= nx < self.board_size and 0 <= ny < self.board_size
    
    @abstractmethod
    def get_legal_moves(self, board, my_pieces, opponent_pieces) -> list:
        pass

    def get_valid_moves(self, board, my_pieces, opponent_pieces):
        legal_moves = self.get_legal_moves(board, my_pieces, opponent_pieces)
        valid_moves = []

        # Check "self - check":
        for move in legal_moves:
            if move['type'] == "normal":
                move_info = make_move(board, self, move, opponent_pieces)
                
                if not is_check(board, my_pieces, opponent_pieces):
                    valid_moves.append(move)
                
                undo_move(board, opponent_pieces, move_info)

            elif move['type'] == "castle" and not is_check(board, my_pieces, opponent_pieces):
                king_new_x, _ = move["new_pos"]
                king_x, king_y = self.x, self.y

                if king_new_x > king_x:
                    squares_to_check = [(king_x + 1, king_y), (king_x + 2, king_y)]
                else:
                    squares_to_check = [(king_x - 1, king_y), (king_x - 2, king_y)]
                
                can_castle = True
                for x, y in squares_to_check:
                    if is_attacked_square(board, x, y, my_pieces, opponent_pieces):
                        can_castle = False
                        break

                if can_castle:
                    valid_moves.append(move)

        return valid_moves

    def moves(self, nx, ny):
        self.x = nx
        self.y = ny

class Knight(Piece):
    def __init__(self, x, y, color, image):
        super().__init__(x, y, color, image)
        self.point = 3
        self.type = "Knight"

    def get_legal_moves(self, board, my_pieces, opponent_pieces) -> list:
        moves = []
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                   (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dx, dy in offsets:
            nx = self.x + dx
            ny = self.y + dy

            if self.is_in_bound(nx, ny) and (board[nx][ny] is None or board[nx][ny].color != self.color):
                move = {
                    "new_pos": (nx, ny),
                    "type": "normal",
                    "captured": board[nx][ny]
                }
                moves.append(move)
            
        return moves
    
class Rook(Piece):
    def __init__(self, x, y, color, image):
        super().__init__(x, y, color, image)
        self.type = "Rook"
        self.point = 5

    def get_legal_moves(self, board, my_pieces, opponent_pieces):
        moves = []
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in direction:
            nx, ny = self.x, self.y
            
            while True:
                nx += dx
                ny += dy

                if not self.is_in_bound(nx, ny):
                    break

                if board[nx][ny] is None:
                    move = {
                        "new_pos": (nx, ny),
                        "type": "normal",
                        "captured": board[nx][ny]
                    }
                    moves.append(move)
                else:
                    if board[nx][ny].color != self.color:
                        move = {
                            "new_pos": (nx, ny),
                            "type": "normal",
                            "captured": board[nx][ny]
                        }
                        moves.append(move)
                    break

        return moves

class Bishop(Piece):
    def __init__(self, x, y, color, image):
        super().__init__(x, y, color, image)
        self.type = "Bishop"
        self.point = 3

    def get_legal_moves(self, board, my_pieces, opponent_pieces):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            nx, ny = self.x, self.y

            while True:
                nx += dx
                ny += dy

                if not self.is_in_bound(nx, ny):
                    break

                if board[nx][ny] is None:
                    move = {
                        "new_pos": (nx, ny),
                        "type": "normal",
                        "captured": board[nx][ny]
                    }
                    moves.append(move)
                else:
                    if board[nx][ny].color != self.color:
                        move = {
                            "new_pos": (nx, ny),
                            "type": "normal",
                            "captured": board[nx][ny]
                        }
                        moves.append(move)
                    break
                
        return moves
    
class Pawn(Piece):
    def __init__(self, x, y, color, image):
        super().__init__(x, y, color, image)
        self.type = "Pawn"
        self.point = 1

        self.direction = -1 if color == "White" else 1

    def get_legal_moves(self, board, my_pieces, opponent_pieces):
        moves = []
        nx = self.x
        ny = self.y + self.direction

        if self.is_in_bound(nx, ny) and board[nx][ny] is None:
            move = {
                "new_pos": (nx, ny),
                "type": "normal",
                "captured": board[nx][ny]
            }
            moves.append(move)

            if self.is_first_move:
                ny2 = self.y + 2 * self.direction

                if self.is_in_bound(nx, ny2) and board[nx][ny2] is None:
                    move = {
                        "new_pos": (nx, ny2),
                        "type": "normal",
                        "captured": board[nx][ny2]
                    }
                    moves.append(move)

        global EN_PASSANT_SQUARE

        for dx in [-1, 1]:
            nx = self.x + dx
            ny = self.y + self.direction

            if self.is_in_bound(nx, ny):

                if board[nx][ny] is not None and board[nx][ny].color != self.color:
                    move = {
                        "new_pos": (nx, ny),
                        "type": "normal",
                        "captured": board[nx][ny]
                    }
                    moves.append(move)

                if (nx, ny) == EN_PASSANT_SQUARE:
                    captured_pawn = board[nx][ny - self.direction]
                    
                    if captured_pawn is not None and captured_pawn.color != self.color:
                        move = {
                            "new_pos": (nx, ny),
                            "type": "en_passant",
                            "captured": captured_pawn,
                            "captured_old_pos": (nx, ny - self.direction)
                        }
                    
                        moves.append(move)
        
        return moves
    
class King(Piece):
    def __init__(self, x, y, color, image):
        super().__init__(x, y, color, image)
        self.type = "King"
        self.point = 0
        self.is_castle = False

    def get_legal_moves(self, board, my_pieces, opponent_pieces) -> list:
        moves = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        
        for dx, dy in offsets:
            nx = self.x + dx
            ny = self.y + dy

            if self.is_in_bound(nx, ny) and (board[nx][ny] is None or board[nx][ny].color != self.color):
                move = {
                    "new_pos": (nx, ny),
                    "type": "normal",
                    "captured": board[nx][ny]
                }
                moves.append(move)

        # Castle move
        if self.is_first_move:
            rook_pieces = [piece for piece in my_pieces if piece.type == "Rook"]
            
            for rook in rook_pieces:
                if rook.is_first_move:
                    can_castle = True

                    for x in range(min(self.x, rook.x) + 1, max(self.x, rook.x)):
                        if board[x][self.y] is not None:
                            can_castle = False
                            break

                    if can_castle:
                        king_nx, king_ny, rook_nx, rook_ny = None, None, None, None
                        if rook.x > self.x: # King side
                            king_nx = self.x + 2
                            king_ny = self.y
                            rook_nx = self.x + 1
                            rook_ny = self.y
                        else: # Queen side
                            king_nx = self.x - 2
                            king_ny = self.y
                            rook_nx = self.x - 1
                            rook_ny = self.y

                        move = {
                            "new_pos": (king_nx, king_ny),
                            "type": "castle",
                            "captured": None,
                            "rook": rook,
                            "rook_new_pos": (rook_nx, rook_ny)
                        }                

                        moves.append(move)

        return moves
    
class Queen(Piece):
    def __init__(self, x, y, color, image):
        super().__init__(x, y, color, image)
        self.type = "Queen"
        self.point = 8

    def get_legal_moves(self, board, my_pieces, opponent_pieces):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            nx, ny = self.x, self.y

            while True:
                nx += dx
                ny += dy

                if not self.is_in_bound(nx, ny):
                    break

                if board[nx][ny] is None:
                    move = {
                        "new_pos": (nx, ny),
                        "type": "normal",
                        "captured": board[nx][ny]
                    }
                    moves.append(move)
                else:
                    if board[nx][ny].color != self.color:
                        move = {
                            "new_pos": (nx, ny),
                            "type": "normal",
                            "captured": board[nx][ny]
                        }
                        moves.append(move)
                    break
                
        return moves