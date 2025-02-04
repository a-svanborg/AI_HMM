import math
import sys

def f_create_matrix(p_matrix_item):
    #l_matrix_list   = list(p_matrix_item.split())
    l_matrix_elem   = list(map(float, p_matrix_item[2:]))
    l_rows          = int(p_matrix_item[0])
    l_cols          = int(p_matrix_item[1])
    l_matrix        = []
    for i_row in range(l_rows):
        t_row_list = []
        for i_col in range(l_cols):
            if l_matrix_elem[i_col] not in l_matrix:
                t_row_list.append(l_matrix_elem[l_cols * i_row + i_col])
        l_matrix.append(t_row_list)
    return l_matrix


def f_alpha_pass(p_trans_matrix_A, p_obs_matrix_B, p_init_prob_pi, p_obs_seq, p_N, p_T):
    l_alpha_list = []
    l_c = []
    for t in range(p_T):
        t_c = 0
        t_alpha_list = []
        t_pi = p_init_prob_pi[0]
        for i in range(p_N):
            if t == 0:
                t_alpha = t_pi[i] * p_obs_matrix_B[i][p_obs_seq[t]]
                t_c += t_alpha
                t_alpha_list.append(t_alpha)
            else:
                t_alpha = 0
                for j in range(p_N):
                    t_alpha += l_alpha_list[t - 1][j] * p_trans_matrix_A[j][i] * p_obs_matrix_B[i][p_obs_seq[t]]
                t_c += t_alpha
                t_alpha_list.append(t_alpha)
        # c_t_r is the reciprocal of t_c (c at time t)
        c_t_r = 1 / t_c
        for m in range(p_N):
            t_alpha_list[m] = c_t_r * t_alpha_list[m]
        l_c.append(c_t_r)
        l_alpha_list.append(t_alpha_list)

    return l_alpha_list, l_c


def f_beta_pass(a, b, p, seq, c, N, T):
    beta_list = []
    pi_temp = p[0]
    for t in range(T):
        beta_temp_list = []
        for i in range(N):     # to state
            if t == 0:
                beta = c[t]
                beta_temp_list.append(beta)
            else:
                sum_term = 0
                for j in range(N):     # from state
                    sum_term += beta_list[t-1][j] * a[i][j] * b[j][seq[t-1]]
                beta_temp_list.append(sum_term)
        if t > 0:
            for m in range(N):
                beta_temp_list[m] = c[t] * beta_temp_list[m]
        beta_list.append(beta_temp_list)

    return beta_list
    
    
def f_comp_gamma(a, b, seq, alpha_list, beta_list, N, T):
    gama_list = []
    gama_ij_list = []
    for t in range(T-1):
        gama_temp_list = []
        gama_ij_temp_list = []
        for i in range(N):
            gama_val_temp = []
            gama = 0
            for j in range(N):
                gama_ij = alpha_list[t][i] * a[i][j] * b[j][seq[t+1]] * beta_list[t + 1][j]
                gama += gama_ij
                gama_val_temp.append(gama_ij)
            gama_temp_list.append(gama)
            gama_ij_temp_list.append(gama_val_temp)
        gama_list.append(gama_temp_list)
        gama_ij_list.append(gama_ij_temp_list)
    gama_temp_list = []
    alpha_temp_list = alpha_list[t+1]
    for k in range(N):
        gama_temp_list.append(alpha_temp_list[k])
    gama_list.append(gama_temp_list)
    return gama_list, gama_ij_list


