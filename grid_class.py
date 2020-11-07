## Liberaires

import numpy as np
import matplotlib.pyplot as plt



## The Grid Class


class Grid(object):
    
    """Return and plot the clustered trajectories
    x_coord : <numpy array> the x coordinates
    y_coord : <numpy array> the y coordinates
    n_rects : <integer> n_rects**2 is the number of cells in the grid
    """
    
    def __init__(self, x_coord:np.array=None, y_coord:np.array=None, n_cells:int=200):
        self.x_coord = x_coord ## The x coordinates of trajectories
        self.y_coord = y_coord ## The y coordinates of trajectories
        self.n_cells = n_cells ## the number of rectangles in the grid
        
        ## getting the edge points and rectangle width and height of the grid
        self.get_edges_points()
        
        ## initialize the grid with 0 values 
        self.initiate_grid()
        
        ## getting the rectangle for the trajectories
        self.get_input_trajectories_cells()
        
        
    def initiate_grid(self):
        
        """return a zero numpy array with the shape (n_rect x n_rects)"""
        
        ## value 0 means that the cell is empty and 1 means that it's occupied
        self.grid = np.zeros((self.n_cells + 1, self.n_cells + 1))
        
    
    def get_edges_points(self):
        
        """return the corner points of the grid and the rectangle's hight and width"""
       
        ## the edge coordinates of the grid
        self.x0, self.y0 = min(self.x_coord)-1, min(self.y_coord)-1
        self.x1, self.y1 = max(self.x_coord)+1, max(self.y_coord)+1
        
        ## the rectangles width and height
        self.cell_width  = (self.x1 - self.x0) / (self.n_cells - 1)
        self.cell_height = (self.y1 - self.y0) / (self.n_cells - 1) 
    
    
    def get_input_trajectories_cells(self):
        
        """return the projection of the x and y coordinates 
        of the input trajectories on the center of the cells of the grid"""
        
        for x, y in zip(self.x_coord, self.y_coord):
            
            ## get the cell that corresponds to the coordiantes x and y
            i, j = self.get_cell(x, y)
            
            ## swaping the value of the cell (i, j) to 1
            self.grid[i, j] = 1
            
    
    def get_cell(self, x:float, y:float) -> tuple:
        
        """return the cell in which the coordinates x and y are in"""
        
        ## getting the cell in wich the coordinate (x, y) is in.
        i = (x - self.x0) // self.cell_width  + 1
        j = (y - self.y0) // self.cell_height + 1
        return int(i), int(j)
    
    
    def get_cell_coordinates(self, i:int, j:int) -> tuple:
        
        """return the coordinates of the cell (i, j)"""
        
        x, y = self.cell_width * i, self.cell_height * j
        x = self.x0 + self.cell_width  * (x // self.cell_width)
        y = self.y0 + self.cell_height * (y // self.cell_height)
        return x, y
        
        
    def get_cell_center(self, i:int, j:int) -> tuple: 
        
        """return the coordinates of the center of the cell (i, j)"""
        
        a, b = self.get_cell_coordinates(i, j)
        return a + self.cell_width / 2 , b + self.cell_height / 2

    
    def get_cell_neighbours(self, i:int, j:int) -> list:
        
        """return the list of neighbours of the cell (i, j)"""
        
        for v in range(max(0, i-4), min(i+5, len(self.grid))):
            for u in range(max(0, j-4), min(j+5, len(self.grid[0]))):
                if self.grid[(v, u)] and any([i!=v, j!=u]):
                    return v, u

                
    def get_trajectories_cells(self) -> list:
        
        """return the cells of clustered trajectories"""
        
        trajectories = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[(i, j)]:
                    a, b = i, j
                    trajectory = [[a, b]]
                    self.grid[(a, b)] = 0
                    while all([self.get_cell_neighbours(a,b)]) :
                        trajectory.append([a, b])
                        a,b = self.get_cell_neighbours(a, b)
                        self.grid[(a, b)] = 0
                    trajectories.append(trajectory)
        return np.array(trajectories)
    
        
    def get_trajectories_coordinates(self, trajectories:np.array)->np.array:
        
        """return the coordinates of clustered trajectories"""
        
        trajectories_coordinates = []
        for trajectory in trajectories:
            x_coord, y_coord = [], []
            for cell in trajectory:
                x, y = self.get_cell_center(*cell)
                x_coord.append(x)
                y_coord.append(y)
            trajectories_coordinates.append([x_coord, y_coord])
        return np.array(trajectories_coordinates) 
    
    
    def save_clustered_trajectories(self, file_name:str):
        
        """save the clustered trajectories with the given file name"""
        
        ## creating x coordinates and y coordinates
        x_coordinates = []
        y_coordinates = []
        for trajectory in self.clustered_trajectories:
            for x, y in zip(trajectory[0], trajectory[1]):
                x_coordinates.append(x)
                y_coordinates.append(y)
            
        ## create the data frame    
        coordinates_dict = {'x' : x_coordinates, 'y' : y_coordinates}
        df = pd.DataFrame.from_dict(coordinates_dict)
        df.to_csv(f'{file_name}.csv')
    
            
    def plot_clustered_trajectories(self, trajectories_centers:np.array):
        
        """plot the clustered trajectories"""
        
        self.clustered_trajectories = self.get_trajectories_coordinates(trajectories_centers)
        for e, trajectory in enumerate(self.clustered_trajectories):
            plt.scatter([trajectory[0][0], trajectory[0][-1]], [trajectory[-1][0], trajectory[1][-1]])
            plt.plot(trajectory[0], trajectory[1], label=f'trajectory {e}')
        

    def plot(self):
        
        """draw the clustered trajectories"""
        
        ## using the seaborn style
        plt.style.use('seaborn')
        
        ## resizing the plot
        plt.rcParams["figure.figsize"] = 8, 8
        
        ## getting the trajectories cells
        trajectories = self.get_trajectories_cells()
        
        ## plotting the clustered trajectories
        self.plot_clustered_trajectories(trajectories)
        plt.title('Clustered Trajectories')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend(bbox_to_anchor=(1.2, 1))
        plt.show()
