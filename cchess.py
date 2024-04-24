# main
from ChineseChess import *
from functions import *


# create 10x9 board to store pieces.
# board = [[None for _ in range(9)] for _ in range(10)]

# King for K
# Advisors for A
# Elephants for E
# Horses for H
# Cannons for C
# Pawn for P
# Chariots for R

# pieces = {
#     # red team
#     'pawn_red1': Pawn('red', [0, 3]),
#     'pawn_red2': Pawn('red', [2, 3]),
#     'pawn_red3': Pawn('red', [4, 3]),
#     'pawn_red4': Pawn('red', [6, 3]),
#     'pawn_red5': Pawn('red', [8, 3]),
#
#     'cannon_red1': Cannon('red', [1, 2]),
#     'cannon_red2': Cannon('red', [7, 2]),
#
#     'chariot_red1': Chariot('red', [0, 0]),
#     'chariot_red2': Chariot('red', [8, 0]),
#
#     'horse_red1': Horse('red', [1, 0]),
#     'horse_red2': Horse('red', [7, 0]),
#
#     'elephant_red1': Elephant('red', [2, 0]),
#     'elephant_red2': Elephant('red', [6, 0]),
#
#     'advisor_red1': Advisor('red', [3, 0]),
#     'advisor_red2': Advisor('red', [5, 0]),
#
#     'king_red': King('red', [4, 0]),
#
#     # black team
#     'pawn_black1': Pawn('black', [0, 6]),
#     'pawn_black2': Pawn('black', [2, 6]),
#     'pawn_black3': Pawn('black', [4, 6]),
#     'pawn_black4': Pawn('black', [6, 6]),
#     'pawn_black5': Pawn('black', [8, 6]),
#
#     'cannon_black1': Cannon('black', [1, 7]),
#     'cannon_black2': Cannon('black', [7, 7]),
#
#     'chariot_black1': Chariot('black', [0, 9]),
#     'chariot_black2': Chariot('black', [8, 9]),
#
#     'horse_black1': Horse('black', [1, 9]),
#     'horse_black2': Horse('black', [7, 9]),
#
#     'elephant_black1': Elephant('black', [2, 9]),
#     'elephant_black2': Elephant('black', [6, 9]),
#
#     'advisor_black1': Advisor('black', [3, 9]),
#     'advisor_black2': Advisor('black', [5, 9]),
#
#     'king_black': King('black', [4, 9]),
# }
# chess_images = {
#     'board': pygame.image.load('assets/images/board.png'),
#     'advisor_black': pygame.image.load('assets/images/advisor_black.png'),
#     'advisor_red': pygame.image.load('assets/images/advisor_red.png'),
#     'elephant_black': pygame.image.load('assets/images/elephant_black.png'),
#     'elephant_red': pygame.image.load('assets/images/elephant_red.png'),
#     'king_red': pygame.image.load('assets/images/king_red.png'),
#     'king_black': pygame.image.load('assets/images/king_black.png'),
#     'horse_red': pygame.image.load('assets/images/horse_red.png'),
#     'horse_black': pygame.image.load('assets/images/horse_black.png'),
#     'chariot_red': pygame.image.load('assets/images/chariot_red.png'),
#     'chariot_black': pygame.image.load('assets/images/chariot_black.png'),
#     'cannon_red': pygame.image.load('assets/images/cannon_red.png'),
#     'cannon_black': pygame.image.load('assets/images/cannon_black.png'),
#     'pawn_red': pygame.image.load('assets/images/pawn_red.png'),
#     'pawn_black': pygame.image.load('assets/images/pawn_black.png')
# }


# no use
# def __init_board_legacy():
#     return [
#         [pieces['chariot_black1'], pieces['horse_black1'], pieces['elephant_black1'], pieces['advisor_black1'],
#          pieces['king_black'], pieces['advisor_black2'], pieces['elephant_black2'], pieces['horse_black2'],
#          pieces['chariot_black2']],
#
#         [None for _ in range(9)],
#
#         [None, pieces['cannon_black1'], None, None, None, None, None, pieces['cannon_black2'], None],
#
#         [pieces['pawn_black1'], None, pieces['pawn_black2'], None, pieces['pawn_black3'], None,
#          pieces['pawn_black4'], None, pieces['pawn_black5']],
#
#         [None for _ in range(9)],
#         # ===================== river =======================
#         # ===================== river =======================
#         [None for _ in range(9)],
#
#         [pieces['pawn_red1'], None, pieces['pawn_red2'], None, pieces['pawn_red3'], None, pieces['pawn_red4'], None,
#          pieces['pawn_red5']],
#
#         [None, pieces['cannon_red1'], None, None, None, None, None, pieces['cannon_red1'], None],
#
#         [None for _ in range(9)],
#
#         [pieces['chariot_red1'], pieces['horse_red1'], pieces['elephant_red1'], pieces['advisor_red1'],
#          pieces['king_red'], pieces['advisor_red2'], pieces['elephant_red2'], pieces['horse_red2'],
#          pieces['chariot_red2']]
#     ]


