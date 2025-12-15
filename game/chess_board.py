from .chess_pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King, pieces_cls

# from game.chess_pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King
from pprint import pprint
from typing import List, Dict
from copy import deepcopy # <----- ?
import json


class GameBoard:  # или игра?
    def __init__(self, new_game=True, board_str=None, current=None):
        self.board = [[None for i in range(8)] for i in range(8)]
        self.white_attack_map = [[0 for i in range(8)] for i in range(8)]
        self.black_attack_map = [[0 for i in range(8)] for i in range(8)]
        if new_game:
            self.current = "white"
            self.kw = [0, 0]
            self.kb = [0, 0]
            # check = None

            self.board[1][0] = Pawn("black", 1, 7)
            self.board[1][6] = Pawn('white', 1, 6, False)
            # self.board[5][5] = Rook('white', 5, 5)

            for col in range(2):
                self.board[6][col] = Pawn("white", 6, col)
                # self.board[1][col] = Pawn("black", 1, col)
            self.board[7][4] = King("white", 7, 4)
            self.board[0][4] = King("black", 0, 4)

            # self.board[7][3] = Queen("white", 7, 3)
            # self.board[0][3] = Queen('black', 0, 3)

            # self.board[7][2] = Bishop("white", 7, 2)
            # self.board[0][2] = Bishop("black", 0, 2)
            # self.board[7][5] = Bishop("white", 7, 5)
            # self.board[0][5] = Bishop("black", 0, 5)

            # self.board[7][1] = Knight("white", 7, 1)
            # self.board[0][1] = Knight("black", 0, 1)
            # self.board[7][6] = Knight("white", 7, 6)
            # self.board[0][6] = Knight("black", 0, 6)

            self.board[7][0] = Rook("white", 7, 0)
            self.board[0][0] = Rook("black", 0, 7)
            self.board[7][7] = Rook("white", 7, 7)
            self.board[0][7] = Rook("black", 0, 0)
        else:
            if not board_str:
                raise TypeError("ты не передал доску")
            self.desearialize_board(board_str, current)

    def board_str_func(self) -> List[List]:
        board = []
        for row in range(8):
            row_data = []
            for col in range(8):
                square = self.board[row][col]
                if square:
                    # гарантируем строку
                    row_data.append(str(square.appearence))
                else:
                    row_data.append("")
            board.append(row_data)
        return board

    def searialize_board(self) -> List[Dict]:
        board = []
        for row in range(8):
            for col in range(8):
                square: Piece = self.board[row][col]
                if square:
                    dic = {
                        "cls": type(square).__name__,
                        "side": square.side,
                        "row": square.row,
                        "col": square.col,
                        "is_first_move": square.is_first_move,
                    }
                    board.append(dic)
        return board

    def desearialize_board(self, board_str, current: str):
        self.current = current
        board_list = json.loads(board_str)
        for figure in board_list:
            row = figure["row"]
            col = figure["col"]
            self.board[row][col] = pieces_cls[figure["cls"]](
                figure["side"], row, col, figure["is_first_move"]
            )
            if figure["cls"] == 'King':
                if figure["side"] == 'white':
                    self.kw = [row, col]
                    print('1 desearialize succes: king white = true')
                else:
                    print('2 dsrl sccs: king black = true')
                    self.kb = [row, col]
        self.calc_attack_map(side=current)

    def move_figure(self, row, col, row2, col2):
        figure: Piece = self.board[row][col]
        if not figure:
            return False
            
        if self.current != figure.side:
            return 'сейчас не ваш ход'

        
        move = [row2, col2]

        if move in figure.moves:
            #на самом деле не временно, если перенести то что касается мата 
            # Временно делаем ход
            temp_piece = self.board[row2][col2]
            self.board[row2][col2] = figure
            self.board[row][col] = None
            old_row, old_col = figure.row, figure.col
            figure.row = row2
            figure.col = col2

            if isinstance(figure, Pawn): #Pawn
                pawn: Pawn = figure
                if pawn.side == 'white':
                    if row2 == 0:
                        print('p_pw')
                        return 'pawn_promotion'
                if pawn.side == 'black':
                    if row2 == 7:
                        print('p_pb')
                        return 'pawn_promotion'

            # # Пересчитываем карту атак противника после хода
            # enemy_side = "black" if self.current == "white" else "white"
            # self.calc_attack_map(enemy_side)

            # # Проверяем, остается ли король под шахом после хода
            # king_pos = self.kw if self.current == "white" else self.kb
            # king_row, king_col = king_pos

            # if ((self.current == "white" and self.black_attack_map[king_row][king_col] > 0) or 
            #     (self.current == "black" and self.white_attack_map[king_row][king_col] > 0)):
            #     # Возвращаем ход назад, так как король остается под шахом
            #     self.board[row][col] = figure
            #     self.board[row2][col2] = temp_piece
            #     figure.row = old_row
            #     figure.col = old_col
            #     raise ValueError("Король остается под шахом после этого хода")

            # # Ход допустим - фиксируем изменения
            # figure.is_first_move = False
            # self.current = "black" if self.current == "white" else "white"
            return 'success'
        return "Невозможный ход"

    def is_free_move(self, move, figure: Piece):
        if self.board[move[0]][move[1]]:
            if self.board[move[0]][move[1]].side == figure.side:
                return False
        if figure.row == move[0] and figure.col != move[1]:
            min_col = min(figure.col, move[1])
            max_col = max(figure.col, move[1])
            for col in range(min_col + 1, max_col):
                if self.board[move[0]][col]:
                    return False
        if abs(figure.row - move[0]) == abs(figure.col - move[1]):
            min_col = min(figure.col, move[1])
            max_col = max(figure.col, move[1])
            min_row = min(figure.row, move[0])
            max_row = max(figure.row, move[0])
            lst_squares = zip(range(min_row + 1, max_row), range(min_col + 1, max_col))
            for row, col in lst_squares:
                if self.board[row][col]:
                    return False
        if figure.row != move[0] and figure.col == move[1]:
            """Фигура делает ход в столбик (только row меняется)"""
            min_row = min(figure.row, move[0])
            max_row = max(figure.row, move[0])
            for row in range(min_row + 1, max_row):
                if self.board[row][move[1]]:
                    return False
        return True

    def clean_attack_moves(self, figure: Piece):
        for move in figure.moves.copy():
            if not self.is_free_move(move, figure):
                figure.moves.remove(move)

    def calc_attack_map(

        self, side
    ):#тут для тех кому поставили шах, if check true, calc_defence_map, для каждой фигуры как калк атак мэп, спасает 
        # для каждой фигуры считает calc_attack_moves + clean_attack_moves
        for row in range(8):
            for col in range(8):
                figure: Piece = self.board[row][col]
                if figure and figure.side == side:
                    figure.calc_attack_moves()
                    print(figure.appearence, figure.moves)
                    self.clean_attack_moves(figure)
                    print("Х", figure.appearence, figure.moves)
                    if isinstance(figure, King):
                        if side == "black":
                            self.kb = [row,col]
                        elif side == "white":
                            self.kw = [row,col]
                        self.is_castling_possible(side)
                        print("castling check happend")
                        

                    for move in figure.moves:
                        r, c = move  # переименовали переменные
                        if side == "black":
                            self.black_attack_map[r][c] += 1
                        elif side == "white":
                            self.white_attack_map[r][c] += 1

        
    def is_castling_possible(self, side):
        '''Короче, сделать метод который считает сходилили ладьи и король и междус ними свободно ли
        если нет, то добавляем move для короля влева 2 врпаов 2'''

        
        king: King = self.board[self.kb[0]][self.kb[1]] if side == 'black' else self.board[self.kw[0]][self.kw[1]]


        if king.is_first_move:
            print("first move succes")
            if king.side == 'white':
                print("king white")
                if isinstance(self.board[7][0], Rook):#если че в 212,213,216 было не self, а game
                    print("rook check")
                    rook: Rook = self.board[7][0]
                    if rook.is_first_move: 
                        print("rook first move check")
                        if self.is_free_move([7, 1], king):
                            print("castle is possible") 
                            king.moves.append([7,2])
                            self.white_attack_map[7][2] += 1 
                if isinstance(self.board[7][7], Rook):
                    rook: Rook = self.board[7][7]
                    if rook.is_first_move:
                        if self.is_free_move([7, 6], king):
                            king.moves.append([7,6])
                            self.white_attack_map[7][6] += 1
            if king.side == 'black':
                print("king white")
                if isinstance(self.board[0][0], Rook):#если че в 212,213,216 было не self, а game
                    print("rook check")
                    rook: Rook = self.board[0][0]
                    if rook.is_first_move: 
                        print("rook first move check")
                        if self.is_free_move([0, 1], king):
                            print("castle is possible") 
                            king.moves.append([0,2])
                            self.white_attack_map[0][2] += 1 
                if isinstance(self.board[0][7], Rook):
                    rook: Rook = self.board[0][7]
                    if rook.is_first_move:
                        if self.is_free_move([0, 6], king):
                            king.moves.append([0,6])
                            self.white_attack_map[0][6] += 1
            
            
                # if self.board[7][7] is Rook:
                #     rook: Rook = self.board[7][7]
                #     if rook.is_first_move:
                #         for col in range(5,7):
                #             if not self.board[7][col]:
                #                 break
                #             else:
                #                 king.moves.append([7,6])
                #                 self.white_attack_map[7][6] += 1

    def pawn_promotion(self, piece: str, row: int, col: int):
                
        if piece == 'q':
            piece = Queen(self.current, row, col)
        if piece == 'r':
            piece = Rook(self.current, row, col)
        if piece == 'b':
            piece = Bishop(self.current, row, col)
        if piece == 'n':
            piece = Knight(self.current, row, col)
        self.board[row][col] = piece

    # def calc_defense_map(self):
    #     if move in figure.moves:
    #         #на самом деле не временно, если перенести то что касается мата 
    #         # Временно делаем ход
    #         temp_piece = self.board[row2][col2]
    #         self.board[row2][col2] = figure
    #         self.board[row][col] = None
    #         old_row, old_col = figure.row, figure.col
    #         figure.row = row2
    #         figure.col = col2

        
        
        
if __name__ == "__main__":
    game = GameBoard()
    game.calc_attack_map("white")
    # pprint(game.board)
    game.calc_attack_map("black")
    pprint(game.white_attack_map)
    pprint(game.black_attack_map)
    # print(game.move_figure(6,0,4,0))
    # print(game.move_figure(1,0,3,0))
    # print(game.move_figure(2,0,4,0))

    # pprint(game.board)
    # pprint(game.board_str())
