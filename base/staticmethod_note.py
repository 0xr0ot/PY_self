# coding=utf-8

class ABC:
    def func(self,x,y):
        return x + y

    @classmethod
    def func_cls(cls,x,y):
        return x + y

    @staticmethod
    def func_stat(x,y):
        return x + y


if __name__ == '__main__':
    abc = ABC()

    print(abc.func)       # 绑定类的实例
    print(abc.func_cls)   # 绑定类本身
    print(abc.func_stat)  # 没有绑定

    print(abc.func(0,0))
    print(abc.func_cls(0,1))
    print(abc.func_stat(0,2))

    print(ABC.func_cls(0,1))
    print(ABC.func_stat(0,2))
