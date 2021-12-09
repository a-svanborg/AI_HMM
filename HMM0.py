def print_results(matrix):
    list_to_print = []
    list_to_print.append(len(matrix))
    list_to_print.append(len(matrix[0]))

    for row in matrix:
        for entry in row:
            list_to_print.append(round(entry, 2))

    for e in list_to_print:
        print(e, end=" ", flush=True)


def mat_mul(matA, matB):
    multiplied_matrix = [[0] * len(matB[0])] * len(matA)
    for i in range(len(matA)):
        for j in range(len(matB[0])):
            for k in range(len(matB)):
                multiplied_matrix[i][j] += matA[i][k] * matB[k][j]
    return multiplied_matrix

def create_matricies():
    A = []
    B = []
    Pi = []
    for i in input().split():
        A.append(float(i))
    
    for j in input().split():
        B.append(float(j))
        
    for k in input().split():
        Pi.append(float(k))

    rows_n = int(A[0])
    cols_n = int(A[1])
    A_matrix = []
    for i in range((rows_n)):
        row = []
        for j in range((cols_n)):
            row.append(A[i*cols_n + j + 2])
        A_matrix.append(row)

    rows_n = int(B[0])
    cols_n = int(B[1])
    B_matrix = []
    for i in range((rows_n)):
        row = []
        for j in range((cols_n)):
            row.append(B[i*cols_n + j + 2])
        B_matrix.append(row)
    
    rows_n = int(Pi[0])
    cols_n = int(Pi[1])
    Pi_matrix = []
    for i in range((rows_n)):
        row = []
        for j in range((cols_n)):
            row.append(Pi[i*cols_n + j+ 2])
        Pi_matrix.append(row)

    return A_matrix, B_matrix, Pi_matrix

def main():
    """
    Assert kattis input to variables A, B and Pi
    A is the transiation matrix
    B is the observation matrix
    Pi is the initial probability matrix
    """
    A, B, Pi = create_matricies()
    result1 = mat_mul(Pi, A)
    result2 = mat_mul(result1, B)

    print_results(result2)

if __name__ == "__main__":
    main()