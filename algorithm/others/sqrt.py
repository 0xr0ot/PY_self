# coding=utf-8

def sqrt(x):
    y = 1.0
    while abs(y**2 - x) > 1e-6:
        y = (y + x/y)/2
    return y
