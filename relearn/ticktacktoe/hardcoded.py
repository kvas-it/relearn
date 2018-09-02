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
