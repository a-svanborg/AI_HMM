# Answers to questions in HMM lab

## Q1: This problem can be formulated in matrix form. Please specify the initial probability vector π, the transition probability matrix A and the observation probability matrix B.

A:

|             |             |
| ----------- | ----------- |
| 0.5         | 0.5         |
| 0.5         | 0.5         |

B:

|             |             |
| ----------- | ----------- |
| 0.9         | 0.1         |
| 0.5         | 0.5         |

Pi:

|             |             |
| ----------- | ----------- |
| 0.5         | 0.5         |

## Q2: What is the result of this operation?

|             |             |
| ----------- | ----------- |
| 0.5         | 0.5         |

## Q3: What is the result of this operation? 

|             |             |
| ----------- | ----------- |
| 0.7         | 0.3         |

## Q4: Why is it valid to substitute O1:t = o1:t with Ot = ot when we condition on the state Xt =xi?
Because we multiply it with the probability of the hidden state and the previous observation sequence up to t-1:  P(Xt =xi,O1:t−1)
Markov property. Only dependent on previous time step.

## Q5: How many values are stored in the matrices δ and δ_idx respectively?
t*i for delta
(t-1)*i for delta_idx since it is not computed for t=1

## Q6: Why we do we need to divide by the sum over the final α values for the di-gamma function?
Normalize. Make sure it is a probability

## Q7: Train an HMM with the same parameter dimensions as above, i.e. A should be a 3 times 3 matrix, etc. Initialize your algorithm with the following matrices:
"args": ["3 3 0.54 0.26 0.20 0.19 0.53 0.28 0.22 0.18 0.6", "3 3 0.5 0.2 0.11 0.19 0.22 0.28 0.23 0.27 0.19 0.21 0.15 0.45", "1 3 0.3 0.2 0.5", "N n1 n2 n3 n4"]
### - Does the algorithm converge? 
1000 observations: Converged after 877 iterations with a difference of -0.0508
3 3 0.687416 0.010919 0.301666 0.097843 0.806907 0.09525 0.200378 0.294055 0.505566
3 4 0.696568 0.231415 0.071274 0.000743 0.068017 0.417218 0.280998 0.233767 0.0 9.3e-05 0.354832 0.645076

10000 observations: Converged after 8947 iterations with a difference of -0.055
3 3 0.694155 0.038791 0.267054 0.117449 0.738351 0.1442 0.153212 0.248767 0.598021
3 4 0.709688 0.186623 0.103688 0.0 0.099083 0.42583 0.314626 0.16046 0.034633 0.176861 0.189405 0.599101

### - How many observations do you need for the algorithm to converge? 
Depends on how we define the convergence. If we would compute the distance from the correct matrix it would be easy to test with a defined threshhold. But with our convergence test it will converge (probability not growing) earlier if we have less observations but with a greater difference.

### - How can you define convergence?
log[P(O | λ)] = −sum(log(c))   where c is the scaling factor.
A distance measure is then: 1/T * (log[P(O | λ_1)] - log[P(O | λ_2)])
Thus, we can define convergence as the difference/distance from the true matrix. Or we define it as when the old (previous iteration in baum-welch) log-probability becomes greater than the new.
i.e. we make sure the probability of the observation sequence keeps getting better.

## Q8. Train an HMM with the same parameter dimensions as above, i.e. A is a 3x3 matrix etc. The initialization is left up to you. 
A reasonable init is to have around uniform but not uniform. Middle gives higher chance of finding global maximum.
3 3 0.3 0.4 0.3 0.3 0.4 0.3 0.3 0.4 0.3
3 4 0.2 0.2 0.3 0.3 0.2 0.2 0.3 0.3 0.2 0.3 0.2 0.3
1 3 0.3 0.3 0.4
### - How close do you get to the parameters above, i.e. how close do you get to the generating parameters in Eq. 3.1? 
10000 observations: Converged after 9103 iterations with a difference of -0.055. (same as Q7)
3 3 0.738351 0.1442 0.117449 0.248767 0.598021 0.153212 0.038791 0.267054 0.694155
3 4 0.099083 0.42583 0.314626 0.16046 0.034633 0.176861 0.189405 0.599101 0.709688 0.186623 0.103688 0.0 1 3 1.0 0.0 0.0
### - What is the problem when it comes to estimating the distance between these matrices? How can you solve these issues?
Columns could be switched. We can solve this issue by calculating the convergence as we do. (Q7)

## Q9. Train an HMM with different numbers of hidden states. 
### - What happens if you use more or less than 3 hidden states? Why? Are three hidden states and four observations the best choice? If not, why? 
### - How can you determine the optimal setting? How does this depend on the amount of data you have?

| T             |  N        | Diff          |
| -----------   | --------- | ------------- | 
| 10000         | 5         | -0.05414      |
| 10000         | 4         | -0.05536      |
| 10000         | 3         | -0.05536      |
| 10000         | 2         | -0.09563      |
| 10000         | 1         | -0.09563      |
| 1000          | 5         | -0.04186      |
| 1000          | 4         | -0.05086      |
| 1000          | 3         | -0.05086      |
| 1000          | 2         | -0.09885      |
| 1000          | 1         | -0.09885      |
| 10            | 5         | 0.628745      |
| 10            | 4         | 0.471770      |
| 10            | 3         | 0.471770      |
| 10            | 2         | -0.05397      |
| 10            | 1         | -0.05397      |

When we have a lot of observations, the correct number of states is very close to the lowest diff which 5 states took. 1 and 2 states gave much worse results. 
We thought we would get better results for N=3 with 10000 observations. Could eb something wrong in the distance calculations.
For 1000 we have similar results.
For 10 observations we see that 1 and 2 hidden states gives the lowest diff.
This tells us that more states require more data. In line with baum welch beeing a model based on statistics.

## Q10. 
### - Initialize your Baum-Welch algorithm with a uniform distribution. How does this affect the learning? 
We get stuck in local maximum. Since B is uniform it does not tell us anything about the outcomes.

### - Initialize your Baum-Welch algorithm with a diagonal A matrix and π = [0, 0, 1]. How does this affect the learning? 
Results in computational error since we get division by 0 error. Happens in the reestimation when we divide digamma with gamma
### - Initialize your Baum-Welch algorithm with a matrices that are close to the solution. How does this affect the learning?
We should reach a global maximum which Q7 proved.





