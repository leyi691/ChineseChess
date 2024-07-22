from abc import abstractmethod

import numpy as np

from CustomError import *
from constants import *
import pygame
from functions import get_piece_at_position


class Piece:
    def __init__(self, color=None, position=None, is_eaten=True):
        # self.kind = kind
        self._score = -1
        self._color = color
        self._position = position  # a list [5, 5] ([x,y]), None if been eaten
        self._image = None
        self._available_moves = None
        self._is_eaten = is_eaten
        self._palace_red = [[x, y] for x in range(3, 6) for y in range(0, 3)]
        self._board_red = [[x, y] for x in range(0, 9) for y in range(0, 5)]
        self._palace_black = [[x, y] for x in range(3, 6) for y in range(7, 10)]
        self._board_black = [[x, y] for x in range(0, 9) for y in range(5, 10)]
        self.move_hint_text = ""

    """
    get the pixel position of the piece on the board (relative to the board sub screen)
    """

    def get_px_position_base_board(self):
        """ get the pixel position of the piece on the board (relative to the board sub screen) """
        pos = self._position
        if pos is not None:
            return (pos[0] * BOARD_SQUARE_SIZE + PIECE_POS_INIT[0],
                    pos[1] * BOARD_SQUARE_SIZE + PIECE_POS_INIT[1])
        else:
            return None

    def get_px_position_base_window(self):
        pos = self._position
        if pos is not None:
            return (pos[0] * BOARD_SQUARE_SIZE + PIECE_POS_INIT[0] + BOARD_LEFT,
                    pos[1] * BOARD_SQUARE_SIZE + PIECE_POS_INIT[1] + BOARD_TOP)
        else:
            return None

    def get_rect_base_window(self):
        return pygame.Rect(self.get_px_position_base_window(), PIECE_SIZE)

    def get_color(self):
        return self._color

    def get_position(self):
        """ Return the position of the piece on the board i.e.: [1, 8] aka [x, y], can be None if been eaten"""
        return self._position

    def set_position(self, position):
        self._position = position

    def get_available_moves(self):
        """
        get the available moves
        :return: a list contain all the available moves
        """
        if self._position is not None:
            return self._available_moves
        else:
            return None

    # @abstractmethod
    def update_position(self, position):
        """update the Piece's position to given position
        :param position: get a list obj [x, y]
        """
        if position is None:
            self._position = None  # that means this piece been eaten

        else:
            x = position[0]
            y = position[1]
            self._position = [x, y]

    def been_eaten(self):
        """This piece been eaten"""
        self._position = None
        self._is_eaten = True

    def is_valid_move(self, _to, board_pieces_position):
        """
        Move the piece to the given position
        :param _to: given position
        :param board_pieces_position: a 2 level list contain all pieces on the board
        :return: True if move was successful, False otherwise
        """

        self.get_available_moves()
        if self._available_moves is not None:
            if _to in self._available_moves:
                return True
        else:
            return False

    def _chariot_cannon_move_help(self, pieces):
        pass

    def get_basic_score(self):
        return self._score


