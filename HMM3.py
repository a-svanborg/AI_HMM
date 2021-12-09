import sys
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

def new_alpha_pass(A, B, Pi, observations):
    alpha_list = []
    for t in range(len(observations)):
        temp_alpha_list = []
        for i in range(len(A)):
            if t == 0:
                temp_alpha_list.append(Pi[0][i] * B[i][observations[t]])
            else:
                sum_ = 0
                for j in range(len(A)):
                    sum_ += alpha_list[t-1][j] * A[j][i]
                temp_alpha_list.append(sum_ * B[i][observations[t]])
        alpha_list.append(temp_alpha_list)
    return alpha_list

def beta_pass(A, B, Pi, observations):
    beta = []
    for i in range(len(observations)):
        beta.append("")
    for t in reversed(range(len(observations))): #T
        temp_beta = []
        for i  in range(len(A)): #N
            if t == len(observations) - 1:
                temp_beta.append(1)
            else:
                sum_ = 0
                for j in range(len(A)):
                    sum_ += beta[t+1][j] * B[j][observations[t+1]] * A[i][j] #* observations[t]
                temp_beta.append(sum_)
        beta[t] = temp_beta
    return beta

def gamma_digamma(A, B ,Pi, observations, alpha, beta):
    digamma = []
    gamma = []
    for t in range(len(observations)-1):
        temp_digamma = []
        temp_gamma = []
        for i in range(len(A)):
            temp2_gamma = []
            gamma_i = 0
            for j in range(len(B)):
                gamma_ij = alpha[t][i] * A[i][j] * B[j][observations[t+1]] * beta[t+1][j]
                temp2_gamma.append(gamma_ij)
                gamma_i += gamma_ij
            temp_gamma.append(gamma_i)
            temp_digamma.append(temp2_gamma)
        digamma.append(temp_digamma)
        gamma.append(temp_gamma)
    return digamma, gamma

def get_column(mat, column_index):
    values = [row[column_index] for row in mat]
    return values

def re_estimate(gamma, digamma, A, B, Pi, observations):
    # A
    new_A = []
    for i in range(len(A)):
        gamma_sum = 0
        temp_new_A = []
        for t in range(len(observations)-1):
            gamma_sum += gamma[t][i]
        for j in range(len(A)):
            digamma_sum = 0
            for t in range(len(observations)-1):
                digamma_sum += digamma[t][i][j]
            temp_new_A.append(digamma_sum/gamma_sum)
        new_A.append(temp_new_A)
    
    # B
    new_B = []
    for j in range(len(A)):
        gamma_sum = 0
        temp_new_B = []
        for t in range(len(observations)-1):
            gamma_sum += gamma[t][j]
        for k in range(len(set(observations))):
            digamma_sum = 0
            for t in range(len(observations)-1):
                if k == observations[t]:
                    digamma_sum += gamma[t][j]
            temp_new_B.append(digamma_sum / gamma_sum)
        new_B.append(temp_new_B)

    # Pi
    new_Pi = []
    for i in range(len(A)):
        new_Pi.append(gamma[0][i])
    new_Pi = [new_Pi]

    return new_A, new_B, new_Pi

def baum_welch(A, B, Pi, observations):
    for t in range(20):
        alpha = new_alpha_pass(A, B, Pi, observations)
        beta = beta_pass(A, B, Pi, observations)
        digamma, gamma = gamma_digamma(A, B, Pi, observations, alpha, beta)
        A, B, Pi = re_estimate(gamma, digamma, A, B, Pi, observations)
    

def main():
    """
    Assert kattis input to variables A, B, Pi and observations
    A is the transiation matrix
    B is the observation matrix
    Pi is the initial probability matrix
    Observations is the list containing previous states
    """
    args = sys.argv[1:]
    A, B, Pi = create_matricies(args)
    observations = []
    for i in args[3].split():
        observations.append(int(i))
    
    observations_n = observations[0]
    observations = observations[1:]
    baum_welch(A,B,Pi,observations)

if __name__ == "__main__":
    main()