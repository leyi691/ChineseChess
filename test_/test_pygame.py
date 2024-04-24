from itertools import chain

from PIL import Image

if __name__ == "__main__":
    pass
    # img = Image.open("../assets/images/select.png")
    #
    # left_half = img.crop((0, 0, img.width // 2, img.height))
    # right_half = img.crop((img.width // 2, 0, img.width, img.height))
    #
    # left_half.save("../assets/images/select_red.png")
    # right_half.save("../assets/images/select_black.png")
    # move_sets = [[_position[0], _position[1] + 1],
    #              [_position[0], _position[1] - 1],
    #              [_position[0] - 1, _position[1]],
    #              [_position[0] + 1, _position[1]]]
