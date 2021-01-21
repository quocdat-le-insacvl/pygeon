import numpy


matrice = [[1,2],[3,4]]
#on veut la matrice [[1,3],[2,4]]

matrice = [[1,2,3,4,5],\
    [6,7,8,9,10],\
    [11,12,13,14,15],\
    [16,17,18,19,20],\
    [21,22,23,24,25]]
#on veut la matrice
#[[1,4,9,14,19],[2,5,10,15,20],[3,6,11,16,21],[4,7,12,17,22],[5,8,13,18,23]]
matriceB = [[matrice[x][y] for x in range(len(matrice))] for y in range(len(matrice[0]))]
print(matriceB)
matriceB = [[matriceB[x][y] for x in range(len(matriceB))] for y in range(len(matriceB[0]))]
print(matriceB)
print(numpy.rot90(matrice,-1))

