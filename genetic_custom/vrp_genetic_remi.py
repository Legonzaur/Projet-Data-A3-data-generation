import random

vrp = [
    [None, 3, 9, 7, 6],
    [3, None, 1, 2, 8],
    [9, 1, None, 1, 4],
    [7, 2, 1, None, 5],
    [6, 8, 4, 5, None]
]

def generate_gene(vrp):
   a = list(range(len(vrp)))
   random.shuffle(a)
   return a
print(generate_gene(vrp))