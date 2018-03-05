def fib(n):
  return n if n < 2 else fib(n-1)+fib(n-2)

def fib2(n):
    x,y=0,1
    while n:
        x,y,n=y,x+y,n-1
    return x
