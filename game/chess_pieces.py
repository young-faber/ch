class Piece():
    def __init__(self, side: str, row: int, col: int):
        self.side = side
        self._row = row
        self._col = col
        self.is_first_move = True
        self.appearence = ''
        self.moves = []
    
    def __repr__(self) -> str: 
        return self.appearence

    @property
    def row(self):
        return self._row
    
    @row.setter
    def row(self, value):
        if 0 <= value <= 8:
            self._row = value
        else:
            raise ValueError('Невозможный ход')

    @property
    def col(self):
        return self._col
    
    @col.setter
    def col(self, value):
        if 0 <= value <= 8:
            self._col = value
        else:
            raise ValueError('Невозможный ход')

    def is_valid_move(self, new_row: int, new_col: int) -> bool:
        '''проверка с точки зрения фигуры'''
        if (0 <= new_row <= 8 and 0 <= new_col <= 8) and (self.row != new_row and self.col != new_col): 
            return True
        else:
            return False
        
    def calc_attack_moves(self):
        '''s'''
        self.moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    self.moves.append([row, col])
        

class Pawn(Piece):
    def __init__(self, side, row, col):
        super().__init__(side, row, col)
        self.appearence = 'Pb' if self.side == 'black' else 'Pw'
    

    def is_valid_move(self, new_row: int, new_col: int) -> bool:
        if self.side == 'black':
            if self.is_first_move: 
                if new_row - self.row in [1,2] and self.col == new_col:
                    return True
            else:
                if new_row - self.row in [1] and self.col == new_col:
                    return True
        else: 
            if self.is_first_move:
                if self.row - new_row in [1,2] and self.col == new_col:
                    return True
            else:
                if self.row - new_row in [1] and self.col == new_col:
                    return True
        return False
        
    
class Knight(Piece):
    def __init__(self, side, row, col):
        super().__init__(side, row, col)
        self.appearence = 'Nb' if self.side == 'black' else 'Nw'

    def is_valid_move(self, new_row: int, new_col: int) -> bool:
        if (abs(self.row - new_row) == 2 and abs(self.col - new_col) == 1 or abs(self.row - new_row) == 1 and abs(self.col - new_col) == 2):
            return True
        return False
        
    
            

class Bishop(Piece):
    def __init__(self, side, row, col):
        super().__init__(side, row, col)
        self.appearence = 'Bb' if self.side == 'black' else 'Bw'

    def is_valid_move(self, new_row: int, new_col: int) -> bool:
        if abs(new_row - self.row) == abs(new_col - self.col):
            return True
        return False
         

class Rook(Piece):
    def __init__(self, side, row, col):
        super().__init__(side, row, col)
        self.appearence = 'Rb' if self.side == 'black' else 'Rw'

    def is_valid_move(self, new_row: int, new_col: int) -> bool:
        if (self.row == new_row or self.col == new_col) and not (self.row == new_row and self.col == new_col):
            return True
        return False
    
    # def calc_attack_moves(self):
    #     pass

class Queen(Piece):
    def __init__(self, side, row, col):
        super().__init__(side, row, col)
        self.appearence = 'Qb' if self.side == 'black' else 'Qw'
    
    def is_valid_move(self, new_row: int, new_col: int) -> bool:
        if abs(new_row - self.row) == abs(new_col - self.col) or (self.row == new_row or self.col == new_col):
            return True
        return False

class King(Piece):
    def __init__(self, side, row, col):
        super().__init__(side, row, col)
        self.appearence = 'Kb' if self.side == 'black' else 'Kw'

    def is_valid_move(self, new_row: int, new_col: int) -> bool:
        if (abs(self.row - new_row) == 1 and abs(self.col - new_col) == 0) or abs(self.row - new_row) == 1 and abs(self.col - new_col) == 1 or abs(self.row - new_row) == 0 and abs(self.col - new_col) == 1:
            return True
        return False
    
if __name__ == '__main__':
    f = Pawn('black', 1, 1)
    print(isinstance(f, Piece))
    print(f.row)
    f.row = 2
    f.col = 2
    print(f.row)
    print(str(f))
    print('1')
