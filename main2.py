import os
import random
import graph
import re

node_count = 16
shard_count = 4

class Node:

    def __init__(self, num):
        self._id = num
        self.next = None

class Graph:

    def __init__(self, row, col):
        self.matrix = [[0] * row for i in range(col)]
        for i in range(row):
            for j in range(col):
                if(i == j):
                    self.matrix[i][j] = 0
                    continue
                self.matrix[i][j] = -1

    def set_value(self, row, col, val):
        self.matrix[row][col] = val
        self.matrix[col][row] = val

class Shard_graph:
    
    def __init__(self, row, col, node_count, shard_count):
        self.matrix = [[0] * row for i in range(col)]
        for i in range(row):
            for j in range(col):
                self.matrix[i][j] = -1
        self.node_count = node_count
        self.shard_count = shard_count

    def set_value(self, row, col):
        self.matrix[row][col] = 0

    def node_connect_shard(self):
        self.node_connect_shard_pair = {}

def dijkstra(g, v, end):
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
            if flag_list[j] == False and dist[j] != 'N':
                max_value = dist[j]
                k = j
        flag_list[k] = True

        for j in range(vex_num):
            if g.matrix[k][j] == 'N':
                tmp = 'N'
            else :
                tmp = max_value + g.matrix[k][j]
            if flag_list[j] == False and tmp != 'N' and tmp < dist[j]:
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
    node_connect_arr = {}

    ## init node
    for i in range(node_count):
        node_arr.append(Node(i))

    shard_arr = create_shard(node_count, shard_count)
    print(shard_arr)

    tmp = 0
    while(tmp != shard_count):
        key = 'shard_graph_' + f'{tmp}'
        g = create_graph(4, 4)
        shard_graph_arr[key] = g
        tmp += 1
    print(shard_graph_arr)
    
    ## not chongdie
    



    

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

    #graph initial
    g_not_shard = Graph(node_count, node_count)
    for i in range(node_count):
        for j in range(i+1):
            if( i == j):
                g_not_shard.set_value(i, j, 0)
                continue
            tmp = random.randint(1, 10)
            g_not_shard.set_value(i, j, tmp)
            g_not_shard.set_value(j, i, tmp)

    #for i in range(16):
    #    print(g_not_shard.matrix[i])

    ## start find
    finished_tx_list = []
    total_length = 0
    for tx in tx_list:
        _input = random.randint(0, node_count - 1)
        _output = random.randint(0, node_count - 1)
        
        if(_input == _output):
            finished_tx_list.append(tx)
        else:
            tmp = dijkstra(g_not_shard, _input, _output)
            total_length += tmp
            finished_tx_list.append(tx)
    

    
