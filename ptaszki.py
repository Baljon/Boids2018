# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 15:03:08 2018

@author: martynap
"""
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

fig = plt.figure()
ax = plt.axes(xlim=(0, 800), ylim=(0, 600))

#testowe wspolrzedne
x=100
y=400
r=10

pts = ax.plot([x], [y], markersize=10, c='skyblue', marker='o', ls='None')
beak = ax.plot([x+r], [y+r], markersize=4, c='black', marker='*', ls='None')

plt.show()

#anim = animation.FuncAnimation(fig, tick, fargs = (pts, beak, boids), 
#                               interval = 50)