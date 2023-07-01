'''
This python file is used to generate malicious traffic graph
'''

import pandas as pd
import datetime
import networkx as nx
import matplotlib.pyplot as plt

'''
time_diff function
-------------------------
This function is used to split the traffic information according to the sampling time
#Arguments
    traffic_dataframe: the original dataframe for traffic information
    start_time: the start time for sampling
    time_range: the sampling time
'''
def time_diff(traffic_dataframe,start_time,time_range):
    start = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S.%f')
    result = [0]
    i = 0
    while i <len(traffic_dataframe):
        if datetime.datetime.strptime(traffic_dataframe.iloc[i]['Ltime'],'%Y-%m-%d %H:%M:%S.%f') < start+datetime.timedelta(hours=time_range):
            i += 1
        else:
            result.append(i)
            start = start+datetime.timedelta(hours=time_range)
            while datetime.datetime.strptime(traffic_dataframe.iloc[i]['Ltime'],'%Y-%m-%d %H:%M:%S.%f') > start+datetime.timedelta(hours=time_range):
                start = start+datetime.timedelta(hours=time_range)
                result.append('None')
    result.append(len(traffic_dataframe))
    return result

'''
traffic_graph_generation function
-------------------------
This function is used to generate malicious traffic graph
#Arguments
    traffic_data: the labeled traffic data
'''
def traffic_graph_generation(traffic_data):
    node_list = []
    edge_dict = dict()
    for i  in range(len(traffic_data)):
        item = traffic_data.iloc[i]
        if item['Label']==1:
            node_list.append(item['srcip'])
            node_list.append(item['dstip'])
            if (item['srcip'],item['dstip']) in edge_dict.keys():
                edge_dict[(item['srcip'],item['dstip'])] += 1
            else:
                edge_dict[(item['srcip'],item['dstip'])] = 1
    node_list = set(node_list)
    G = nx.DiGraph()
    G.add_nodes_from(node_list)
    for item in edge_dict:
        G.add_edge(item[0],item[1],weight = edge_dict[item])
    return G

'''
cent_node_find function
-------------------------
This function is used to find the central nodes in the graph
#Arguments
    G: the malicious traffic graph
    prop: the proportion of central nodes
'''
def cent_node_find(G,prop):
    cent_node_num = len(list(G.nodes(data=True)))*prop
    if cent_node_num < 1:
            cent_node_num = 1
    degree_cent = nx.degree_centrality(G)
    degree_cent = sorted(degree_cent.items(),key = lambda x:x[1],reverse = True)
    cent_node_list = degree_cent[:int(cent_node_num)]
    cent_node = list(list(zip(*cent_node_list))[0])
    return cent_node

'''
one_path_connect function
-------------------------
This function is used to calculate the intimacy of a single path from central node to normal node
#Arguments
    G: the malicious traffic graph
    path: the list of nodes on the path from central node to normal node
'''

def one_path_connect(G,path):
    con = 0
    weights = nx.get_edge_attributes(G, 'weight')
    radio = 1
    for i in range(len(path)-1):
        con += weights[path[i],path[i+1]]*radio
        radio /=2
    return con

'''
Intimacy_calculate function
-------------------------
This function is used to calculate the intimacy between central node and normal node
#Arguments
    G: the malicious traffic graph
    cen_node: central node
    target_node :normal node
'''
def Intimacy_calculate(G,cen_node,target_node):
    all_path = list(nx.all_simple_paths(G,cen_node,target_node))
    n = len(all_path)
    if n==0:
        return 0
    sum_con = 0
    for path in all_path:
        sum_con+=one_path_connect(G,path)
    avg_con = sum_con/n
    return avg_con

'''
all_process function
-------------------------
This function is the whole process of ThreatSA for situation assessment in a certain sampling period
#Arguments
    G: the malicious traffic graph
    prop: the proportion of central nodes
'''
def all_process(G,prop):
    all_nodes = list(G.nodes(data=True))
    cent_nodes = cent_node_find(G,prop)
    Intimacy_dict = dict()
    for node in cent_nodes:
        all_nodes.remove((node, {}))
    if len(all_nodes) == 0:
        for node in cent_nodes:
            Intimacy_dict[node] = 0
        return Intimacy_dict
    for normal_node in all_nodes:
        max_intimacy = 0
        for cent_node in cent_nodes:
            intimacy_cal =  Intimacy_calculate(G,cent_node,normal_node[0])
            if intimacy_cal>max_intimacy:
                max_intimacy = intimacy_cal
        Intimacy_dict[normal_node[0]]=max_intimacy
    for node in cent_nodes:
        Intimacy_dict[node] = max(list(Intimacy_dict.values()))
    return Intimacy_dict

'''
Intimacy_calculate function
-------------------------
#Arguments
    data_path: the csv file path of labeled traffic data
    prop: the proportion of central nodes
    start_time: the start time for sampling
    time_range: the sampling time
    out_path: the outpath for situation assessment result
'''
def main(data_path,prop,start_time,time_range,out_path):
    data_df = pd.read_csv(data_path,header=0,index_col=None)
    hour_split = time_diff(data_df,start_time,time_range)
    Inti_reuslt = []
    output_result = []
    for i in range(len(hour_split)-1):
        G = traffic_graph_generation(data_df.iloc[hour_split[i]:hour_split[i+1]])
        Inti = all_process(G,prop)
        Inti_reuslt.append(Inti)
    node_all = set(list(data_df['srcip'])+list(data_df['dstip']))
    for node in node_all:
        node_inti = [node]
        for inti_dict in Inti_reuslt:
            if node in list(inti_dict.keys()):
                node_inti.append(inti_dict[node])
            else:
                node_inti.append(0)
        output_result.append(node_inti)
    output_result = pd.DataFrame(output_result)
    output_result.to_csv(out_path+str(prop)+'.csv',index=False,header=False)
