"""Mit Kapadia"""
from typing import Any
from random import choice
from games import Game


def interactive_strategy(game: Game) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move:")
    return game.str_to_move(move)


def random_strategy(game: Game) -> Any:
    """
    Return a randomly chosen move for game.
    """
    move = choice(game.current_state.get_possible_moves())
    return game.str_to_move(move)


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
