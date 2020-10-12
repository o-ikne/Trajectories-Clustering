import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Grid(object):
    
    def __init__(self, trajs=None):
        self.trajs = trajs
        self.get_coordinates()
        self.n_rects = 5
        self.get_edges_points()
        self.grid = np.zeros((self.n_rects + 1, self.n_rects + 1))
        self.get_edges_rects()
        #self.get_rects()
        self.draw()
        
    def __repr__(self):
        return str(self.trajs)
    
    def get_coordinates(self):
        self.x_coord = np.array([x for traj in [self.trajs[i]['x'] for i in self.trajs] for x in traj])
        self.y_coord = np.array([y for traj in [self.trajs[i]['y'] for i in self.trajs] for y in traj])
        
    
    def get_edges_points(self):
        self.x0, self.y0 = min(self.x_coord)-1, min(self.y_coord)-1
        self.x1, self.y1 = max(self.x_coord)+1, max(self.y_coord)+1
        self.rect_width  = (self.x1 - self.x0) / (self.n_rects - 1)
        self.rect_height = (self.y1 - self.y0) / (self.n_rects - 1) 
    
    def get_edges_rects(self):
        for x,y in zip(self.x_coord, self.y_coord):
            i, j = self.get_rect(x, y)
            self.grid[i, j] = 1
    
    def get_rect(self, x, y):
        i = (x - self.x0) // self.rect_width
        j = (y - self.y0) // self.rect_height
        return int(i), int(j)
    
    def get_rect_coord(self, i, j):
        x, y = self.rect_width * i, self.rect_height * j
        x = self.x0 + self.rect_width*(x // self.rect_width)
        y = self.y0 + self.rect_height*(y // self.rect_height)
        return x, y
    
    def draw_arrow(self, x0, y0, x1, y1):
        head_length = 0.5
        dx = x1 - x0
        dy = y1 - y0
        vec_ab = [dx,dy]
        vec_ab_magnitude = np.sqrt(dx**2+dy**2)
        dx = dx / vec_ab_magnitude
        dy = dy / vec_ab_magnitude
        vec_ab_magnitude = vec_ab_magnitude - head_length
        plt.arrow(x0, y0, vec_ab_magnitude*dx, vec_ab_magnitude*dy, head_width=0.1, head_length=0.5)
            
    def get_rects(self, ax):
        rects = []
        d = np.sqrt((self.rect_width)**2 + (self.rect_height)**2)
        for traj in self.trajs:
            traj_rects = []
            x_coord = self.trajs[traj]['x']
            y_coord = self.trajs[traj]['y']
            for i, j in zip(range(len(x_coord)-1), range(len(y_coord)-1)):
                x0, y0 = x_coord[i], y_coord[j]
                x1, y1 = x_coord[i+1], y_coord[j+1]
                v = np.array([x1 - x0, y1 - y0])
                v = v / np.sqrt(np.sum(v**2))
                #self.draw_arrow(x0, y0, x1, y1)
                #self.draw_arrow(x0, y0, x0+v[0], y0+v[1])
                traj_rects.append(self.get_rect(x0, y0))
                self.grid[self.get_rect(x0, y0)] = 1           
                while np.sqrt(np.sum(np.array([x1 - x0, y1 - y0])**2)) > d:
                    x0 += (self.rect_width) * v[0]
                    y0 += (self.rect_height) * v[1]
                    a = self.get_rect(x0, y0)
                    traj_rects.append(a)
                    self.grid[a] = 1 
            rects.append(traj_rects)
        self.new_coord =  np.array(rects)

                       
    def draw_trajs(self, ax):
        for traj in self.trajs:
            ax.scatter(self.trajs[traj]['x'], self.trajs[traj]['y'])
            ax.plot(self.trajs[traj]['x'], self.trajs[traj]['y'])
        
    def get_rect_center(self, i, j): 
        a, b = self.get_rect_coord(i, j)
        return a + self.rect_width / 2 , b + self.rect_height / 2
        
    def draw_grid(self, ax):
        for coord in self.new_coord:
            for rect in coord:
                    x, y = self.get_rect_coord(*rect)
                    
                    
    def traj_rects_centers(self, ax):
        colors = ['b', 'r', 'g', 'y', 'c', 'm', 'k']
        for rect in self.new_coord:
            color = np.random.choice(colors)
            colors.remove(color)
            for i in range(len(rect) -1):
                x0, y0 = self.get_rect_center(*rect[i])
                x1, y1 = self.get_rect_center(*rect[i + 1])
                ax.plot([x0, x1], [y0, y1], c=color)
                ax.scatter(x0, y0, c=color)
                ax.scatter(x1, y1, c=color)
                x, y = self.get_rect_coord(*rect[i+1])
                rect_ = patches.Rectangle((x, y), self.rect_width, self.rect_height,linewidth=2,edgecolor='red', facecolor='none')
                ax.add_patch(rect_)
                
    def draw(self):
        fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, sharex=True)
        #plt.style.use("seaborn")
        plt.rcParams["figure.figsize"] = 8, 8
        x_axis = np.linspace(self.x0, self.x1, self.n_rects)
        y_axis = np.linspace(self.y0, self.y1, self.n_rects) 
        ax2.grid(True)
        self.get_rects(ax2)
        self.traj_rects_centers(ax2)
        self.draw_trajs(ax1)
        plt.xticks(x_axis, rotation="vertical")
        plt.yticks(y_axis)
        plt.title('Clustering Trajectories')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

#Grid({1:{'x':[1, 2, 4, 5], 'y':[2,3,4,5]}})

