import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import path

from grid1 import Grid

file_path = 'cabspottingdata/new_eedigkr.txt'

class Trajectory(object):

    def __init__(self, file_path=None):        
        self.file_path = file_path
        self.get_coord()
        
    def get_coord(self):
        df = pd.read_csv(self.file_path, names=['x', 'y', 'nx', 'ny'], sep=' ')
        df = df.dropna(axis=0, how="any")
        print(df)
        self.x_coord = df['x']
        self.y_coord = df['y']
        #plt.plot(self.x_coord, self.y_coord, c='r')
        #plt.show()



    
traj = Trajectory(file_path)
grid = Grid(traj.x_coord, traj.y_coord)