# ## Liberaires

import numpy as np
import matplotlib.pyplot as plt


# ## The Grid Class

class Grid(object):
    
    """Return and plot the clustered trajectories
    x_coord : <numpy array> the x coordinates
    y_coord : <numpy array> the y coordinates
    n_rects : <integer> n_rects**2 is the number of cells in the grid
    """
    
    def __init__(self, x_coord:np.array=None, y_coord:np.array=None, n_rects:int=200):
        self.x_coord = x_coord ## The x coordinates of trajectories
        self.y_coord = y_coord ## The y coordinates of trajectories
        self.n_rects = n_rects ## the number of rectangles in the grid
        
        ## getting the edge points and rectangle width and height of the grid
        self.get_edges_points()
        
        ## initialize the grid with 0 values 
        self.init_grid()
        
        ## getting the rectangle for the trajectories
        self.get_rects()
        
    def init_grid(self):    
        
        """return a zero numpy array with the shape (n_rect x n_rects)"""
        
        self.grid = np.zeros((self.n_rects + 1, self.n_rects + 1))
    
    def get_edges_points(self):
        
        """return the corner points of the grid and the rectangle's hight and width"""
       
        ## the edge coordinates of the grid
        self.x0, self.y0 = min(self.x_coord)-1, min(self.y_coord)-1
        self.x1, self.y1 = max(self.x_coord)+1, max(self.y_coord)+1
        
        ## the rectangles width and height
        self.rect_width  = (self.x1 - self.x0) / (self.n_rects - 1)
        self.rect_height = (self.y1 - self.y0) / (self.n_rects - 1) 
    
    def get_rects(self):
        
        """return the projection of the x and y coordinates 
        of the trajectory on the center of the rectangles of the grid"""
        
        for x, y in zip(self.x_coord, self.y_coord):
            i, j = self.get_rect(x, y)
            self.grid[i, j] = 1
    
    def get_rect(self, x:float, y:float) -> tuple:
        
        """return the rectangle in which the coordinates x and y are in"""
        
        i = (x - self.x0) // self.rect_width + 1
        j = (y - self.y0) // self.rect_height + 1
        return int(i), int(j)
    
    def get_rect_coord(self, i:int, j:int) -> tuple:
        
        """return the coordinates of the rectangle (i, j)"""
        
        x, y = self.rect_width * i, self.rect_height * j
        x = self.x0 + self.rect_width  * (x // self.rect_width)
        y = self.y0 + self.rect_height * (y // self.rect_height)
        return x, y         
        
    def get_rect_center(self, i:int, j:int) -> tuple: 
        
        """return the cordinates of the center of the rectangle (i, j)"""
        
        a, b = self.get_rect_coord(i, j)
        return a + self.rect_width / 2 , b + self.rect_height / 2

    def get_neighbours(self, i:int, j:int) -> list:
        
        """return the list of neighbours of the rectangle (i, j)"""
        
        for v in range(max(0, i-4), min(i+5, len(self.grid))):
            for u in range(max(0, j-4), min(j+5, len(self.grid[0]))):
                if self.grid[(v, u)] and any([i!=v, j!=u]):
                    return v, u

    def get_trajectories_rects(self) -> list:
        
        """return the clustered trajectories"""
        
        trajs = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[(i, j)]:
                    a, b = i, j
                    traj = [[a, b]]
                    self.grid[(a, b)] = 0
                    while all([self.get_neighbours(a,b)]) :
                        traj.append([a, b])
                        a,b = self.get_neighbours(a, b)
                        self.grid[(a, b)] = 0
                    if len(traj) > 5:
                        trajs.append(traj)
        return np.array(trajs)
        
    def get_trajectories_coord(self, trajs:np.array)->np.array:
        
        """draw the path of each trajectory"""
        
        trajs_coord = []
        for traj in trajs:
            x_coord, y_coord = [], []
            for rect in traj:
                x0, y0 = self.get_rect_center(*rect)
                x_coord.append(x0)
                y_coord.append(y0)
            trajs_coord.append([x_coord, y_coord])
        return np.array(trajs_coord) 
            
    def plot_clustered_trajs(self, trajs_centers:np.array, ax):
        
        """plot the clustered trajectories"""
        
        trajs_coord = self.get_trajectories_coord(trajs_centers)
        for e, traj in enumerate(trajs_coord):
            ax.scatter([traj[0][0], traj[0][-1]], [traj[-1][0], traj[1][-1]])
            ax.plot(traj[0], traj[1], label='trajectory ' + str(e))
        

    def plot(self):
        
        """draw the input and the output trajectories"""
        plt.style.use('seaborn')
        plt.rcParams["figure.figsize"] = 8, 8

        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True)

        ## ploting the input trajectories
        ax1.plot(self.x_coord, self.y_coord)
        ax1.set_title('Input trajectories')
        
        ## ploting the clustered trajectories
        trajs = self.get_trajectories_rects()
        self.plot_clustered_trajs(trajs, ax2)
        ax2.set_title(f'Clustered Trajectories for {self.n_rects}x{self.n_rects} cells')
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.legend(bbox_to_anchor=(1.25, 1))
        plt.show()