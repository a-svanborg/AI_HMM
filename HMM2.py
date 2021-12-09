# import sys
def create_matricies(args):
    A = []
    B = []
    Pi = []
    for i in args[0].split():
        A.append(float(i))
    
    for j in args[1].split():
        B.append(float(j))
        
    for k in args[2].split():
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

def argmax(x):
    return max(range(len(x)), key=lambda i: x[i])

def viterbi(A, B, Pi, observations):
    # Important lengths
    A_len = len(A)
    O_len = len(observations)
    
    # Initialize lists
    delta =         [[0 for i in range(O_len)] for j in range(A_len)]
    delta_index =   [[0 for i in range(O_len-1)] for j in range(A_len)]

    # Initialize delta for later dynamic programming
    initialization = multiply(Pi[0], [el[observations[0]] for el in B])
    ## Set first column in delta to initialization vector
    for row in range(A_len):
        test = delta[row][0]
        delta[row][0] = initialization[row]

    # Build delta and delta_index through dynamic programming
    for n in range(1, O_len):
        for i in range(A_len):
            # temp = multiply(A[::][i], delta[::][n-1])
            temp = multiply([el[i] for el in A], [el[n-1] for el in delta])
            delta[i][n] = max(temp) * B[i][observations[n]]
            argmax1 = argmax(temp)
            delta_index[i][n-1] = argmax(temp)
    
    # Perform backtracking to find optimal path
    ## Initialize path
    path = [0 for i in range(O_len)]
    path[-1] = argmax([el[i] for el in delta])
    # Perform backtracking
    for n in range(len(observations)-2, -1, -1):
        path[n] = delta_index[path[n+1]][n]

    return path

def main():
    """
    Assert kattis input to variables A, B, Pi and observations
    A is the transiation matrix
    B is the observation matrix
    Pi is the initial probability matrix
    Observations is the list containing previous states
    """
    # args = sys.argv[1:]
    args = []
    args.append(input())
    args.append(input())
    args.append(input())
    args.append(input())
    A, B, Pi = create_matricies(args)
    observations = []
    for i in args[3].split():
        observations.append(int(i))
    
    observations_n = observations[0]
    observations = observations[1:]

    path = viterbi(A, B, Pi, observations)

    print(' '.join(map(str, path)))

if __name__ == "__main__":
    main()