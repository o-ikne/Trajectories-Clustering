![GitHub Contributors Image](https://contrib.rocks/image?repo=o-ikne/Trajectories-Clustering)
[![Generic badge](https://img.shields.io/badge/Made_With-Python-<COLOR>.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Library-pandas-red.svg)](https://shields.io/)
[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
![visitor badge](https://visitor-badge.glitch.me/badge?page_id=o-ikne.Trajectories-Clustering)

## __Trajectories-Clustering__
This project is realized as a computer science project in the Master 1 of data science at the university of Lille. 01/11/2020

### __Overview__
This repository contains :

- `trajectory_class.py` : python script for the class Trajectory.

- `grid_class.py`       : python script for the class Grid.

- `test_trajectory.py`  : python script for testing the trajectory class with the __TDD__(Test-Driven Development) method.

- `clustering trajectories.ipynb` : A jupyter notebook version of the 3 sripts above that contains all the classes (Trajectory, Grid, Test)

For the txt files used in this project they are in the "cabspottingdata" folder that is available in this link: https://drive.google.com/file/d/1VI9b0sF4Br3alozUtSsEP8tnboID0Xqc/view?usp=sharing

### __Test-Driven Development (TDD) steps__
-1. Add a new unit test
-2. Check it fails
-3. Make it pass (with the others)
-4. Refactor (if needed)
-5. Commit (& push)
-6. Go to 1.

### __TDD on Project__

Identify input/output structures
- Input: Set of trajectories
  - Classes: Trajectory, Point
- Output: Graph of paths
  - Classes: Graph, Node, Edge
Apply TDD to develop your clustering algorithm

### __Importing & plotting data__

- Download the mobility dataset from here (SF cabs)
- Use the CSV python parser to load each filcabspottingdata.tar.gze in the directory (1 file = 1 trajectory) as an input trajectory for your algorithm
- Run clustering algorithm on the loaded dataset by creating a new Application class that combines the parser with the clustering algorithm
- Plot the resulting graph using matplotlib for basic rendering of the resulting graph, or:
- Explore the effects of changing the clustering “depths” on the resulting graph
