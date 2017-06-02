def prime_number(n): ## n > 2.
    r = [x for x in range(2,n) if not [y for y in range(2,x) if x % y == 0]]
    return r