class King(Piece):
    """
    Limited to the palace: 3-5, 1-3(red)/ 8-10(black)
    """

    def __init__(self, color, position):
        super().__init__(color, position, False)
        self.is_kings_facing = False
        self.move_hint_text = ("A King can move (and capture) either vertically or horizontally within its 3x3 palace, "
                               "one block at a time. It also has a special capturing move: "
                               "if a king is facing the opponent’s King (i.e. on the same vertical line), "
                               "then it can capture the opponent’s King directly.")

    def get_basic_score(self):
        self._score = SCORE_KING
        return self._score

    def get_available_moves(self):
        """
        :return: a list containing all the available moves not consider other situation.
        """
        move_sets = [[self._position[0], self._position[1] + 1],
                     [self._position[0], self._position[1] - 1],
                     [self._position[0] - 1, self._position[1]],
                     [self._position[0] + 1, self._position[1]]]
        if self._color == TEAM_BLACK:
            self._available_moves = [move for move in move_sets if move in self._palace_black]
        elif self._color == TEAM_RED:
            self._available_moves = [move for move in move_sets if move in self._palace_red]
        else:
            self._available_moves = None
        return self._available_moves

    def handle_kings_facing(self, pieces):
        current_pos = self._position
        current_x = current_pos[0]

        vertical_pieces = [piece for piece in pieces if piece.get_position()[0] == current_x]
        vertical_pieces.sort(key=lambda piece: piece.get_position()[1], reverse=False)
        index_self = vertical_pieces.index(self)
        for i in range(len(vertical_pieces)):
            if isinstance(vertical_pieces[i], King) and abs(i-index_self) == 1:  # kings are at one line and no piece in between
                return vertical_pieces[i].get_position()
        if len(vertical_pieces) >= 2:
            if isinstance(vertical_pieces[0], King) and isinstance(vertical_pieces[1], King):  # kings are at one line and no piece in between
                return vertical_pieces[1].get_position()
        return None

    def is_valid_move(self, _to, board_pieces_position):
        self.get_available_moves()
        if self.is_kings_facing:
            return True
        elif _to in self._available_moves:
            return True
        else:
            return False



# 仕/士
class Advisor(Piece):
    def __init__(self, color, position):
        super().__init__(color, position, False)
        self.move_hint_text = "An Advisor can only move (and capture) diagonally by a block in the 3x3 palace."

    def get_basic_score(self):
        self._score = SCORE_ADVISOR
        return self._score

    def get_available_moves(self):
        """Advisor can make diagonal movement """
        move_sets = [[self._position[0] + 1, self._position[1] + 1],
                     [self._position[0] - 1, self._position[1] - 1],
                     [self._position[0] + 1, self._position[1] - 1],
                     [self._position[0] - 1, self._position[1] + 1]]
        if self._color == TEAM_BLACK:
            self._available_moves = [move for move in move_sets if move in self._palace_black]
        elif self._color == TEAM_RED:
            self._available_moves = [move for move in move_sets if move in self._palace_red]

        return self._available_moves
        # return self._available_moves if self._available_moves is not None else None


# 象
class Elephant(Piece):
    def __init__(self, color, position):
        super().__init__(color, position, False)
        self.move_hint_text = ("An elephant moves to the opposite corner of a square formed by 2x2 blocks, "
                               "but it cannot go across the river; it can capture the opponent’s pieces in this way "
                               "too. A move is not possible if there is a piece on the point in between")

    def get_basic_score(self):
        return SCORE_ELEPHANT

    def move_obsolete(self, step: str):
        _to = step[2:]
        _from = step[:2]
        if _from != self.position:
            raise StepError()
        else:
            if 0 <= int(_to[0]) <= 8 and 0 <= int(_to[1]) <= 4:  # find out is valid area
                if abs(int(_to[0]) - int(_from[0])) == 2 and abs(int(_to[1]) - int(_from[1])) == 2:
                    # these two pairs, each pair should differ by 2
                    self.position = [int(_to[0]), int(_to[1])]
                else:
                    raise StepError()
            else:
                raise StepError()

    def get_available_moves(self):
        """Elephant can move inside a side of the board"""
        move_sets = [[self._position[0] + 2, self._position[1] + 2],
                     [self._position[0] - 2, self._position[1] - 2],
                     [self._position[0] + 2, self._position[1] - 2],
                     [self._position[0] - 2, self._position[1] + 2]]

        # Elephant cannot jump over the river.
        if self.get_color() == TEAM_BLACK:
            self._available_moves = [move for move in move_sets if move in self._board_black]
        if self.get_color() == TEAM_RED:
            self._available_moves = [move for move in move_sets if move in self._board_red]
        return self._available_moves
        # return self._available_moves if self._available_moves is not None else None

    def is_valid_move(self, _to, board_pieces_position):
        """checking is elephant is blocked"""
        if _to is None:
            return False
        self.get_available_moves()

        # min_x = min(self._position[0], _to[0])
        # min_y = min(self._position[1], _to[1])

        # is_block = [piece.get_position() for piece in pieces if piece.get_position() == [min_x + 1, min_y + 1]]

        block_position = []

        # if (self._position[0]+1 < 9 and self._position[1]+1 < 10) or (self._position[0]-1 > 0 and self._position[1]-1 > 0):
        if not isinstance(get_piece_at_position(board_pieces_position, [self._position[0] + 1, self._position[1] + 1]), Just_Piece):
            block_position.append([self._position[0] + 2, self._position[1] + 2])
        if not isinstance(get_piece_at_position(board_pieces_position, [self._position[0] + 1, self._position[1] - 1]), Just_Piece):
            block_position.append([self._position[0] + 2, self._position[1] - 2])
        if not isinstance(get_piece_at_position(board_pieces_position, [self._position[0] - 1, self._position[1] + 1]), Just_Piece):
            block_position.append([self._position[0] - 2, self._position[1] + 2])
        if not isinstance(get_piece_at_position(board_pieces_position, [self._position[0] - 1, self._position[1] - 1]), Just_Piece):
            block_position.append([self._position[0] - 2, self._position[1] - 2])

        if _to in self._available_moves and _to not in block_position:
            return True
        else:
            return False


