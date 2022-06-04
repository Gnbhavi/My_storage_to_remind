import numpy as np

# Initialising the inputs and outputs of the ANN model
inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
expected_output = np.array([[0], [1], [1], [0]])
lr = 0.1  # learning rate of the model
j = 0


def relu(x):  # defining the sigmoid function for future use.
    return 1 if x > 0 else 0


def relu_derivative(x):  # The speciality of the sigmoid function is the calculation of the derivative its easy
    return 1 if x > 0 else 0


inputLayerNeurons, hiddenLayerNeurons, outputLayerNeurons = 2, 2, 1
# Initializing number od input hidden and output layers.
hidden_weights = np.random.uniform(size=(inputLayerNeurons, hiddenLayerNeurons))
# For starting we are giving random numbers to all the weights. Here hidden_weights implies the weight matrix from
# input to hidden layers each column is represented for the input of one neuron.
hidden_bias = np.random.uniform(size=(1, hiddenLayerNeurons))
# Same thing is for bias.
output_weights = np.random.uniform(size=(hiddenLayerNeurons, outputLayerNeurons))
# For starting we are giving random numbers to all the weights. Here hidden_weights implies the weight matrix from
# hidden to output layers each column is represented for the input of one neuron.
output_bias = np.random.uniform(size=(1, outputLayerNeurons))
predicted_output = 0
comparison_value = False
# Running until the program gives the correct values
while not comparison_value:
    hidden_layer_activation = np.dot(inputs, hidden_weights)
    # Now it will be converted into a vector to be fed as an inout to the hidden layer neurons.
    hidden_layer_activation += hidden_bias
    # Bias is also a vector here.
    hidden_layer_output = relu(hidden_layer_activation)
    # Here for all three sigmoid function will be used.

    output_layer_activation = np.dot(hidden_layer_output, output_weights)
    # The above process is done for the weights from hidden layer to output layer.
    output_layer_activation += output_bias
    predicted_output = relu(output_layer_activation)

    # Backpropagation
    error = expected_output - predicted_output
    d_predicted_output = error * relu_derivative(predicted_output)
    # Backpropagation of hidden layers.
    error_hidden_layer = d_predicted_output.dot(output_weights.T)
    d_hidden_layer = error_hidden_layer * relu_derivative(hidden_layer_output)

    # Updating Weights and Biases for both hidden and output layer
    # .t function gives the transpose of the matrix in the np array.
    output_weights += hidden_layer_output.T.dot(d_predicted_output) * lr
    output_bias += np.sum(d_predicted_output, axis=0, keepdims=True) * lr
    hidden_weights += inputs.T.dot(d_hidden_layer) * lr
    hidden_bias += np.sum(d_hidden_layer, axis=0, keepdims=True) * lr
    # checking whether both the arrays are same in all position
    comparing = predicted_output == expected_output
    # even one wrong it will give false
    comparison_value = comparing.all()
    j += 1

print('predicted_output', predicted_output)
print("hidden_weights", hidden_weights)
print('hidden_bias', hidden_bias)
print('output_weights', output_weights)
print('output_bias', output_bias)
print(j)
