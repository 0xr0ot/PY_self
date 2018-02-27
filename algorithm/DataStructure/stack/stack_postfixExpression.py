# coding=utf-8
# uliontse

operators = {
    '+': lambda a,b: a+b,
    '-': lambda a,b: a-b,
    '*': lambda a,b: a*b,
    '/': lambda a,b: a/b
}

def postfixExpression(expr):
    s = []
    tokens = expr.split()

    for token in tokens:
        if token.isdigit():
            s.append(int(token))
        elif token in operators:
            f = operators[token]
            b = s.pop()
            a = s.pop()
            s.append(f(a,b))
    return s.pop()


if __name__ == '__main__':
    print(postfixExpression('2 3 4 * +'))
    
