from string import ascii_lowercase as lowercase, ascii_uppercase as uppercase
alphabet = lowercase + uppercase

directions = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}

EMPTY = '.'
APPLE = '*'
WALL = '#'

is_empty = EMPTY.__eq__
is_apple = APPLE.__eq__
is_wall = WALL.__eq__

def is_vacant(cell):
    return cell in (EMPTY, APPLE)

def is_blocking(cell):
    return cell not in (EMPTY, APPLE)

def is_snake(cell):
    return cell in alphabet

def is_snake_head(cell):
    return cell in uppercase

def is_snake_body(cell):
    return cell in lowercase

def is_enemy_snake(cell, me):
    assert me.isupper()
    return is_snake(cell) and cell.upper() != me

def is_my_snake(cell, me):
    assert me.isupper()
    return cell.upper() == me

def get_size(board):
    height = len(board)
    width = len(board[0])
    return width, height

def in_bounds(x, y, width, height):
    return (
        x >= 0 and x < width and
        y >= 0 and y < height
    )

def get_cell(board, x, y, wrap=True):
    width, height = get_size(board)
    if wrap:
        x %= width
        y %= height
    elif not in_bounds(x, y, width, height):
        return None
    return board[y][x]
