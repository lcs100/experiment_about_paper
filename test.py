    #!usr/bin/env python
    #encoding:utf-8
import random
import time

MAX_VALUE = 1000

def random_matrix_genetor(vex_num=10):
    '''''
    随机图顶点矩阵生成器
    输入：顶点个数，即矩阵维数
    '''
    data_matrix=[]
    for i in range(vex_num):
        one_list=[]
        for j in range(vex_num):
            one_list.append(random.randint(1, 100))
        data_matrix.append(one_list)
    return data_matrix

def dijkstra(data_matrix, start_node):
    '''''
    Dijkstra求解最短路径算法
    输入：原始数据矩阵，起始顶点
    输出；起始顶点到其他顶点的最短距离
    '''
    vex_num=len(data_matrix)
    flag_list=['False']*vex_num
    prev=[0]*vex_num
    dist=['0']*vex_num
    for i in range(vex_num):
        flag_list[i]=False
        prev[i]=0
        dist[i]=data_matrix[start_node][i]

    flag_list[start_node]=False
    dist[start_node]=0
    k=0

    for i in range(1, vex_num):
        min_value=99999
        for j in range(vex_num):
            if flag_list[j]==False and dist[j] != MAX_VALUE:
                min_value=dist[j]
                k=j
        flag_list[k]=True
        for j in range(vex_num):
            if data_matrix[k][j] == MAX_VALUE:
                temp = MAX_VALUE
            else:
                temp = min_value + data_matrix[k][j]

            if flag_list[j] == False and temp != MAX_VALUE and temp < dist[j]:
                dist[j]=temp
                prev[j]=k
    for i in range(vex_num):
        print ('顶点'+str(start_node)+'到顶点'+str(i)+'最短距离是--->'+str(dist[i]))

def main_test_func(vex_num=10):
    '''''
    主测试函数
    '''
    start_time=time.time()
    data_matrix=random_matrix_genetor(vex_num)
    dijkstra(data_matrix,1)
    end_time=time.time()
    return end_time-start_time

if __name__ == '__main__':
    data_matrix=[[0,2,3,MAX_VALUE],[2,0,MAX_VALUE,5],[3,MAX_VALUE,0,9],[MAX_VALUE,5,9,0]]
    dijkstra(data_matrix, 1)
    time_list=[]
    print ('----------------------------10顶点测试-------------------------------------')
    time10=main_test_func(10)
    time_list.append(time10)
    print ('----------------------------50顶点测试-------------------------------------')
    time50=main_test_func(50)
    time_list.append(time50)
    print ('----------------------------100顶点测试-------------------------------------')
    time100=main_test_func(100)
    time_list.append(time100)
    print ('---------------------------------时间消耗对比--------------------------------')
    for one_time in time_list:
        print(one_time)

