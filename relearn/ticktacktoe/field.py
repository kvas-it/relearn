"""Define ticktacktoe field."""

X = 'X'
O = 'O'  # flake8: noqa
_ = ' '

SYMBOLS = [_, X, O]
VALUES = {
    sym: value
    for value, sym in enumerate(SYMBOLS)
}

LINESOF3 = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def posno_to_field(posno):
    """Map position number to a string that shows items in each cell.

    Examples
    --------
    0 -> '         '
    7 -> 'XO       '
    14263 -> 'XO  OXX O'

    """
    return ''.join(
        SYMBOLS[posno // (3 ** i) % 3]
        for i in range(9)
    )


def field_to_posno(field):
    """Map field position (string) to position number."""
    return sum(
        VALUES[field[i]] * 3 ** i
        for i in range(9)
    )


def emptycells(posno):
    """Yield empty cells in a given position.

    Parameters
    ----------
    posno : int
        Current position number.

    Yields
    ------
    cell : int
        Cell numbers that are empty.

    """
    for cell in range(9):
        if posno // (3 ** cell) % 3 == 0:
            yield cell


def is_full(posno):
    """Check if the field is full."""
    return list(emptycells(posno)) == []


def play(posno, player, where):
    """Play a move and return new position.

    Parameters
    ----------
    posno : int
        Starting position number.
    player : str
        Which player plays: X or O.
    where : int
        Where to play (0 - 8).

    Returns
    -------
    new_posno : int
        Position after the move is played.

    Raises
    ------
    ValueError
        If target cell is occupied.

    """
    mul = 3 ** where
    if posno // mul % 3 != 0:
        raise ValueError("Cant' play at {}".format(where))

    return posno + mul * VALUES[player]


def winner(posno):
    """Yield the player that won the game or _ if nobody won."""
    field = posno_to_field(posno)
    for line in LINESOF3:
        a, b, c = [field[p] for p in line]
        if a == b == c:
            if a != _:
                return a
    return _


def rungame(x, o):
    """Run a game between two policies.

    Parameters
    ----------
    x : Policy
        Policy that plays X.
    o : Policy
        Policy that plays O.

    Returns
    -------
    gamelog : list of int
        Log of positions (as position numbers).

    """
    x.start()
    o.start()
    log = [0]  # Start with an empty field.

    def playmove(policy, player):
        before = log[-1]
        move = policy.genmove(before)
        after = play(before, player, move)
        log.append(after)
        if winner(after) != _ or is_full(after):
            x.gameover(after)
            o.gameover(after)
            return True

    while True:
        if playmove(x, X):
            break
        if playmove(o, O):
            break

    return log
