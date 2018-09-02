"""Simple learner based on a value table."""

import random

from . import field as f


def init_vtable(player):
    """Generate initial value map.

    Parameters
    ----------
    player : str
        Player for whom we're generating the map.

    Returns
    -------
    map : list of float
        19683 numbers that show initial probability of winning from this
        position. It would be 1 if `player` won, 0 if opponent won and 0.5
        if nobody won yet.

    """
    vmap = []
    for posno in range(19683):
        w = f.winner(posno)
        if w == player:
            vmap.append(1)
        elif w == f._:
            vmap.append(0.5)
        else:
            vmap.append(0)

    return vmap


class VTablePolicy:
    """Policy based on a value table that is updated as we learn."""

    # Position after our last move (used for learning).
    _last_posno = None

    def __init__(self, player, alpha, curiosity, vtable=None):
        """Initialize the policy.

        Parameters
        ----------
        player : str
            Player for which we'll be playing.
        alpha : float
            Learning speed.
        curiosity : float
            Probability of exploratory steps (picking not max-value next move).
        vtable : list of floats
            Value table to start with (it will be copied). By default all
            winning positions are assigned a value of 1, all losing positions
            are assigned a value of 0, and everything else gets 0.5.

        """
        self.player = player
        self.alpha = alpha
        self.curiosity = curiosity

        if vtable is None:
            self.vtable = init_vtable(player)
        else:
            self.vtable = list(vtable)

    def _learn(self, value):
        """Propagate value to the position before current."""
        if self._last_posno is None:
            return
        if self.alpha == 0:
            return

        delta = value - self.vtable[self._last_posno]
        self.vtable[self._last_posno] += self.alpha * delta
        self._last_posno = None

    def start(self):
        """Start new game."""
        self._last_posno = None

    def gameover(self, posno):
        """The game is over."""
        self._learn(self.vtable[posno])

    def evalmove(self, posno, move):
        """Evaluate move (based on value map).

        Parameters
        ----------
        posno : int
            Position from which the move is made.
        move : int
            Cell into which we move.

        Returns
        -------
        value : float
            Value of the resulting position.

        """
        result = f.play(posno, self.player, move)
        return self.vtable[result]

    def genmove(self, posno):
        """Generate next move.

        Parameters
        ----------
        posno : int
            Position from which to start.

        Returns
        -------
        move : int
            Position for the next move.

        """
        moves = list(f.emptycells(posno))
        move_values = {
            move: self.evalmove(posno, move)
            for move in moves
        }
        max_value = max(move_values.values())

        # Learn that we could get to this best value from last move.
        self._learn(max_value)

        explore = random.random() < self.curiosity
        if explore:
            move = random.choice(moves)
        else:
            top_moves = [m for m, v in move_values.items() if v == max_value]
            move = random.choice(top_moves)

        # Remember where we moved for the next iteration of learning.
        self._last_posno = f.play(posno, self.player, move)

        return move
