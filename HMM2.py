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

def multiply(matA, matB):
    multiplied = [a*b for a, b in zip(matA,matB)]
    return multiplied

def get_column(mat, column_index):
    values = [row[column_index] for row in mat]
    return values

def viterbi(A, B, Pi, observations):
    delta = []
    temp_list = []
    for i in range(len(Pi[0])):
        temp_list.append(Pi[0][i] * B[i][observations[0]])
    delta.append(temp_list)
    for t in range(1, len(observations)):
        temp_list = []
        for i in range(len(A)):
            probability = max(delta[t-1][j] * A[j][i] * B[i][observations[t]] for j in range(len(A)))
            temp_list.append(probability)
        delta.append(temp_list)

    # Argmax
    for row in delta:
        idx = row.index(max(row))
        print(idx, end=" ", flush=True)

def main():
    """
    Assert kattis input to variables A, B, Pi and observations
    A is the transiation matrix
    B is the observation matrix
    Pi is the initial probability matrix
    Observations is the list containing previous states
    """
    A, B, Pi = create_matricies()
    observations = []
    for i in input().split():
        observations.append(int(i))
    
    observations_n = observations[0]
    observations = observations[1:]

    viterbi(A, B, Pi, observations)

if __name__ == "__main__":
    main()