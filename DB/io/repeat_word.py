#coding:utf-8


def read_bigfile(path):
    content = []
    with open(path, 'r', encoding='utf-8') as f:
        mark = True
        while mark:
            content.append((f.readline())[:-1]) ##del '\n'
            mark = content[-1]
    return content[1:-1]

def write_file(path,items):
    with open(path, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(str(item))


if __name__ == '__main__':
    data = read_bigfile('test_del.txt')
    pool = set()
    with open('vv.txt', 'w', encoding='utf-8') as f:
        for name in data:
            for ind,v in enumerate(name):
                if ind != len(name)-1:
                    if v == name[ind +1]:
                        vv= v*2
                        print(vv)
                        if vv not in pool:
                            f.write(vv + '\n')
                        pool.add(vv)

    print(pool)
