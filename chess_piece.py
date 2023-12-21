class chess_piece:
    def __init__(self, name:str, color:0|1, img_file:str = None) -> None:
        self.name = name
        self.__has_moved = False
        self.__color = color # 0:White, 1 Black
        self.board_x = 0
        self.board_y = 0

    def __repr__(self) -> str:
        return f"{self.name}, Color: {self.__color}, has_moved: {self.__has_moved}"
    
    def get_color(self):
        return self.__color
    
    def set_color(self, color):
        if color not in [0, 1]:
            raise "Color not valid"
        else:
            self.__color = color
            self.__repr__()
    
    def has_moved(self):
        return self.__has_moved
    
    def set_has_moved(self, value:bool):
        if type(value) is not bool:
            raise "Invalid type value for has_moved property; Use bool type only"
        else:
            self.__has_moved = value
            self.__repr__()

    def valid_moves(self, x:int, y:int):
        pass

import json
piece_file_dict = None
with open('piece_dict.json') as f:
    piece_file_dict = json.load(f)
piece_file_dict = piece_file_dict['0']

class rook(chess_piece):
    def __init__(self, color: 0 | 1, img_file: str = None) -> None:
        super().__init__('rook', color, img_file)
        self.color = color
        self.img_file = piece_file_dict['R' if color == 0 else 'r']
        

    def valid_moves(self, x: int, y: int):
        all_moves = [
                        zip([y]*8, range(x+1, 8)),
                        zip([y]*8, range(x-1, -1, -1)),
                        zip(range(y+1, 8), [x]*8),
                        zip(range(y-1, -1, -1), [x]*8)
                    ]
        return all_moves
    
class bishop(chess_piece):
    def __init__(self,  color: 0 | 1, img_file: str = None) -> None:
        super().__init__('bishop', color, img_file)
        self.color = color
        self.img_file = piece_file_dict['B' if color == 0 else 'b']
    
    def valid_moves(self, x: int, y: int):
        all_moves = [
                        zip(range(y+1, 8), range(x+1,8)),
                        zip(range(y+1, 8), range(x-1, -1, -1)),
                        zip(range(y-1, -1, -1), range(x+1, 8)),
                        zip(range(y-1, -1, -1), range(x-1, -1, -1))
                    ]
        return all_moves
    
class knight(chess_piece):
    def __init__(self,  color: 0 | 1, img_file: str = None) -> None:
        super().__init__('knight', color, img_file)
        self.color = color
        self.img_file = piece_file_dict['N' if color == 0 else 'n']
    
    def valid_moves(self, x: int, y: int):
        all_moves = [
                            [y-1, x+2],
                            [y-2, x+1],
                            [y-1, x-2],
                            [y-2, x-1],
                            [y+1, x-2],
                            [y+1, x+2],
                            [y+2, x+1],
                            [y+2, x-1]
                        ]
        return all_moves
    
class king(chess_piece):
    def __init__(self,  color: 0 | 1, img_file: str = None) -> None:
        super().__init__('king', color, img_file)
        self.color = color
        self.in_check = False
        self.img_file = piece_file_dict['K' if color == 0 else 'k']
    
    def valid_moves(self, x: int, y: int):
        all_moves = [
                        [y+1, x],
                        [y+1, x+1],
                        [y+1, x-1],
                        [y-1, x],
                        [y-1, x+1],
                        [y-1, x-1],
                        [y, x-1],
                        [y, x+1]
                    ]
        return all_moves
    
class queen(chess_piece):
    def __init__(self,  color: 0 | 1, img_file: str = None) -> None:
        super().__init__('queen', color, img_file)
        self.color = color
        self.img_file = piece_file_dict['Q' if color == 0 else 'q']
    
    def valid_moves(self, x: int, y: int):
        all_moves = [
                        zip([y]*8, range(x+1, 8)),
                        zip([y]*8, range(x-1, -1, -1)),
                        zip(range(y+1, 8), [x]*8),
                        zip(range(y-1, -1, -1), [x]*8),
                        zip(range(y+1, 8), range(x+1,8)),
                        zip(range(y+1, 8), range(x-1, -1, -1)),
                        zip(range(y-1, -1, -1), range(x+1, 8)),
                        zip(range(y-1, -1, -1), range(x-1, -1, -1))
                    ]
        return all_moves

class pawn(chess_piece):
    def __init__(self,  color: 0 | 1, img_file: str = None) -> None:
        super().__init__('pawn', color, img_file)
        self.color = color
        self.direction = -1 
        self.has_moved_two = False
        self.img_file = piece_file_dict['P' if color == 0 else 'p']
    
    def valid_moves(self, x: int, y: int):
        all_moves = [
                        [y+self.direction, x] # normal
                    ]
        return all_moves
