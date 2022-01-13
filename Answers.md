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
?

## Q5: How many values are stored in the matrices δ and δi d x respectively?


## Q6: Why we do we need to divide by the sum over the final α values for the di-gamma function?


## Q7: Train an HMM with the same parameter dimensions as above, i.e. A should be a 3 times 3 matrix, etc. Initialize your algorithm with the following matrices:
"args": ["3 3 0.54 0.26 0.20 0.19 0.53 0.28 0.22 0.18 0.6", "3 3 0.5 0.2 0.11 0.19 0.22 0.28 0.23 0.27 0.19 0.21 0.15 0.45", "1 3 0.3 0.2 0.5", "N n1 n2 n3 n4"]
### - Does the algorithm converge? 
### - How many observations do you need for the algorithm to converge? 
### - How can you define convergence?


## Q8. Train an HMM with the same parameter dimensions as above, i.e. A is a 3x3 matrix etc. The initialization is left up to you. 
### - How close do you get to the parameters above, i.e. how close do you get to the generating parameters in Eq. 3.1? 
### - What is the problem when it comes to estimating the distance between these matrices? How can you solve these issues?

## Q9. Train an HMM with different numbers of hidden states. 
### - What happens if you use more or less than 3 hidden states? Why? Are three hidden states and four observations the best choice? If not, why? 
### - How can you determine the optimal setting? How does this depend on the amount of data you have?


## Q10. Initialize your Baum-Welch algorithm with a uniform distribution. How does this affect the learning? 
## - Initialize your Baum-Welch algorithm with a diagonal A matrix and π = [0, 0, 1]. How does this affect the learning? 
## - Initialize your Baum-Welch algorithm with a matrices that are close to the solution. How does this affect the learning?






