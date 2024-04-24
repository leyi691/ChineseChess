from constants import *
from Piece import *
import pygame
import sys
from functions import *


class ChineseChess:
    """ The Game Engine """

    def __init__(self):
        """ Initialize the game state, check state, turn, eat pieces, playing pieces. """
        self._game_state = GAME_STATE_UNFINISHED
        self._turn = TEAM_RED  # 0 for red, 1 for black
        self._pieces = {
            # red team
            'pawn_red1': Pawn('red', [0, 3]),
            'pawn_red2': Pawn('red', [2, 3]),
            'pawn_red3': Pawn('red', [4, 3]),
            'pawn_red4': Pawn('red', [6, 3]),
            'pawn_red5': Pawn('red', [8, 3]),

            'cannon_red1': Cannon('red', [1, 2]),
            'cannon_red2': Cannon('red', [7, 2]),

            'chariot_red1': Chariot('red', [0, 0]),
            'chariot_red2': Chariot('red', [8, 0]),

            'horse_red1': Horse('red', [1, 0]),
            'horse_red2': Horse('red', [7, 0]),

            'elephant_red1': Elephant('red', [2, 0]),
            'elephant_red2': Elephant('red', [6, 0]),

            'advisor_red1': Advisor('red', [3, 0]),
            'advisor_red2': Advisor('red', [5, 0]),

            'king_red': King('red', [4, 0]),

            # black team
            'pawn_black1': Pawn('black', [0, 6]),
            'pawn_black2': Pawn('black', [2, 6]),
            'pawn_black3': Pawn('black', [4, 6]),
            'pawn_black4': Pawn('black', [6, 6]),
            'pawn_black5': Pawn('black', [8, 6]),

            'cannon_black1': Cannon('black', [1, 7]),
            'cannon_black2': Cannon('black', [7, 7]),

            'chariot_black1': Chariot('black', [0, 9]),
            'chariot_black2': Chariot('black', [8, 9]),

            'horse_black1': Horse('black', [1, 9]),
            'horse_black2': Horse('black', [7, 9]),

            'elephant_black1': Elephant('black', [2, 9]),
            'elephant_black2': Elephant('black', [6, 9]),

            'advisor_black1': Advisor('black', [3, 9]),
            'advisor_black2': Advisor('black', [5, 9]),

            'king_black': King('black', [4, 9]),
        }
        self._chess_images = {
            'board': pygame.image.load('assets/images/board.png'),
            'advisor_black': pygame.image.load('assets/images/advisor_black.png'),
            'advisor_red': pygame.image.load('assets/images/advisor_red.png'),
            'elephant_black': pygame.image.load('assets/images/elephant_black.png'),
            'elephant_red': pygame.image.load('assets/images/elephant_red.png'),
            'king_red': pygame.image.load('assets/images/king_red.png'),
            'king_black': pygame.image.load('assets/images/king_black.png'),
            'horse_red': pygame.image.load('assets/images/horse_red.png'),
            'horse_black': pygame.image.load('assets/images/horse_black.png'),
            'chariot_red': pygame.image.load('assets/images/chariot_red.png'),
            'chariot_black': pygame.image.load('assets/images/chariot_black.png'),
            'cannon_red': pygame.image.load('assets/images/cannon_red.png'),
            'cannon_black': pygame.image.load('assets/images/cannon_black.png'),
            'pawn_red': pygame.image.load('assets/images/pawn_red.png'),
            'pawn_black': pygame.image.load('assets/images/pawn_black.png')
        }
        self._board_pieces_position = [[Just_Piece() for row in range(10)] for column in range(9)]
        self._board_subsurface = None

    def init_board(self, screen):
        """ init the board """
        # draw board and pieces, place board to center
        for piece in self._pieces.values():
            if piece.get_position() is not None:
                self._board_pieces_position[piece.get_position()[0]][piece.get_position()[1]] = piece

        # show which turn by now
        if self.get_turn() == TEAM_RED:
            text_turn_info = 'Turn:' + self.get_turn()
            text_font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
            text_surface = text_font.render(text_turn_info, True, RED_COLOR)
            screen.blit(text_surface, (12, 12))
        elif self.get_turn() == TEAM_BLACK:
            text_turn_info = 'Turn:' + self.get_turn()
            text_font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
            text_surface = text_font.render(text_turn_info, True, BLACK_COLOR)
            screen.blit(text_surface, (12, 12))

        global BOARD_TOP, BOARD_LEFT, BOARD_RIGHT, BOARD_BOTTOM
        board_width, board_height = self._chess_images['board'].get_size()
        window_center_x, window_center_y = WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2
        BOARD_LEFT = window_center_x - board_width // 2
        BOARD_TOP = window_center_y - board_height // 2
        BOARD_RIGHT = window_center_x + board_width // 2
        BOARD_BOTTOM = window_center_y + board_height // 2
        screen.blit(self._chess_images['board'], (BOARD_LEFT, BOARD_TOP))

        # create a subsurface based on the board image.
        bg_rect = pygame.Rect((WINDOW_SIZE[0] // 2 - board_width // 2, WINDOW_SIZE[1] // 2 - board_height // 2),
                              self._chess_images['board'].get_size())
        self._board_subsurface = screen.subsurface(bg_rect)
        # Draw pieces on the board
        self.draw_piece(self._board_subsurface, KING_RED, KING_RED)
        self.draw_piece(self._board_subsurface, KING_BLACK, KING_BLACK)
        self.draw_piece(self._board_subsurface, HORSE_RED, HORSE_RED + '1')
        self.draw_piece(self._board_subsurface, HORSE_RED, HORSE_RED + '2')
        self.draw_piece(self._board_subsurface, HORSE_BLACK, HORSE_BLACK + '1')
        self.draw_piece(self._board_subsurface, HORSE_BLACK, HORSE_BLACK + '2')
        self.draw_piece(self._board_subsurface, CANNON_BLACK, CANNON_BLACK + '1')
        self.draw_piece(self._board_subsurface, CANNON_BLACK, CANNON_BLACK + '2')
        self.draw_piece(self._board_subsurface, CANNON_RED, CANNON_RED + '1')
        self.draw_piece(self._board_subsurface, CANNON_RED, CANNON_RED + '2')
        self.draw_piece(self._board_subsurface, PAWN_BLACK, PAWN_BLACK + '1')
        self.draw_piece(self._board_subsurface, PAWN_BLACK, PAWN_BLACK + '2')
        self.draw_piece(self._board_subsurface, PAWN_BLACK, PAWN_BLACK + '3')
        self.draw_piece(self._board_subsurface, PAWN_BLACK, PAWN_BLACK + '4')
        self.draw_piece(self._board_subsurface, PAWN_BLACK, PAWN_BLACK + '5')
        self.draw_piece(self._board_subsurface, PAWN_RED, PAWN_RED + '1')
        self.draw_piece(self._board_subsurface, PAWN_RED, PAWN_RED + '2')
        self.draw_piece(self._board_subsurface, PAWN_RED, PAWN_RED + '3')
        self.draw_piece(self._board_subsurface, PAWN_RED, PAWN_RED + '4')
        self.draw_piece(self._board_subsurface, PAWN_RED, PAWN_RED + '5')
        self.draw_piece(self._board_subsurface, ADVISOR_BLACK, ADVISOR_BLACK + '1')
        self.draw_piece(self._board_subsurface, ADVISOR_BLACK, ADVISOR_BLACK + '2')
        self.draw_piece(self._board_subsurface, ADVISOR_RED, ADVISOR_RED + '1')
        self.draw_piece(self._board_subsurface, ADVISOR_RED, ADVISOR_RED + '2')
        self.draw_piece(self._board_subsurface, ELEPHANT_BLACK, ELEPHANT_BLACK + '1')
        self.draw_piece(self._board_subsurface, ELEPHANT_BLACK, ELEPHANT_BLACK + '2')
        self.draw_piece(self._board_subsurface, ELEPHANT_RED, ELEPHANT_RED + '1')
        self.draw_piece(self._board_subsurface, ELEPHANT_RED, ELEPHANT_RED + '2')
        self.draw_piece(self._board_subsurface, CHARIOT_BLACK, CHARIOT_BLACK + '1')
        self.draw_piece(self._board_subsurface, CHARIOT_BLACK, CHARIOT_BLACK + '2')
        self.draw_piece(self._board_subsurface, CHARIOT_RED, CHARIOT_RED + '1')
        self.draw_piece(self._board_subsurface, CHARIOT_RED, CHARIOT_RED + '2')

        # self._board_subsurface.blit(self._chess_images['king_red'],
        #                             self._pieces['king_red'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['king_black'],
        #                             self._pieces['king_black'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['advisor_red'],
        #                             self._pieces['advisor_red1'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['advisor_red'],
        #                             self._pieces['advisor_red2'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['elephant_red'],
        #                             self._pieces['elephant_red1'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['elephant_red'],
        #                             self._pieces['elephant_red2'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['horse_red'],
        #                             self._pieces['horse_red1'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['horse_red'],
        #                             self._pieces['horse_red2'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['chariot_red'],
        #                             self._pieces['chariot_red1'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['chariot_red'],
        #                             self._pieces['chariot_red2'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['cannon_red'],
        #                             self._pieces['cannon_red1'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['cannon_red'],
        #                             self._pieces['cannon_red2'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['pawn_red'],
        #                             self._pieces['pawn_red1'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['pawn_red'],
        #                             self._pieces['pawn_red2'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['pawn_red'],
        #                             self._pieces['pawn_red3'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['pawn_red'],
        #                             self._pieces['pawn_red4'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['pawn_red'],
        #                             self._pieces['pawn_red5'].get_px_position_base_board())
        # # black team
        # self._board_subsurface.blit(self._chess_images['advisor_black'],
        #                             self._pieces['advisor_black1'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['advisor_black'],
        #                             self._pieces['advisor_black2'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['elephant_black'],
        #                             self._pieces['elephant_black1'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['elephant_black'],
        #                             self._pieces['elephant_black2'].get_px_position_base_board())
        #
        # self._board_subsurface.blit(self._chess_images['horse_black'],
        #                             self._pieces['horse_black2'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['chariot_black'],
        #                             self._pieces['chariot_black1'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['chariot_black'],
        #                             self._pieces['chariot_black2'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['cannon_black'],
        #                             self._pieces['cannon_black1'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['cannon_black'],
        #                             self._pieces['cannon_black2'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['pawn_black'],
        #                             self._pieces['pawn_black1'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['pawn_black'],
        #                             self._pieces['pawn_black2'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['pawn_black'],
        #                             self._pieces['pawn_black3'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['pawn_black'],
        #                             self._pieces['pawn_black4'].get_px_position_base_board())
        # self._board_subsurface.blit(self._chess_images['pawn_black'],
        #                             self._pieces['pawn_black5'].get_px_position_base_board())

    def get_pieces(self, color=None):
        """ Return a list pieces not include the eaten pieces (died) """

        if color is not None:  # return 'color' team pieces.
            pieces = [p for p in self._pieces.values() if p.get_color() == color
                      and p.get_position() is not None]

        else:  # return all pieces
            pieces = [p for p in self._pieces.values() if p.get_position() is not None]

        return pieces

    def get_turn(self):
        return self._turn

    def get_game_state(self):
        return self._game_state

    def get_piece_at_position(self, position):
        """get the piece at location
        return None if no piece there
        :param position: position in board i.e [0, 0] return Chariot object
        """
        if position is None:
            return None

        return self._board_pieces_position[position[0]][position[1]]

    def get_chess_images(self):
        return self._chess_images

    def get_state(self):
        return self._game_state

    def get_board_subsurface(self):
        return self._board_subsurface

    def set_turn(self, color):
        self._turn = color

    def turn_change(self):
        if self._turn == TEAM_RED:
            self._turn = TEAM_BLACK
        elif self._turn == TEAM_BLACK:
            self._turn = TEAM_RED
        else:
            raise InvalidTurnError(self._turn)

    def win_the_game(self, color):
        """change game status, change game turn"""
        message = f"TEAM {color} WIN THE GAME."
        print(message)
        self._game_state = GAME_STATE_FINISHED
        self.turn_change()

    def get_legit_moves(self, piece):
        """Return a list of legal moves"""
        available_moves = piece.get_available_moves()
        legit_moves = [move for move in available_moves
                       if self.check_move(piece.get_position(), move)]
        if isinstance(piece, King):
            res = piece.handle_kings_facing(self.get_pieces())
            if res is not None:
                legit_moves.append(res)
                piece.is_kings_facing = True
        legit_moves.sort()

        return legit_moves

    def check_move(self, _from, _to):
        """check whether the move is legit or not, _from to _to position

        :param _from:  of the original position i.e. [3, 6] 3 as x, 6 as y
        :param _to: position of the wanted position i.e. [3, 6] 3 as x, 6 as y
        :return True if legal moves, False if not
        """
        if 0 <= _to[0] <= 8 and 0 <= _to[1] <= 9:
            # RULE 1. check _to a position do not have the same kind of piece
            moving_piece = self.get_piece_at_position(_from)
            target_piece = self.get_piece_at_position(_to)

            # piece cannot move to positions which are stand the same team pieces.
            if target_piece.get_color() != moving_piece.get_color():
                # this move may eat the target piece
                original_position = moving_piece.get_position()

                is_valid_move = moving_piece.is_valid_move(_to, self.get_pieces())

                # just for check, will not move.
                moving_piece.update_position(original_position)

                return is_valid_move

            else:
                return False
        else:
            return False

    def make_piece_move(self, _from, _to):
        """
        from _from to _to position
        :param _from:
        :param _to:
        :return:
        """
        if self.get_game_state() != GAME_STATE_UNFINISHED:
            return False

        moving_piece = self.get_piece_at_position(_from)
        target_piece = self.get_piece_at_position(_to)

        if (moving_piece.get_color() is None or
                self.get_turn() != moving_piece.get_color()  # check if the moving piece at right turn
        ):
            return False

        if not moving_piece.is_valid_move(_to, self.get_pieces()):
            return False

        is_different_team = target_piece.get_color() != moving_piece.get_color()
        is_target_piece_exist = target_piece.get_color() is not None
        is_eaten_move = is_different_team and is_target_piece_exist

        if is_eaten_move:
            # if King been eaten
            if isinstance(target_piece, King):
                self.win_the_game(self.get_turn())
            # this piece been eaten
            target_piece.been_eaten()

        # update board position info
        # 1. clear _from pos
        self._board_pieces_position[_from[0]][_from[1]] = Just_Piece()
        moving_piece.set_position(_to)

        # 2. _from piece move to _to pos
        moving_piece.update_position(_to)
        self._board_pieces_position[_to[0]][_to[1]] = moving_piece
        # 3. check if checkmate status
        # self.is_in_check(moving_piece)
        self.is_in_check_all_board()
        return True

    def draw_piece(self, surface, piece_img_name, piece_name):
        if self._pieces[piece_name].get_position() is None:
            return False
        else:
            surface.blit(self._chess_images[piece_img_name], self._pieces[piece_name].get_px_position_base_board())
            return True

    def is_in_check(self, piece):
        """Check if the game is in check status
        :param piece: moving piece
        :return True if this piece can in check."""
        legit_moves = self.get_legit_moves(piece)
        for move in legit_moves:
            if isinstance(self.get_piece_at_position(move), King):
                # in checkmate status
                popup_window_showinfo("Check", f"in check.")
                return True

    def is_in_check_all_board(self):
        """Check if the game is in check status but check all pieces.
        :return True if this piece can in check."""
        for piece in self.get_pieces():
            legit_moves = self.get_legit_moves(piece)
            for move in legit_moves:
                if isinstance(self.get_piece_at_position(move), King):
                    # in checkmate status
                    popup_window_showinfo("Check", f"in check.")
                    return True
