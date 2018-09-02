"""Hardcoded policies to play against."""

from . import field as f


class Policy:
    """Base class for policies."""

    def start(self):
        pass

    def gameover(self, posno):
        pass

    def genmove(self, posno):
        raise NotImplementedError()


class TopLeftPolicy(Policy):
    """Policy that plays in leftmost empty cell in topmost nonfull row."""

    def genmove(self, posno):
        return next(f.emptycells(posno))


class CenterCornersPolicy(Policy):
    """Policy that moves into center and then corners."""

    #              Center, Corners   , Sides     .
    preference_order = [4, 0, 2, 6, 8, 1, 3, 5, 7]

    def genmove(self, posno):
        options = [
            (self.preference_order.index(m), m)
            for m in f.emptycells(posno)
        ]
        return min(options)[1]


class BlockAttackPolicy(Policy):
    """Policy that tries to block opponent's lines and build its own."""

    value = {
        'XXX': 100,   # 3 ours -- we win!
        ' OO': -100,  # 2 opps -- we lose next move :(
        ' XX': 10,    # 2 ours -- opportunity for the future.
        '  O': -10,   # 1 opps -- watch out.
        '  X': 1,     # 1 ours -- ok.

        # We don't care about lines that have both players, they are dead.
    }

    def __init__(self, player):
        self.player = player
        if player == f.X:
            self.map = {'X': 'X', 'O': 'O'}
        else:
            self.map = {'X': 'O', 'O': 'X'}

    def normalize(self, chars):
        """Normalize field to make us X."""
        return ''.join(self.map.get(c, ' ') for c in chars)

    def assess_position(self, posno):
        field = self.normalize(f.posno_to_field(posno))
        score = 0
        for line in f.LINESOF3:
            chars = ''.join(sorted(field[c] for c in line))
            score += self.value.get(chars, 0)
        return score

    def genmove(self, posno):
        options = [
            (self.assess_position(f.play(posno, self.player, m)), m)
            for m in f.emptycells(posno)
        ]
        return max(options)[1]
