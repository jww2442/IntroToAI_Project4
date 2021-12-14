#THIS IS THE MAIN PROGRAM. EXECUTE THIS TO BUILD A DECISION TREE AND TEST ITS ACCURACY USING THE CAR.TXT DATASET

import math
from statistics import mean
from random import shuffle

import anytree

import file_io

def learn_tree(examples, attributes, parent_exs, formula_entropy = True):

    if(len(examples[0]) == 0 and len(examples[1]) == 0):
        return anytree.Node(_plurality_val(parent_exs))
    elif(len(examples[1]) == 0):
        return anytree.Node('unacc')
    elif(len(examples[0]) == 0):
        return anytree.Node('acc_better')
        
    if(len(attributes) == 0):
        return anytree.Node(_plurality_val(examples))

    att = _most_important_att(attributes, examples, formula_entropy)
    tree = anytree.Node(att)
    poss_att_vals = attributes.pop(att)

    for val in poss_att_vals:

        matched_exs = _matching_exs(examples, att, val)
        subtree = learn_tree(matched_exs, attributes, examples, formula_entropy)
        subtree.attval = subtree.name
        subtree.name = '(' + att + '=' + val + ')' + subtree.name

        subtree.edge_val = val

        helper_children = list(tree.children)
        helper_children.append(subtree)
        tree.children = tuple(helper_children)
        #tree.add_branch(val, subtree) #! this needs val or att?

    #needed?
    #attributes.update({att: poss_att_vals})

    return tree

def _matching_exs(examples, att, val):
    matching_exs = [[], []]
    for ex in examples[0]:
        if(ex.get(att) == val):
            matching_exs[0].append(ex)
    for ex in examples[1]:
        if(ex.get(att) == val):
            matching_exs[1].append(ex)

    return matching_exs

def sort_examples_by_class(examples):
    unacc_exs = []
    acc_ex = []
    for ex in examples:
        if(ex.get('class') == 'unacc'):
            unacc_exs.append(ex)
        elif(ex.get('class') == 'acc_better'):
            acc_ex.append(ex)
        else: 
            print(ex.get('class'))
            print('error029')
            exit()
    return [unacc_exs, acc_ex]

def _plurality_val(examples):

    if(len(examples[0])>len(examples[1])):
        return 'unacc'
    elif(len(examples[0])<len(examples[1])):
        return 'acc_better'
    else: #may need to use random?
        return 'acc_better'

#calc boolean entropy
def boolean_entropy(fract):
    if(fract == 0 or fract == 1):
        return 0
    return -(fract*math.log(fract, 2) + (1-fract)*math.log(1-fract, 2))

#calc remainder of an att
#uses entropy or gini index depending on parameter
def __remainder_of_att(att, attributes, examples, formula_is_entropy):
    att_vals = attributes.get(att)
    r_val = 0
    if(len(examples[0])+len(examples[1])==0):
        print('len examples == 0 err952')
        exit()
    for val in att_vals:
        num_pos_at_val = 0
        num_neg_at_val = 0
        for ex in examples[0]: 
            if(ex.get(att) == val):
                num_neg_at_val += 1
        for ex in examples[1]:
            if(ex.get(att) == val):
                num_pos_at_val += 1

        coeff = (num_neg_at_val + num_pos_at_val)/len(examples)
        if(not(num_pos_at_val == 0)):
            if(formula_is_entropy):
                r_val += coeff*boolean_entropy(num_pos_at_val/(num_pos_at_val+num_neg_at_val))
            else: 
                p = num_pos_at_val/(num_pos_at_val + num_neg_at_val)
                r_val -= p*(1-p)

    return r_val

#determine which att has the smallest remainder (largest gain) for the given example set
def _most_important_att(attributes, examples, formula_entropy):
    if(len(attributes) == 0):
        print('err321')
        exit()
    min_rem_att = None
    min_rem_val = 10000
    for att in attributes: 
        rem = __remainder_of_att(att, attributes, examples, formula_entropy)
        if(rem < min_rem_val):
            min_rem_val = rem
            min_rem_att = att
    if(min_rem_att==None):
        print('none error 821')
        exit()
    return min_rem_att


#testgroup is unsorted by class
def classify(testgroup, tree):

    num_correct = 0
    tree.attval = tree.name
    for example in testgroup:
        curr_node = tree
        class_found = False
        while(not class_found):
            att = curr_node.attval

            if(len(curr_node.children) > 0):
                attval = example.get(att)
                for child in curr_node.children:
                    if(child.edge_val == attval):
                        curr_node = child
                        break
            else: 
                class_found = True

        if(att == example.get('class')):
            num_correct += 1

    return num_correct/len(testgroup)
               

#prints classification accuracy
def cross_validation(attributes, folded_dataset, presorted_data, kval):

    stats = []
    groupsize = len(presorted_data) // kval

    for i in range(kval):

        testgroup = presorted_data[i*groupsize:(i+1)*groupsize]
        train_data = []

        for j in range(len(folded_dataset)):
            if(j == i):
                continue
            train_data.extend(folded_dataset[j])

        tree = learn_tree(train_data, attributes, [])
        print(anytree.RenderTree(tree).by_attr())

        stat = classify(testgroup, tree)
        stats.append(stat)

    return stats



attributes = {
    'buying': ['vhigh', 'high', 'med', 'low'],
    'maint': ['vhigh', 'high', 'med', 'low'],
    'doors': ['2', '3', '4', '5more'],
    'persons': ['2', '4', 'more'],
    'lug_boot': ['small', 'med', 'big'], 
    'safety': ['low', 'med', 'high']
}


kval = 5
testgroupnum = 0

#EDIT BELOW TO USE THE ENTROPY/GINI INDEX SPLITTING FUNCTION
use_entropy_instead_of_gini_index = True

#loads dataset
five_groups = file_io.init_groups(1725, kval, 'C:\\Users\\white\\Documents\\spring2021\\artificial-intelligence\\p4\\supervised_learner\\car.txt')
#creates dataset
examps = file_io.storeAll(five_groups, kval)
statistics = []





shuffle(examps)
#sorts dataset by class
examples = sort_examples_by_class(examps)
#splits dataset into 5 class sorted datasets
#folded_dataset = data_manipu.k_fold_creation(examples, kval)
trainset = [[],[]]
testsize = len(examps)//kval
trainset[0] = examples[0][testsize:]
trainset[1] = examples[1][testsize:]

testgroup = examps[0:testsize]

print('Tree: \n-------------------------')
tree = learn_tree(trainset, attributes, [], use_entropy_instead_of_gini_index)
print(anytree.RenderTree(tree).by_attr())

stats = classify(testgroup, tree)


print('\n% Accuracy of decision tree on 5 instances of car.txt: ',stats, '\n')
if(use_entropy_instead_of_gini_index):
    print('The entropy measure splitting function was used')
else:
    print('The Gini index splitting function was used')