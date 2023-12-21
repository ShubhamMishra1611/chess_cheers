from chess_piece import *

board_white = [
            # [rook(1), knight(1), bishop(1), queen(1), king(1), None, None, rook(1)],
            [rook(1), knight(1), bishop(1), queen(1), king(1), bishop(1), knight(1), rook(1)],
            [pawn(1), pawn(1), pawn(1), pawn(1), pawn(1), pawn(1), pawn(0), pawn(1)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [pawn(0), pawn(0), pawn(0), pawn(0), pawn(0), pawn(0), pawn(0), pawn(0)],
            # [rook(0), knight(0), bishop(0), queen(0), king(0), bishop(0), knight(0), rook(0)] 
            [rook(0), knight(0), bishop(0), queen(0), king(0), None, None, rook(0)] 
        ]

board_black = [
            [rook(0), knight(0), bishop(0), queen(0), king(0), bishop(0), knight(0), rook(0)],
            [pawn(0), pawn(0), pawn(0), pawn(0), pawn(0), pawn(0), pawn(0), pawn(0)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [pawn(1), pawn(1), pawn(1), pawn(1), pawn(1), pawn(1), pawn(1), pawn(1)],
            [rook(1), knight(1), bishop(1), queen(1), king(1), bishop(1), knight(1), rook(1)]
        ]


castle_test = [
            [rook(1), knight(1), bishop(1), queen(1), king(1), None, None, rook(1)],
            [pawn(1), pawn(1), pawn(1), pawn(1), pawn(1), pawn(1), pawn(1), pawn(1)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [pawn(0), pawn(0), pawn(0), pawn(0), pawn(0), pawn(0), pawn(0), pawn(0)],
            [rook(0), knight(0), bishop(0), queen(0), king(0), None, None, rook(0)] 
        ]
en_passant = [
            [rook(1), knight(1), bishop(1), queen(1), king(1), None, None, rook(1)],
            [pawn(1), pawn(1), pawn(1), pawn(1), pawn(1), pawn(1), pawn(1), pawn(1)],
            [None, None, None, None, None, None, None, None],
            [None, pawn(0), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [pawn(0), pawn(0), pawn(0), pawn(0), pawn(0), pawn(0), pawn(0), pawn(0)],
            [rook(0), knight(0), bishop(0), queen(0), king(0), None, None, rook(0)] 
        ]

mate_in_one =  [
    [None, None, None, None, None, None, None, king(1)],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [rook(1), None, None, king(0), None, None, None, rook(1)],
    [None, None, None, None, None, None, None, None]
]




if __name__ == "__main__":
    # print beautiful board
    for row in board_white:
        print(row)
        print("\n")
    

