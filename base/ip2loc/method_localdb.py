###########################################  纯真ip  ######################################

#https://github.com/gwind/ylinux/tree/master/tools/IP/QQWry
#https://segmentfault.com/a/1190000000352578

##更新本地dat文件
#from qqwry import updateQQwry
#result = updateQQwry('qqwry.dat')

##use
from qqwry import QQwry

q = QQwry()
q.load_file('qqwry.dat')#工作路径
result = q.lookup('xxx.xxx.xx.xx')
print(result)

######################################  ipip.net  #########################################

#https://github.com/17mon/python

import os
from ipip import IP#目前无法pip(python3.5.1)
from ipip import IPX

IP.load(os.path.abspath("mydata4vipday2.dat"))#工作路径
print IP.find("118.28.8.8")

IPX.load(os.path.abspath("mydata4vipday2.datx"))#工作路径
print IPX.find("118.28.8.8")

>>>中国	天津	天津		鹏博士
>>>中国	天津	天津		鹏博士	39.128399	117.185112	Asia/Shanghai	UTC+8	120000
