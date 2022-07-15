import numpy as np


def binary_list(n):
    return [[int(j) for j in '{:0{}b}'.format(i, n)] for i in range(1, 2**n)]
    # {:b}.format(i) will give the binary form of i
    #  for having n bits in each of the binary numbers we are using {:0{}b}.format(i,n)
    # (i.e), to get 0 as 00000(n=5) we are using.

def cubing_polynomial(beta):
    # Cubing the beta values and returning
    beta_3 = np.polymul(beta, beta)
    beta_3 = np.polymul(beta_3, beta)
    return beta_3

Minimal_polynomial= [1, 0, 0, 1, 0, 1]
# The polynomial to divide is the Minimal polynomial 
Poly_list = binary_list(5)
# Creating all the binary list from 0 to 2**n
beta_3 = [0]*len(Poly_list)
# Intializing beta cube values

for i in range(len(Poly_list)):
    beta_3[i] = cubing_polynomial(Poly_list[i])
    # Finding the cube of Beta
    _, beta_3[i] = np.polydiv(beta_3[i], Minimal_polynomial)
    # Storing the remainder of ith beta in beta cube
    beta_3[i] = np.mod(beta_3[i], 2)
    # Moding it to 2 since we are dealing with bianry
    # If the length of beta is less than 5 we are adding zeros in front
    if len(beta_3[i]) < 5:
        l=[0]*(5 - len(beta_3[i]))
        beta_3[i] = [*l, *beta_3[i]]
        # This is to extract all the values of list and append it together

Poly_list = np.array(Poly_list)
beta_3 = np.array(beta_3)
# Converting those into array so we can use as matrix.
Parity_check_matrix = np.hstack((Poly_list, beta_3))
# Doing a horizontal stacking since we need to stack with the 5 rows
# Parity_check_matrix = Parity_check_matrix[1:]
# # Leaving the zero row.
Parity_check_matrix = np.transpose(Parity_check_matrix)
recived_word = [0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1]
syndrome = np.mod(np.matmul(Parity_check_matrix, recived_word), 2)
print(syndrome)
k1,k2=0,0
Beta_value, Beta_3_value = 0, 0 
for i in range(Parity_check_matrix.shape[1]):
    if np.array_equal(Poly_list[i], syndrome[:5]):
        Beta_value = Poly_list[i]
        k1=i
    if np.array_equal(beta_3[i], syndrome[5:]):
        Beta_3_value = beta_3[i]
        k2 =i
print('S1 is', k1, Beta_value)
print('S3 is', k2, Beta_3_value)
