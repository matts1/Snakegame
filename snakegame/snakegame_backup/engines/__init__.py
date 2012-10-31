try:
    from collections import OrderedDict as MaybeOrderedDict
except ImportError:
    MaybeOrderedDict = dict

from snakegame.engines.base import Engine

BUILTIN_ENGINES = MaybeOrderedDict()

def add_engine(name):
    class_name = name.title() + 'Engine'
    BUILTIN_ENGINES[name] = 'snakegame.engines.%s:%s' % (name, class_name)

add_engine('pyglet')
add_engine('pygame')
add_engine('curses')
