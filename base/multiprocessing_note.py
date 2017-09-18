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
