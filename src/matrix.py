import numpy as np

def Transpose(matrix):
    rowCount = len(matrix)
    columnCount = len(matrix[0])

    transpose = [[0 for x in range(rowCount)] for y in range(columnCount)]

    for i in range(rowCount):
        for j in range(columnCount):
            transpose[j][i] = matrix[i][j]

    return (transpose)

matrix = [[1, 2, 3, 4], [9, 8, 7, 6]]

transpose = Transpose(matrix)

print(transpose)

