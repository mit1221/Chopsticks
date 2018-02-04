"""Mit Kapadia"""
from typing import List, Union, Optional, Any


class Game:
    """
    A base game class for creating games.

    player - the starting player of the game
    current_state - the current state of the game
    """
    player: str
    current_state: 'CurrentState'

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize a game with player 1 or player 2 starting depending on
        is_p1_turn.

        >>> a = Game(True)
        >>> a.player
        'p1'
        """
        if is_p1_turn:
            self.player = 'p1'
        else:
            self.player = 'p2'
        self.current_state = CurrentState(self.player)

    def get_instructions(self) -> str:
        """
        Return the instructions for self.
        """
        raise NotImplementedError("Need subclasses")

    def str_to_move(self, move: str) -> Any:
        """
        Convert the string move to an actual move to be used by the game.
        """
        raise NotImplementedError("Need subclasses")

    def is_over(self, state: 'CurrentState') -> bool:
        """
        Return True iff state has no more possible moves meaning that the
        game is over.
        """
        return state.get_possible_moves() == []

    def is_winner(self, player: str) -> bool:
        """
        Return True iff player is the winner of the game and False otherwise.
        """
        if self.is_over(self.current_state):
            return self.current_state.current_player != player
        return False

    def __eq__(self, other: Any) -> bool:
        """
        Return True iff self and other are equivalent.
        """
        return issubclass(type(self), Game) == issubclass(type(other), Game) \
            and self.get_instructions() == other.get_instructions()

    def __str__(self) -> str:
        """
        Return a string representation of self.
        """
        raise NotImplementedError("Need subclasses")


class SubtractSquare(Game):
    """
    The Subtract Square game.

    player - the starting player of the game
    current_state - the current state of the game
    """
    player: str
    current_state: 'SubtractSquareState'

    INSTRUCTIONS = 'Players take turns subtracting square numbers from the ' \
                   'starting number. The winner is the person who subtracts ' \
                   'to 0.'

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize a Subtract Square game with player 1 or player 2
        starting depending on is_p1_turn and the initial number to subtract
        from.

        Extends __init__ method from Game.
        """
        Game.__init__(self, is_p1_turn)

        initial_num = input("Enter a non-negative whole number to subtract "
                            "from: ")
        while (not initial_num.isdigit()) or int(initial_num) < 0:
            initial_num = input("Enter a non-negative whole number to subtract "
                                "from: ")
        self.current_state = SubtractSquareState(self.player, int(initial_num))

    def __str__(self) -> str:
        """
        Return a string representation of self.
        """
        return 'The game is Subtract Square.'

    def get_instructions(self) -> str:
        """
        Return the instructions for self. Overrides get_instructions from Game.
        """
        return SubtractSquare.INSTRUCTIONS

    def str_to_move(self, move: Union[str, int]) -> Optional[int]:
        """
        Convert the string move to an actual move to be used by the game.
        """
        if type(move) is int:
            return move
        elif move.isdigit():
            return int(move)
        return None


