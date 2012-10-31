from collections import defaultdict, deque
from copy import deepcopy
from random import Random
from string import ascii_lowercase as lowercase
import sys
import traceback

from snakegame.colour import hash_colour
from snakegame import common

class Engine(object):
    def __init__(
        self,
        rows, columns, n_apples,
        wrap=True, results=False,
        random=None,
        *args, **kwargs
    ):
        super(Engine, self).__init__(*args, **kwargs)

        if random is None:
            random = Random()
        self.random = random

        self.wrap = wrap
        self.bots = {}
        self.results = None
        if results:
            self.results = open('results.csv', 'a+')

        self.new_game(rows, columns, n_apples)

    def get_random_position(self):
        x = self.random.randrange(0, self.columns)
        y = self.random.randrange(0, self.rows)
        return (x, y)

    def replace_random(self, old, new):
        for i in xrange(self.rows * self.columns):
            x, y = self.get_random_position()
            if self.board[y][x] == old:
                self.board[y][x] = new
                return x, y

    def new_game(self, rows, columns, n_apples):
        self.game_ticks = 0
        self.game_id = self.random.randint(0, sys.maxint)

        self.letters = list(lowercase)
        self.letters.reverse()

        self.rows = rows
        self.columns = columns

        self.messages_by_team = defaultdict(dict)

        # make board
        self.board = [[common.EMPTY for x in xrange(columns)] for y in xrange(rows)]
        for i in xrange(n_apples):
            x, y = self.get_random_position()
            self.board[y][x] = common.APPLE

    def add_bot(self, bot, team=None):
        """
        A bot is a callable object, with this method signature:
            def bot_callable(
                board=[[cell for cell in row] for row in board],
                position=(snake_x, snake_y)
                ):
                return random.choice('RULD')

        If team is not None, this means you will get a third parameter,
        containing messages from the other bots on your team.
        """
        letter = self.letters.pop()

        name = bot.__name__
        colour = hash_colour(name)

        position = self.replace_random(common.EMPTY, letter.upper())
        if position is None:
            raise KeyError, "Could not insert snake into the board."

        self.bots[letter] = [bot, colour, deque([position]), team]
        return letter

    def remove_bot(self, letter):
        letter = letter.lower()

        time_score = self.game_ticks

        for row in self.board:
            for x, cell in enumerate(row):
                if cell.lower() == letter:
                    row[x] = common.EMPTY

        bot = self.bots[letter]
        del self.bots[letter]
        
        if not self.results:
            try:
                name = bot[0].__name__
                print "%s died with %d length at time %d\n%d bots remaining" % (name, len(bot[2]), time_score, len(self.bots))
                if not len(self.bots):
                    print "Round over. %s wins!\n\n" % name
            except AttributeError:
                pass
            return

        try:
            name = bot[0].__name__
        except AttributeError:
            pass
        else:
            apple_score = len(bot[2])
            self.results.write('%s,%s,%s,%s\n' % \
                (self.game_id, name, apple_score, time_score))
            self.results.flush()

    def update_snakes(self):
        self.game_ticks += 1

        for letter, (bot, colour, path, team) in self.bots.items():
            board = deepcopy(self.board)
            try:
                x, y = path[-1]

                if team is None:
                    d = bot(board, (x, y))
                else:
                    messages = self.messages_by_team[team]
                    d, message = bot(board, (x, y), messages)

                    assert isinstance(message, str), \
                        "Message should be a byte string, not %s (%r)." % (
                            type(message),
                            message,
                        )
                    messages[letter] = message

                # Sanity checking...
                assert isinstance(d, basestring), \
                    "Return value should be a string."
                d = d.upper()
                assert d in common.directions, "Return value should be 'U', 'D', 'L' or 'R'."

                # Get new position.
                dx, dy = common.directions[d]
                nx = x + dx
                ny = y + dy

                if self.wrap:
                    ny %= self.rows
                    nx %= self.columns
                else:
                    if ny < 0 or ny >= self.rows or nx < 0 or nx >= self.columns:
                        self.remove_bot(letter)
                        continue

                oldcell = self.board[ny][nx]
                if common.is_vacant(oldcell):
                    # Move snake forward.
                    self.board[ny][nx] = letter.upper()
                    path.append((nx, ny))

                    # Make old head into body.
                    self.board[y][x] = letter.lower()

                    if oldcell == common.APPLE:
                        # Add in an apple to compensate.
                        self.replace_random(common.EMPTY, common.APPLE)
                    else:
                        # Remove last part of snake.
                        ox, oy = path.popleft()
                        self.board[oy][ox] = common.EMPTY
                else:
                    self.remove_bot(letter)

            except:
                print "Exception in bot %s (%s):" % (letter.upper(), bot)
                print '-'*60
                traceback.print_exc()
                print '-'*60
                self.remove_bot(letter)

