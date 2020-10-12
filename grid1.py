import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

class Grid(object):
    
    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = y
        self.n_rects = 200
        self.get_edges_points()
        self.grid = np.zeros((self.n_rects + 1, self.n_rects + 1))
        self.get_edges_rects()
        #self.get_rects()
        self.draw()
        
    def __repr__(self):
        return str('traj')
        
    
    def get_edges_points(self):
        self.x0, self.y0 = min(self.x_coord)-1, min(self.y_coord)-1
        self.x1, self.y1 = max(self.x_coord)+1, max(self.y_coord)+1
        self.rect_width  = (self.x1 - self.x0) / (self.n_rects - 1)
        self.rect_height = (self.y1 - self.y0) / (self.n_rects - 1) 
    
    def get_edges_rects(self):
        for x, y in zip(self.x_coord, self.y_coord):
            i, j = self.get_rect(x, y)
            self.grid[i, j] = 1
    
    def get_rect(self, x, y):
        i = (x - self.x0) // self.rect_width + 1
        j = (y - self.y0) // self.rect_height + 1
        return int(i), int(j)
    
    def get_rect_coord(self, i, j):
        x, y = self.rect_width * i, self.rect_height * j
        x = self.x0 + self.rect_width*(x // self.rect_width)
        y = self.y0 + self.rect_height*(y // self.rect_height)
        return x, y         

                       
    def draw_trajs(self, ax):
        ax.plot(self.x_coord, self.y_coord)
        
    def get_rect_center(self, i, j): 
        a, b = self.get_rect_coord(i, j)
        return a + self.rect_width / 2 , b + self.rect_height / 2

    def relate_to_next_neighbor(self, i, j):
        nbrs = []
        for v in range(max(0, i-5), min(i+6, len(self.grid))):
            for u in range(max(0, j-5), min(j+6, len(self.grid[0]))):
                if self.grid[(v, u)] and any([i!=v, j!=u]):
                    nbrs.append([v, u])
        if len(nbrs):
            return nbrs
        return [None]

    def remove_neighboors(self, i, j):
        nbrs = self.relate_to_next_neighbor(i, j)
        if len(nbrs) > 30: 
            for i in nbrs[1:]:
                #n = random.choice(nbrs)
                self.grid[(i[0], i[1])] = 0

    def number_neighbor(self, i, j):
        s = 0
        for v in range(max(0, i-1), min(i+2, len(self.grid))):
            for u in range(max(0, j-1), min(j+2, len(self.grid[0]))):
                if self.grid[(v, u)] and any([i!=u, j!=v]):
                    s += 1
        return s

    def get_trajectories(self):
        trajs = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.number_neighbor(i, j) == 1:
                    a, b = i, j
                    self.grid[(i, j)] = 0
                    traj = []
                    while all([self.relate_to_next_neighbor(a,b)[0]]) : #[a, b] not in [rect for rect in traj for rect in trajs]]):
                        traj.append([a, b])
                        a,b = self.relate_to_next_neighbor(a, b)[0]
                        self.grid[(a, b)] = 0
                        self.remove_neighboors(a, b)
                    traj.append([a, b])   
                    if len(traj) > 5:
                        print(traj)
                        trajs.append(traj)
        self.trajs = trajs
                    
    def traj_rects_centers(self, ax):
        rect = []
        for i, a in enumerate(self.grid[1:]):
            for j, b in enumerate(a[1:]):
                if b:
                    x0, y0 = self.get_rect_center(i, j)
                    ax.scatter(x0, y0, c='r', s=0.3)
                    rect.append([i, j])
        self.new_coord = np.array(rect)
        
    def draw_path(self, ax):
        colors = ['b', 'r', 'g', 'y', 'c', 'm', 'k']
        for traj in self.trajs:
            color = np.random.choice(colors)
            x0, y0 = self.get_rect_center(*traj[0])
            x1, y1 = self.get_rect_center(*traj[-1])
            ax.scatter(x0, y0,c=color)
            ax.scatter(x1, y1,c=color)
            for i in range(len(traj) -1):
                x0, y0 = self.get_rect_center(*traj[i])
                x1, y1 = self.get_rect_center(*traj[i + 1])
                ax.plot([x0, x1], [y0, y1], c=color)

                
    def draw(self):
        fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, sharex=True)
        plt.rcParams["figure.figsize"] = 8, 8
        #x_axis = np.linspace(self.x0, self.x1, self.n_rects)
        #y_axis = np.linspace(self.y0, self.y1, self.n_rects) 
        #ax2.grid(True)
        self.traj_rects_centers(ax2)
        self.get_trajectories()
        self.draw_path(ax2)
        self.draw_trajs(ax1)
        #plt.xticks(x_axis, rotation="vertical")
        #plt.yticks(y_axis)
        plt.title('Clustering Trajectories')
        plt.xlabel('x')
        plt.ylabel('y')
        print(len(self.trajs))
        plt.show()


#Grid({1:{'x':[1, 2, 4, 5], 'y':[2,3,4,5]}})

