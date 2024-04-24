import pygame
from constants import *


def main():
    # init pygame
    pygame.init()
    clock = pygame.time.Clock()

    # set window size and title
    SCREEN_WIDTH, SCREEN_HEIGHT = WINDOW_WIDTH, WINDOW_HEIGHT = WINDOW_SIZE[0], WINDOW_SIZE[1]

    # return a surface obj
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chinese Chess")

    # set chess images as dict
    # the grid of the board is 56x56 px, first node is at x-40, y-60
    chess_images = {
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

    # main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # clear the screen and redraw everything
        screen.fill(WHITE_COLOR)

        # draw board and pieces
        # place board to center
        board_width, board_height = chess_images['board'].get_size()
        window_center_x, window_center_y = WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2
        board_left = window_center_x - board_width // 2
        board_top = window_center_y - board_height // 2
        screen.blit(chess_images['board'], (board_left, board_top))

        # create a subsurface based on the board image.
        bg_rect = pygame.Rect((WINDOW_SIZE[0] // 2 - board_width // 2, WINDOW_SIZE[1] // 2 - board_height // 2),
                              chess_images['board'].get_size())
        background_subsurface = screen.subsurface(bg_rect)
        pygame.draw.circle(background_subsurface, 'red', (40, 40), radius=5)

        # # 更新显示
        # pygame.display.update()

        # 更新屏幕
        pygame.display.flip()

    # 退出Pygame
    pygame.quit()

if __name__ == '__main__':
    main()
