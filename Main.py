import pygame
import FindPath
import copy
import time

# Intialize some variables
grid = []
blindgrid = []

# General Setup
grid_num = input("Enter grid number (0-49): ")
grid_file = 'grid'+str(grid_num)+'.txt'
ins = open('Grids/'+grid_file, 'r')
for line in ins:
    row = line.split(',')
    grid.append(list(map(int, line.split(','))))
gridsize = len(grid)
# Getting the start and end points of the grid
for i in range(gridsize):
    for j in range(gridsize):
        # Lets find the start point
        if grid[i][j] == 2:
            start = (i, j)
        # Lets find the end point
        if grid[i][j] == 3:
            end = (i, j)
# Set up the blind grid
for i in range(len(grid)):
    blindgrid.append([])
    for j in range(gridsize):
        blindgrid[i].append(0)
blindgrid[start[0]][start[1]] = 2
blindgrid[end[0]][end[1]] = 3
# Repeated Forward
'''
print("blind grid \t\t\tgrid")
for i in range(len(blindgrid)):
    print(str(blindgrid[i])+'\t\t\t'+str(grid[i]))
'''
# Repeated Backward
# Adaptive


# Grid output
pygame.init()
size = (5*gridsize, 5*gridsize)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Grid 1")
done = False
clock = pygame.time.Clock()
screen.fill(pygame.Color('White'))
for i in range(gridsize):
    for j in range(gridsize):
        if(grid[i][j] == 0):
            pygame.draw.rect(screen, pygame.Color(
                'White'), [j*5, i*5, 5, 5])
        elif(grid[i][j] == 2):
            pygame.draw.rect(screen, pygame.Color(
                'Blue'), [j*5, i*5, 5, 5])
        elif(grid[i][j] == 3):
            pygame.draw.rect(screen, pygame.Color(
                'Red'), [j*5, i*5, 5, 5])
        else:
            pygame.draw.rect(screen, pygame.Color(
                'Black'), [j*5, i*5, 5, 5])
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print('Repeated Backwards A*')
                backward = FindPath.Astar(grid, copy.deepcopy(
                    blindgrid), len(grid), start, end)
                t1 = time.process_time()
                rba_path = backward.RepeatedBAStar(
                    backward.start, backward.goal, screen)
                # print('Repeated Back A*: {}'.format(rba_path))
                if rba_path != False:
                    print('length: {}'.format(len(rba_path)))
                else:
                    print('There is no path!')
                print('Time: {}'.format(time.process_time() - t1))
                # print(backward.counter)
            if event.key == pygame.K_RIGHT:
                print('Repeated Foward A*')
                forward = FindPath.Astar(grid, copy.deepcopy(
                    blindgrid), len(grid), start, end)
                t0 = time.process_time()
                rfa_path = forward.RepeatedFAStar(
                    forward.start, forward.goal, screen)
                # print('Repeated Forward A*: {}'.format(rfa_path))
                if rfa_path != False:
                    print('length: {}'.format(len(rfa_path)))
                else:
                    print('There is no path!')
                print('Time: {}'.format(time.process_time() - t0))
                # print(forward.counter)
            if event.key == pygame.K_UP:
                print('Adaptive A*')
                adaptive = FindPath.Astar(grid, copy.deepcopy(
                    blindgrid), len(grid), start, end)
                t2 = time.process_time()
                adp_path = adaptive.AdaptiveAStar(
                    adaptive.start, adaptive.goal, screen)
                # print('Adaptive A*: {}'.format(adp_path))
                if adp_path != False:
                    print('length: {}'.format(len(adp_path)))
                else:
                    print('There is no path!')
                print('Time: {}'.format(time.process_time() - t2))
                # print(adaptive.counter)
            if event.key == pygame.K_DOWN:
                for i in range(gridsize):
                    for j in range(gridsize):
                        if(grid[i][j] == 0):
                            pygame.draw.rect(screen, pygame.Color(
                                'White'), [j*5, i*5, 5, 5])
                        elif(grid[i][j] == 2):
                            pygame.draw.rect(screen, pygame.Color(
                                'Blue'), [j*5, i*5, 5, 5])
                        elif(grid[i][j] == 3):
                            pygame.draw.rect(screen, pygame.Color(
                                'Red'), [j*5, i*5, 5, 5])
                        else:
                            pygame.draw.rect(screen, pygame.Color(
                                'Black'), [j*5, i*5, 5, 5])
    pygame.display.flip()
# Close the window and quit.
pygame.quit()
