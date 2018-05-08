# coding=utf-8

data = {
    'FlyLine': flyLine,
    'latlng': [30,-100]
}

with open("/path/data.json",'w',encoding='utf-8') as json_file:
    json.dump(data,json_file,ensure_ascii=False) #不保证英文编码

print('save ok.')