def f_re_estimate(gama_list, gama_ij_list, seq, M, N, T):
    # Re-estimate value of pi
    pi_temp_list = []
    for i in range(N):
        pi_temp_list.append(gama_list[0][i])

    # Re-estimating transition matrix A
    trans_mat_new = []
    for i in range(N):
        denom = 0
        trans_mat_temp_list = []
        for t in range(T-1):
            denom += gama_list[t][i]
        for j in range(N):
            numer = 0
            for t in range(T-1):
                gama_temp_i = gama_ij_list[t][i]
                numer += gama_temp_i[j]
            trans_mat_temp_list.append(numer/denom)
        trans_mat_new.append(trans_mat_temp_list)

    # Re-estimating transition matrix B
    obs_mat_new = []
    for i in range(N):
        denom = 0
        obs_mat_temp_list = []
        for t in range(T):
            denom += gama_list[t][i]
        for j in range(M):
            numer = 0
            for t in range(T):
                if seq[t] == j:
                    numer += gama_list[t][i]
            obs_mat_temp_list.append(numer / denom)
        obs_mat_new.append(obs_mat_temp_list)

    return [pi_temp_list], trans_mat_new, obs_mat_new


def f_prob_log(c, T):
    logprob = 0
    for i in range(T):
        logprob -= math.log(c[i])
    return logprob

def main():
    #l_input_file    = open("hmm4_01.in")
    #l_matrices_list = l_input_file.read().splitlines()
    args = sys.argv[1:]
    a = [float(x) for x in args[0].split()]
    b = [float(x) for x in args[1].split()]
    pi = [float(x) for x in args[2].split()]
    e = [int(x) for x in args[3].split()]

    l_trans_matrix_A    = f_create_matrix(a)
    l_obs_matrix_B      = f_create_matrix(b)
    l_init_prob_pi      = f_create_matrix(pi)
    l_obs_seq   = e[1:]

    # We are flipping the observation sequence because the Beta pass
    # operations are the same as the alpha pass operations
    # The output of Beta pass needs to be flipped so that the index will
    # correspond to the right time stamp
    
    l_M = len(set(l_obs_seq))           # Count of unique elements in obs seq 
    l_N = len(l_trans_matrix_A)
    l_T = len(l_obs_seq)

    l_iter_cnt      = 0
    l_max_iters     = 50
    l_old_log_prob  = float("-inf")
    l_log_prob      = 1

    while l_iter_cnt < l_max_iters and l_log_prob > l_old_log_prob:
        l_iter_cnt += 1
        #print("Iteration count : ", str(l_iter_cnt))
        if l_iter_cnt != 1:
            l_old_log_prob = l_log_prob
            
        l_alpha_vals, l_c_val = f_alpha_pass(l_trans_matrix_A, l_obs_matrix_B, l_init_prob_pi, l_obs_seq, l_N, l_T)
        
        l_c_beta    = l_c_val[::-1]
        l_seq_beta  = l_obs_seq[::-1]
        l_beta_flip = f_beta_pass(l_trans_matrix_A, l_obs_matrix_B, l_init_prob_pi, l_seq_beta, l_c_beta, l_N, l_T)
        l_beta_vals = l_beta_flip[::-1]

        l_gamma_list, l_gamma_ij_list = f_comp_gamma(l_trans_matrix_A, l_obs_matrix_B, l_obs_seq, l_alpha_vals, l_beta_vals, l_N, l_T)

        l_init_prob_pi, l_trans_matrix_A, l_obs_matrix_B = f_re_estimate(l_gamma_list, l_gamma_ij_list, l_obs_seq, l_M, l_N, l_T)

        l_log_prob = f_prob_log(l_c_val, l_T) 

    for i in range(len(l_trans_matrix_A)):
        l_trans_matrix_A[i] = [round(num, 6) for num in l_trans_matrix_A[i]]
    #print("a_n: "  + str(l_trans_matrix_A))

    A = [item for sublist in l_trans_matrix_A for item in sublist]
    t_str_A = ' '.join([str(l_elem) for l_elem in A])
    print(l_N, l_N, t_str_A)
    
    for i in range(len(l_obs_matrix_B)):
        l_obs_matrix_B[i] = [round(num, 6) for num in l_obs_matrix_B[i]]
    #print("b_n: "  + str(l_obs_matrix_B))

    B = [item for sublist in l_obs_matrix_B for item in sublist]
    t_str_B = ' '.join([str(l_elem) for l_elem in B])
    print(l_N, l_M, t_str_B)

if __name__ == "__main__":
    main()