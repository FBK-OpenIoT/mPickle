# from micropython-lib
def count(start=0, step=1):
    while True:
        yield start
        start += step


def cycle(p):
    try:
        len(p)
    except TypeError:
        # len() is not defined for this type. Assume it is
        # a finite iterable so we must cache the elements.
        cache = []
        for i in p:
            yield i
            cache.append(i)
        p = cache
    while p:
        yield from p


def repeat(el, n=None):
    if n is None:
        while True:
            yield el
    else:
        for i in range(n):
            yield el


def chain(*p):
    for i in p:
        yield from i


def islice(iterable, *args):
    print(args)
    start = 0
    stop = None
    step = 1
    if len(args) == 1:
        stop = args[0]
    elif len(args) >= 2:
        start = args[0]
        stop = args[1]
        if len(args)==3:
            step = args[2]
    if start < 0 or (stop is not None and stop < 0) or step <= 0:
        raise ValueError
    #
    indices = count() if stop is None else range(max(start, stop))
    next_i = start
    for i, element in zip(indices, iterable):
        if i == next_i:
            yield element
            next_i += step


def tee(iterable, n=2):
    return [iter(iterable)] * n


def starmap(function, iterable):
    for args in iterable:
        yield function(*args)


def accumulate(iterable, func=lambda x, y: x + y):
    it = iter(iterable)
    try:
        acc = next(it)
    except StopIteration:
        return
    yield acc
    for element in it:
        acc = func(acc, element)
        yield acc
