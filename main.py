from Engine import *

if __name__ == "__main__":
    white_pieces, black_pieces, board = init()

    play_chess(board=board, white_pieces=white_pieces, black_pieces=black_pieces, depth=5, turn="White")