# init the board
# def init_board(screen):
#     # draw board and pieces
#     # place board to center
#     global BOARD_TOP, BOARD_LEFT, BOARD_RIGHT, BOARD_BOTTOM
#     board_width, board_height = chess_images['board'].get_size()
#     window_center_x, window_center_y = WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2
#     BOARD_LEFT = window_center_x - board_width // 2
#     BOARD_TOP = window_center_y - board_height // 2
#     BOARD_RIGHT = window_center_x + board_width // 2
#     BOARD_BOTTOM = window_center_y + board_height // 2
#     screen.blit(chess_images['board'], (BOARD_LEFT, BOARD_TOP))
#
#     # create a subsurface based on the board image.
#     bg_rect = pygame.Rect((WINDOW_SIZE[0] // 2 - board_width // 2, WINDOW_SIZE[1] // 2 - board_height // 2),
#                           chess_images['board'].get_size())
#     background_subsurface = screen.subsurface(bg_rect)
#     background_subsurface.blit(chess_images['king_red'], pieces['king_red'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['king_black'], pieces['king_black'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['advisor_red'], pieces['advisor_red1'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['advisor_red'], pieces['advisor_red2'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['elephant_red'], pieces['elephant_red1'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['elephant_red'], pieces['elephant_red2'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['horse_red'], pieces['horse_red1'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['horse_red'], pieces['horse_red2'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['chariot_red'], pieces['chariot_red1'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['chariot_red'], pieces['chariot_red2'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['cannon_red'], pieces['cannon_red1'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['cannon_red'], pieces['cannon_red2'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['pawn_red'], pieces['pawn_red1'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['pawn_red'], pieces['pawn_red2'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['pawn_red'], pieces['pawn_red3'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['pawn_red'], pieces['pawn_red4'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['pawn_red'], pieces['pawn_red5'].get_px_position_base_board())
#
#     background_subsurface.blit(chess_images['advisor_black'], pieces['advisor_black1'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['advisor_black'], pieces['advisor_black2'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['elephant_black'], pieces['elephant_black1'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['elephant_black'], pieces['elephant_black2'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['horse_black'], pieces['horse_black1'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['horse_black'], pieces['horse_black2'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['chariot_black'], pieces['chariot_black1'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['chariot_black'], pieces['chariot_black2'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['cannon_black'], pieces['cannon_black1'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['cannon_black'], pieces['cannon_black2'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['pawn_black'], pieces['pawn_black1'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['pawn_black'], pieces['pawn_black2'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['pawn_black'], pieces['pawn_black3'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['pawn_black'], pieces['pawn_black4'].get_px_position_base_board())
#     background_subsurface.blit(chess_images['pawn_black'], pieces['pawn_black5'].get_px_position_base_board())


