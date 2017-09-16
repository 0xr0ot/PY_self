###########################################  纯真ip  ######################################

##update local_database
#from qqwry import updateQQwry
#result = updateQQwry('qqwry.dat')

##use
from qqwry import QQwry

q = QQwry()
q.load_file('qqwry.dat')#工作路径
result = q.lookup('xxx.xxx.xx.xx')
print(result)

######################################  ipip.net  #########################################