# 傌/馬
class Horse(Piece):
    def __init__(self, color, position):
        super().__init__(color, position, False)
        self.move_hint_text = ("A Horse moves to the opposite corner of a rectangle formed by 1x2 blocks "
                               "(i.e. it goes forward for one block, and then go across a diagonal of another block); "
                               "it can capture the opponent’s pieces in this way too. A move is not possible "
                               "if there is a piece on the point in between")
    def get_basic_score(self):
        if self.get_color() == TEAM_RED:
            self_board = self._board_red
            other_board = self._board_black
        elif self.get_color() == TEAM_BLACK:
            self_board = self._board_black
            other_board = self._board_red
        else:
            raise ColorError(self.get_color())
        # 1. if pawn at their side of board, have 1 score
        if self._position in self_board:
            self._score = SCORE_HORSE_SELF_BOARD
            return self._score
        # 2. if pawn at the other side of board, have 10 score
        elif self._position in other_board:
            self._score = SCORE_HORSE_OTHER_BOARD
            return self._score
        else:
            raise ColorError(self.get_color())

    def move_obsolete(self, step: str):
        _to = step[2:]
        _from = step[:2]
        if _from != self.position:
            raise StepError()
        else:
            if abs(int(_to[0]) - int(_from[0])) == 2 and abs(int(_to[1]) - int(_from[1])) == 1:
                # can only move by 1x2 blocks
                self.position = [int(_to[0]), int(_to[1])]
            elif abs(int(_to[0]) - int(_from[0])) == 1 and abs(int(_to[1]) - int(_from[1])) == 2:
                # can only move by 1x2 blocks
                self.position = [int(_to[0]), int(_to[1])]
            else:
                raise StepError()

    def get_available_moves(self):
        """only consider horse can move by 1x2 or 2x1"""
        x = self._position[0]
        y = self._position[1]
        self._available_moves = [[x + 1, y + 2], [x + 2, y + 1],
                                 [x + 1, y - 2], [x + 2, y - 1],
                                 [x - 1, y + 2], [x - 2, y + 1],
                                 [x - 1, y - 2], [x - 2, y - 1]]
        return self._available_moves if self._available_moves is not None else None

    def is_valid_move(self, _to, board_pieces_position):
        """A Horse moves to the opposite corner of a rectangle formed by 1x2 blocks
        (i.e. it goes forward for one block, and then go across a diagonal of another block);
        it can capture the opponent’s pieces in this way too.
        A move is not possible if there is a piece on the point in between"""
        if _to is None:
            return False
        self.get_available_moves()  # update available moves

        current_pos = self._position
        x = current_pos[0]
        y = current_pos[1]

        # check if there is a block.
        blocked_position = []

        if x+1 < 9:
            if not isinstance(board_pieces_position[x + 1, y], Just_Piece):  # right side of horse
                blocked_position.append([x + 2, y + 1])
                blocked_position.append([x + 2, y - 1])
        if x-1 >= 0:
            if not isinstance(board_pieces_position[x - 1, y], Just_Piece):  # left side of the horse
                blocked_position.append([x - 2, y + 1])
                blocked_position.append([x - 2, y - 1])

        if y+1 < 10:
            if not isinstance(board_pieces_position[x, y + 1], Just_Piece):  # top side of the horse
                blocked_position.append([x - 1, y + 2])
                blocked_position.append([x + 1, y + 2])
        if y-1 >= 0:
            if not isinstance(board_pieces_position[x, y - 1], Just_Piece):  # bottom side of the horse
                blocked_position.append([x - 1, y - 2])
                blocked_position.append([x + 1, y - 2])

        if _to in self._available_moves and _to not in blocked_position:
            return True
        else:
            return False


