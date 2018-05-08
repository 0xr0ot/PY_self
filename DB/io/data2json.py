# coding=utf-8
import json
from pprint import pprint as ppt

data = {
    'FlyLine': ['beijing','shanghai','123'],
    'latlng': [30,-100]
}
## save:
with open("/path/data.json",'w',encoding='utf-8') as json_file:
    json.dump(data,json_file,ensure_ascii=False) #不保证英文编码

## read:   
with open(r"C:\path\data.json",'r',encoding='utf-8') as json_file:
    data = json.load(json_file)
    print(data.keys())
