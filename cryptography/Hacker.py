# coding:utf-8

from Cipher import *

# 1 反转解密--跟加密一样
def reverse_hacker(msg):
    return reverse_cipher(msg)


# 2 凯撒加密--暴力破解
def caesar_hacker(msg):
    for key,_ in enumerate(LETTERS):
        print(key,caesar_cipher(msg,key))
#TODO
