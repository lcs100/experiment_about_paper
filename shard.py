import os
import random
import re
import threading
import time

node_count = 16
shard_count = 4
MAX_VALUE = -1
class Node:

    def __init__(self, index, num, shard_index):
        self._id = index
        self.router = num
        self.shard_index = shard_index
    
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

def create_shard(node_count, shard_count):
    node_index_arr = list(range(0, node_count))
    shard_dict = {}
    ## daluan fenpei
    random.shuffle(node_index_arr)

    for i in range(shard_count):
        key = 'shard_arr_' + f'{i}'
        shard_dict.setdefault(key, [])
    
    shard_own_node_count = node_count / shard_count
    for i in range(shard_count):
        for j in range(int(shard_own_node_count)):
            key = 'shard_arr_' + f'{i}'
            shard_dict[key].append(node_index_arr[i*int(shard_own_node_count) + j])
    
    return shard_dict

def create_graph(vex_num, edge_num):
    if(edge_num < vex_num):
        return False

    if(2*edge_num < (vex_num - 1) * (vex_num - 2) + 2):
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
    
def run(tx_list, node_arr, shard_graph_arr, shard_arr):
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

if __name__ == '__main__':
    node_arr = []
    shard_arr = {}
    shard_graph_arr = {}
    node_connect_arr = []

    shard_arr = create_shard(node_count, shard_count)

    tmp = 0
    shard_own_node_count = int(node_count / shard_count)
    while(tmp != shard_count):
        key = 'shard_graph_' + f'{tmp}'
        edge_num = int((shard_own_node_count - 1)*(shard_own_node_count - 2)/2) + 1
        g = create_graph(shard_own_node_count, edge_num)
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
    
    ## init node
    for i in range(node_count):
        for j in range(shard_count):
            key = f'shard_arr_{j}'
            if(shard_arr[key].count(i) != 0):
                n = Node(i, shard_arr[key][0], j)
                node_arr.append(n)
    
    ## tx init
    tx_dict = {}
    for i in range(shard_count):
        key = f'{i}'
        tx_dict.setdefault(key, [])
    
    i = 0
    with open('res.txt') as f:
        for line in f.readlines():
            _str = ''.join(line)[3:9]
            key = f'{i}'
            if(len(tx_dict[key]) < 100000):
                tx_dict[key].append(_str)
            else:
                i += 1
            if(i >= shard_count):
                break
    
    total_length = 0
    threads = []
    start = time.time()
    for i in range(shard_count):
        key = f'{i}'
        t = threading.Thread(target=run, args=(tx_dict[key], node_arr, shard_graph_arr, shard_arr))
        threads.append(t)
        t.start()
        t.join()
    end = time.time()
    print("Execution Time: ", end - start)