# main
import time

from ChineseChess import *
from functions import *
from aiplay import *
from copy import copy, deepcopy
import constants


def main():
    # init pygame
    pygame.init()
    clock = pygame.time.Clock()

    # init game
    cchess = ChineseChess()

    # set a slider to choose difficulty.
    difficulty = MIN_DIFFICULTY
    difficulty_font = pygame.font.SysFont(FONT_FAMILY_DIFFICULTY, size=FONT_SIZE_DIFFICULTY)
    knob_x_pos = constants.KNOB_X_POS
    # set round font
    text_game_round = 1
    round_font = pygame.font.SysFont(FONT_FAMILY, size=FONT_SIZE)
    text_ai_move = None
    ai_engine = MinimaxEngine(cchess, AI_TEAM_COLOR, depth_limit=difficulty)
    # set chess images as dict
    # the grid of the board is 56x56 px, the first node is at x-40, y-60
    is_highlight = False
    highlight_piece_pos = None, None
    highlighted_piece, moving_piece = None, None  # highlighted_piece may None, if moving, using moving_piece
    highlight_team = TEAM_RED

    # set the window and title.
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Chinese Chess")

    # main loop
    running = True
    while running:
        if cchess.get_state() == GAME_STATE_FINISHED:
            # if game at finished state check.
            if game_over(get_other_color(cchess.get_turn())):
                cchess = ChineseChess()
                difficulty = MIN_DIFFICULTY
                ai_engine = MinimaxEngine(cchess, AI_TEAM_COLOR, depth_limit=difficulty)

                is_highlight = False
                highlight_piece_pos = None, None
                highlighted_piece, moving_piece = None, None
                highlight_team = TEAM_RED
                text_game_round = 1
                text_ai_move = None
            else:
                running = False
        elif cchess.get_state() == GAME_STATE_DRAW:
            if popup_window_askokcancel("Too many rounds",
                                        f"Reach {text_game_round} round, now is DRAW, want another game?"):
                cchess = ChineseChess()
                difficulty = MIN_DIFFICULTY
                ai_engine = MinimaxEngine(cchess, AI_TEAM_COLOR, depth_limit=difficulty)

                is_highlight = False
                highlight_piece_pos = None, None
                highlighted_piece, moving_piece = None, None
                highlight_team = TEAM_RED
                text_game_round = 1
                text_ai_move = None
            else:
                running = False
        # elif text_game_round == 50:
        #     # game reach the 50 round
        #     cchess._game_state = GAME_STATE_DRAW
        else:
            # clear the screen and redraw everything
            screen.fill(BOARD_COLOR)
            cchess.init_board(screen=screen)  # init the board and place the pieces to their position.
            round_surface = round_font.render(f'Round: {text_game_round}', True, HAITANG_RED_COLOR)
            screen.blit(round_surface, (480, 750))

            # game is continuing...
            # set AI difficulty slider
            knob_x_pos = SLIDER_X_POS + (
                    (difficulty - MIN_DIFFICULTY) / (MAX_DIFFICULTY - MIN_DIFFICULTY)) * SLIDER_WIDTH
            pygame.draw.rect(screen, SLIDER_COLOR, (SLIDER_X_POS, SLIDER_Y_POS, SLIDER_WIDTH, SLIDER_HEIGHT))
            pygame.draw.circle(screen, KNOB_COLOR, (knob_x_pos, SLIDER_Y_POS + SLIDER_HEIGHT // 2), KNOB_RADIUS)
            for i in range(MIN_DIFFICULTY, MAX_DIFFICULTY + 1):
                line_x = SLIDER_X_POS + ((i - MIN_DIFFICULTY) / (MAX_DIFFICULTY - MIN_DIFFICULTY)) * SLIDER_WIDTH
                pygame.draw.line(screen, DARK_GRAY, (line_x - 1, SLIDER_Y_POS - 2), (line_x - 1, SLIDER_Y_POS + 8), 2)
                # showing difficulty number
                difficulty_text_i = str(i)
                text_font = pygame.font.SysFont(FONT_FAMILY, 30)
                text_surface = text_font.render(difficulty_text_i, True, DARK_GRAY)
                screen.blit(text_surface, (line_x - 5, SLIDER_Y_POS + 10))
            # showing the current difficulty
            difficulty_text = difficulty_font.render(f"Difficulty: {difficulty}", True, DARK_GRAY)
            screen.blit(difficulty_text, (TEXT_DIFFICULTY_X, TEXT_DIFFICULTY_Y))

            text_ai_move_font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
            text_ai_move_surface = text_ai_move_font.render(text_ai_move, True, DARK_GRAY)
            screen.blit(text_ai_move_surface, (12, 750))

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

            if cchess.get_turn() == AI_TEAM_COLOR:
                # cchess_copy = copy(cchess)
                # ai_engine = MinimaxEngine(cchess, AI_TEAM_COLOR)
                piece, _to = ai_engine.AI_Play()
                # No need to update the board info, the AI class has reference this,
                # Which means when human make a move, the AI class's board will also move.
                _from = piece.get_position()
                if piece.get_position() is not None:
                    # cchess.make_piece_move(_from, _to)
                    if not cchess.make_piece_move(_from, _to):
                        pass
                cchess.set_turn(get_other_color(AI_TEAM_COLOR))
                text_game_round += 1
                class_name = extract_class_name(str(type(piece)))
                text_ai_move = f"AI move: {class_name} from {_from} to {_to}"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # when a user clicks a piece, if it is their turn, than show this piece can move to where?
                    if event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # set a difficulty slider
                        if (SLIDER_X_POS <= mouse_x <= SLIDER_X_POS + SLIDER_WIDTH and
                                SLIDER_Y_POS - KNOB_RADIUS * 2 <= mouse_y <= SLIDER_Y_POS + KNOB_RADIUS * 2):
                            knob_x_pos = mouse_x
                            # get difficulty closest to the knob on the slider
                            relative_position = (knob_x_pos - SLIDER_X_POS) / SLIDER_WIDTH
                            difficulty = round(relative_position * (MAX_DIFFICULTY - MIN_DIFFICULTY) + MIN_DIFFICULTY)
                            ai_engine.depth_limit = difficulty
                            # set knob pos according to the difficulty setting.
                            knob_x_pos = SLIDER_X_POS + (
                                    (difficulty - MIN_DIFFICULTY) / (MAX_DIFFICULTY - MIN_DIFFICULTY)) * SLIDER_WIDTH

                        # print(f'mouse_x, mouse_y: {mouse_x, mouse_y}')
                        # may add undo function
                        # may add new game
                        if cchess.get_turn() == TEAM_RED:
                            pieces_pos_list = [p.get_px_position_base_window() for p in
                                               cchess.get_pieces(TEAM_RED)]  # just a list of red piece position
                            # print(f'pieces_pos_list:{pieces_pos_list}\n'
                            #       f'cchess.get_pieces(TEAM_RED):{cchess.get_pieces(TEAM_RED)}')
                            if pieces_pos_list is not None and is_on_board(mouse_x, mouse_y):
                                # highlight the piece
                                highlight_piece_pos, highlighted_piece = (
                                    highlighted_piece_rect_pos(mouse_x, mouse_y, cchess.get_pieces(TEAM_RED))
                                )  # contain x and y

                                # print(f'highlight_piece_pos: {highlight_piece_pos}')
                                if highlight_piece_pos is not None:  # the user clicked a piece, highlight it
                                    is_highlight = True
                                    moving_piece = highlighted_piece
                                    # print(f"available_move:{highlighted_piece.get_available_moves()}")
                                    # print(f"legit_move:{cchess.get_legit_moves(highlighted_piece)}")

                                # the user was clicked a piece then clicked a _to position
                                elif is_highlight:
                                    # get the user want's move
                                    try:
                                        _to_position = is_dot_clicked(cchess, moving_piece, mouse_x, mouse_y)
                                        if _to_position is not None and cchess.make_piece_move(
                                                moving_piece.get_position(), _to_position):
                                            is_highlight = False
                                            cchess.turn_change()
                                            text_ai_move = "Thinking..."
                                        elif _to_position is None:
                                            raise NoneException("_to_position")
                                    except NoneException:
                                        text_hint = (
                                            f'The {extract_class_name(str(type(moving_piece)))} cannot move there, '
                                            'it can only move to positions marked by red dots.\n'
                                            f'{moving_piece.move_hint_text}')
                                        print(text_hint)
                                        # popup_window_showinfo("You cannot move there!", text_hint)

                        elif cchess.get_turn() == TEAM_BLACK:
                            pass
                            # just a list of red piece position
                            pieces_pos_list = [p.get_px_position_base_window() for p in
                                               cchess.get_pieces(TEAM_BLACK)]  # just a list of red piece position
                            # print(f'pieces_pos_list:{pieces_pos_list}\n'
                            #       f'cchess.get_pieces(TEAM_BLACK):{cchess.get_pieces(TEAM_BLACK)}')
                            if pieces_pos_list is not None and is_on_board(mouse_x, mouse_y):
                                # highlight the piece
                                highlight_piece_pos, highlighted_piece = (
                                    highlighted_piece_rect_pos(mouse_x, mouse_y, cchess.get_pieces(TEAM_BLACK))
                                )  # contain x and y

                                # print(f'highlight_piece_pos: {highlight_piece_pos}')
                                if highlight_piece_pos is not None:  # the user clicked a piece, highlight it
                                    is_highlight = True
                                    moving_piece = highlighted_piece
                                    # print(f"available_move:{highlighted_piece.get_available_moves()}")
                                    # print(f"legit_move:{cchess.get_legit_moves(highlighted_piece)}")

                                # the user was clicked a piece then clicked a _to position
                                elif is_highlight:
                                    # get the user want's move
                                    try:
                                        _to_position = is_dot_clicked(cchess, moving_piece, mouse_x, mouse_y)
                                        if _to_position is not None and cchess.make_piece_move(
                                                moving_piece.get_position(), _to_position):
                                            is_highlight = False
                                            cchess.turn_change()
                                        elif _to_position is None:
                                            raise NoneException("_to_position")
                                    except NoneException:
                                        print(f'_to_position: None')

    # exit pygame
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
