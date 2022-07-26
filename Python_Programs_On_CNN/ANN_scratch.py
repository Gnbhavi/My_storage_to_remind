import tensorflow
import numpy as np
import pandas as pd
np.random.seed(10)

def sigmoid(x):
    return 1/(1+np.exp(-x))


def deriv_sigmoid(x):
  # Derivative of sigmoid: f'(x) = f(x) * (1 - f(x))
  fx = sigmoid(x)
  return fx * (1 - fx)


def mse_loss(y_true, y_pred):
  # y_true and y_pred are numpy arrays of the same length.
  return ((y_true - y_pred) ** 2).mean()



class Our_neural_network:
    def __init__(self, first_layer_neuron_count, hidden_layer_neuron_count):
        print(first_layer_neuron_count)
        self.weight_1 = np.random. normal(size = (first_layer_neuron_count, hidden_layer_neuron_count))
        self.bias_1 = np.random.normal(hidden_layer_neuron_count)
        self.weight_2 = np.random.normal(size = (hidden_layer_neuron_count))
        self.bias_2 = np.random.normal()
        # self.first_layer = neuron(weight_1, bias_1)
        # self.hidden_layer = neuron(weight_2, bias_2)
    
    def feed_forward(self, x):
        h = sigmoid(np.dot(x, self.weight_1)+ self.bias_1)
        o = sigmoid(np.dot(x, self.weight_2)+ self.bias_2)
        return o
    #     first_layer_output = self.first_layer.feed_forward(input)
    #     second_layer_output = self.hidden_layer.feed_forward(np.array(first_layer_output))

    #     return second_layer_output
    
    def train(self, data, all_y_trues):
        '''
        - data is a (n x 2) numpy array, n = # of samples in the dataset.
        - all_y_trues is a numpy array with n elements.
        Elements in all_y_trues correspond to those in data.
        '''
        learn_rate = 0.1
        epochs = 1 # number of times to loop through the entire dataset
        print("weight_1", self.weight_1)
        print("bias_1", self.bias_1)

        for epoch in range(epochs):
            for x, y_true in zip(data, all_y_trues):
                sum_hidden_layer = np.dot(x, self.weight_1)+ self.bias_1
                h = sigmoid(sum_hidden_layer)
                sum_output_layer = np.dot(x, self.weight_2)+ self.bias_2
                o = sigmoid(sum_output_layer)
                y_pred = o
                # --- Calculate partial derivatives.
                # --- Naming: d_L_d_w1 represents "partial L / partial w1"
                d_L_d_ypred = -2 * (y_true - y_pred)

                # Neuron Output Layer
                d_ypred_d_w2 = h * deriv_sigmoid(sum_output_layer)
                d_ypred_d_b2 = deriv_sigmoid(sum_output_layer)
                d_ypred_d_h = self.weight_2 * deriv_sigmoid(sum_hidden_layer)
                

                # Neuron Hidden layer
                d_h1_d_w1 = x * deriv_sigmoid(sum_hidden_layer)
                d_h1_d_b1 = deriv_sigmoid(sum_hidden_layer)

                # --- Update weights and biases
                # Neuron hidden layer
                self.weight_1 -= learn_rate * d_L_d_ypred * d_ypred_d_h * d_h1_d_w1
                self.bias_1 -= learn_rate * d_L_d_ypred * d_ypred_d_h * d_h1_d_b1


                # Neuron o1
                self.weight_2 -= learn_rate * d_L_d_ypred * d_ypred_d_w2
                self.bias_2 -= learn_rate * d_L_d_ypred * d_ypred_d_b2

                 # --- Calculate total loss at the end of each epoch
                if epoch % 10 == 0:
                    y_preds = np.apply_along_axis(self.feed_forward, 1, data)
                    loss = mse_loss(all_y_trues, y_preds)
                    print("Epoch %d loss: %.3f" % (epoch, loss))



data = np.array([
  [-2, -1],  # Alice
  [25, 6],   # Bob
  [17, 4],   # Charlie
  [-15, -6], # Diana
])
all_y_trues = np.array([
  1, # Alice
  0, # Bob
  0, # Charlie
  1, # Diana
])

network = Our_neural_network(2, 2)
input = np.array([0, 1])
network.train(data, all_y_trues)

emily = np.array([-7, -3]) # 128 pounds, 63 inches
frank = np.array([20, 2])  # 155 pounds, 68 inches
print("Emily: %.3f" % network.feed_forward(emily)) # 0.951 - F
print("Frank: %.3f" % network.feed_forward(frank)) # 0.039 - M