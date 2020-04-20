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

        for k in range(shard_count):
            key = f'shard_arr_{k}'
            if len(shard_dict[key]) != shard_own_node_count and shard_dict[key].count(i) == 0:
                shard_dict[key].append(i)    
                node_arr[i].shard_index_2 = k
                break

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

    tmp = 0
    shard_own_node_count = 2 * int(node_count / shard_count)
    while(tmp != shard_count):
        key = 'shard_graph_' + f'{tmp}'
        g = create_graph(shard_own_node_count, shard_own_node_count + 2)
        shard_graph_arr[key] = g
        tmp += 1
    
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

    # feichongdiefenpian
    total_length = 0
    for tx in tx_list:
        _input = random.randint(0, node_count - 1)
        _output = random.randint(0, node_count - 1)

        if(_input == _output):
            total_length += 1
            continue
        else:
            input_shard_1 = node_arr[_input].shard_index_1
            input_shard_2 = node_arr[_input].shard_index_2
            
            output_shard_1 = node_arr[_output].shard_index_1
            output_shard_2 = node_arr[_output].shard_index_2

            if input_shard_1 == output_shard_1 or input_shard_1 == output_shard_2:
                _input_graph = f'shard_graph_{input_shard_1}'
                _input_shard = f'shard_arr_{input_shard_1}'
                sum1 = dijkstra(shard_graph_arr[_input_graph], shard_arr[_input_shard].index(_input), shard_arr[_input_shard].index(_output), shard_own_node_count)
                total_length += sum1
                continue
            if input_shard_2 == output_shard_1 or input_shard_2 == output_shard_2:
                _input_graph = f'shard_graph_{input_shard_2}'
                _input_shard = f'shard_arr_{input_shard_2}'
                sum1 = dijkstra(shard_graph_arr[_input_graph], shard_arr[_input_shard].index(_input), shard_arr[_input_shard].index(_output), shard_own_node_count)
                total_length += sum1
                continue
            else:
                for i in range(shard_arr[input_shard_1]):
                    if node_arr[i].shard_index_1 == output_shard_1 or node_arr[i].shard_index_2 == output_shard_2:
                        break
            
                middle_node_index = i

                sum1 = sum2 = 0
                _input_graph = f'shard_graph_{input_shard_1}'
                _input_shard = f'shard_arr_{input_shard_1}'
                sum1 = dijkstra(shard_graph_arr[_input_graph], shard_arr[_input_shard].index(_input), middle_node_index, shard_own_node_count)
                
                if node_arr[middle_node_index].shard_index_1 == output_shard_1:
                    _output_graph = f'shard_graph_{output_shard_1}'
                    _output_shard = f'shard_arr{output_shard_1}'
                    sum2 = dijkstra(shard_graph_arr[_output_graph], shard_arr[_output_graph].index(_output), middle_node_index, shard_own_node_count)
                
                if node_arr[middle_node_index].shard_index_2 == output_shard_2:
                    _output_graph = f'shard_graph_{output_shard_2}'
                    _output_shard = f'shard_arr{output_shard_2}'
                    sum2 = dijkstra(shard_graph_arr[_output_graph], shard_arr[_output_graph].index(_output), middle_node_index, shard_own_node_count)
                
                total_length = total_length + sum1 + sum2

    print(total_length)   
