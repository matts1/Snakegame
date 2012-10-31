from snakegame.engines import BUILTIN_ENGINES

def first(d):
    for item in d:
        return item

def rsplit_get(s, sep, default):
    if sep not in s:
        return (s, default)
    return s.rsplit(sep, 1)

def import_thing(name, default_obj):
    pkg, obj = rsplit_get(name, ':', default_obj)
    mod = __import__(pkg, fromlist=[obj])
    return getattr(mod, obj)

def load_engine(name, builtins=BUILTIN_ENGINES):
    engine = BUILTIN_ENGINES.get(name, name)
    return import_thing(engine, 'Engine')

def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument(
        '-e', '--engine',
        default=first(BUILTIN_ENGINES),
    )
    parser.add_argument(
        '-l', '--loop',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '-w', '--width',
        default=30,
    )
    parser.add_argument(
        '-h', '--height',
        default=20,
    )
    parser.add_argument(
        '-a', '--apples',
        default=40,
    )
    parser.add_argument('bot', nargs='+')
    args = parser.parse_args(argv)

    engine = load_engine(args.engine)

    game = engine(args.height, args.width, args.apples)

    for name in args.bot:
        bot = import_thing(name, 'bot')
        game.add_bot(bot)

    game.run()

    if args.loop:
        while True:
            game.run()

