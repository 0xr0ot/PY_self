#!usr/bin/env python3
#-*-coding: utf-8-*-


import csv
import numpy as np
import pandas as pd

path_0 = '/Users/qwe/test0.csv'
path_1 = '/Users/qwe/test1.csv'
items = [{'中原地产': 67}, {'我爱我家': 68}]



def read_bigfile(path):
    content = []
    with open(path, 'r', encoding='utf-8') as f:
        mark = True
        while mark:
            content.append((f.readline())[:-1]) ##del '\n'
            mark = content[-1]
    return content[:-1]##list


def read_smallfile(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.readlines() ##has '\n'
    return content
        

def write_file(path):
    with open(path, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(str(item))



np_data = np.genfromtxt(path_0, skip_header=1, dtype=None, delimiter=',')
print(np_data[0][0].decode('utf-8'))

pd_data = pd.read_csv(path_0, header=0, sep=',', encoding='utf-8')##header=None
#read_table
pd_data.to_csv('test0_to_csv.xlsx', sep='\t', index=False, encoding='utf-8')

#TODO
