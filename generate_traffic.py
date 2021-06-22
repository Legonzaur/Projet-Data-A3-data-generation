import copy
import pprint
import random

initial_matrix = [
    [None,1,None,None],
    [1,None,1,None],
    [None,1,None,1],
    [None,None,None,None]
]

temp_matrix = copy.deepcopy(initial_matrix)

def generate_traffic():
    rand = random.randint(1,10)
    return rand

def browse_matrix(matrix):
    output = copy.deepcopy(matrix)
    #Iterate through matrix
    for ligneIndex, ligne in enumerate(matrix):
        for colonneIndex, case in enumerate(ligne):
            #If connection is present
            if case == 1:
                output[ligneIndex][colonneIndex] = generate_traffic()
                #If connection is bidirectional
                if matrix[colonneIndex][ligneIndex] == 1:
                    matrix[colonneIndex][ligneIndex] = None
                    output[colonneIndex][ligneIndex] = output[ligneIndex][colonneIndex]
    return output

pprint.pprint(browse_matrix(temp_matrix))