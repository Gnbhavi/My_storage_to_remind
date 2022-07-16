import numpy as np
np.random.seed(10)

def sigmoid(x):
    return 1/(1+np.exp(-x))

class neuron:
    def __init__(self, weight, bias):
        self.weight = weight
        self.bias = bias
    
    def feed_forward(self, inputs):
        total =  np.dot(self.weight, inputs) + self.bias
        return sigmoid(total)


class Our_neural_network:
    def __init__(self):
        weight_1 = np.random.random(2)
        bias_1 = np.random.rand(1)
        weight_2 = np.random.random(2)
        bias_2 = np.random.rand(1)
        self.first_layer = neuron(weight_1, bias_1)
        self.hidden_layer = neuron(weight_2, bias_2)
    
    def feed_forward(self, x):
        first_layer_output = self.first_layer.feed_forward(input)
        second_layer_output = self.hidden_layer.feed_forward([first_layer_output] * 
                                        self.weight_2.shape[0])


input = np.array([0, 1])
