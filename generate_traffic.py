test_matrix = [
    [0,1,0,0],
    [1,0,1,0],
    [0,1,0,1],
    [0,0,1,0]
]

def browse_matrix(matrix):
    for ligneIndex, ligne in enumerate(matrix):
        for colonneIndex, case in enumerate(ligne):
             print(ligneIndex, colonneIndex, case)




generate_traffic(test_matrix)