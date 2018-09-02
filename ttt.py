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


x = vtable.VTablePolicy(field.X, 0.2, 0.2)
o = hardcoded.BlockAttackPolicy(field.O)

# Train
games_in_round = 10
rounds = 10
curiosity_multiplier = 0.5

for i in range(rounds):
    wins, losses = runmatch(x, o, games_in_round)
    print('Round {} (of {} games): curiosity = {:5f}  '
          'WIN: {:4.0%}, LOSE: {:4.0%}'
          .format(i, games_in_round, x.curiosity, wins, losses))
    x.curiosity *= curiosity_multiplier

# Demo!
print('')
print('Demo:')
log = field.rungame(x, o)
fields = [field.posno_to_field(p) for p in log]
print('|'.join(f[:3] for f in fields))
print('|'.join(f[3:6] for f in fields))
print('|'.join(f[6:] for f in fields))
