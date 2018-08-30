# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 14:47:24 2018

@author: owo

MAZE-PRATICE
"""
import time
t1 = time.time()

import numpy as np
import matplotlib.pyplot as plt

global I_MazeSize, I_NewPoint_X, I_NewPoint_Y
global I_WallBreak_X, I_WallBreak_Y
global I_MazeSize_X, I_MazeSize_Y

def WallCheck(I_NewPoint_X, I_NewPoint_Y):
    Ay_Maze[I_NewPoint_X, I_NewPoint_Y] = 1
    if I_NewPoint_X - 1 >= 0:
        if Ay_Maze[I_NewPoint_X - 1, I_NewPoint_Y] == 50:
            Ay_Maze[I_NewPoint_X - 1, I_NewPoint_Y] = 51
        elif Ay_Maze[I_NewPoint_X - 1, I_NewPoint_Y] == 51:
            Ay_Maze[I_NewPoint_X - 1, I_NewPoint_Y] = 53
            
    if I_NewPoint_Y - 1 >= 0:
        if Ay_Maze[I_NewPoint_X, I_NewPoint_Y - 1] == 50:
            Ay_Maze[I_NewPoint_X, I_NewPoint_Y - 1] = 51
        elif Ay_Maze[I_NewPoint_X, I_NewPoint_Y - 1] == 51:
            Ay_Maze[I_NewPoint_X, I_NewPoint_Y - 1] = 53
     
    if I_NewPoint_X + 1 < len(Ay_Maze[:]):
        if Ay_Maze[I_NewPoint_X + 1, I_NewPoint_Y] == 50:
            Ay_Maze[I_NewPoint_X + 1, I_NewPoint_Y] = 51
        elif Ay_Maze[I_NewPoint_X + 1, I_NewPoint_Y] == 51:
            Ay_Maze[I_NewPoint_X + 1, I_NewPoint_Y] = 53
            
    if I_NewPoint_Y + 1 < len(Ay_Maze[0,:]):
        if Ay_Maze[I_NewPoint_X, I_NewPoint_Y + 1] == 50:
            Ay_Maze[I_NewPoint_X, I_NewPoint_Y + 1] = 51
        elif Ay_Maze[I_NewPoint_X, I_NewPoint_Y + 1] == 51:
            Ay_Maze[I_NewPoint_X, I_NewPoint_Y + 1] = 53

def WallBreak():
    Ay_WallPool = np.where(Ay_Maze==51)
    I_RandomChose = np.random.choice(range(len(Ay_WallPool[0])))
    Ay_Maze[Ay_WallPool[0][I_RandomChose], Ay_WallPool[1][I_RandomChose]] = 52
    I_WallBreak_X = Ay_WallPool[0][I_RandomChose]
    I_WallBreak_Y = Ay_WallPool[1][I_RandomChose]
    return I_WallBreak_X, I_WallBreak_Y
    
def PointUpdate(I_WallBreak_X, I_WallBreak_Y):
    if I_WallBreak_X - 1 >= 0:
        if Ay_Maze[I_WallBreak_X - 1, I_WallBreak_Y] == 0:
            Ay_Maze[I_WallBreak_X - 1, I_WallBreak_Y] = 1
            I_NewPoint_X = I_WallBreak_X - 1
            I_NewPoint_Y = I_WallBreak_Y
            
    if I_WallBreak_Y - 1 >= 0:
        if Ay_Maze[I_WallBreak_X, I_WallBreak_Y - 1] == 0:
            Ay_Maze[I_WallBreak_X, I_WallBreak_Y - 1] = 1
            I_NewPoint_X = I_WallBreak_X
            I_NewPoint_Y = I_WallBreak_Y - 1
     
    if I_WallBreak_X + 1 < len(Ay_Maze[:]):
        if Ay_Maze[I_WallBreak_X + 1, I_WallBreak_Y] == 0:
            Ay_Maze[I_WallBreak_X + 1, I_WallBreak_Y] = 1
            I_NewPoint_X = I_WallBreak_X + 1
            I_NewPoint_Y = I_WallBreak_Y
            
    if I_WallBreak_Y + 1 < len(Ay_Maze[:,0]):
        if Ay_Maze[I_WallBreak_X, I_WallBreak_Y + 1] == 0:
            Ay_Maze[I_WallBreak_X, I_WallBreak_Y + 1] = 1
            I_NewPoint_X = I_WallBreak_X 
            I_NewPoint_Y = I_WallBreak_Y + 1
    
    return I_NewPoint_X, I_NewPoint_Y
    
I_MazeSize_X = 5
I_MazeSize_Y = 4

Lst_DestructibleWall = []

Ay_Maze = np.zeros((I_MazeSize_X*2-1,I_MazeSize_Y*2-1)).astype('int') + 50

for i in np.arange(0,len(Ay_Maze[:]),2):
    for j in np.arange(0,len(Ay_Maze[0,:]),2):
        Ay_Maze[i, j] = 0

I_NewPoint_X = 0*2
I_NewPoint_Y = 1*2
#j = 0
i = 0
while i == 0: 
    try:
        WallCheck(I_NewPoint_X, I_NewPoint_Y)
        I_WallBreak_X, I_WallBreak_Y = WallBreak()
        I_NewPoint_X, I_NewPoint_Y = PointUpdate(I_WallBreak_X, I_WallBreak_Y)
#        plt.scatter(np.where(Ay_Maze==1)[0], np.where(Ay_Maze==1)[1], s = 3)
#        plt.scatter(np.where(Ay_Maze==0)[0], np.where(Ay_Maze==0)[1], s = 3)
#        plt.axis('equal')
#        plt.savefig('{0}.png'.format(j))
#        plt.clf()
#        j += 1
    except:
        i = 1
    
Ay_Maze[np.where(Ay_Maze==53)] = 55
Ay_Maze[np.where(Ay_Maze==50)] = 55
Ay_Maze[np.where(Ay_Maze==52)] = 1

Ay_Maze_ = np.zeros((len(Ay_Maze[:])+2, len(Ay_Maze[0,:])+2)) + 55
Ay_Maze_[1:len(Ay_Maze[:])+1,1:len(Ay_Maze[0,:])+1] = Ay_Maze
Ay_Maze = Ay_Maze_

print(time.time() - t1)

plt.scatter(np.where(Ay_Maze==55)[0], np.where(Ay_Maze==55)[1], s = 3)

plt.axis('equal')
