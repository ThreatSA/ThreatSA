'''
This python file is used to calculate the similarity between situation assessment result
with dataset feature
'''
from shapesimilarity import shape_similarity
import numpy as np
import pandas as pd
import math

'''
trans function
-------------------------
This function is used for standardization of assessment results
#Arguments
    dataframe: the dataframe of assessment results
    ip_list: the list of ip need to assess
'''
def trans(dataframe,ip_list):
    df = dataframe.loc[ip_list]
    result = []
    for ip in ip_list:
        value_1 = list(df.loc[ip])
        value = [x for x in value_1 if math.isnan(x) == False]
        trans_result = [num/max(value) for num in value]
        trans_result.insert(0,ip)
        result.append(trans_result)
    result = pd.DataFrame(result,index=None)
    return result

'''
line_shape_host function
-------------------------
This function is used for calculate the similarity of hosts
#Arguments
    dataset: the dataset feature
    test: the assessment result
    ip_list: the list of ip need to assess
'''
def line_shape_host(dataset,test,ip_list):
    simi_result = []
    for ip in ip_list:
        print(ip)
        dl_np = []
        tl_np = []
        dataset_line = list(dataset.loc[ip])
        test_line = list(test.loc[ip])
        for i in range(len(dataset_line)):
            dl_np.append((i,dataset_line[i]))
            tl_np.append((i,test_line[i]))
        dl_np = np.column_stack(dl_np)
        tl_np = np.column_stack(tl_np)
        sim = shape_similarity(dl_np,tl_np)
        print(sim)
        print('\n')
        simi_result.append(sim)
    return sum(simi_result)/len(simi_result)

'''
line_shape_network function
-------------------------
This function is used for calculate the similarity of the network
#Arguments
    dataset: the dataset feature
    ip_list: the list of ip need to assess
    result_root: the root path of asssessment result 
'''
def line_shape_network(dataset,ip_list,result_root):
    cent_list = ['degree','katz','close','all','avg-noharm']
    num_list = [0.1,0.2,0.3,0.4,0.5]
    data_np = []
    for i in range(len(dataset)):
        data_np.append((i,dataset[i]))
    data_np = np.column_stack(data_np)
    for cent in cent_list:
        print(cent)
        for num in num_list:
            print(num)
            file1_path = result_root+cent+str(num)+'.csv'
            file1 = pd.read_csv(file1_path,header=None,index_col=False)
            result = []
            for i in range(1,21):
                result.append(max(list(file1.iloc[:,i])))
            test_line = [num/max(result) for num in result]
            test_np = []
            for i in range(len(test_line)):
                test_np.append((i,test_line[i]))
            test_np = np.column_stack(test_np)
            print(shape_similarity(data_np,test_np))
        print('----------------------------------------------------')
