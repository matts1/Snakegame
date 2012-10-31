from random import choice

from snakegame import common

def make_direction_bot(direction, human):
    def bot(board, position):
        return direction
    bot.__doc__ = 'This bot always moves %s.' % human
    return bot

up_bot = make_direction_bot('U', 'up')
down_bot = make_direction_bot('D', 'down')
left_bot = make_direction_bot('L', 'left')
right_bot = make_direction_bot('R', 'right')

def random_bot(board, position):
    "This bot just chooses a random direction to move."
    return choice('UDLR')

def random_avoid_bot(board, position):
    """
    This bot chooses a random direction to move, but will not move into a
    square which will kill it immediately (unless it has no choice).
    """
    x, y = position

    available = []
    for direction, (dx, dy) in common.directions.items():
        cell = common.get_cell(board, x + dx, y + dy)
        if common.is_vacant(cell):
            available.append(direction)

    if not available:
        return 'U'
    return choice(available)

BUILTIN_BOTS = {
    'up_bot': up_bot,
    'down_bot': down_bot,
    'left_bot': left_bot,
    'right_bot': right_bot,
    'random_bot': random_bot,
    'random_avoid_bot': random_avoid_bot,
}
