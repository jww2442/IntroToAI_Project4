from random import shuffle

#SHUFFLE AND SEPARATE DATA INTO K FOLDS
#input data, return randomized k folds
def k_folds(dataset, k_value):
    shuffle(dataset)

    set_size = len(dataset) // k_value
    k_groups = []

    for k in range(k_value):
        group = dataset[k*set_size: (k+1)*set_size]
        k_groups.append(group)

    return k_groups

#input k_groups, separate into train and test groups
def sep_groups(test_group_num, k_groups):

    train_group = []

    for i in range(len(k_groups)):
        if(i == test_group_num):
            continue
        else:
            train_group.extend(k_groups[i])

    return train_group





#NORMALIZATION
#find min and max of inputs 
def inputs_minimax(dataset):
    input = []
    for data in dataset:
        input.append(data[0])
    minmax_inputs = []
    for col in zip(*input):
        minmax_inputs.append([min(col), max(col)])
    return minmax_inputs

def normalize_dataset(dataset, minimax):
    for inout_pair in dataset: 
        for input_i in range(len(inout_pair[0])):

            inout_pair[0][input_i] = (inout_pair[0][input_i] - minimax[input_i][0])/(minimax[input_i][1]-minimax[input_i][0])