class Chopsticks(Game):
    """ The Chopsticks game.

    player - the starting player of the game
    current_state - the current state of the game
    """
    player: str
    current_state: 'ChopsticksState'

    INSTRUCTIONS = "Players take turns adding the values of one of their " \
                   "hands to one of their opponents (modulo 5). A hand with a" \
                   " total of 5 (or 0; 5 modulo 5) is considered 'dead'. The " \
                   "first player to have 2 dead hands is the loser."

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize a Chopsticks game with player 1 or player 2
        starting depending on is_p1_turn and each player's hand starting
        with 1 finger out.

        Extends __init__ method from Game.

        >>> a = Chopsticks(False)
        >>> a.player
        'p2'
        """
        Game.__init__(self, is_p1_turn)

        self.current_state = ChopsticksState(self.player, [1, 1, 1, 1])

    def __str__(self) -> str:
        """
        Return a string representation of self.

        >>> a = Chopsticks(True)
        >>> str(a)
        'The game is Chopsticks.'
        """
        return 'The game is Chopsticks.'

    def get_instructions(self) -> str:
        """
        Return the instructions for self. Overrides get_instructions from Game.

        >>> a = Chopsticks(True)
        >>> a.get_instructions() == Chopsticks.INSTRUCTIONS
        True
        """
        return Chopsticks.INSTRUCTIONS

    def str_to_move(self, move: str) -> Optional[str]:
        """Convert the string move to an actual move to be used by the game.

        >>> a = Chopsticks(True)
        >>> a.str_to_move('lr')
        'lr'
        >>> print(a.str_to_move('ab'))
        None
        """
        if move in ['ll', 'lr', 'rl', 'rr']:
            return move
        return None


class CurrentState:
    """The current state of a game.

    current_player - the current player who makes the next move in the game
    """
    current_player: str

    def __init__(self, current_player: str) -> None:
        """
        Initialize a current state where current_player makes the next move.

        >>> state = CurrentState('p1')
        >>> state.current_player
        'p1'
        """
        self.current_player = current_player

    def is_valid_move(self, move: Any) -> bool:
        """
        Return True iff move is a valid move in the game being played.
        """
        return move in self.get_possible_moves()

    def get_current_player_name(self) -> str:
        """
        Return the current player's name.

        >>> state = CurrentState('p2')
        >>> state.get_current_player_name()
        'p2'
        """
        return self.current_player

    def get_possible_moves(self) -> List[Any]:
        """
        Return a list of the possible moves for self.
        """
        raise NotImplementedError("Need subclasses")

    def make_move(self, move: str) -> "CurrentState":
        """
        Return a new CurrentState object with the next player and the
        new state of the game based on move.
        """
        raise NotImplementedError("Need subclasses")

    def __str__(self) -> str:
        """
        Return a string representation of self.
        """
        raise NotImplementedError("Need subclasses")

    def __eq__(self, other: Any) -> bool:
        """
        Return True iff self and other are equivalent.
        """
        raise NotImplementedError("Need subclasses")


class SubtractSquareState(CurrentState):
    """The current state for a Subtract Square game.

    current_player - the current player who makes the next move in the game
    number - the current number to subtract from
    """
    current_player: str
    number: int

    def __init__(self, current_player: str, number: int) -> None:
        """
        Initialize a current state for Subtract Square where current_player
        makes the next move and number is the number to subtract from.

        Extends __init__ method from CurrentState.

        >>> state = SubtractSquareState('p2', 20)
        >>> state.current_player
        'p2'
        >>> state.number
        20
        """
        CurrentState.__init__(self, current_player)
        self.number = number

    def get_possible_moves(self) -> List[int]:
        """
        Return a list of the possible moves for self.

        >>> state1 = SubtractSquareState('p1', 16)
        >>> state1.get_possible_moves()
        [1, 4, 9, 16]
        >>> state2 = SubtractSquareState('p2', 0)
        >>> state2.get_possible_moves()
        []
        """
        return [num for num in range(1, self.number + 1) if
                num ** (1/2) % 1 == 0]

    def make_move(self, move: int) -> "SubtractSquareState":
        """
        Return a new SubtractSquareState object with the next player and the
        new number based on move.

        >>> state1 = SubtractSquareState('p1', 20)
        >>> str(state1.make_move(16))
        'The current player is Player 2 and the current value is 4'
        """
        if self.current_player == 'p1':
            new_player = 'p2'
        else:
            new_player = 'p1'
        return SubtractSquareState(new_player, self.number - move)

    def __str__(self) -> str:
        """
        Return a string representation of self.

        >>> state = SubtractSquareState('p1', 20)
        >>> str(state)
        'The current player is Player 1 and the current value is 20'
        """
        return f'The current player is Player {self.current_player[1]} and ' \
               f'the current value is {self.number}'

    def __eq__(self, other: Any) -> bool:
        """
        Return True iff self and other are equivalent.

        >>> a = SubtractSquareState('p1', 20)
        >>> b = SubtractSquareState('p1', 20)
        >>> c = SubtractSquareState('p1', 10)
        >>> d = ChopsticksState('p1', [1, 1, 1, 2])
        >>> a == b
        True
        >>> a == c
        False
        >>> a == d
        False
        """
        return type(self) == type(other) and self.current_player == \
            other.current_player and self.number == other.number


class ChopsticksState(CurrentState):
    """The current state for a Chopsticks game.

    current_player - the current player who makes the next move in the game
    hands - A tuple where index:
    0: p1's left hand,
    1: p1's right hand,
    2: p2's left hand,
    3: p2's right hand
    """
    current_player: str
    hands: List[int]

    hand_index = {'p1': {'l': 0, 'r': 1, 'll': 2, 'rl': 2, 'lr': 3, 'rr': 3},
                  'p2': {'l': 2, 'r': 3, 'll': 0, 'rl': 0, 'lr': 1, 'rr': 1}}

    def __init__(self, current_player: str, hands: List[int]) -> None:
        """
        Initialize a current state for Chopsticks where current_player
        makes the next move and hands represents the number of fingers out
        on each hand for both players.

        Extends __init__ method from CurrentState.

        >>> state = ChopsticksState('p2', [1, 1, 1, 1])
        >>> state.current_player
        'p2'
        >>> state.hands
        [1, 1, 1, 1]
        """
        CurrentState.__init__(self, current_player)
        self.hands = hands

    def get_possible_moves(self) -> List[str]:
        """
        Return a list of the possible moves for self.

        >>> state1 = ChopsticksState('p1', [1, 1, 1, 1])
        >>> sorted(state1.get_possible_moves())
        ['ll', 'lr', 'rl', 'rr']
        >>> state2 = ChopsticksState('p2', [1, 3, 1, 0])
        >>> sorted(state2.get_possible_moves())
        ['ll', 'lr']
        """
        possible_moves = {'ll', 'lr', 'rl', 'rr'}
        moves_to_remove = set()

        if self.current_player == 'p1':
            current_left_hand = 0
            opponent_left_hand = 2
        else:
            current_left_hand = 2
            opponent_left_hand = 0

        if self.hands[current_left_hand] == 0:
            moves_to_remove.add('ll')
            moves_to_remove.add('lr')
        if self.hands[current_left_hand + 1] == 0:
            moves_to_remove.add('rl')
            moves_to_remove.add('rr')
        if self.hands[opponent_left_hand] == 0:
            moves_to_remove.add('ll')
            moves_to_remove.add('rl')
        if self.hands[opponent_left_hand + 1] == 0:
            moves_to_remove.add('lr')
            moves_to_remove.add('rr')

        return list(possible_moves - moves_to_remove)

    def make_move(self, move: str) -> "ChopsticksState":
        """
        Return a new ChopsticksState object with the next player and the
        new state of each player's hands based on move.

        >>> state1 = ChopsticksState('p1', [1, 1, 1, 1])
        >>> str(state1.make_move('ll'))
        'Player 1: 1-1; Player 2: 2-1'
        >>> state2 = ChopsticksState('p2', [1, 2, 3, 1])
        >>> str(state2.make_move('lr'))
        'Player 1: 1-0; Player 2: 3-1'
        """
        change_index = self.hand_index[self.current_player][move]
        current_player_index = self.hand_index[self.current_player][move[0]]
        return_hands = self.hands[:]

        return_hands[change_index] = (self.hands[change_index] + self.hands
                                      [current_player_index]) % 5

        if self.current_player == 'p1':
            new_player = 'p2'
        else:
            new_player = 'p1'

        return ChopsticksState(new_player, return_hands)

    def __str__(self) -> str:
        """
        Return a string representation of self.

        >>> state = ChopsticksState('p1', [2, 1, 1, 2])
        >>> str(state)
        'Player 1: 2-1; Player 2: 1-2'
        """
        return f'Player 1: {self.hands[0]}-{self.hands[1]}; Player 2: ' \
               f'{self.hands[2]}-{self.hands[3]}'

    def __eq__(self, other: Any) -> bool:
        """
        Return True iff self and other are equivalent.

        >>> a = ChopsticksState('p1', [1, 2, 1, 1])
        >>> b = ChopsticksState('p1', [1, 2, 1, 1])
        >>> c = ChopsticksState('p1', [2, 2, 1, 1])
        >>> d = SubtractSquareState('p1', 20)
        >>> a == b
        True
        >>> a == c
        False
        >>> a == d
        False
        """
        return type(self) == type(other) and self.current_player == \
            other.current_player and self.hands == other.hands


if __name__ == "__main__":
    import python_ta
    from doctest import testmod
    python_ta.check_all(config="a1_pyta.txt")
    testmod()
