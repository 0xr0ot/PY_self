# coding=utf-8
# uliontse

import requests
# import pandas as pd

path_r = r'C:\{your_path}\city.txt'
path_r = r'C:\{your_path}\city_latlng.txt'

def googleMap(city):
    error_data = {'lat': 404, 'lng': 404}

    if city in [None,'None','','NULL','null','未知']: return error_data
    elif '<' in city: return error_data
    elif len(city) < 2: return error_data
    else:
        if city == 'BJ':
            city = 'BeiJing'
        try:
            key = '{your_key}'
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(city,key)
            json_data = requests.get(url).json()
            data = json_data.get('results')[0].get('geometry').get('location')
            return data
        except:
            return error_data

def read_bigfile(path):
    content = []
    with open(path, 'r', encoding='utf-8') as f:
        mark = True
        while mark:
            content.append((f.readline())[:-1]) ##del '\n'
            mark = content[-1]
    return content[:-1]##list

def main():
    with open(path_r,'r',encoding='utf-8') as f1:
        city = True
        n = 1
        with open(path_w, 'a', encoding='utf-8') as f2:
            while city:
                city = f1.readline()[:-1]
                if n < 993:
                    # data = googleMap(city)
                    # data = mapQuest(city)
                    data = baiduMap(city)
                    line = ';'.join([str(n), city, str(round(data['lat'],4)), str(round(data['lng'],4))])
                    print(line)
                    f2.write(line + '\n')
                n += 1

if __name__ == '__main__':
    main()

# city_pool = read_bigfile(path)

# # new_city = []
# lat_pool, lng_pool = [], []
# for city in city_pool:
#     data = googleMap(city)
#     print(city, data)
#     lat_pool.append(data['lat'])
#     lng_pool.append(data['lng'])
#     # new_city.append(city.strip())

# print(len(city_pool),len(lat_pool),len(lng_pool))

# pool = [city_pool,lat_pool,lng_pool]
# df = pd.DataFrame(columns=['city','lat','lng'],data=pool)
# df.to_csv(r'C:\{your_path}\city_axis.csv')
