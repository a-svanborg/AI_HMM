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

def alpha_pass(alpha, remaining_observations, A, B):
    if len(remaining_observations) < 1:
        return round(sum(alpha), 6)
    term1 = [sum(multiply(alpha, get_column(A, i))) for i in range(len(A))]
    alpha_new = multiply(term1, get_column(B, remaining_observations[0]))
    alpha_t = alpha_pass(alpha_new, remaining_observations[1:], A, B)
    return alpha_t

def get_column(mat, column_index):
    values = [row[column_index] for row in mat]
    return values

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

    alpha_1 = multiply(Pi[0], get_column(B, observations[0]))
    alpha_t = alpha_pass(alpha_1, observations[1:], A, B)
    print(alpha_t)

if __name__ == "__main__":
    main()