# Fun with reinforcement learning

This repository contains toy examples of reinforcement learning algorithms.

## TickTackToe

`relearn.ticktacktoe` contains a setup for playing TickTackToe policies against
each other together with a couple of hardcoded policies and one learning one.

The learning policy keeps an estimate of probability of wining from each
position and updates it as it tries playing different moves. It can usually
learn to always beat the best hardcoded policy I have here (obviously not the
optimal one) after 100 games (in the first rounds the hardcoded policy usually
wins all games):

    $ python /Users/vkuznetsov/Documents/prog/personal/relearn/ttt.py
    Round 0 (of 10 games): curiosity = 0.200000  WIN:   0%, LOSE:  70%
    Round 1 (of 10 games): curiosity = 0.100000  WIN:   0%, LOSE:  70%
    Round 2 (of 10 games): curiosity = 0.050000  WIN:   0%, LOSE:  60%
    Round 3 (of 10 games): curiosity = 0.025000  WIN:   0%, LOSE:  50%
    Round 4 (of 10 games): curiosity = 0.012500  WIN:   0%, LOSE:  40%
    Round 5 (of 10 games): curiosity = 0.006250  WIN:  10%, LOSE:  40%
    Round 6 (of 10 games): curiosity = 0.003125  WIN:  30%, LOSE:  70%
    Round 7 (of 10 games): curiosity = 0.001563  WIN: 100%, LOSE:   0%
    Round 8 (of 10 games): curiosity = 0.000781  WIN: 100%, LOSE:   0%
    Round 9 (of 10 games): curiosity = 0.000391  WIN: 100%, LOSE:   0%

    Demo:
       |  X|  X|  X|  X|X X|X X|XXX
       |   | O | O | O | O |OO |OO
       |   |   |X  |X O|X O|X O|X O

What happens is that the learning policy learns to build forks and the
hardcoded policy doesn't know how to avoid that.

## Testing

Run tests with Tox:

    $ tox
