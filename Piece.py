from abc import ABC, abstractmethod

def map_to_block(pos, board_size=8):
    x, y = pos 
    return chr(x + 65) + str(board_size - y)

def init(board_size = 8):
    white_pieces = [Rook(0, 7, "White"), Knight(1, 7, "White"), Bishop(2, 7, "White"), 
                    Queen(3, 7, "White"), King(4, 7, "White"), Bishop(5, 7, "White"), 
                    Knight(6, 7, "White"), Rook(7, 7, "White")]
    
    for x in range(board_size):
        white_pieces.append(Pawn(x, 6, "White"))

    black_pieces = [Rook(0, 0, "Black"), Knight(1, 0, "Black"), Bishop(2, 0, "Black"),
                    Queen(3, 0, "Black"), King(4, 0, "Black"), Bishop(5, 0, "Black"), 
                    Knight(6, 0, "Black"), Rook(7, 0, "Black")]
    
    for x in range(board_size):
        black_pieces.append(Pawn(x, 1, "Black"))

    board = [[None for _ in range(board_size)] for _ in range(board_size)]

    for piece in white_pieces:
        board[piece.x][piece.y] = piece

    for piece in black_pieces:
        board[piece.x][piece.y] = piece

    return white_pieces, black_pieces, board

def is_attacked_square(board, nx, ny, opponent_pieces):
    for piece in opponent_pieces:
        moves = piece.get_legal_moves(board)

        if any(x == nx and y == ny for (x, y) in moves):
            return True
        
    return False

def is_check(board, my_pieces, opponent_pieces):
    my_king = [piece for piece in my_pieces if piece.type == "King"][0]

    return is_attacked_square(board, my_king.x, my_king.y, opponent_pieces)

def is_checkmate(board, my_pieces, opponent_pieces):
    if not is_check(board, my_pieces, opponent_pieces):
        return False
    
    moves = []
    for piece in my_pieces:
        moves += piece.get_valid_moves(board, my_pieces, opponent_pieces)

    return len(moves) == 0

def make_move(board, piece, nx, ny, opponent_pieces):
    captured = board[nx][ny]
    move_info = MoveInfo(piece, piece.x, piece.y, nx, ny, captured)

    if captured is not None:
        opponent_pieces.remove(captured)

    board[piece.x][piece.y] = None
    board[nx][ny] = piece

    piece.moves(nx, ny)

    return move_info

def undo_move(board, opponent_pieces, move_info):
    piece = move_info.piece
    old_x = move_info.old_x
    old_y = move_info.old_y
    new_x = move_info.new_x
    new_y = move_info.new_y
    captured_piece = move_info.captured_piece

    board[old_x][old_y] = piece
    board[new_x][new_y] = captured_piece

    piece.moves(old_x, old_y)
    
    if captured_piece is not None:
        opponent_pieces.append(captured_piece)

class MoveInfo:
    def __init__(self, piece, old_x, old_y, new_x, new_y, captured_piece):
        self.piece = piece
        self.old_x = old_x
        self.old_y = old_y
        self.new_x = new_x
        self.new_y = new_y
        self.captured_piece = captured_piece

    def __repr__(self):
        return f"(piece={self.piece}, from={map_to_block((self.old_x, self.old_y))}, to={map_to_block((self.new_x, self.new_y))}, captured={self.captured_piece})"

class Piece(ABC):
    def __init__(self, x, y, color, board_size = 8):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.board_size = board_size

    def __repr__(self):
        return f"{self.type}"

    def is_in_bound(self, nx, ny):
        return 0 <= nx < self.board_size and 0 <= ny < self.board_size
    
    @abstractmethod
    def get_legal_moves(self, board) -> list:
        pass

    def get_valid_moves(self, board, my_pieces, opponent_pieces):
        legal_moves = self.get_legal_moves(board)
        valid_moves = []

        # Check "self - check":
        for nx, ny in legal_moves:
            move_info = make_move(board, self, nx, ny, opponent_pieces)
            
            if not is_check(board, my_pieces, opponent_pieces):
                valid_moves.append((nx, ny))
            
            undo_move(board, opponent_pieces, move_info)

        return valid_moves

    def moves(self, nx, ny):
        self.x = nx
        self.y = ny

class Knight(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.point = 3
        self.type = "Knight"

    def get_legal_moves(self, board) -> list:
        moves = []
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                   (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dx, dy in offsets:
            nx = self.x + dx
            ny = self.y + dy

            if self.is_in_bound(nx, ny) and (board[nx][ny] is None or board[nx][ny].color != self.color):
                moves.append((nx, ny))
            
        return moves
    
class Rook(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.type = "Rook"
        self.point = 5

    def get_legal_moves(self, board):
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
                    moves.append((nx, ny))
                else:
                    if board[nx][ny].color != self.color:
                        moves.append((nx, ny))
                    break

        return moves

class Bishop(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.type = "Bishop"
        self.point = 3

    def get_legal_moves(self, board):
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
                    moves.append((nx, ny))
                else:
                    if board[nx][ny].color != self.color:
                        moves.append((nx, ny))
                    break
                
        return moves
    
class Pawn(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.type = "Pawn"
        self.point = 1

        self.direction = -1 if color == "White" else 1

    def get_legal_moves(self, board):
        moves = []
        nx = self.x
        ny = self.y + self.direction

        if self.is_in_bound(nx, ny) and board[nx][ny] is None:
            moves.append((nx, ny))

            if (self.color == "White" and self.y == 6) or (self.color == "Black" and self.y == 1):
                ny2 = self.y + 2 * self.direction

                if self.is_in_bound(nx, ny2) and board[nx][ny2] is None:
                    moves.append((nx, ny2))

        for dx in [-1, 1]:
            nx = self.x + dx
            ny = self.y + self.direction

            if self.is_in_bound(nx, ny):

                if board[nx][ny] is not None and board[nx][ny].color != self.color:
                    moves.append((nx, ny))

        return moves
    
class King(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.type = "King"
        self.point = 0

    def get_legal_moves(self, board) -> list:
        moves = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        
        for dx, dy in offsets:
            nx = self.x + dx
            ny = self.y + dy

            if self.is_in_bound(nx, ny) and (board[nx][ny] is None or board[nx][ny].color != self.color):
                moves.append((nx, ny))

        return moves
    
class Queen(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.type = "Queen"
        self.point = 8

    def get_legal_moves(self, board):
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
                    moves.append((nx, ny))
                else:
                    if board[nx][ny].color != self.color:
                        moves.append((nx, ny))
                    break
                
        return moves