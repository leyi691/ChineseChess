import unittest
import pygame
from constants import *
from Piece import *
from functions import *

from ChineseChess import ChineseChess


class TestProjects(unittest.TestCase):

    def test_ChineseChess(self):
        cchess = ChineseChess()
        cchess._pieces={}
        # Test king
        # cchess._board_pieces_position[4][0] = Piece.King(TEAM_RED, [4, 0])
        # print(cchess.make_piece_move([4, 0], [4, 1]))
        # # result
        # print(cchess._board_pieces_position[4][0],
        #       cchess._board_pieces_position[4][1])

        horse = Horse(TEAM_RED, [5, 5])
        cannon = Cannon(TEAM_RED, [4, 6])
        cannon2 = Cannon(TEAM_RED, [6, 6])

        cchess._board_pieces_position[5][5] = horse
        cchess._board_pieces_position[4][6] = cannon
        cchess._board_pieces_position[5][6] = cannon2

        cchess._pieces['test_horse'] = horse
        cchess._pieces['test_cannon'] = cannon
        cchess._pieces['test_cannon2'] = cannon2

        print(horse.is_valid_move([4, 3], cchess.get_pieces()))

    def test_elephant(self):

        cchess = ChineseChess()

        cchess._pieces={}

        elephant = Elephant(TEAM_RED, [6, 4])
        cannon = Cannon(TEAM_RED, [5, 3])
        cannon2 = Cannon(TEAM_RED, [5, 6])

        cchess._board_pieces_position[6][4] = elephant
        cchess._board_pieces_position[5][3] = cannon
        # cchess._board_pieces_position[5][6] = cannon2

        cchess._pieces['test_elephant'] = elephant
        cchess._pieces['test_cannon'] = cannon
        # cchess._pieces['test_cannon2'] = cannon2

        print(elephant)
        print(elephant.is_valid_move([8, 2], cchess.get_pieces()))

    def test_functions(self):
        popup_window_askokcancel("Check", "popup Check")

