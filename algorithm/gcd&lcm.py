def gcd(n_big, n_small):
    '''The greatest common divisor func.'''
    return bcd(n_small, n_big % n_small) if n_big % n_small > 0 else n_small

def lcm(n_big, n_small):
    '''The lowest common multiple func.'''
    return n_big * n_small // gcd(n_big, n_small)
