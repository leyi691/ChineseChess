import pygame
from constants import *
import tkinter.messagebox


def is_on_board(x, y):
    """ check if x and y are, mouse was clicked on the board image area. """
    if BOARD_LEFT <= x <= BOARD_RIGHT and BOARD_TOP <= y <= BOARD_BOTTOM:
        return True
    else:
        return False


def highlight_the_piece(surface, position, color):
    """ highlight the piece(at position) that user was clicked on """
    if color == TEAM_RED:
        image = pygame.image.load('assets/images/select_red.png')
        surface.blit(image, position)
    elif color == TEAM_BLACK:
        image = pygame.image.load('assets/images/select_black.png')
        surface.blit(image, position)


def highlighted_piece_rect_pos(mouse_x, mouse_y, pieces):
    """ return the piece position(base window) that mouse clicked on the screen.
        :return x, y: position
                piece: which specific piece to highlight
    """
    rect_list = {p: p.get_rect_base_window() for p in pieces}
    for piece, rect in rect_list.items():
        if rect.collidepoint(mouse_x, mouse_y):
            x, y = piece.get_px_position_base_board()
            print(f'x, y:{x}, {y}')
            return (x, y), piece
    return None, None


def draw_piece_legit_moves(game, piece):
    """ display the available moves for the piece
    :param game: cchess
    :param board_subsurface: board subsurface
    :param piece: piece
    """
    legit_moves = game.get_legit_moves(piece)
    legit_moves_px = [dot_px_position_base_board(pos[0], pos[1]) for pos in legit_moves]
    for pos in legit_moves_px:
        pygame.draw.circle(game.get_board_subsurface(), 'red', pos, radius=DOT_RADIUS)
    return True


def piece_px_position_base_board(piece_x, piece_y):
    """ return the relative position(a tuple, position relative to the board image) of the piece based on the window """
    return (piece_x * BOARD_SQUARE_SIZE + PIECE_POS_INIT[0],
            piece_y * BOARD_SQUARE_SIZE + PIECE_POS_INIT[1])


def dot_px_position_base_board(piece_x, piece_y):
    """ return the relative position(a tuple, position relative to the board image) of the piece based on the window """
    return (piece_x * BOARD_SQUARE_SIZE + DOT_POS_INIT[0],
            piece_y * BOARD_SQUARE_SIZE + DOT_POS_INIT[1])


def piece_px_position_base_window(piece_x, piece_y):
    """ return the abstract position(tuple) of the piece based on the window """
    return (piece_x * BOARD_SQUARE_SIZE + PIECE_POS_INIT[0] + BOARD_LEFT,
            piece_y * BOARD_SQUARE_SIZE + PIECE_POS_INIT[1] + BOARD_TOP)


def dot_px_position_base_window(piece_x, piece_y):
    """ return the abstract position(tuple) of the piece based on the window """
    return (piece_x * BOARD_SQUARE_SIZE + DOT_POS_INIT[0] + BOARD_LEFT,
            piece_y * BOARD_SQUARE_SIZE + DOT_POS_INIT[1] + BOARD_TOP)


# def mouse_pos_to_board_position(mouse_x, mouse_y):
#     """ return the board position i.e. [4, 2]"""
#     pass


def is_dot_clicked(game, highlight_piece, mouse_x, mouse_y):
    """ check if the dot is clicked, then piece can move to that position or not
    :param game: game entity
    :param highlight_piece: highlighted piece
    :param mouse_x: mouse x position
    :param mouse_y: mouse y position
    :return: a dot position where mouse clicked position, or None if no such position.
    """
    legit_moves = game.get_legit_moves(highlight_piece)
    # print(f'legit_moves: {legit_moves}')
    for pos in legit_moves:
        # meantime, draw a pygame.Rect on the board to make easier for later detection.
        # rect = pygame.Rect(dot_px_position_base_window(pos[0], pos[1]), PIECE_SIZE)

        print(f"dot_px_position_base_window(pos[0], pos[1]) :{dot_px_position_base_window(pos[0], pos[1])}")
        print(f'mouse_position                              :{mouse_x, mouse_y}')

        if (0 <= abs(dot_px_position_base_window(pos[0], pos[1])[0] - mouse_x) <= DOT_RADIUS*2
                and 0 <= abs(dot_px_position_base_window(pos[0], pos[1])[1] - mouse_y) <= DOT_RADIUS*2):
            return pos
    return None


def get_other_color(color):
    """return the other color of the param: color"""
    if color == TEAM_RED:
        return TEAM_BLACK
    elif color == TEAM_BLACK:
        return TEAM_RED


def popup_window_askokcancel(title, message):
    """using tkinter.messagebox to create a popup window"""
    return_value = tkinter.messagebox.askokcancel(title, message)
    # print(type(return_value), return_value)
    return return_value


def popup_window_showinfo(title, message):
    """using tkinter.messagebox to create a popup window"""
    return_value = tkinter.messagebox.showinfo(title, message)
    # print(type(return_value), return_value)
    return return_value


def game_over(color):
    """return True if player clicked yes, otherwise False"""
    return popup_window_askokcancel("GAME OVER", f"Team {color} win the game, want another?")
