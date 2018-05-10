# coding=utf-8

def filter(func):
    def inner(*args, **kwargs):
        try:
            r = func(*args, **kwargs) + 1
        except:
            r = func(*args, **kwargs) + ', hello world!'
        return r
    return inner

@filter
def f(x):
    return x

print(f(1))
print(f('Python'))
