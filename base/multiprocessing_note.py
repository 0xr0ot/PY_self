import time
from multiprocessing import Pool

def main(x):
    pl = []
    pl.append(x)
    print(len(pl),x)
    
                  
if __name__ == '__main__':
    
    t1 = time.time()
    with Pool(4) as p:
        #for i in range(12345):
            #p.apply(main,(i,))
        p.map(main,range(120))
        #main(i)
    t2 = time.time()
    print(t2-t1)
    
#normal:0.1716
#pool_map:0.37
#pool_apply:3.046


from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
