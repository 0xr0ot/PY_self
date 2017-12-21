# coding=utf-8

import numpy as np
from numpy.random import randn
import matplotlib.pyplot as plt


## 具体图形内容
# 对数坐标图
# w = np.linspace(0.1,1000,1000)
# p = np.abs(1/(1+w*0.1j))#虚数
# func_pool = ['plot','semilogx','semilogy','loglog']
# fig,axes = plt.subplots(2,2)
# for ax,fname in zip(axes.ravel(),func_pool):#ravel方法：np的数组降维
#     func = getattr(ax,fname)
#     func(w,p,lw=2)
#     #ax.set_ylim(0,1.5)


## 准备画布，分块
fig = plt.figure()
#ax1 = fig.add_subplot(3,4,1)


# 折线图
ax1 = fig.add_subplot(3,4,1)
ax1.plot(randn(20).cumsum(),'b--')
# 散点图
ax2 = fig.add_subplot(3,4,2)
ax2.scatter(randn(100),randn(100),marker=(5,1),alpha=0.8)
# 柱状图、直方图
ax3 = fig.add_subplot(3,4,3)
ax3.bar(list(range(1,6)),list(randn(5)))
# 极坐标图
theta = np.arange(0,2*np.pi,0.02)

ax4 = fig.add_subplot(3,4,4,polar=True)
ax4.plot(theta,1.6*np.ones_like(theta),linewidth=2)
ax4.plot(3*theta,theta/3,'--',linewidth=2)#陀螺线

ax5 = fig.add_subplot(3,4,5,polar=True)
ax5.plot(theta,1.4*np.cos(5*theta),'--',linewidth=2)
ax5.plot(theta,1.8*np.cos(4*theta),lw=2)
plt.rgrids(np.arange(0.5,2,0.5),angle=45)#玫瑰线
plt.thetagrids([0,45])
# 等值(高)线图
ax6 = fig.add_subplot(3,4,6)
x,y = np.ogrid[-2:2:200j,-3:3:300j]
z = x*np.exp(-x**2-y**2)
extent = [np.min(x),np.max(x),np.min(y),np.max(y)]
cs = ax6.contour(z,10,extent=extent)
ax6.clabel(cs)

# ax7 = fig.add_subplot(3,4,7)
# ax7.contourf(x.reshape(-1),y.reshape(-1),z,20)#wrong

# 三维图形
# import mpl_toolkits.mplot3d
# x,y = np.mgrid[-2:2:20j,-2:2:20j]
# z = x*np.exp(-x**2-y**2)
# ax8 = fig.add_subplot(3,4,8,projection='3d')
# ax8.plot_surface(x,,y,z,rstride=2,cstride=1,cmap=plt.cm.Blues_r)##wrong,version_difference.


## 细节完善
# plt.xlabel('X_lab')
# plt.ylabel('Y_lab')
# plt.title('Title')
# plt.xlim(0,20)
# plt.ylim(-10,10)
plt.show()
