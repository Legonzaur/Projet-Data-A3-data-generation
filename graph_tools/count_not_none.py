import functools


def reductfunc(acc, val):
    if acc != 0 and acc != 1:
        acc = 0
    if val == None:
        return acc
    return 1


def count_not_none(iterable):
    return functools.reduce(reductfunc, iterable)