# 俥/車
class Chariot(Piece):
    """A Chariot can move and capture either vertically or horizontally by any number of
       blocks, and it can capture the opponent’s pieces in this way too."""

    def __init__(self, color, position):
        super().__init__(color, position, False)
        self.move_hint_text = ("A Chariot can move and capture either vertically or horizontally by any number "
                               "of blocks, and it can capture the opponent’s pieces in this way too.")
    def get_basic_score(self):
        if self.get_color() == TEAM_RED:
            self_board = self._board_red
            other_board = self._board_black
        elif self.get_color() == TEAM_BLACK:
            self_board = self._board_black
            other_board = self._board_red
        else:
            raise ColorError(self.get_color())
        # 1. if pawn at their side of board, have 1 score
        if self._position in self_board:
            self._score = SCORE_CHARIOT_SELF_BOARD
            return self._score
        # 2. if pawn at the other side of board, have 10 score
        elif self._position in other_board:
            self._score = SCORE_CHARIOT_OTHER_BOARD
            return self._score
        else:
            raise ColorError(self.get_color())

    def get_available_moves(self):
        current_x, current_y = self._position
        move_sets = [[x, current_y] for x in range(9)] + [[current_x, y] for y in range(10)]
        move_sets.remove([current_x, current_y])
        self._available_moves = move_sets

        return self._available_moves

    def is_valid_move(self, _to, board_pieces_position):
        """A Chariot can move and capture either vertically or horizontally
           cannot jump over pieces"""
        if _to is None:
            return False
        self.get_available_moves()
        current_pos = self._position
        current_x = current_pos[0]
        current_y = current_pos[1]

        # check if the move is vertically or horizontally
        is_vertical = _to[0] == current_x and _to[1] != current_y
        is_horizontal = _to[0] != current_x and _to[1] == current_y

        if is_vertical:
            for piece in board_pieces_position[current_x, :]:
                if not isinstance(piece, Just_Piece):
                    if _to[1] < piece.get_position()[1] < current_y:  # move vertically and not jump over other piece
                        return False
                    if _to[1] > piece.get_position()[1] > current_y:  # move vertically and not jump over other piece
                        return False
            return True

        elif is_horizontal:
            for piece in board_pieces_position[:, current_y]:
                if not isinstance(piece, Just_Piece):
                    if _to[0] < piece.get_position()[0] < current_x:  # move horizontally and not jump over other piece
                        return False
                    if _to[0] > piece.get_position()[0] > current_x:  # move horizontally and not jump over other piece
                        return False
            return True

        else:
            return False

        # # Check valid
        # if is_vertical:
        #     for piece in pieces:
        #         if piece.get_position()[0] == current_x:
        #             if _to[1] < piece.get_position()[1] < current_y:  # move vertically and not jump over other piece
        #                 return False
        #             if _to[1] > piece.get_position()[1] > current_y:  # move vertically and not jump over other piece
        #                 return False
        #     return True
        #
        # elif is_horizontal:
        #     for piece in pieces:
        #         if piece.get_position()[1] == current_y:
        #             if _to[0] < piece.get_position()[0] < current_x:  # move horizontally and not jump over other piece
        #                 return False
        #             if _to[0] > piece.get_position()[0] > current_x:  # move horizontally and not jump over other piece
        #                 return False
        #     return True
        #
        # else:
        #     return False


