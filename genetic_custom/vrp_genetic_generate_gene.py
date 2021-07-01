import random


def generate_gene(vrp):
    a = list(range(1, len(vrp)))
    random.shuffle(a)
    return a
