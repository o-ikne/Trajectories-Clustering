import pytest
import pandas as pd
import numpy as np

class Trajectory(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.csv_file = pd.read_csv(file_name, header=None, skip_blank_lines=False)
        self.csv_file = self.csv_file.replace(np.nan, False)
        self.test = 0
        self.input_data = None
        self.output_data = None

    def next_test(self):
        self.test += 1

    def get_input_data(self):
        self.file_spliters = 0
        for row in self.csv_file.index.to_list():
            if not self.csv_file.loc[row].all():
                self.split_row = row
                self.file_spliters += 1
        self.input_data = self.csv_file.iloc[:self.split_row]

    def get_output_data(self):
        self.output_data = self.csv_file[self.split_row + 1:]

    def check_number(self, L):
        try:
            a, b = list(map(int, L.to_list()[0]))
            if not isinstance(a, int) and not isinstance(a, float):
                return False
            if not isinstance(b, int) and not isinstance(b, float):
                return False
            return True
        except:
            return False

    def check(self):
        if self.test == 0:
            if self.file_name.endswith('.csv'):
                return 'file format is csv'
            
        if self.test == 1:
            if self.csv_file.shape[0] >= 3:
                return 'csv file is not empty'

        if self.test == 2:
            if len(self.input_data) and len(self.output_data) and self.file_spliters == 1:
                return 'all data is there'

        if self.test == 3:
            value_format = True
            if not all([self.input_data[col].str.contains(':').any() for col in self.input_data.columns]):
                value_format = False
            if not all([self.output_data[col].str.contains(':').any() for col in self.output_data.columns]):
                value_format = False
            if not any(list(map(self.check_number, [self.input_data[row].apply(lambda x:x.split(':')) for row in self.input_data.columns]))):
                value_format = False
            if not any(list(map(self.check_number, [self.output_data[row].apply(lambda x:x.split(':')) for row in self.output_data.columns]))):
                value_format = False
            if value_format:
                return 'data format is correct'

            
            


def test_file_format():
    traj = Trajectory('data.csv')
    assert traj.check() == 'file format is csv'

def test_empty_file():
    traj = Trajectory('data.csv')
    traj.check()
    traj.next_test()
    assert traj.check() == 'csv file is not empty'

def test_input_output_data():
    traj = Trajectory('data.csv')
    traj.check()
    traj.next_test()
    traj.check()
    traj.next_test()
    traj.get_input_data()
    traj.get_output_data()
    assert traj.check() == 'all data is there'

def test_input_output_format():
    traj = Trajectory('/home/iken/Documents/M1/Python refresher/data.csv')
    traj.check()
    traj.next_test()
    traj.check()
    traj.next_test()
    traj.get_input_data()
    traj.get_output_data()
    traj.check()
    traj.next_test()
    assert traj.check() == 'data format is correct'   