# 炮
class Cannon(Piece):
    def __init__(self, color, position):
        super().__init__(color, position, False)
        self.move_hint_text = ("A Cannon can move either vertically or horizontally by any number of blocks, just "
                               "like a Chariot. To capture an opponent’s piece, however, it needs (exactly) one "
                               "intermittent piece between the source and the target.")

    def get_basic_score(self):
        if self.get_color() == TEAM_RED:
            self_board = self._board_red
            other_board = self._board_black
        elif self.get_color() == TEAM_BLACK:
            self_board = self._board_black
            other_board = self._board_red
        else:
            raise ColorError(self.get_color())
        # 1. if pawn at their side of board, have 1 score
        if self._position in self_board:
            self._score = SCORE_CANNON_SELF_BOARD
            return self._score
        # 2. if pawn at the other side of board, have 10 score
        elif self._position in other_board:
            self._score = SCORE_CANNON_OTHER_BOARD
            return self._score
        else:
            raise ColorError(self.get_color())

    def get_available_moves(self):
        current_x, current_y = self._position
        move_sets = [[x, current_y] for x in range(9)] + [[current_x, y] for y in range(10)]
        move_sets.remove([current_x, current_y])
        self._available_moves = move_sets

        return self._available_moves

    def is_valid_move_legacy(self, _to, pieces):
        """A Chariot can move and capture either vertically or horizontally
           cannot jump over pieces"""
        if _to is None:
            return False
        self.get_available_moves()
        current_pos = self._position
        current_x = current_pos[0]
        current_y = current_pos[1]

        # check if the move is vertically or horizontally
        is_vertical = _to[0] == current_x and _to[1] != current_y
        is_horizontal = _to[0] != current_x and _to[1] == current_y

        # Check valid
        if is_vertical:
            # move vertically can jump over one piece
            # only if one other team piece behind it.
            vertical_pieces = [piece for piece in pieces if piece.get_position()[0] == current_x]
            vertical_pieces.sort(key=lambda piece: piece.get_position()[1], reverse=False)
            if len(vertical_pieces) < 3:
                for piece in vertical_pieces:
                    if piece.get_position()[0] == current_x:
                        if _to[1] <= piece.get_position()[1] < current_y:
                            return False
                        if _to[1] >= piece.get_position()[1] > current_y:
                            return False
                return True
            else:  # have more than 3 pieces on the column, if this move  is the other team's, return True
                index_self = vertical_pieces.index(self)
                # which means there are at least 2 piece at top of this cannon
                if index_self >= 2:
                    if (vertical_pieces[index_self - 2].get_color() != self.get_color()
                            and _to[1] == vertical_pieces[index_self - 2].get_position()[1]):
                        # valid move to eat that piece
                        return True
                if len(vertical_pieces)-1 - index_self >= 2:
                    if (vertical_pieces[index_self + 2].get_color() != self.get_color()
                            and _to[1] == vertical_pieces[index_self + 2].get_position()[1]):
                        # valid move to eat that piece
                        return True
                # any empty space between cannon and two closest pieces is valid move
                if index_self != 0:
                    if vertical_pieces[index_self-1].get_position()[1] < _to[1] < current_y:
                        return True
                if index_self+1 < len(vertical_pieces):
                    if vertical_pieces[index_self+1].get_position()[1] > _to[1] > current_y:
                        return True

        elif is_horizontal:
            horizontal_pieces = [piece for piece in pieces if piece.get_position()[1] == current_y]
            horizontal_pieces.sort(key=lambda piece: piece.get_position()[0], reverse=False)
            if len(horizontal_pieces) < 3:
                for piece in horizontal_pieces:
                    if piece.get_position()[1] == current_y:
                        if _to[0] <= piece.get_position()[0] < current_x:  # move horizontally can jump over one piece.
                            return False
                        if _to[0] >= piece.get_position()[0] > current_x:  # move horizontally can jump over one piece.
                            return False
                return True
            else:  # have more than 3 pieces on the row, if this move is the other team's Piece, return True
                index_self = horizontal_pieces.index(self)
                if index_self >= 2:  # there are at least 2 pieces on this cannon's left
                    if (horizontal_pieces[index_self - 2].get_color() != self.get_color()
                            and _to[0] == horizontal_pieces[index_self - 2].get_position()[0]):
                        # its valid move
                        return True
                if len(horizontal_pieces) - 1 - index_self >= 2:  # there are at least 2 pieces on this cannon's right
                    if (horizontal_pieces[index_self + 2].get_color() != self.get_color()
                            and _to[0] == horizontal_pieces[index_self + 2].get_position()[0]):
                        return True
                # any empty space between cannon and two closest pieces is valid move
                if index_self != 0:
                    if horizontal_pieces[index_self-1].get_position()[0] < _to[0] < current_x:
                        return True
                if index_self+1 < len(horizontal_pieces):
                    if horizontal_pieces[index_self+1].get_position()[0] > _to[0] > current_x:
                        return True
        else:
            return False

    def help_is_valid_move(self, _to, board_pieces_position):
        """return True if this move is the special move for cannon"""
        current_x, current_y = self._position
        to_x, to_y = _to
        to_piece = board_pieces_position[_to[0], _to[1]]

        # for piece in pieces:
        #     if piece.get_position() == _to:
        #         to_piece = piece
        if isinstance(to_piece, Just_Piece):
            to_piece = None

        is_horizontal = to_y == current_y
        is_vertical = to_x == current_x

        if is_vertical:
            # vertical_pieces = [piece for piece in pieces if piece.get_position()[0] == current_x]
            vertical_pieces = [piece for piece in board_pieces_position[current_x, :] if not isinstance(piece, Just_Piece)]
            vertical_pieces = sorted(vertical_pieces, key=lambda _p: _p.get_position()[1], reverse=False)
            index_self = vertical_pieces.index(self)
            try:
                index_to = vertical_pieces.index(to_piece)
                if abs(index_self - index_to) == 2 and to_piece.get_color() != self.get_color():
                    return True
            except ValueError:
                return False

        if is_horizontal:
            # horizontal_pieces = [piece for piece in pieces if piece.get_position()[1] == current_y]
            horizontal_pieces = [piece for piece in board_pieces_position[:, current_y] if not isinstance(piece, Just_Piece)]
            horizontal_pieces = sorted(horizontal_pieces, key=lambda _p: _p.get_position()[0], reverse=False)
            index_self = horizontal_pieces.index(self)
            try:
                index_to = horizontal_pieces.index(to_piece)
                if abs(index_self - index_to) == 2 and to_piece.get_color() != self.get_color():
                    return True
            except ValueError:
                return False
        # finally
        return False

    def is_valid_move(self, _to, board_pieces_position):
        self.get_available_moves()
        current_x, current_y = self._position
        to_x, to_y = _to

        is_horizontal = to_y == current_y
        is_vertical = to_x == current_x

        if self.help_is_valid_move(_to, board_pieces_position):
            return True

        if is_vertical:
            vertical_pieces = [piece for piece in board_pieces_position[current_x, :] if not isinstance(piece, Just_Piece)]
            vertical_pieces = sorted(vertical_pieces, key=lambda _p: _p.get_position()[1], reverse=False)
            # index_self = vertical_pieces.index(self)
            # 2. _to is enemy position by special rule by cannon

            for i in range(len(vertical_pieces)):
                piece = vertical_pieces[i]
                # 1.no pieces between _to and current position
                if to_y >= piece.get_position()[1] > current_y:
                    return False
                if to_y <= piece.get_position()[1] < current_y:
                    return False
            # end of for
            return True

        if is_horizontal:
            horizontal_pieces = [piece for piece in board_pieces_position[:, current_y] if not isinstance(piece, Just_Piece)]
            # np.argsort(horizontal_pieces[:, 0])
            horizontal_pieces = sorted(horizontal_pieces, key=lambda _p: _p.get_position()[0], reverse=False)
            # index_self = horizontal_pieces.index(self)

            for i in range(len(horizontal_pieces)):
                piece = horizontal_pieces[i]
                # 1. no pieces in between to and current position
                if to_x <= piece.get_position()[0] < current_x:
                    # 2. _to is enemy position by special rule by cannon
                    return False
                if to_x >= piece.get_position()[0] > current_x:
                    # 2. _to is enemy position by special rule by cannon
                    return False
            # end of for
            return True
        # finally
        return False


