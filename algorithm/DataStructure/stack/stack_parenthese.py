# coding=utf-8
# uliontse

LEFT = ['(','[','{']
RIGHT = [')',']','}']

def match(expr):
    s = []

    for i in expr:
        if i in LEFT: s.append(i)
        elif i in RIGHT:
            if not s: return False
            elif not 1 <= ord(i) - ord(s[-1]) <= 2: return False
            s.pop()
    return not s

if __name__ == '__main__':
    print(match('(){}[][]'))

    # print([ord(x) for x in LEFT])
    # print([ord(y) for y in RIGHT])
