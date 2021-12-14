from os import write
import random



'''inputs num of lines/items in text file (fileSize), num of partitions for those items (N), and the num of the group that is to be tested (testGroup)'''
'''outputs a list containing item objects'''
def init_groups(fileSize, N, path='C:\\Users\\white\\Documents\\spring2021\\artificial-intelligence\\p4\\supervised_learner\\car.txt'):
    with open(path) as f:
        file = f.read().splitlines(True)

    random.shuffle(file)
    
    groupSize = fileSize//N
    nGroups = []
    for i in range(N):
        nGroups.append(file[groupSize*i : groupSize*(i+1)])
        #this is = to [file[0:200], file[200:400], file[400:600], file[600:800], file[800:1000]]

    return nGroups


'''inputs all 5 groups (list of lists), the loc of the test group (int), and the number of total groups (int). 
outputs all 4 example groups combined in a list of Item objects. '''
def storeAll(nGroups, N):

    #combines all example groups together
    exampleGroups = []
    for i in range(N):
        # if(i==testGroupNum):
        #     continue
        exampleGroups.extend(nGroups[i])

    #creates new list of item objects to replace example groups
    exampleItems = []
    for ex in exampleGroups:
        example = _make_example(ex)
        if(len(example)>1):
            exampleItems.append(example)
        
    return exampleItems

def _make_example(lineText):
    
    example = {}

    forward = 0
    back = 0
    num = 0
    if(not len(lineText) <= 1):
        for char in lineText: 

            if(char == ','):
                if(num==0):
                    example.update({'buying': lineText[back:forward]})
                if(num==1):
                    example.update({'maint': lineText[back:forward]})
                if(num==2):
                    example.update({'doors': lineText[back:forward]})
                if(num==3):
                    example.update({'persons': lineText[back:forward]})
                if(num==4):
                    example.update({'lug_boot': lineText[back:forward]})
                if(num==5):
                    example.update({'safety': lineText[back:forward]})
                if(num==6):
                    print('err821')

                back = forward + 1
                num+=1

            if(char == '\n'):
                val = lineText[back:forward]
                if(val == 'unacc'):
                    example.update({'class': val})
                elif(val == 'acc' or val == 'good' or val == 'vgood'):
                    example.update({'class': 'acc_better'})#!I made this value
                else: 
                    print('err682')
                    print(val)
                    print(lineText)
            
            forward+=1 
    
    return example


def write_examples(path, file_size, num_examples_desired, shuffle):
    exs = init_groups(file_size, 5, path)
    combined_exs = []
    for i in exs:
        combined_exs.extend(i)
    if(shuffle):
        random.shuffle(combined_exs) 
    examples = combined_exs[0:num_examples_desired]

    with open('your_file', 'w') as file_handler:
        for item in examples:
            file_handler.write(item)



balance_atts = {
    'class': ['L', 'R'],
    'left-weight': [1, 2, 3, 4, 5], 
    'left-distance': [1, 2, 3, 4, 5], 
    'right-weight': [1, 2, 3, 4, 5], 
    'right-distance': [1, 2, 3, 4, 5]
}

def store_balance_scale(path = 'balance_scaledata.txt'):

    
    file = open(path, 'r')
    lines = file.readlines()

    dataset = [[], []]                        

    for lineText in lines:

        example = {}

        forward = 0
        back = 0
        num = 0

        for char in lineText: 

            if(char == ',' or char.isspace()):

                if(num==0):
                    example.update({'class': lineText[back:forward]})
                if(num==1):
                    example.update({'left-weight': lineText[back:forward]})
                if(num==2):
                    example.update({'left-distance': lineText[back:forward]})
                if(num==3):
                    example.update({'right-weight': lineText[back:forward]})
                if(num==4):
                    example.update({'right-distance': lineText[back:forward]})
                if(num==5):
                    print('err821')

                back = forward + 1
                num+=1
            
            forward+=1 
        
        if(example.get('class') == 'L'):
            dataset[0].append(example)
        elif(example.get('class') == 'R'):
            dataset[1].append(example)
        elif(example.get('class') == 'B'):
            pass
        else:
            print(example)
            print('err716')
            exit()
    random.shuffle(dataset[0])
    random.shuffle(dataset[1])
    
    return dataset


#write_examples('C:\\Users\\white\\Documents\\spring2021\\artificial-intelligence\\p4\\supervised_learner\\car.txt', 1725, 50, True)