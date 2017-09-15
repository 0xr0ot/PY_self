import pandas as pd

path = r'F:\year_addr.csv'

data = pd.read_csv(path, header=None, sep=',', encoding='utf-8')
data_13 = data[data[0]==2014]#第一列为2014的所有行数据
dt_13 = data_13[[1,2]]#只要第2,3列数据
  
dict_13 = dict()
for i in range(34,68):
    dict_13[dt_13.ix[i,1]] = dt_13.ix[i,2]
    
print(dict_13)
