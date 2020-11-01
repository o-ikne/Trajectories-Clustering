## Liberaires
import pytest
from trajectory_class import Trajectory
import pandas as pd
from os import path


## Ckeking method

def check(trajectory:Trajectory):
    
    """applying the TDD method to the Trajectory class"""
    
    ## cheking if the file path exists
    if trajectory.test == 0:
        if path.exists(trajectory.file_path):
            return 'file path exists'
     
    ## checking if the file is a csv or txt file
    if trajectory.test == 1:
        if trajectory.file_path.endswith('.csv'):
            trajectory.df = pd.read_csv(trajectory.file_path)
            return 'file format is correct'
            
        if trajectory.file_path.endswith('.txt'):
            trajectory.df = pd.read_csv(trajectory.file_path, sep=' ')
            trajectory.df = trajectory.df.dropna(axis=0, how="any")
            return 'file format is correct'
        
    ## cheking if the file is not empty        
    if trajectory.test == 2:
        if trajectory.df.shape[0] >= 3 and trajectory.df.shape[1] >= 2:
            return 'file is not empty'
        
    ## cheking if the data shape is correct    
    if trajectory.test == 3:
        if trajectory.df.shape[1] == 4:
            trajectory.df.columns = ['x', 'y', 'nx', 'ny']
            return 'all data is there'

    ## cheking the format of the data
    if trajectory.test == 4:
        if (trajectory.df[['x', 'y']].dtypes == 'float64').all() or (trajectory.df[['x', 'y']].dtypes == 'int64').all():
            trajectory.df = trajectory.df.select_dtypes(include=['float64'])
            return 'data format is correct'
    
    ## cheking if coordinates are uploaded succesfuly
    if trajectory.test == 5:
        trajectory.get_coord()
        print(f"Trajectory '{trajectory}' is uploaded succesfuly")
        return 'Trajectory is uploaded succesfuly'


## Example
### file path
file_path = '/home/iken/Documents/M1/Python refresher/clustering Trajectories/cabspottingdata/new_uvreoipy.txt'


### The input Trajectories



## TESTS

## test 0
def test_file_existence():
    
    """cheking the existence of the file path"""
    trajectory = Trajectory(file_path)
    assert check(trajectory) == 'file path exists'    

## test 1
def test_file_format():
    
    """cheking the file format"""
    trajectory = Trajectory(file_path)
    check(trajectory)
    trajectory.next_test()
    assert check(trajectory) == 'file format is correct'

## test 2
def test_empty_file():
    
    """cheking that the file is not empty"""
    
    trajectory = Trajectory(file_path)
    check(trajectory)
    trajectory.next_test()
    check(trajectory)
    trajectory.next_test()
    assert check(trajectory) == 'file is not empty'
    
## test 3
def test_all_data_there():
    
    """cheking that all data is there"""

    trajectory = Trajectory(file_path)
    check(trajectory)
    trajectory.next_test()
    check(trajectory)
    trajectory.next_test()
    check(trajectory)
    trajectory.next_test()
    assert check(trajectory) == 'all data is there'    

## test 4
def test_data_format():
    
    """cheking the data format is correct"""
    
    trajectory = Trajectory(file_path)
    check(trajectory)
    trajectory.next_test()
    check(trajectory)
    trajectory.next_test()
    check(trajectory)
    trajectory.next_test()
    check(trajectory)
    trajectory.next_test()
    assert check(trajectory) == 'data format is correct'

## test 5
def test_upload_coordinates():
    
    """cheking the coordinates upload"""
    
    trajectory = Trajectory(file_path)
    check(trajectory)
    trajectory.next_test()
    check(trajectory)
    trajectory.next_test()
    check(trajectory)
    trajectory.next_test()
    check(trajectory)
    trajectory.next_test()
    check(trajectory)
    trajectory.next_test()
    assert check(trajectory) == 'Trajectory is uploaded succesfuly'
