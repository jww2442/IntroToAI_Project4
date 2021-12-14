from math import exp
from statistics import mean
from random import random

from file_io import general_file_to_inout_lists, file_inout_lists_iris, file_inout_lists_labeled_examples
import data_manipulation


#INITIALIZE init and return network with random weights
def init_neural_net(num_input_nodes, num_hidden_neurons, num_hidden_layers, num_output_nodes):
    layers = []
    
    for i in range(num_hidden_layers):
        hidden_layer = []
        num_neuron_input = 0 
        if(i == 0):
            num_neuron_input = num_input_nodes + 1
        else:
            num_neuron_input = num_hidden_neurons

        for j in range(num_hidden_neurons):
            neuron = {'weights': []}
            for k in range(num_neuron_input):
                neuron.get('weights').append(random())
            hidden_layer.append(neuron)
        layers.append(hidden_layer)

    output_layer = []
    for i in range(num_output_nodes):
        neuron = {'weights': []}
        for j in range(num_hidden_neurons + 1):
            neuron.get('weights').append(random())
        output_layer.append(neuron)

    layers.append(output_layer)

    return layers



#FORWARD PROPOGATION
#return activation of a single neuron given its weights and inputs
def activate_neuron(weights, inputs):
    activation = 0
    for i in range(len(weights) - 1):
        activation += weights[i]*inputs[i]
    activation += weights[len(weights) - 1]

    return activation

#returns value of activation when inputted into the sigmoid function
def sigmoid_transfer_function(activation):
    transfer = 1/(1+exp(-activation))
    return transfer

#forward propogates an input vector into the provided neural net and returns the output vector
def forward_propogate(inputs, neural_net):
    
    new_inputs = inputs
    for layer in neural_net:
        next_inputs = []
        for neuron in layer: 
            activation = activate_neuron(neuron.get('weights'), new_inputs)
            neuron_output = sigmoid_transfer_function(activation)
            neuron.update({'output': neuron_output})
            next_inputs.append(neuron.get('output'))
        new_inputs = next_inputs
    return new_inputs
        
        


#BACKWARD PROPOGATION
#return derivative of sigmoid function given output of neuron
def sigmoid_transfer_derivative(neuron_output):
    derivative = neuron_output * (1.0 - neuron_output)
    return derivative

#calculate error (based on diff from desired output) and backpropogate error in network given an expected output, change the network, return nothing
def backpropogate(neural_network, desired_out):
    
    #determine error of output layer
    output_layer = neural_network[len(neural_network) - 1]
    for neuron_i in range(len(output_layer)):
        neuron = output_layer[neuron_i]

        error = ((desired_out[neuron_i] - neuron.get('output'))*sigmoid_transfer_derivative(neuron.get('output')))

        neuron.update({'error': error})

    #determine error of hidden layers
    for layer_i in reversed(range(len(neural_network))):
        if(layer_i == len(neural_network) - 1):
            continue

        layer = neural_network[layer_i]
        next_layer = neural_network[layer_i + 1]

        for neuron_i in range(len(layer)):
            neuron = layer[neuron_i]

            total_neuron_error = 0
            for next_neuron in next_layer:
                
                total_neuron_error += (next_neuron.get('weights')[neuron_i] * next_neuron.get('error'))
            
            total_neuron_error = total_neuron_error*sigmoid_transfer_derivative(neuron.get('output'))
            
            neuron.update({'error': total_neuron_error})

            

#TRAINING NETWORK
#update weights in given network given some inputs, return nothing
def update_weights(inputs, neural_network, learning_rate):

    new_inputs = inputs
    for layer_i in range(len(neural_network)):
        layer = neural_network[layer_i]
        next_inputs = []

        for neuron_i in range(len(layer)):
            neuron = layer[neuron_i]

            new_weights = []
            for weight_i in range(len(neuron.get('weights')) - 1): #-1 to exclude bias weight
                
                weight = neuron.get('weights')[weight_i]
                new_weight = weight + learning_rate*neuron.get('error')*new_inputs[weight_i]

                new_weights.append(new_weight)
            
            new_bias_weight = neuron.get('weights')[-1] + learning_rate * neuron.get('error')
            new_weights.append(new_bias_weight)

            neuron.update({'weights': new_weights})
            next_inputs.append(neuron.get('output'))

        new_inputs = next_inputs

#trains the network for some number of epochs
#dataset is list of lists, each inner list contains two elements, the inputs in a list and the outputs in a list
def train_neural_network(dataset, learning_rate, num_epochs, neural_network):

    for epoch in range(num_epochs):
        epoch_error = 0
        for in_out_pair in dataset:
            inputs = in_out_pair[0]
            outputs = in_out_pair[1]
            net_output = forward_propogate(inputs, neural_network)

            for i in range(len(net_output)):
                epoch_error += (net_output[i] - outputs[i])**2
            backpropogate(neural_network, outputs)

            update_weights(inputs, neural_network, learning_rate)

        #print('Total error at epoch {}: {}'.format(epoch, epoch_error))
        


#PREDICTION
#returns list with 1 at index indicating predicted class
def predict(neural_net, input):

    prediction = forward_propogate(input, neural_net)
    class_prediction_list = []
    max_val = -1
    max_i = -1
    for i in range(len(prediction)):
        class_prediction_list.append(0)
        if(prediction[i]>max_val):
            max_val = prediction[i]
            max_i = i
    class_prediction_list[max_i] = 1
    return class_prediction_list

def test_predict_accuracy(neural_network, dataset):
    correct_predictions = 0
    predictions = []
    for inout_pair in dataset:
        predicted_class = predict(neural_network, inout_pair[0])
        if(predicted_class == inout_pair[1]):
            correct_predictions += 1
        predictions.append(predicted_class)

    accuracy = correct_predictions/len(dataset)
    return accuracy


def main(path, k_value, num_classes_in_data, num_input_atts, num_hidden_nodes, num_hidden_layers):
        
    if(path == 'iris_data.txt'):
        dataset = file_inout_lists_iris(path)
    elif(path == 'labeled_examples.txt'):
        dataset = file_inout_lists_labeled_examples(path)
    elif(path == 'seeds_dataset.txt'):
        dataset = general_file_to_inout_lists(path, 7, 3)
    else: 
        print('err629')
        exit()

    minimax = data_manipulation.inputs_minimax(dataset)
    data_manipulation.normalize_dataset(dataset, minimax)

    k_groups = data_manipulation.k_folds(dataset, k_value)

    accuracies = []
    #changes the test_group number each iteration
    for test_group_num in range(k_value):
        train_group = data_manipulation.sep_groups(test_group_num, k_groups)
        test_group = k_groups[test_group_num]

        network = init_neural_net(num_input_atts, num_hidden_nodes, num_hidden_layers, num_classes_in_data)

        train_neural_network(train_group, 0.3, 300, network)
        pred = test_predict_accuracy(network, test_group)

        accuracies.append(pred)
        #print('{} percent complete'.format((100//k_value)*(test_group_num+1))) for showing progress

    print('Statistics of NN performance on {} dataset, with {} fold cross validation,\n using {} hidden nodes in each of {} hidden layer(s)\n-------------------------------'.format(path, k_value, num_hidden_nodes, num_hidden_layers))
    print('% Accuracy of each test set in', path, ':', accuracies)
    print('Average % accuracy of test sets in', path, ':', mean(accuracies))    
    print('\n')

