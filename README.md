# Chess AI

This Chess Engine is a computer program designed to handle the logic and rules of the game of chess. It provides functionality for move generation, position evaluation, and other essential operations required for playing chess.

State of code: 16/06/2023
> - Currently the code only acts as an engine for chess and has no AI functionality currently, however this will be added in future progression.

State of code: 20/06/2023
> - A simple AI has been added to be able to make a random move out of the valid available moves to the computer.

State of code: 22/06/2023
> - An AI is able to use NegaMax and alpha beta pruning to select the best moves, with a depth selectable. Currently too slow to have recursion depths of 5+.

## Features

> - Move Generation: The engine can generate all legal moves for a given chess position, including standard moves, castling, en passant, and pawn promotion.

> - Move Validation: The engine can validate whether a given move is legal or not for a specific chess position.

> - Position Evaluation: The engine provides a simple position evaluation function that assigns a score to each board position based on piece values.

> - Game Logic: The engine handles the rules of chess, such as checking for checkmate, stalemate, draw conditions, and en passant captures.

> - User Interface: The project includes a simple text-based user interface that allows players to interact with the engine and play games using algebraic notation.