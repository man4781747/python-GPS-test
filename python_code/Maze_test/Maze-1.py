# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 14:47:24 2018

@author: owo

MAZE-PRATICE
"""

import numpy as np

global I_MazeSize
global Ay_Maze

def WallCheck():
    Ay_PointWall = np.where(Ay_Maze==1)
    for i in range(len(Ay_PointWall[0])):
        if Ay_PointWall[0][i] - 1 >= 0:
            if Ay_Maze[Ay_PointWall[0][i] - 1, Ay_PointWall[1][i]] == 50:
                Ay_Maze[Ay_PointWall[0][i] - 1, Ay_PointWall[1][i]] = 51
            elif Ay_Maze[Ay_PointWall[0][i] - 1, Ay_PointWall[1][i]] == 51:
                Ay_Maze[Ay_PointWall[0][i] - 1, Ay_PointWall[1][i]] = 53
                
        if Ay_PointWall[1][i] - 1 >= 0:
            if Ay_Maze[Ay_PointWall[0][i], Ay_PointWall[1][i] - 1] == 50:
                Ay_Maze[Ay_PointWall[0][i], Ay_PointWall[1][i] - 1] = 51
            elif Ay_Maze[Ay_PointWall[0][i], Ay_PointWall[1][i] - 1] == 51:
                Ay_Maze[Ay_PointWall[0][i], Ay_PointWall[1][i] - 1] = 53
         
        if Ay_PointWall[0][i] + 1 < len(Ay_Maze):
            if Ay_Maze[Ay_PointWall[0][i] + 1, Ay_PointWall[1][i]] == 50:
                Ay_Maze[Ay_PointWall[0][i] + 1, Ay_PointWall[1][i]] = 51
            elif Ay_Maze[Ay_PointWall[0][i] + 1, Ay_PointWall[1][i]] == 51:
                Ay_Maze[Ay_PointWall[0][i] + 1, Ay_PointWall[1][i]] = 53
                
        if Ay_PointWall[1][i] + 1 < len(Ay_Maze):
            if Ay_Maze[Ay_PointWall[0][i], Ay_PointWall[1][i] + 1] == 50:
                Ay_Maze[Ay_PointWall[0][i], Ay_PointWall[1][i] + 1] = 51
            elif Ay_Maze[Ay_PointWall[0][i], Ay_PointWall[1][i] + 1] == 51:
                Ay_Maze[Ay_PointWall[0][i], Ay_PointWall[1][i] + 1] = 53
        
def WallBreak():
    Ay_WallPool = np.where(Ay_Maze==51)
    I_RandomChose = np.random.choice(range(len(Ay_WallPool[0])))
    Ay_Maze[Ay_WallPool[0][I_RandomChose], Ay_WallPool[1][I_RandomChose]] = 52
    
def PointUpdate():
    Ay_52Pool = np.where(Ay_Maze==52)
    for i in range(len(Ay_52Pool[0])):
        if Ay_52Pool[0][i] - 1 >= 0:
            if Ay_Maze[Ay_52Pool[0][i] - 1, Ay_52Pool[1][i]] == 0:
                Ay_Maze[Ay_52Pool[0][i] - 1, Ay_52Pool[1][i]] = 1
            elif Ay_Maze[Ay_52Pool[0][i] - 1, Ay_52Pool[1][i]] == 50:
                Ay_Maze[Ay_52Pool[0][i] - 1, Ay_52Pool[1][i]] = 55
        if Ay_52Pool[1][i] - 1 >= 0:
            if Ay_Maze[Ay_52Pool[0][i], Ay_52Pool[1][i] - 1] == 0:
                Ay_Maze[Ay_52Pool[0][i], Ay_52Pool[1][i] - 1] = 1
            elif Ay_Maze[Ay_52Pool[0][i], Ay_52Pool[1][i] - 1] == 50:
                Ay_Maze[Ay_52Pool[0][i], Ay_52Pool[1][i] - 1] = 55
         
        if Ay_52Pool[0][i] + 1 < len(Ay_Maze):
            if Ay_Maze[Ay_52Pool[0][i] + 1, Ay_52Pool[1][i]] == 0:
                Ay_Maze[Ay_52Pool[0][i] + 1, Ay_52Pool[1][i]] = 1
            elif Ay_Maze[Ay_52Pool[0][i] + 1, Ay_52Pool[1][i]] == 50:
                Ay_Maze[Ay_52Pool[0][i] + 1, Ay_52Pool[1][i]] = 55
                
        if Ay_52Pool[1][i] + 1 < len(Ay_Maze):
            if Ay_Maze[Ay_52Pool[0][i], Ay_52Pool[1][i] + 1] == 0:
                Ay_Maze[Ay_52Pool[0][i], Ay_52Pool[1][i] + 1] = 1
            elif Ay_Maze[Ay_52Pool[0][i], Ay_52Pool[1][i] + 1] == 50:
                Ay_Maze[Ay_52Pool[0][i], Ay_52Pool[1][i] + 1] = 55
                
def WallRestart():
    Ay_Maze[np.where(Ay_Maze==51)] = 50
    
I_MazeSize = 10

Lst_DestructibleWall = []

Ay_Maze = np.zeros((I_MazeSize*2-1,I_MazeSize*2-1)).astype('int') + 50

for i in np.arange(0,len(Ay_Maze),2):
    for j in np.arange(0,len(Ay_Maze),2):
        Ay_Maze[i, j] = 0

I_PointStart_X = 0*2
I_PointStart_Y = 1*2

Ay_Maze[I_PointStart_X, I_PointStart_Y] = 1

while len(np.where(Ay_Maze==0)[0]) > 0 or len(np.where(Ay_Maze==51)[0]) > 0:
    print(len(np.where(Ay_Maze==0)[0]))
    try:
        WallCheck()
        WallBreak()
        PointUpdate()
        WallRestart()
    except:
        pass
    
Ay_Maze[np.where(Ay_Maze==53)] = 55
Ay_Maze[np.where(Ay_Maze==50)] = 55
Ay_Maze[np.where(Ay_Maze==52)] = 1