def main():
    # init pygame
    pygame.init()
    clock = pygame.time.Clock()

    # init game
    cchess = ChineseChess()
    # set chess images as dict
    # the grid of the board is 56x56 px, the first node is at x-40, y-60
    is_highlight = False
    highlight_piece_pos = None, None
    highlighted_piece, moving_piece = None, None  # highlighted_piece may None, if moving, using moving_piece
    highlight_team = TEAM_RED

    # set window size and title
    SCREEN_WIDTH, SCREEN_HEIGHT = WINDOW_WIDTH, WINDOW_HEIGHT = WINDOW_SIZE[0], WINDOW_SIZE[1]

    # return a surface obj
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chinese Chess")

    # main loop
    running = True
    while running:
        if cchess.get_state() == GAME_STATE_FINISHED:
            if game_over(cchess.get_turn()):
                cchess = None
                cchess = ChineseChess()
                is_highlight = False
                highlight_piece_pos = None, None
                highlighted_piece, moving_piece = None, None
                highlight_team = TEAM_RED
            else:
                running = False
            # screen.fill(WHITE_COLOR)
            # text_turn_info = f"GAME OVER, TEAM {cchess.get_turn().upper()} WIN THE GAME."
            # text_font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
            # text_surface = text_font.render(text_turn_info, True, BLACK_COLOR)
            # screen.blit(text_surface, (20, WINDOW_HEIGHT // 2))
            # pygame.display.flip()
        else:
            # clear the screen and redraw everything
            screen.fill(BOARD_COLOR)
            cchess.init_board(screen=screen)  # init the board and place the pieces to their position.

            # show available moves(dots) and highlight the specific piece.
            if is_highlight and highlight_piece_pos is not None:
                draw_piece_legit_moves(cchess, highlighted_piece)
                # is_highlight = False
                highlight_the_piece(cchess.get_board_subsurface(), highlight_piece_pos, highlight_team)
            else:
                # remove highlight_piece_pos
                is_highlight = False

            # update screen
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # when a user clicks a piece, if it is their turn, than show this piece can move to where?
                    if event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        print(f'mouse_x, mouse_y: {mouse_x, mouse_y}')
                        # may add undo function
                        # may add new game
                        if cchess.get_turn() == TEAM_RED:
                            pieces_pos_list = [p.get_px_position_base_window() for p in cchess.get_pieces(TEAM_RED)]  # just a list of red piece position
                            print(f'pieces_pos_list:{pieces_pos_list}\n'
                                  f'cchess.get_pieces(TEAM_RED):{cchess.get_pieces(TEAM_RED)}')
                            if pieces_pos_list is not None and is_on_board(mouse_x, mouse_y):
                                # highlight the piece
                                highlight_piece_pos, highlighted_piece = (
                                    highlighted_piece_rect_pos(mouse_x, mouse_y, cchess.get_pieces(TEAM_RED))
                                )  # contain x and y

                                print(f'highlight_piece_pos: {highlight_piece_pos}')
                                if highlight_piece_pos is not None:  # the user clicked a piece, highlight it
                                    is_highlight = True
                                    moving_piece = highlighted_piece
                                    print(f"available_move:{highlighted_piece.get_available_moves()}")
                                    print(f"legit_move:{cchess.get_legit_moves(highlighted_piece)}")

                                # the user was clicked a piece then clicked a _to position
                                elif is_highlight:
                                    # get the user want's move
                                    try:
                                        _to_position = is_dot_clicked(cchess, moving_piece, mouse_x, mouse_y)
                                        if _to_position is not None and cchess.make_piece_move(moving_piece.get_position(), _to_position):
                                            is_highlight = False
                                            cchess.turn_change()
                                        elif _to_position is None:
                                            raise NoneException("_to_position")
                                    except NoneException:
                                        print(f'_to_position: None')

                        elif cchess.get_turn() == TEAM_BLACK:
                            # just a list of red piece position
                            pieces_pos_list = [p.get_px_position_base_window() for p in
                                               cchess.get_pieces(TEAM_BLACK)]  # just a list of red piece position
                            print(f'pieces_pos_list:{pieces_pos_list}\n'
                                  f'cchess.get_pieces(TEAM_BLACK):{cchess.get_pieces(TEAM_BLACK)}')
                            if pieces_pos_list is not None and is_on_board(mouse_x, mouse_y):
                                # highlight the piece
                                highlight_piece_pos, highlighted_piece = (
                                    highlighted_piece_rect_pos(mouse_x, mouse_y, cchess.get_pieces(TEAM_BLACK))
                                )  # contain x and y

                                print(f'highlight_piece_pos: {highlight_piece_pos}')
                                if highlight_piece_pos is not None:  # the user clicked a piece, highlight it
                                    is_highlight = True
                                    moving_piece = highlighted_piece
                                    print(f"available_move:{highlighted_piece.get_available_moves()}")
                                    print(f"legit_move:{cchess.get_legit_moves(highlighted_piece)}")

                                # the user was clicked a piece then clicked a _to position
                                elif is_highlight:
                                    # get the user want's move
                                    try:
                                        _to_position = is_dot_clicked(cchess, moving_piece, mouse_x, mouse_y)
                                        if _to_position is not None and cchess.make_piece_move(moving_piece.get_position(), _to_position):
                                            is_highlight = False
                                            cchess.turn_change()
                                        elif _to_position is None:
                                            raise NoneException("_to_position")
                                    except NoneException:
                                        print(f'_to_position: None')

    # exit pygame
    pygame.quit()


if __name__ == '__main__':
    main()
