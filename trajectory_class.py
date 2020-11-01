# ## Liberaires

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd




# ## The Trajectory Class

class Trajectory(object):

    """return and plot the input trajectories to be clustered
    file_path : <string> the file path of the data"""
    
    def __init__(self, file_path:str=None): 
        ## the file path
        self.file_path = file_path
        
        ## test counter
        self.test = 0

    def __str__(self):
        return self.file_path.split('/')[-1]
        
    def next_test(self):
        
        """return the next value for the test counter"""
        
        self.test += 1
        
    def get_coord(self):
        
        """getting the coordinates of the trajectories from the csv file"""
        
        ## reading the csv file
        df = pd.read_csv(self.file_path, names=['x', 'y', 'nx', 'ny'], sep=' ')
        
        ## drop None valeus
        df = df.dropna(axis=0, how="any")
        
        ## drop non-numeric values
        df = df.select_dtypes(include=['float64'])
        
        self.x_coord = df['x']
        self.y_coord = df['y']
        
    def plot(self):
        
        """plot the input trajectories"""
        
        plt.style.use('seaborn')
        plt.plot(self.x_coord, self.y_coord, label='input trajectories')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('The input trajectories')
        plt.legend()
        plt.show()