# coding:utf-8

LETTERS = r'''!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`a bcdefghijklmnopqrstuvwxyz{|}~'''

# 1 反转加密
def reverse_cipher(msg):
    translated = '' 
    i = len(msg) - 1
    while i > 0:
        translated += msg[i]
        i -= 1
    return translated
    

# 2 凯撒加密
def caesar_cipher(msg,key=0):
    translated = ''
    for symbol in msg:
        if symbol in LETTERS:
            num = LETTERS.find(symbol)#index()
            num += key
  
            if num >= len(LETTERS):
                num -= len(LETTERS)
            elif num < 0:
                num += len(LETTERS)
            translated += LETTERS[num]
        else:
            translated += symbol
    return translated


# 3 换位加密
def transposition_cipher(msg):
    pass
#TODO
