import random

import Piece
from constants import *
from functions import get_other_color, is_piece_at_self_board, extract_class_name
from numpy import inf
from Piece import *
from collections import namedtuple
from copy import copy, deepcopy
import time


PieceData = namedtuple('Successor_eval', ['piece', 'position', 'value'])


class MinimaxEngine:
    def __init__(self, chinese_chess_obj, ai_team_color, depth_limit=None):
        self.cchess = copy(chinese_chess_obj)

        self.free_position = None
        self.AI_team_color = ai_team_color
        self.se_count = 0  # how many status for this move count
        self.depth_explored = 0  # how many depth this time
        self.pruned_count = 0  # how many branch were pruned
        if depth_limit is None:
            self.depth_limit = 2  # control game difficulty
        else:
            self.depth_limit = depth_limit
        self.successor_evaluations = []  # a namedtuple of piece, move and move's value (piece='',position='',value='')
        self.use_pruning = True  # using pruning?
        # self.trace_indent = 0  # trace printing utility
        # self.verbose = False

    def AI_Play(self):
        """AI make move"""
        print('Thinking...')
        self.start_evaluation()
        print("Explored to depth " + str(self.depth_explored) + ", " + str(self.se_count) +
              " static evaluations, " + str(self.pruned_count) + " pruned branches")
        best_piece_move = self.get_best_piece_with_move()  # get [(Piece),(move)]
        piece, move = best_piece_move
        return piece, move
        # if self.cchess.make_piece_move(piece.get_position(), move):
        #     self.cchess.set_turn(get_other_color(self.AI_team_color))
        #     return True

    def occupy(self, piece, position, cchess):
        """Since multiple recursions are required,
        the child nodes of each recursion assume that a move has been made, which is occupy()"""
        if not isinstance(piece, Just_Piece) and piece is not None and piece.get_position() is not None:
            _to = position
            _to_piece = cchess.get_piece_at_position(position)
            if isinstance(_to_piece, Just_Piece):
                _to_is_just_piece = True
            else:
                _to_is_just_piece = False
            _from = piece.get_position()
            _from_piece = cchess.get_piece_at_position(piece.get_position())
            cchess.make_piece_move_occupy(_from, _to)
            return _from_piece, _from, _to_piece, _to, _to_is_just_piece
        else:
            if piece.get_position() is None:
                pass
            return None


    def restore(self, _from_piece, _from, _to_piece, _to, _to_is_just_piece, cchess):
        """All _from _to is original piece position, it's before occupy()."""
        _from_piece.set_position(_from)
        _to_piece.set_position(_to)
        _from_piece._is_eaten = False
        if not _to_is_just_piece:
            _to_piece._is_eaten = False
        cchess._board_pieces_position[_from[0], _from[1]] = _from_piece
        cchess._board_pieces_position[_to[0], _to[1]] = _to_piece
        if cchess._game_state == GAME_STATE_FINISHED:
            cchess._game_state = GAME_STATE_UNFINISHED

    def start_evaluation(self):
        """start to recursively assess the value of where each piece walks"""
        # Initialize counters for statistics
        self.se_count, self.depth_explored, self.pruned_count = 0, 0, 0
        # Initialize the list to store successor evaluations, which includes piece, move, and the move's value
        self.successor_evaluations = []  # A namedtuple of piece, move, and move's value (piece='', position='', value='')
        # Start the minimax algorithm with initial parameters
        self.minimax(Just_Piece(), None, 0, -inf, inf)

    def static_evaluation(self, player):
        """return the value of the leaf node"""
        result = 0
        # Check if the AI has won
        if self.cchess.has_won(AI_TEAM_COLOR):
            result = float("inf")
        # Check if the human player has won
        elif self.cchess.has_won(HUMAN_TEAM_COLOR):
            result = float("-inf")
        else:
            # Check if any king is in check
            if self.cchess.in_check[2]:
                # If AI's king is in check, deduct points
                if self.cchess.in_check[0].get_color() == AI_TEAM_COLOR:
                    result += 500  # Human in check
                # If human's king is in check, add points
                if self.cchess.in_check[0].get_color() == HUMAN_TEAM_COLOR:
                    result -= 500  # AI in check
            # Add the team score to the result
            result += self.count_team_score()
        # print(f"Static evaluation for {player}: {result}")
        return result

    def count_team_score(self):
        def get_king_position(color):
            """Get the position of the king of the given color"""
            if color == TEAM_RED:
                return self.cchess._pieces[KING_RED].get_position()
            else:
                return self.cchess._pieces[KING_BLACK].get_position()

        res_score = 0
        # Get positions of both AI and human kings
        king_ai_position = get_king_position(self.AI_team_color)
        king_human_position = get_king_position(get_other_color(self.AI_team_color))

        def calculate_piece_score(piece, king_position, king_color):
            """Calculate the score for a single piece."""
            piece_score = piece.get_basic_score() * 8
            piece_position = piece.get_position()
            valid_moves = self.cchess.get_legit_moves(piece)

            distance_score = 0
            attacking_map = [Horse, Chariot, Cannon, Pawn]
            # Calculate distance-based score if the piece is an attacking piece
            if piece_position is not None and piece in attacking_map:
                # Calculate Manhattan distance to the enemy king
                distance = abs(piece_position[0] - king_position[0]) + abs(piece_position[1] - king_position[1])
                distance_score = distance

                # If the piece is closer to the enemy king, increase its score
                if piece.get_color() == get_other_color(king_color):
                    piece_score += distance_score

            # Define a scoring map for different pieces
            scoring_map = {
                King: SCORE_KING,
                Advisor: SCORE_ADVISOR,
                Elephant: SCORE_ELEPHANT,
                Horse: (SCORE_HORSE_SELF_BOARD, SCORE_HORSE_OTHER_BOARD),
                Chariot: (SCORE_CHARIOT_SELF_BOARD, SCORE_CHARIOT_OTHER_BOARD),
                Cannon: (SCORE_CANNON_SELF_BOARD, SCORE_CANNON_OTHER_BOARD)
            }
            move_score = 0
            # Calculate additional score based on valid moves
            for valid_move in valid_moves:
                obj_on_the_move_pos = self.cchess.get_piece_at_position(valid_move)
                if obj_on_the_move_pos and not isinstance(obj_on_the_move_pos, Just_Piece):
                    # Extra points for capturing the piece putting the king in check
                    piece_type = type(obj_on_the_move_pos)
                    if self.cchess.in_check[2] and obj_on_the_move_pos == self.cchess.in_check[0]:
                        piece_score += 200  # Extra points for capturing the piece putting the king in check
                    if piece_type in scoring_map:
                        score_ = scoring_map[piece_type]
                        if isinstance(score_, tuple):  # For pieces with different scores on self/other board
                            if is_piece_at_self_board(obj_on_the_move_pos):
                                score_ = score_[1] if piece.get_color() == self.AI_team_color else -score_[1]
                            else:
                                score_ = score_[0] if piece.get_color() == self.AI_team_color else -score_[0]
                        else:
                            score_ = score_ if piece.get_color() == self.AI_team_color else -score_
                        move_score += score_
            piece_score += move_score
            # Print the piece score for debugging
            # print(
            #     f"Piece: {piece}, Basic score: {piece.get_basic_score()}, Distance score: {distance_score}, Total score: {piece_score}")
            return piece_score

        # Calculate the score for all AI pieces
        for piece in self.cchess.get_pieces(AI_TEAM_COLOR):
            res_score += calculate_piece_score(piece, king_human_position, HUMAN_TEAM_COLOR)
        # Calculate the score for all human pieces
        for piece in self.cchess.get_pieces(HUMAN_TEAM_COLOR):
            res_score -= calculate_piece_score(piece, king_ai_position, AI_TEAM_COLOR)

        # Print the final score to be sent to minimax
        # print(f"send to minimax score: {res_score}")

        return res_score



    def minimax(self, piece, position, depth, alpha, beta):
        """Perform the minimax algorithm with alpha-beta pruning."""
        # print(f"Minimax called: depth {depth}, piece {piece}, position {position}, alpha {alpha}, beta {beta}")

        # Determine if we are maximizing or minimizing based on the depth
        maximizing = True if depth % 2 == 0 else False
        cchess = self.cchess

        # Occupy the position with the piece and store the previous state for restoration
        _restore = self.occupy(piece, position, cchess)

        self.depth_explored = max(depth, self.depth_explored)

        # Get the free positions available for AI and Human teams
        free_positions_black_dict = self.get_free_positions(AI_TEAM_COLOR)
        free_positions_red_dict = self.get_free_positions(HUMAN_TEAM_COLOR)

        # Initial best value based on static evaluation
        best_value = self.static_evaluation(AI_TEAM_COLOR)
        # print(f"Initial best value at depth {depth}: {best_value}")

        # If the depth limit is reached, count this evaluation
        if depth >= self.depth_limit:
            self.se_count += 1
        else:
            # If we are maximizing
            if maximizing:
                best_value = -float('inf')
                for _piece, poses in free_positions_black_dict.items():
                    for pos in poses:
                        # Recursively call minimax for the next depth
                        value = self.minimax(_piece, pos, depth + 1, alpha, beta)
                        # print(
                        #     f"Maximizing: depth {depth}, piece {_piece}, pos {pos}, value {value}, alpha {alpha}, beta {beta}")
                        # Store the evaluation for the top level call
                        if depth == 0:
                            self.successor_evaluations.append(PieceData(piece=_piece, position=pos, value=value))
                        # Update the best value and alpha for maximizing player
                        best_value = max(best_value, value)
                        alpha = max(alpha, best_value)
                        # Alpha-beta pruning
                        if self.use_pruning and alpha >= beta:
                            self.pruned_count += 1
                            break
                    if self.use_pruning and alpha >= beta:
                        break
            # If we are minimizing
            else:
                best_value = float('inf')
                for _piece, poses in free_positions_red_dict.items():
                    for pos in poses:
                        # Recursively call minimax for the next depth
                        value = self.minimax(_piece, pos, depth + 1, alpha, beta)
                        # print(
                        #     f"Minimizing: depth {depth}, piece {_piece}, pos {pos}, value {value}, alpha {alpha}, beta {beta}")
                        # Update the best value and beta for minimizing player
                        best_value = min(best_value, value)
                        beta = min(beta, best_value)
                        # Alpha-beta pruning
                        if self.use_pruning and alpha >= beta:
                            self.pruned_count += 1
                            break
                    if self.use_pruning and alpha >= beta:
                        break

        # Restore the previous state of the board
        if _restore is not None:
            _from_piece, _from, _to_piece, _to, _to_is_just_piece = _restore
            self.restore(_from_piece, _from, _to_piece, _to, _to_is_just_piece, cchess)

        # print(f"Returning best value at depth {depth}: {best_value}")
        return best_value

    # def pruning_warning(self, depth, alpha, beta, value):
    #     print("Bounds breached at depth " + str(depth) + ": beta " + str(beta) + ", value " + str(
    #         value) + ", alpha " + str(alpha))

    def get_free_positions(self, color=None):
        """Return a dictionary of pieces and their legal moves for the specified color.

        The dictionary format is:
        {Piece: [[x1, y1], [x2, y2], ...]}

        Args:
            color: The color of the pieces to get moves for.

        Returns:
            A dictionary mapping each piece to a list of its legal moves.
        """
        piece_move_dict = {}
        for piece in self.cchess.get_pieces(color):
            piece_move_dict[piece] = self.cchess.get_legit_moves(piece)

        return piece_move_dict

    def get_best_piece_with_move(self):
        """Determine the best piece and move based on the evaluations of successor states.

        This function finds the move with the highest evaluation value. If there are multiple
        moves with the same highest value, it randomly selects one among them.

        Returns:
            A list containing the best piece and its move.
        """
        maximize = float("-inf")
        best = None
        equal_count = 0
        # Iterate through all evaluated successor states
        for _ in self.successor_evaluations:
            piece, move, value = _
            # Count how many moves have the maximum value
            if maximize == value:
                equal_count += 1
            # Update the best move if a higher value is found
            if maximize <= value:
                maximize = value
                best = [piece, move]
        # print(equal_count, len(self.successor_evaluations))
        # If all evaluated moves have the same value, randomly choose one
        if equal_count == len(self.successor_evaluations)-1:
            _ = self.successor_evaluations[random.randint(0, len(self.successor_evaluations))]
            piece, move, value = _
            best = [piece, move]
            print(f"random choice")
        # Print the best move for debugging
        print(f'best move is:{extract_class_name(str(type(best[0])))}, {best[0].get_color()}, {best[1]}: {maximize}\n')
        return best
