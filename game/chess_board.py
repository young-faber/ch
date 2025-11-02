from .chess_pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, pieces_cls

# from game.chess_pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King
from pprint import pprint
from typing import List, Dict
import json


class GameBoard:  # или игра?
    def __init__(self, new_game=True, board_str=None, current=None):
        self.board = [[None for i in range(8)] for i in range(8)]
        self.white_attack_map = [[0 for i in range(8)] for i in range(8)]
        self.black_attack_map = [[0 for i in range(8)] for i in range(8)]
        if new_game:
            self.current = "black"
            self.kw = [0, 0]
            self.kb = [0, 0]
            check = None

            # self.board[1][0] = Pawn("black", 1, 0)
            # self.board[5][5] = Rook('white', 5, 5)

            # for col in range(8):
                # self.board[6][col] = Pawn("white", 6, col)
                # self.board[1][col] = Pawn("black", 1, col)
            self.board[7][4] = King("white", 7, 4)
            self.board[0][4] = King("black", 0, 4)

            self.board[7][3] = Queen("white", 7, 3)
            # self.board[0][3] = Queen('black', 0, 3)

            self.board[7][2] = Bishop("white", 7, 2)
            # self.board[0][2] = Bishop("black", 0, 2)
            self.board[7][5] = Bishop("white", 7, 5)
            # self.board[0][5] = Bishop("black", 0, 5)

            self.board[7][1] = Knight("white", 7, 1)
            # self.board[0][1] = Knight("black", 0, 1)
            self.board[7][6] = Knight("white", 7, 6)
            # self.board[0][6] = Knight("black", 0, 6)

            self.board[7][0] = Rook("white", 7, 0)
            # self.board[0][0] = Rook("black", 7, 2)
            self.board[7][7] = Rook("white", 7, 7)
            # self.board[0][7] = Rook("black", 7, 2)
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
                    print(1)
                else:
                    print(2)
                    self.kb = [row, col]

    def move_figure(self, row, col, row2, col2):
        figure: Piece = self.board[row][col]
        if not figure:
            return False

        if self.current != figure.side:
            raise KeyError('Ходит другая сторона')
        
        # Вычисляем возможные ходы
        figure.calc_attack_moves()
        self.clean_attack_moves(figure)
        
        move = [row2, col2]
        

        if self.current == figure.side and move in figure.moves:
            figure.row = row2
            figure.col = col2

            if self.current == "white":
                print('курент посчитался')
                r, c = self.kw
                if self.black_attack_map[r][c] > 0:
                    print('Мапа просчиталась')
                    raise ValueError("шах")

            if self.current == "black":
                r, c = self.kb
                if self.white_attack_map[r][c] > 0:
                    raise ValueError("шах")

            self.board[row][col], self.board[row2][col2] = (
                self.board[row2][col2],
                self.board[row][col],
            )
            figure.is_first_move = False
            # Меняем текущего игрока
            self.current = "black" if self.current == "white" else "white"
            return True
        raise ValueError("Невозможный ход")  # Исправлено: правильный raise

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
    ):  # для каждой фигуры считает calc_attack_moves + clean_attack_moves
        for row in range(8):
            for col in range(8):
                figure: Piece = self.board[row][col]
                if figure and figure.side == side:
                    figure.calc_attack_moves()
                    print(figure.appearence, figure.moves)
                    self.clean_attack_moves(figure)
                    print("Х", figure.appearence, figure.moves)
                    for move in figure.moves:
                        r, c = move  # переименовали переменные
                        if side == "black":
                            self.black_attack_map[r][c] += 1
                            if self.board[r][c] == King:
                                self.kb = [r][c]
                        elif side == "white":
                            if self.board[r][c] == King:
                                self.kw = [r][c]
                            self.white_attack_map[r][c] += 1


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
