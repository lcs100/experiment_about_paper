import os
import random
import re

node_count = 16
shard_count = 4
MAX_VALUE = 10000

class Node:

    def __init__(self, index, num, shard_index_1, shard_index_2):
        self._id = index
        self.router = num
        self.shard_index_1 = shard_index_1
        self.shard_index_2 = shard_index_2
  
class Graph:

    def __init__(self, row, col):
        self.matrix = [[0] * row for i in range(col)]
        for i in range(row):
            for j in range(col):
                if(i == j):
                    self.matrix[i][j] = 0
                    continue
                self.matrix[i][j] = MAX_VALUE

    def set_value(self, row, col, val):
        self.matrix[row][col] = val
        self.matrix[col][row] = val

def dijkstra(g, v, end, node_count):
    vex_num = node_count
    flag_list = ['False']*vex_num
    prev = [0]*vex_num
    dist = ['0'] * vex_num

    for i in range(vex_num):
        flag_list[i] = False
        prev[i] = 0
        dist[i] = g.matrix[v][i]

    flag_list[v] = False
    dist[v] = 0
    k = 0

    for i in range(1, vex_num):
        max_value = 99999
        for j in range(vex_num):
            if flag_list[j] == False and dist[j] != MAX_VALUE:
                max_value = dist[j]
                k = j
        flag_list[k] = True

        for j in range(vex_num):
            if g.matrix[k][j] == MAX_VALUE:
                tmp = MAX_VALUE
            else :
                tmp = max_value + g.matrix[k][j]
            if flag_list[j] == False and tmp != MAX_VALUE and tmp < dist[j]:
                dist[j] = tmp
                prev[j] = k
    
    for i in range(vex_num):
        if( i == end):
            return dist[i]

def create_overlap_shard(node_arr, node_count, shard_count):
    node_index_arr = list(range(0, node_count))
    shard_dict = {}
    ## daluan fenpei
    random.shuffle(node_index_arr)

    for i in range(shard_count):
        key = 'shard_arr_' + f'{i}'
        shard_dict.setdefault(key, [])

    shard_own_node_count = 2 * int(node_count / shard_count)

    ## daluan
    for i in node_index_arr:
        j = random.randint(0, shard_count - 1)
        key = f'shard_arr_{j}'

        while len(shard_dict[key]) == shard_own_node_count:
            j = random.randint(0, shard_count - 1) 
            key = f'shard_arr_{j}'

        shard_dict[key].append(i)    
        node_arr[i].shard_index_1 = j
        
        k = random.randint(0, shard_count - 1)
        while k == j:
            k = random.randint(0, shard_count - 1)
        
        key = f'shard_arr_{k}'
        while len(shard_dict[key]) == shard_own_node_count:
            k = random.randint(0, shard_count - 1) 
            while k == j:
                k = random.randint(0, shard_count - 1)
            key = f'shard_arr_{k}'
        
        shard_dict[key].append(i)    
        node_arr[i].shard_index_2 = k
    
    return shard_dict

def create_graph(vex_num, edge_num):
    if(edge_num < vex_num):
        return False

    if(2 * edge_num > vex_num*(vex_num - 1)):
        return False

    g_graph = Graph(vex_num, vex_num)

    while(edge_num != 0):
        j = random.randint(0, vex_num - 1)
        k = random.randint(0, vex_num - 1)
        if(j == k):
            continue
        if(g_graph.matrix[j][k] == 1):
            continue
        g_graph.set_value(j, k, 1)
        edge_num -= 1

    return g_graph
    
if __name__ == '__main__':
    node_arr = []
    shard_arr = {}
    shard_graph_arr = {}
    node_connect_arr = []

    ## init node
    for i in range(node_count):
        n = Node(i, 0, 0, 0)
        node_arr.append(n)

    shard_arr = create_overlap_shard(node_arr, node_count, shard_count)
    print(shard_arr)


    tmp = 0
    while(tmp != shard_count):
        key = 'shard_graph_' + f'{tmp}'
        g = create_graph(4, 4)
        shard_graph_arr[key] = g
        tmp += 1
    
    ## not chongdie
    ## node between shard
    for i in range(shard_count):
        key1 = 'shard_arr_' + f'{i}'
        tmp1 = shard_arr[key1][0]
        for j in range(i+1, shard_count):
            key2 = 'shard_arr_' + f'{j}'
            tmp2 = shard_arr[key2][0]
            node_connect_arr.append((tmp1, tmp2))
    

    
    ## tx init
    tx_list = []
    count = 0
    with open('res.txt') as f:
        for line in f.readlines():
            _str = ''.join(line)[3:9]
            tx_list.append(_str)
            count += 1
            if(count > 1000):
                break
'''
    # feichongdiefenpian
    total_length = 0
    for tx in tx_list:
        _input = random.randint(0, node_count - 1)
        _output = random.randint(0, node_count - 1)

        if(_input == _output):
            continue
        else:
            input_shard = node_arr[_input].shard_index
            output_shard = node_arr[_output].shard_index

            if(input_shard == output_shard):
                _input_graph = f'shard_graph_{input_shard}'
                _input_shard = f'shard_arr_{input_shard}'
                sum1 = dijkstra(shard_graph_arr[_input_graph], shard_arr[_input_shard].index(_input), shard_arr[_input_shard].index(_output), int(node_count/shard_count))
                total_length += sum1
                continue
            else:
                _input_graph = f'shard_graph_{input_shard}'
                _input_shard = f'shard_arr_{input_shard}'
                
                sum1 = sum2 = sum3 = 0
                if(shard_arr[_input_shard].index(_input) == 0):
                    sum1 = 1
                else:
                    sum1 = dijkstra(shard_graph_arr[_input_graph], 0, shard_arr[_input_shard].index(_input), int(node_count/shard_count))
                
                sum2 = 1

                _output_graph = f'shard_graph_{output_shard}'
                _output_shard = f'shard_arr_{output_shard}'
                
                sum3 = dijkstra(shard_graph_arr[_output_graph], 0, shard_arr[_output_shard].index(_output), int(node_count/shard_count))
                total_length = total_length + sum1 + sum2 + sum3

    print(total_length)   

    ## start find
    g_not_shard = create_graph(node_count, node_count + 2)

    total_length = 0
    for tx in tx_list:
        _input = random.randint(0, node_count - 1)
        _output = random.randint(0, node_count - 1)
        
        if(_input == _output):
            total_length += 1
        else:
            tmp = dijkstra(g_not_shard, _input, _output, node_count)
            total_length += tmp
    
    print(total_length)
'''    
    ## chongdie fenpian
