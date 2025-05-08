from abc import ABC, abstractmethod
# from ChessState import ChessState

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
    def get_legal_moves(self, chess_state) -> list:
        pass

    def get_valid_moves(self, chess_state):
        legal_moves = self.get_legal_moves(chess_state)
        valid_moves = []

        # * Self check
        for move in legal_moves:
            move_info = chess_state.make_move(self, move)
            if not chess_state.is_in_check(self.color):
                valid_moves.append(move)

            chess_state.undo_move(move_info)
        
        return valid_moves

    def moves(self, nx, ny):
        self.x = nx
        self.y = ny


class Knight(Piece):
    def __init__(self, x, y, color, image):
        super().__init__(x, y, color, image)
        self.point = 3
        self.type = "Knight"

    def get_legal_moves(self, chess_state) -> list:
        moves = []
        board = chess_state.board
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

    def get_legal_moves(self, chess_state):
        moves = []
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        board = chess_state.board
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

    def get_legal_moves(self, chess_state):
        board = chess_state.board

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

    def get_legal_moves(self, chess_state) -> list:
        board = chess_state.board
        moves = []
        one_step_y = self.y + self.direction

        # forward
        if self.is_in_bound(self.x, one_step_y) and board[self.x][one_step_y] is None:
            move_type = "promotion" if one_step_y in (0, self.board_size-1) else "normal"
            moves.append({
                "new_pos": (self.x, one_step_y),
                "type": move_type,
                "captured": None
            })

            # double
            if self.is_first_move:
                two_step_y = self.y + 2 * self.direction
                if self.is_in_bound(self.x, two_step_y) and board[self.x][two_step_y] is None:
                    moves.append({
                        "new_pos": (self.x, two_step_y),
                        "type": "normal",
                        "captured": None
                    })

        # captures
        for dx in (-1, 1):
            nx, ny = self.x + dx, one_step_y
            if not self.is_in_bound(nx, ny):
                continue

            target = board[nx][ny]
            if target is not None and target.color != self.color:
                move_type = "promotion" if ny in (0, self.board_size-1) else "normal"
                moves.append({
                    "new_pos": (nx, ny),
                    "type": move_type,
                    "captured": target
                })

            # en passant
            if (nx, ny) == chess_state.en_passant:
                captured = board[nx][ny - self.direction]
                moves.append({
                    "new_pos": (nx, ny),
                    "type": "normal",
                    "captured": captured,
                })

        return moves
    
class King(Piece):
    def __init__(self, x, y, color, image):
        super().__init__(x, y, color, image)
        self.type = "King"
        self.point = 0
        self.is_castle = False

    def get_legal_moves(self, chess_state) -> list:
        moves = []
        board = chess_state.board
        my_pieces = chess_state.white_pieces if self.color == "White" else chess_state.black_pieces

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

    def get_legal_moves(self, chess_state):
        board = chess_state.board
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

