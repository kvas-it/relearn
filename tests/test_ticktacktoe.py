"""Tests for ticktacktoe."""

from hypothesis import given
from hypothesis.strategies import integers
import pytest

from relearn.ticktacktoe import field as ttf
from relearn.ticktacktoe import vtable as vt
from relearn.ticktacktoe import hardcoded as hc


@pytest.mark.parametrize('posno,field', [
    (0, '         '),
    (7, 'XO       '),
    (14263, 'XO  OXX O'),
    (19682, 'OOOOOOOOO'),
])
def test_posno_to_field(posno, field):
    assert ttf.posno_to_field(posno) == field


@given(integers(0, 19682))
def test_posno_to_field_and_back(posno):
    assert ttf.field_to_posno(ttf.posno_to_field(posno)) == posno


@pytest.mark.parametrize('posno,cells', [
    (0, list(range(9))),
    (14263, [2, 3, 7]),
    (19682, []),
])
def test_emptycells(posno, cells):
    assert list(ttf.emptycells(posno)) == cells


@pytest.mark.parametrize('posno,is_full', [
    (0, False),
    (14263, False),
    (17060, False),
    (17141, True),
    (17222, True),
    (19682, True),
])
def test_is_full(posno, is_full):
    assert ttf.is_full(posno) == is_full


@pytest.mark.parametrize('posno,player,move,result', [
    (0, ttf.X, 0, 1),
    (0, ttf.O, 0, 2),
    (14263, ttf.X, 2, 14272),
    (14263, ttf.X, 3, 14290),
    (14263, ttf.X, 4, ValueError),
    (14263, ttf.O, 2, 14281),
])
def test_play(posno, player, move, result):
    if result == ValueError:
        with pytest.raises(ValueError):
            ttf.play(posno, player, move)
    else:
        assert ttf.play(posno, player, move) == result


@pytest.mark.parametrize('posno,winner', [
    (0, ttf._),
    (13, ttf.X),
    (26, ttf.O),
    (757, ttf.X),
    (6643, ttf.X),
    (1638, ttf.O),
])
def test_winner(posno, winner):
    assert ttf.winner(posno) == winner


@pytest.mark.parametrize('posno,move', [
    (0, 0),
    (1, 1),
    (4, 2),
    (13, 3),
])
def test_top_left(posno, move):
    tl = hc.TopLeftPolicy()
    tl.start()
    assert tl.genmove(posno) == move


@pytest.fixture(scope='session')
def vtable_const():
    """VTable policy that doesn't learn and doesn't explore."""
    return vt.VTablePolicy(ttf.X, 0, 0)


@pytest.fixture(scope='function')
def vtable_learn(vtable_const):
    """VTable policy with zeroed out vtable that learns and doesn't explore."""
    return vt.VTablePolicy(ttf.X, 0.5, 0, vtable=([0] * 19683))


@pytest.mark.parametrize('posno,value', [
    (0, 0.5),
    (13, 1),
    (26, 0),
])
def test_vtable_init(vtable_const, posno, value):
    assert vtable_const.vtable[posno] == value


@pytest.mark.parametrize('posno,move', [
    (4, 2),
    (28, 6),
])
def test_vtable_genmove(vtable_const, posno, move):
    vtable_const.start()
    assert vtable_const.genmove(posno) == move


@pytest.mark.parametrize('posno', [
    0,
    2,
    10469,  # A fork by O set up so that TopLeftPolicy will win.
])
def test_vtable_learn(vtable_learn, posno):
    """Test that the policy learns from its moves."""
    vtable_learn.start()
    tl = hc.TopLeftPolicy()
    tl.start()

    # Generate a random move move.
    move = vtable_learn.genmove(posno)
    # And remember position after it.
    pos1 = ttf.play(posno, vtable_learn.player, move)
    # Now let top_left play one move.
    pos2 = ttf.play(pos1, ttf.O, tl.genmove(pos1))

    gameover = ttf.winner(pos2) != ttf._
    if gameover:
        vtable_learn.vtable[pos2] = 1
        vtable_learn.gameover(pos2)
        # If the game is over, we expect value propagation from pos2 to pos1.
        assert vtable_learn.vtable[pos1] == 0.5
    else:
        # If it's not over, we pre-program agent's next move:
        next_move = next(ttf.emptycells(pos2))
        # by placing reward there.
        pos3 = ttf.play(pos2, vtable_learn.player, next_move)
        vtable_learn.vtable[pos3] = 2
        # Now we expect value propagation from pos3 to pos1.
        assert vtable_learn.genmove(pos2) == next_move
        assert vtable_learn.vtable[pos1] == 1


def test_rungame_tl():
    """Run game between two instances of TopLeftPolicy."""
    x = hc.TopLeftPolicy()
    o = hc.TopLeftPolicy()
    assert ttf.rungame(x, o) == [0, 1, 7, 16, 70, 151, 637, 1366]


def test_rungame_cc():
    """Run game between two instances of CenterCornersPolicy."""
    x = hc.CenterCornersPolicy()
    o = hc.CenterCornersPolicy()
    assert ttf.rungame(x, o) == [0, 81, 83, 92, 1550, 8111,
                                 8117, 8144, 8630, 10817]


def test_rungame_ba():
    """Run a game between two instances of BlockAttackPolicy."""
    x = hc.BlockAttackPolicy(ttf.X)
    o = hc.BlockAttackPolicy(ttf.O)
    expect = [0, 81, 13203, 13932, 13950, 14193, 14247, 14250, 18624, 18625]
    assert ttf.rungame(x, o) == expect
