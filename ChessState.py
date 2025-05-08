import Piece

from dataclasses import dataclass
from typing import Optional, Tuple, Any, List

from collections import Counter

@dataclass
class MoveInfo:
    type: str # * ["Normal", "Castle", "Promotion"]
    # * Piece info
    piece            :  Any 
    from_pos         :  Tuple[int, int]
    to_pos:             Tuple[int, int]
    piece_first_move :  bool

    # * Captured info
    captured         :  Optional[Any]             = None
    captured_old_pos :  Optional[Tuple[int,int]]  = None  

    en_passant_prev  :  Optional[Tuple[int, int]] = None

    # * Castle info
    rook             :  Optional[Any]             = None
    rook_from        :  Optional[Tuple[int,int]]  = None
    rook_to          :  Optional[Tuple[int,int]]  = None
    rook_first_move  :  bool                      = False
    
    # * Promotion info
    promotion        :  Optional[Any]             = None
    promotion_from   :  Optional[Tuple[int,int]]  = None
    

class ChessState:
    def __init__(self, white_pieces: List[Any], black_pieces: List[Any], images: dict, board_size: int = 8):
        self.board_size = board_size
        self.white_pieces = white_pieces
        self.black_pieces = black_pieces
        self.images = images

        self.board = [[None for _ in range(board_size)] for _ in range(board_size)]

        for p in white_pieces + black_pieces:
            self.board[p.x][p.y] = p

        self.en_passant: Optional[Tuple[int,int]] = None
        self.state_counter = Counter()

    @classmethod
    def init_begin_state(cls, piece_images, board_size: int = 8):
        white_pieces = [
            Piece.Rook(0, 7, "White", piece_images["white_rook"]),
            Piece.Knight(1, 7, "White", piece_images["white_knight"]),
            Piece.Bishop(2, 7, "White", piece_images["white_bishop"]),
            Piece.Queen(3, 7, "White", piece_images["white_queen"]),
            Piece.King(4, 7, "White", piece_images["white_king"]),
            Piece.Bishop(5, 7, "White", piece_images["white_bishop"]),  
            Piece.Knight(6, 7, "White", piece_images["white_knight"]),  
            Piece.Rook(7, 7, "White", piece_images["white_rook"])
        ]
        
        for x in range(board_size):
            white_pieces.append(Piece.Pawn(x, 6, "White", piece_images["white_pawn"]))
        
        black_pieces = [
            Piece.Rook(0, 0, "Black", piece_images["black_rook"]),
            Piece.Knight(1, 0, "Black", piece_images["black_knight"]),
            Piece.Bishop(2, 0, "Black", piece_images["black_bishop"]),
            Piece.Queen(3, 0, "Black", piece_images["black_queen"]),
            Piece.King(4, 0, "Black", piece_images["black_king"]),
            Piece.Bishop(5, 0, "Black", piece_images["black_bishop"]),  
            Piece.Knight(6, 0, "Black", piece_images["black_knight"]),  
            Piece.Rook(7, 0, "Black", piece_images["black_rook"])
        ]

        for x in range(board_size):
            black_pieces.append(Piece.Pawn(x, 1, "Black", piece_images["black_pawn"]))

        return cls(white_pieces, black_pieces, piece_images, board_size)

    def _add_piece(self, piece: Any, x: int, y: int):
        lst = self.white_pieces if piece.color == 'White' else self.black_pieces
        lst.append(piece)
        self.board[x][y] = piece

    def _remove_piece(self, piece: Any):
        lst = self.white_pieces if piece.color=='White' else self.black_pieces
        lst.remove(piece)
        self.board[piece.x][piece.y] = None

    def _move_piece(self, piece: Any, src: Tuple[int,int], dst: Tuple[int,int]):
        sx, sy = src; dx, dy = dst

        self.board[sx][sy] = None
        self.board[dx][dy] = piece

        piece.moves(dx, dy)

    def _replace_piece(self, old: Any, new: Any):
        lst = self.white_pieces if old.color=='White' else self.black_pieces
        idx = lst.index(old)
        lst[idx] = new

    def map_to_block(self, pos, board_size=8):
        x, y = pos 
        return chr(x + 65) + str(board_size - y)
    
    def map_to_sym(self, type):
        if type == "Knight":
            return "N"
        return type[0]

    def make_move(self, piece, move) -> MoveInfo:
        captured = move["captured"]
        move_info = MoveInfo(
            type                =   move["type"],
            piece               =   piece,
            from_pos            =   (piece.x, piece.y),
            piece_first_move    =   piece.is_first_move,
            to_pos              =   move["new_pos"],
            captured            =   captured,
            captured_old_pos    =   (captured.x, captured.y) if captured else None,
            en_passant_prev     =   self.en_passant
        )        

        if captured:
            self._remove_piece(captured)

        # * Update en_passant
        if piece.type == 'Pawn' and abs(move_info.to_pos[1] - move_info.from_pos[1]) == 2:
            self.en_passant = (move_info.to_pos[0], (move_info.from_pos[1] + move_info.to_pos[1]) // 2)
        else:
            self.en_passant = None

        self._move_piece(piece, (move_info.from_pos), (move_info.to_pos))
        piece.is_first_move = False

        if move_info.type == 'castle':
            rook                        = move['rook']
            move_info.rook              = rook
            move_info.rook_first_move   = rook.is_first_move
            move_info.rook_from         = (rook.x, rook.y)
            move_info.rook_to           = move['rook_new_pos']

            self._move_piece(rook, move_info.rook_from, move_info.rook_to)
            rook.is_first_move = False

        elif move_info.type == 'promotion':
            promoted                    = Piece.Queen(move_info.to_pos[0], move_info.to_pos[1], piece.color, self.images[f"{piece.color.lower()}_queen"])
            move_info.promotion         = promoted
            move_info.promotion_from    = move_info.from_pos

            self._replace_piece(piece, promoted)

            self.board[move_info.to_pos[0]][move_info.to_pos[1]] = promoted

        return move_info
    
    def undo_move(self, move_info: MoveInfo) -> None:
        self.en_passant = move_info.en_passant_prev

        if move_info.type == 'promotion':
            self._replace_piece(move_info.promotion, move_info.piece)
            self._move_piece(move_info.piece, move_info.promotion_from, move_info.promotion_from)
        
        elif move_info.type == 'castle':
            self._move_piece(move_info.rook, move_info.rook_to, move_info.rook_from)
            move_info.rook.is_first_move = move_info.rook_first_move

        self._move_piece(move_info.piece, move_info.to_pos, move_info.from_pos)
        move_info.piece.is_first_move = move_info.piece_first_move

        if move_info.captured:
            pos = move_info.captured_old_pos or move_info.to_pos
            self._add_piece(move_info.captured, pos[0], pos[1])

    def is_attacked(self, x, y, attack_turn):
        attackers = self.white_pieces if attack_turn == "White" else self.black_pieces
        for piece in attackers:
            moves = piece.get_legal_moves(self)

            for move in moves:
                if move['new_pos'] == (x, y):
                    return True
                
        return False
    
    def is_in_check(self, turn):
        pieces = self.white_pieces if turn == "White" else self.black_pieces
        king = next((p for p in pieces if p.type=='King'), None)

        return self.is_attacked(king.x, king.y, 'Black' if turn=='White' else 'White')
    
    def is_checkmate(self, turn):
        if not self.is_in_check(turn):
            return False
        
        pieces = self.white_pieces if turn=='White' else self.black_pieces

        for piece in pieces:
            moves = piece.get_legal_moves(self)

            for move in moves:
                move_info = self.make_move(piece, move)
                in_check = self.is_in_check(turn)
                self.undo_move(move_info)

                if not in_check:
                    return False
                
        return True
    
    def is_stalemate(self, turn):
        if self.is_in_check(turn):
            return False
        
        pieces = self.white_pieces if turn=='White' else self.black_pieces

        for piece in pieces:
            moves = piece.get_legal_moves(self)

            for move in moves:
                move_info = self.make_move(piece, move)
                in_check = self.is_in_check(turn)
                self.undo_move(move_info)

                if not in_check:
                    return False
                
        return True
    
    def is_insufficient_material(self) -> bool:
        all_p = self.white_pieces + self.black_pieces
        types = [p.type for p in all_p]

        if types.count('King')==2 and len(all_p)==2:
            return True

        if len(all_p)==3 and types.count('King')==2 and ('Bishop' in types or 'Knight' in types):
            return True
        
        return False
        
    def get_castle_rights(self):
        rights_white, rights_black = [], []

        # * White
        wking = next(p for p in self.white_pieces if p.type=="King")
        if wking.is_first_move:
            for rook_pos, flag in [((7,7),"K"), ((0,7),"Q")]:
                rook = next((r for r in self.white_pieces if r.type=="Rook" and (r.x,r.y)==rook_pos), None)
                if rook and rook.is_first_move:
                    rights_white.append(flag)

        # * Black
        bking = next(p for p in self.black_pieces if p.type=="King")
        if bking.is_first_move:
            for rook_pos, flag in [((7,0),"k"), ((0,0),"q")]:
                rook = next((r for r in self.black_pieces if r.type=="Rook" and (r.x,r.y)==rook_pos), None)
                if rook and rook.is_first_move:
                    rights_black.append(flag)

        return [rights_white, rights_black]

    def encode_state(self, turn: str) -> str:
        # Board layout
        rows = []
        for y in range(self.board_size-1, -1, -1):
            empty = 0
            row = ""
            for x in range(self.board_size):
                p = self.board[x][y]
                if p is None:
                    empty += 1
                else:
                    if empty:
                        row += str(empty)
                        empty = 0
                    sym = self.map_to_sym(p.type)
                    row += sym.upper() if p.color=='White' else sym.lower()
            if empty:
                row += str(empty)
            rows.append(row)
        board_fen = "/".join(rows)

        stm = 'w' if turn.lower().startswith('w') else 'b'

        rights_white, rights_black = self.get_castle_rights()
        cr = ''.join(rights_white + rights_black) or '-'

        ep = self.map_to_block(self.en_passant) if self.en_passant else '-'

        return f"{board_fen} {stm} {cr} {ep}"

    def record_state(self, turn):
        key = self.encode_state(turn)
        self.state_counter[key] += 1

        return self.state_counter[key]

    def is_threefold_repetition(self, turn: str) -> bool:
        key = self.encode_state(turn)

        return self.state_counter.get(key,0) >= 3

    def detect_draw(self, turn: str):
        if self.is_stalemate(turn):
            return "Draw by stalemate"
        if self.is_insufficient_material():
            return "Draw by insufficient material "
        if self.is_threefold_repetition(turn):
            return "Draw by threefold repetition"
        
        return None