# 兵
class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position, False)
        self.move_hint_text = ("A Pawn can only move forward by a single block, but it will get “promoted” and acquire "
                               "the capability to move sideways (by a single block) if it goes across the river; "
                               "the same for its capturing moves too.")
    def get_basic_score(self):
        if self.get_color() == TEAM_RED:
            self_board = self._board_red
            other_board = self._board_black
        elif self.get_color() == TEAM_BLACK:
            self_board = self._board_black
            other_board = self._board_red
        else:
            raise ColorError(self.get_color())
        # 1. if pawn at their side of board, have 1 score
        if self._position in self_board:
            self._score = SCORE_PAWN_SELF_BOARD
            return self._score
        # 2. if pawn at the other side of board, have 10 score
        elif self._position in other_board:
            self._score = SCORE_PAWN_OTHER_BOARD
            return self._score
        else:
            raise ColorError(self.get_color())


    def get_available_moves(self):
        x, y = self._position
        move_sets = [[x, y+1], [x+1, y],
                     [x-1, y], [x, y-1]]
        self._available_moves = move_sets
        return self._available_moves

    def is_valid_move(self, _to, board_pieces_position):
        self.get_available_moves()
        # return True
        x, y = self._position
        self_board = None
        other_board = None
        if self.get_color() == TEAM_RED:
            self_board = self._board_red
            other_board = self._board_black
        elif self.get_color() == TEAM_BLACK:
            self_board = self._board_black
            other_board = self._board_red
        else:
            raise ColorError(self.get_color())

        if self.get_color() == TEAM_RED:
            # 1. if pawn at their side of board, can only move forward 1 step
            if _to in self_board and _to[0] == x and _to[1] == y+1:
                return True
            # 2. if pawn at the other side of board, can move left and right, still, pawn only move forward.
            elif _to in other_board:
                if _to[0] == x and _to[1] == y+1:  # move forward
                    return True
                if _to[1] == y and (_to[0] == x-1 or _to[0] == x+1):
                    return True
            else:
                return False
        elif self.get_color() == TEAM_BLACK:
            # 1. if pawn at their side of board, can only move forward 1 step
            if _to in self_board and _to[0] == x and _to[1] == y-1:
                return True
            # 2. if pawn at the other side of board, can move left and right, still, pawn only move forward.
            elif _to in other_board:
                if _to[0] == x and _to[1] == y-1:  # move forward
                    return True
                if _to[1] == y and (_to[0] == x-1 or _to[0] == x+1):
                    return True
            else:
                return False
        else:
            return False


class Just_Piece(Piece):
    def __init__(self):
        super().__init__(TEAM_OTHER, [-1, -1], False)
