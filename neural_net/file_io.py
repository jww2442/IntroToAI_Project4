
#only works for small_dataset.txt?
def file_to_inout_lists(path):
    file = open(path, 'r')
    lines = file.readlines()

    dataset = []

    for line in lines:
        datapair = [[], []]
        b = 0
        f = 0
        words = 0
        on_space = False
        for char in line:
            if(not on_space):
                if(line[f].isspace()):
                    on_space = True
                    if(words == 0):
                        words += 1
                        datapair[0].append(float(line[b:f]))
                    elif(words == 1):
                        words +=1
                        datapair[0].append(float(line[b:f]))
                    elif(words == 2): #output
                        words += 1
                        outval = float(line[b:f])
                        if(outval == 1):
                            datapair[1] = [1,0]
                        elif(outval == 2):
                            datapair[1] = [0,1]
                        else:
                            print('err019')
                            exit()
                    else: 
                        print('err810')
                    b = f
            else:
                if(not line[f].isspace()):
                    on_space = False
                    b = f
                    
            f+=1
        
        dataset.append(datapair)

    return dataset


#only works when each dataItem belongs to one and only one class
#assumes classes are ints starting from 1
def general_file_to_inout_lists(path, num_atts, num_classes):
    file = open(path, 'r')
    lines = file.readlines()

    dataset = []                        

    for line in lines:
        datapair = [[], []]
        for i in range(num_classes):
            datapair[1].append(0)
        b = 0
        f = 0
        words = 0
        on_space = False
        for char in line:
            if(not on_space):
                if(line[f].isspace()):
                    on_space = True
                    if(words>= 0 and words< num_atts):
                        words += 1
                        datapair[0].append(float(line[b:f]))
                    
                    elif(words == num_atts): #class output
                        words += 1
                        
                        classval = int(line[b:f])
                        datapair[1][classval - 1] = 1
                        
                    else: 
                        print('err081')
                    b = f
            else:
                if(not line[f].isspace()):
                    on_space = False
                    b = f
            f+=1
            
        
        dataset.append(datapair)

    return dataset



def file_inout_lists_iris(path = 'iris_data.txt'):

    file = open(path, 'r')
    lines = file.readlines()

    dataset = []                        

    for line in lines:
        datapair = [[], [0, 0, 0]]
        b = 0
        f = 0
        words = 0

        for char in line:
            if(line[f] == ','):

                words += 1
                datapair[0].append(float(line[b:f]))
                b = f+1
                
            elif(line[f].isspace()): #class output
                words += 1
                
                classval = line[b:f]
                if(classval == 'Iris-setosa'):
                    datapair[1][0] = 1
                elif(classval == 'Iris-versicolor'):
                    datapair[1][1] = 1
                elif(classval == 'Iris-virginica'):
                    datapair[1][2] = 1  
                else: 
                    print('err081')
                
            
            f+=1
            
        
        dataset.append(datapair)

    return dataset



def file_inout_lists_labeled_examples(path = 'labeled_examples.txt'):


    file = open(path, 'r')
    lines = file.readlines()

    dataset = []                        

    for line in lines:
        datapair = [[], [0, 0]]
        b = 0
        f = 0
        words = 0

        for char in line:
            if(line[f].isspace()):
                if(words == 0):
                    words +=1
                    classval = int(line[b:f])
                    datapair[1][classval] = 1
                elif(words > 0 and words <3):
                    words += 1
                    datapair[0].append(float(line[b:f]))
                    b = f+1
                elif(words == 3):
                    break
                else: 
                    print('err512')
                    exit()
                b = f+1
            
            f+=1
            
        dataset.append(datapair)

    return dataset

