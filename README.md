# Introduction
This project provides a comprehensive analysis of the development and implementation of an inter-active Chinese Chess game, focusing on key aspects such as gameplay mechanics, search algorithms, move validation, and challenges encountered during the development process. The project aimed to create an engaging and intelligent Chinese Chess game where a human player competes against a computer AI. The AI employs the Minimax algorithm with Alpha-Beta pruning to make strategic decisions, while the game interface ensures an immersive and user-friendly experience.
# Minimax Evaluation and Alpha-Beta Pruning
The AI employs the Minimax algorithm with Alpha-Beta pruning to optimize decision-making. The minimax method recursively evaluates game states to a specified depth, alternating between maximizing and minimizing players. Alpha-Beta pruning is used to eliminate branches that do not need to be explored, significantly reducing the computational usage. The algorithm tracks the best move evaluations, updating alpha and beta values to prune unnecessary branches effectively. This approach helps the AI make informed decisions several steps ahead and choose the move that maximizes its score.
# Use of Heuristics
Heuristics are used to evaluate the desirability of game states. The static_evaluation method calculates a score based on various factors such as piece value, board control, and the safety of the king. Additional heuristic elements include distance-based scoring for attacking pieces and capturing potential. The count_team_score method further refines the evalua- tion by considering the positions and potential moves of all pieces, ensuring a comprehensive assessment of the game state. This use of heuristics allows the AI to make more nuanced and strategic decisions. More detailed, this methods take 4 marking criteria, in all situation, AI is max player. Firstly, if current state of the board is human player win the game, than score is negative infinite, if AI player win the game, score is positive infinite. Secondly, if current state of the board is AI’s king in check, minus 500 score, if human player’s king in check, add 500 score, which is a huge score, because if put enemy’s king in check is a good. Thirdly, get all pieces in the board and count their score by 3 approaches which are calculate the attack_pieces’ (Horse, Chariot, Cannon, Pawn) attacking score by calculate the Manhattan distance to the enemy’s king, calculate the additional score based on their valid moves which can capturing the piece, put enemy’s king in check, self score, and the score of capturing the piece which make self king in check is 200. Add self side pieces’ score and minus other side pieces’ score.
# Board Representation
The board is visually represented on the screen using Pygame, displaying all pieces in their correct positions on a 10x9 grid, matching the traditional Chinese Chess layout. The graphical interface pleasing visual representation. This visual setup is initialized at the start and updates dynamically as the game progresses, accurately reflecting the game state at all times. The board also accurately reflects the unique elements of Chinese Chess, such as the ”river” in the middle and the ”palaces” where the kings and advisors are confined, horses can move by 1x2 or 2x1, but invalid if there is a piece on the point in between. A Chariot can move and capture either vertically or horizontally by any number of blocks, and it can capture the opponent’s pieces in this way too, and other pieces can only move under rules. Additionally, the four corners of the window display information about the current turn, the AI player’s difficulty level, the AI’s actions, and the round state (as shown in figures 1 and 2).
<img width="868" alt="image" src="https://github.com/user-attachments/assets/966bfa3e-e102-4452-a771-9ddc48af26f8">
# Rejection of Invalid Move
Invalid user moves are promptly rejected by the game, with explanations provided to the player. When a user attempts an invalid move, the game highlights the issue and provides feedback, helping the player understand why the move is not allowed. This feedback mechanism is implemented within the is_valid_move methods of each piece class, which return False if a move does not comply with the rules. The interface then informs the player of the invalid move, maintaining clarity and enhancing the learning experience (as shown in figure 3).
<img width="868" alt="image" src="https://github.com/user-attachments/assets/f8a5de5f-7712-40f9-a4b1-e55e0e7ff3b0">
