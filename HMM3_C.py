#import sys
import math
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

def new_alpha_pass(A, B, Pi, observations):
    alpha_list = []
    scale_factors = []
    for t in range(len(observations)):
        temp_alpha_list = []
        scale_sum = 0
        for i in range(len(A)):
            if t == 0:
                temp_alpha_list.append(Pi[0][i] * B[i][observations[t]])
                scale_sum += Pi[0][i] * B[i][observations[t]]
            else:
                sum_ = sum([alpha_list[t-1][j] * A[j][i] * B[i][observations[t]] for j in range(len(A))])
                temp_alpha_list.append(sum_)
                scale_sum += sum_
        scale = 1/scale_sum
        scale_factors.append(scale)
        temp_alpha_list = [scale * x for x in temp_alpha_list]
        alpha_list.append(temp_alpha_list)
    return alpha_list, scale_factors

def beta_pass(A, B, Pi, observations, scale_factors):
    beta = [0 for i in range(len(observations))]
    for t in reversed(range(len(observations))): #T
        temp_beta = []
        for i  in range(len(A)): #N
            if t == len(observations) - 1:
                temp_beta.append(scale_factors[t])
            else:
                sum_ = sum([beta[t+1][j] * A[i][j] * B[j][observations[t+1]] for j in range(len(A))])
                temp_beta.append(sum_ * scale_factors[t])
        beta[t] = temp_beta
    return beta

def gamma_digamma(A, B ,Pi, observations, alpha, beta):
    digamma = [0 for t in range(len(observations)-1)]
    gamma = [0 for t in range(len(observations)-1)]
    for t in range(len(observations)-1):
        temp_digamma = [0 for t in range(len(A))]
        temp_gamma = [0 for t in range(len(A))]
        for i in range(len(A)):
            temp2_gamma = [0 for t in range(len(B))]
            for j in range(len(B)):
                temp2_gamma[j] = alpha[t][i] * A[i][j] * B[j][observations[t+1]] * beta[t+1][j]
            temp_gamma[i] = sum(temp2_gamma)
            temp_digamma[i] = temp2_gamma
        digamma[t] = temp_digamma
        gamma[t] = temp_gamma
    return digamma, gamma

def re_estimate(gamma, digamma, A, B, Pi, observations):
    # A
    new_A = []
    for i in range(len(A)):
        temp_new_A = []
        gamma_sum = sum([gamma[t][i] for t in range(len(observations)-1)])
        for j in range(len(A)):
            digamma_sum = 0
            for t in range(len(observations)-1):
                test = digamma[t][i]
                digamma_sum += test[j]
            temp_new_A.append(digamma_sum/gamma_sum)
        new_A.append(temp_new_A)
    
    # B
    new_B = []
    for j in range(len(A)):
        temp_new_B = []
        gamma_sum = sum([gamma[t][j] for t in range(len(observations)-1)])
        for k in range(len(set(observations))):
            digamma_sum = 0
            for t in range(len(observations)-1):
                if k == observations[t]:
                    digamma_sum += gamma[t][j]
            temp_new_B.append(digamma_sum / gamma_sum)
        new_B.append(temp_new_B)

    # Pi
    new_Pi = [[gamma[0][i] for i in range(len(A))]]

    return new_A, new_B, new_Pi

def baum_welch(A, B, Pi, observations):
    oldLogProb = -99999999
    logProb = 0
    maxIterations = 10000
    iterations = 0
    while (iterations < maxIterations and oldLogProb < logProb):
        if iterations != 0:
            oldLogProb = logProb
        alpha, scale_factors = new_alpha_pass(A, B, Pi, observations)
        beta = beta_pass(A, B, Pi, observations, scale_factors)
        digamma, gamma = gamma_digamma(A, B, Pi, observations, alpha, beta)
        A, B, Pi = re_estimate(gamma, digamma, A, B, Pi, observations)
        logProb = 0
        for i in range(len(observations)-1):
            logProb += math.log(scale_factors[i])
        logProb = -logProb
        iterations += 1
    
    logProbGenerating = logProbGen(observations)
    diff = (1/len(observations))*(logProb-logProbGenerating)
    print("Distance between generating and generated: %s" % diff)
    print(iterations)
    print(logProb)
    return A, B, Pi

def logProbGen(observations):
    A = [[0.7,0.05,0.25],[0.1,0.8,0.1],[0.2,0.3,0.5]]
    B = [[0.7,0.2,0.11,0.19],[0.1,0.4,0.3,0.2],[0,0.1,0.2,0.7]]
    Pi = [[1,0,0]]
    alpha, scale_factors = new_alpha_pass(A,B,Pi,observations)
    logProb = 0
    for i in range(len(observations)-1):
        logProb += math.log(scale_factors[i])
    logProb = -logProb
    return logProb



def print_matrix(matrix):
    list_to_print = []
    list_to_print.append(len(matrix))
    list_to_print.append(len(matrix[0]))

    for row in matrix:
        for entry in row:
            list_to_print.append(round(entry, 6))

    for e in list_to_print:
        print(e, end=" ", flush=True)


    

def main():
    """
    Assert kattis input to variables A, B, Pi and observations
    A is the transiation matrix
    B is the observation matrix
    Pi is the initial probability matrix
    Observations is the list containing previous states
    """
    #args = sys.argv[1:]
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
    A, B, Pi = baum_welch(A,B,Pi,observations)
    print_matrix(A)
    print("")
    print_matrix(B)
    print_matrix(Pi)

if __name__ == "__main__":
    main()