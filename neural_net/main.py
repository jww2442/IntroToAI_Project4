#EXECUTE THIS TO RUN THE NEURAL NETWORK TRAINING AND TEST

import back_prop_learning as bpl

#list of desired parameters and datasets to use with my neural network. 
#each sublist contains the path of the data in index 0, the num_classes at index 1, 
#the num_attributes at index 2, the num_hidden_nodes (for each hidden layer) at index 3, and the num_hidden_layers at index 4

datasets = [['seeds_dataset.txt', 3, 7, 6, 1]]

#UNCOMMENT BELOW TO TEST THE NN ON THE OTHER DATASETS
#datasets.extend([['iris_data.txt', 3, 4, 6, 1], ['labeled_examples.txt', 2, 2, 6, 1]]) 


k_value = 5 #5 fold cross validation
num_runs = 0

print('Test of dataset(s) beginning...')
for dataset in datasets:
    bpl.main(dataset[0], k_value, dataset[1], dataset[2], dataset[3], dataset[4])
    num_runs +=1




'''
#EXAMPLE OF HOW TO USE MAIN() BY ITSELF
path = 'seeds_dataset.txt'
num_classes_in_data = 3 #classes are 1, 2, and 3
num_input_atts = 7
num_hidden_nodes = 2
num_hidden_layers = 2
k_value = 5 #for k folds cross validation

bpl.main(path, k_value, num_classes_in_data, num_input_atts, num_hidden_nodes, num_hidden_layers)'''