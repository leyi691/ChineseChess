WINDOW_SIZE = (600, 800)
LINE_COLOR = BLACK_COLOR = (0, 0, 0)
BOARD_COLOR = (255, 186, 90)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
HAITANG_RED_COLOR = (200,55,86)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)
LIGHT_BLUE_COLOR = (173, 216, 230)
YELLOW_COLOR = (255, 255, 0)
DARK_GRAY = (85,85,88)

BOARD_SQUARE_SIZE = 56  # Board's Square Size
PIECE_POS_INIT = (13, 16)  # relative to the board left top, locate by left top
DOT_POS_INIT = (40, 40)  # relative to the board left top, locate by center

BOARD_LEFT = 35  # board image left px relative to the window surface.
BOARD_RIGHT = 565  # will change after init the board
BOARD_TOP = 107  # will change after init the board
BOARD_BOTTOM = 693  # will change after init the board

GRID_LEFT = 13  # relative to the board surface
GRID_TOP = 16  #

TEAM_RED = "red"
TEAM_BLACK = "black"
TEAM_OTHER = "white"

GAME_STATE_UNFINISHED = "unfinished"
GAME_STATE_DRAW = "draw"
GAME_STATE_FINISHED = "finished"

DOT_RADIUS = 10

PIECE_SIZE = (53, 52)

HORSE_BLACK1 = 'horse_black1'
HORSE_BLACK2 = 'horse_black2'
HORSE_RED1 = 'horse_red1'
HORSE_RED2 = 'horse_red2'
CANNON_BLACK1 = 'cannon_black1'
CANNON_BLACK2 = 'cannon_black2'
CANNON_RED1 = 'cannon_red1'
CANNON_RED2 = 'cannon_red2'
PAWN_BLACK1 = 'pawn_black1'
PAWN_BLACK2 = 'pawn_black2'
PAWN_BLACK3 = 'pawn_black3'
PAWN_BLACK4 = 'pawn_black4'
PAWN_BLACK5 = 'pawn_black5'
PAWN_RED1 = 'pawn_red1'
PAWN_RED2 = 'pawn_red2'
PAWN_RED3 = 'pawn_red3'
PAWN_RED4 = 'pawn_red4'
PAWN_RED5 = 'pawn_red5'
ADVISOR_BLACK1 = 'advisor_black1'
ADVISOR_BLACK2 = 'advisor_black2'
ADVISOR_RED1 = 'advisor_red1'
ADVISOR_RED2 = 'advisor_red2'
KING_BLACK = 'king_black'
KING_RED = 'king_red'
ELEPHANT_BLACK1 = 'elephant_black1'
ELEPHANT_BLACK2 = 'elephant_black2'
ELEPHANT_RED1 = 'elephant_red1'
ELEPHANT_RED2 = 'elephant_red2'
CHARIOT_BLACK1 = 'chariot_black1'
CHARIOT_BLACK2 = 'chariot_black2'
CHARIOT_RED1 = 'chariot_red1'
CHARIOT_RED2 = 'chariot_red2'

IS_KINGS_FACING = False
FONT_FAMILY = 'Arial'
FONT_SIZE = 30

SCORE_KING = 30
SCORE_ADVISOR = 3
SCORE_ELEPHANT = 4
SCORE_HORSE_SELF_BOARD, SCORE_HORSE_OTHER_BOARD = 5, 10
SCORE_CHARIOT_SELF_BOARD, SCORE_CHARIOT_OTHER_BOARD = 15, 20
SCORE_CANNON_SELF_BOARD, SCORE_CANNON_OTHER_BOARD = 10, 15
SCORE_PAWN_SELF_BOARD, SCORE_PAWN_OTHER_BOARD = 1, 5


AI_TEAM_COLOR = TEAM_BLACK
HUMAN_TEAM_COLOR = TEAM_RED
AI_INF_VALUE = float('inf')

# Minimax Difficulty slider.
MIN_DIFFICULTY = 1
MAX_DIFFICULTY = 4
# slider pos, shapes, color
SLIDER_X_POS = 480
SLIDER_Y_POS = 10
SLIDER_WIDTH = 100
SLIDER_HEIGHT = 8
SLIDER_COLOR = LIGHT_BLUE_COLOR
# shape and color of the knob on the slider.
KNOB_RADIUS = 5
KNOB_X_POS = SLIDER_X_POS
KNOB_COLOR = DARK_GRAY
# difficulty font
FONT_FAMILY_DIFFICULTY = FONT_FAMILY
FONT_SIZE_DIFFICULTY = 30
TEXT_DIFFICULTY_X = 320
TEXT_DIFFICULTY_Y = 8
