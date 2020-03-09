import numpy as np
import random
# Grid generator
# Initial Grid
grid = []
visited = []
neighbor = []
mode = 'random'
# Change the range to change the size of the grid
gridsize = 101
for i in range(gridsize):
    grid.append([])
    for j in range(gridsize):
        grid[i].append(0)
# Create Walls for grid
# There are different modes to generate the mazes
# Walls are represented as 1
'''
Figure3 mode
Note that this mode should only run when the grid size is 5
This mode will generate a maze from the assignment 
'''
if(mode == 'figure3'):
    print(mode)
    grid[1][2] = 1
    grid[2][2] = 1
    grid[3][2] = 1
    grid[2][3] = 1
    grid[3][3] = 1
    grid[4][3] = 1
    grid[4][2] = 2
    grid[4][4] = 3
'''
Easy Mode:
Just go through the grid and set a 30% chance that a section will be blocked
This is a easy way to just to start off the project
'''
if(mode == 'random'):
    for i in range(gridsize):
        for j in range(gridsize):
            # If number is less then 30 then mark the grid space as a wall
            if(random.randint(1, 100) <= 30):
                grid[i][j] = 1
    # Set start and end point (top left -> bottom right)
    grid[0][0] = 2
    grid[gridsize-1][gridsize-1] = 3
'''
Hard Algorithm:
while(len of visited is not gridsize^2):
    check neighbor list for avaliable point
    if there is no valid point pick a random point on the grid
        check if point is in the visited list
        if the point is valid set the wall value depending on random int
        then get the neighbors
        check if neighbors are valid or already have been visited
    if there is a valid neighbor
        select one of the neighbors by random
        set wall value depending on random int
        
'''
if(mode == 'hard'):
    # start at a random point
    wallx = random.randint(0, gridsize-1)
    wally = random.randint(0, gridsize-1)
    # Add point to visited heap
    grid[wallx][wally] = 1
    visited.append((wallx, wally))
    # From this point check for valid neighbors
'''
# Random start and end point code, might not be needed
# Getting the start point of agent represented by 2
startx = random.randint(0, gridsize-1)
starty = random.randint(0, gridsize-1)
grid[startx][starty] = 2
# Getting the end point target for the agent
endx = random.randint(0, gridsize-1)
endy = random.randint(0, gridsize-1)
# Need to make sure that the end target doesn't equal the start point
# End point is represented by 3
while(endx == startx & endy == starty):
    endx = random.randint(0, gridsize-1)
    endy = random.randint(0, gridsize-1)
grid[endx][endy] = 3
'''
# Take grid and save it to a text file
'''
with open('test.txt', 'w') as filehandle:
    for x in grid:
        filehandle.write('%s\n' % x)
'''
np.savetxt('Grids/test.txt', grid, delimiter=",", newline="\n", fmt='%i')
# Print final grid to check output
for x in range(50):
    grid = []
    for i in range(gridsize):
        grid.append([])
        for j in range(gridsize):
            grid[i].append(0)
    for i in range(gridsize):
        for j in range(gridsize):
            # If number is less then 30 then mark the grid space as a wall
            if(random.randint(1, 100) <= 30):
                grid[i][j] = 1
    # Set start and end point (top left -> bottom right)
    grid[0][0] = 2
    grid[gridsize-1][gridsize-1] = 3
    filename = 'grid'+str(x)+'.txt'
    np.savetxt('Grids/'+filename, grid, delimiter=",", newline="\n", fmt='%i')
