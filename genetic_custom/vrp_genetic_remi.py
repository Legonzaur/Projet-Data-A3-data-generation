import sys
import random
import math

# On a une grapue à 5 nodes et 8 arêtes

vrp = [
    [None, 3, 9, 7, 6],
    [3, None, 1, 2, 8],
    [9, 1, None, 1, 4],
    [7, 2, 1, None, 5],
    [6, 8, 4, 5, None]
]


#
# Premièrement, on lit le VRP
