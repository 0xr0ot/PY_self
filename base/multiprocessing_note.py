import time
from multiprocessing import Pool

def main(name):
    print(name)
    
                  
if __name__ == '__main__':
    name_list = ['Frank','Fiona','Lip','Ian','Debbie','Carl','Liam']
    t1 = time.time()
    
    p = Pool(4) #python2 不能使用 with...as...写法
    p.map(main,name_list)
    p.terminate()
    
    t2 = time.time()
    print(t2-t1)

    #python2: multiprocessing.cpu_count()
    #python3: os.cpu_count()
    
    
    
    
    

# from multiprocessing import Process
# import os

# # 子进程要执行的代码
# def run_proc(name):
#     print('Run child process %s (%s)...' % (name, os.getpid()))

# if __name__=='__main__':
#     print('Parent process %s.' % os.getpid())
#     p = Process(target=run_proc, args=('test',))
#     print('Child process will start.')
#     p.start()
#     p.join()
#     print('Child process end.')
