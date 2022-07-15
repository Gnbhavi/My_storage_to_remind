# In this program We are going to say how convolution filter 
# multiplication is done by using the help of matrix


import numpy as np


# input_matrix = np.zeros((7,7,3))
input_matrix_0 = np.array([[2,1,0,1,0], [0,0,0,2,2],[2,1,1,1,0], [1,0,0,1,2],
						   [2,1,1,1,0]])
input_matrix_1 = np.array([[1,2,1,1,2], [2,0,0,2,1], [2,0,1,1,2], [0,1,2,1,0],
						   [2,2,1,1,1]])
input_matrix_2 = np.array([[2,1,0,2,1], [1,2,2,2,2], [0,2,2,1,0], [2,1,2,2,1],
						   [0,1,0,2,1]])

# We are creating a matrices which will be given as inputs.
input_matrix = np.stack([input_matrix_0, input_matrix_1, input_matrix_2], axis=0)
# To create a 3D matrix we are using the first layer to stack as we had used other two like (Z,X,Y)
P = 1
# We are going to do the padding now. Here the padding is 1, but we will do later for the coding
#################################################################################################
# We are trying to do padding now#
N = input_matrix.shape[1]
# A =  np.zeros(N+2)  this is for adding a zero row
#Padding is done for how many rounds it needs
for the in range(P):
	A = np.zeros(input_matrix.shape[1]+2)
	input_matrix =np.array([np.vstack((A, np.array([np.hstack(([0],input_matrix[hell,val,:],[0]))
								for val in range(N)]), A)) for hell in range(input_matrix.shape[0])])
# vstack is to add a row to the numpy directly if it has a correct dimension with the others
# hstack is to add a column to the numpy directly if it has a correct dimension with the others
# we are using 0 and adding the padding to the input_matrix itself
##################################################################################################	
first_filter_0 = [[0,0,1], [-1,0,1], [1,0,0]]
first_filter_1 = [[1,1,-1], [1,0,0], [1,-1,-1]]
first_filter_2 = [[0,0,-1], [0,0,0], [1,-1,-1]] 
second_filter_0 = [[1,1,-1], [0,0,-1], [-1,0,-1]]
second_filter_1 = [[1,-1,-1], [-1,0,-1], [1,0,-1]]
second_filter_2 = [[0,1,0], [-1,1,1], [1,0,0]]
# We are going to use this our filter for the first layer
filters = np.array([np.stack([first_filter_0, first_filter_1, first_filter_2], axis=0),
		   np.stack([second_filter_0, second_filter_1, second_filter_2], axis=0)])
F = filters.shape[1]  #because the first axis is the RGB layers
S, K = 2, filters.shape[0] # Stride size, K is the number of filters
bias = [1, 0] #bias for the two layers
output_layer_1_size = int(((N-F+2*P)/S)+1)
# output_layer_1_size is the size of the matrix 
# after the first filter.
s = (K,output_layer_1_size, output_layer_1_size)
output_filtered_matrix = np.zeros(s)
for val in range(K):
	output_filtered_matrix[val] =np.array([[np.sum(input_matrix[:, i*S:i*S+F, j*S:j*S+F]*filters[val])
				 + bias[val]for j in range(output_layer_1_size)]for i in range(output_layer_1_size)])
# Converting the for loop to a single line
	# for i in range(output_layer_1_size):
	# 	for j in range(output_layer_1_size):
	# 		output_filtered_matrix[val, i, j] = np.sum(input_matrix[:, i*S:i*S+F, j*S:j*S+F]*filters[val]) + bias[val]
		
print(output_filtered_matrix.astype(int))
