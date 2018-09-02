#!/usr/bin/python3

from relearn.ticktacktoe import field, vtable, hardcoded


def runmatch(x, o, n):
    """Run a match between two policies.

    Parameters
    ----------
    x : Policy
        Policy that plays X.
    o : Policy
        Policy that plays O.
    n : int
        Number of games in the match.

    Returns
    -------
    xwin, owin : tuple of float
        Wins percentages (1 - xwin - owin = number of draws).

    """
    xwins = owins = 0
    for i in range(n):
        log = field.rungame(x, o)
        winner = field.winner(log[-1])
        if winner == field.X:
            xwins += 1
        elif winner == field.O:
            owins += 1

    return 1.0 * xwins / n, 1.0 * owins / n


x = vtable.VTablePolicy(field.X, 0.1, 0.1)
o = hardcoded.CenterCornersPolicy()

# Train Train Train
print(runmatch(x, o, 100))
print(runmatch(x, o, 100))
print(runmatch(x, o, 100))
print(runmatch(x, o, 100))
print(runmatch(x, o, 100))

# Test
x.curiosity = 0
print(runmatch(x, o, 100))
