'''
Class that contains functions that take care of the A* part of the program
A* Versions:
TODO: Repeated Foward A*, Repeated Backward A*, and Adaptive A*
'''
import heapq
import pygame


class Astar:

    # Initalize the properties of the Astar object
    def __init__(self, grid, blindgrid, gridsize, start_point, goal_point):
        self.grid = grid
        self.blindgrid = blindgrid
        self.gridsize = len(self.grid)
        self.start = start_point
        self.goal = goal_point
        self.counter = 0

    # Heuristic calculation (Manhatten distance)
    def man_dist(self, start, goal):
        x = abs(start[0] - goal[0])
        y = abs(start[1] - goal[1])
        return x + y

    def new_heuristic(self, old_g_score, g_goal):
        # print('original g_score list: {}'.format(old_g_score))
        # print('g_goal: {}'.format(g_goal))
        for key, value in old_g_score.items():
            old_g_score[key] = g_goal - value
        # print('new g_score list: {}'.format(old_g_score))
        # This is the updated g_score list to be used for the heuristic
        return old_g_score

    # Get the neighboring spots around a specific point
    # Returns list of VALID neighbor coords
    def get_neighbors(self, point, grid):
        # This is the position of each neighbor around
        neighbors = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        valid_neighbors = []
        point = point
        # Checking if potential neighbor is a walkable block
        for i, j in neighbors:
            potential_neighbor = point[0] + i, point[1] + j
            if 0 <= potential_neighbor[0] < len(grid):
                if 0 <= potential_neighbor[1] < len(grid):
                    if grid[potential_neighbor[0]][potential_neighbor[1]] != 1:
                        valid_neighbors.append(potential_neighbor)
        return valid_neighbors

    # Updates the blind grid, basically this is the memory of the agent, if there is a new wall that the agent encounters
    # Returns if the blind grid was updated or not NOTE: might not be needed
    def update_blindgrid(self, point):
        updated = False
        neighbors = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        valid_neighbors = []
        point = point
        # Checking if potential neighbor is a walkable block
        for i, j in neighbors:
            potential_neighbor = point[0] + i, point[1] + j
            if 0 <= potential_neighbor[0] < self.gridsize:
                if 0 <= potential_neighbor[1] < self.gridsize:
                    # Found a new wall so we update the blind grid and made sure this is a new wall
                    if self.grid[potential_neighbor[0]][potential_neighbor[1]] == 1 and self.blindgrid[potential_neighbor[0]][potential_neighbor[1]] != 1:
                        self.blindgrid[potential_neighbor[0]
                                       ][potential_neighbor[1]] = 1
                        updated = True
                        '''
                        print('new blind grid')
                        for i in range(len(self.blindgrid)):
                            print(self.blindgrid[i])
                        '''
        return updated

    # Implementation of regular A* algorithm
    # Return either the shorted path from a point to the goal of the grid or False if there is a dead end
    def RegAStar(self, start, goal, gridspace, screen):
        # List of spots that are open
        openList = []
        # List of nodes that have been visited
        closedList = []
        from_path = {}
        # g_score is given the starting node and since its also the current node the distance is 0
        g_score = {start: 0}
        # total tracel score starts at 0
        f_score = {start: self.man_dist(start, goal)}
        # We are pusing the following:
        #   (openList, (fscore[(0,0)], (0,0))
        heapq.heappush(openList, (f_score[start], g_score[start], start))
        # While there is an item in the open list
        while openList:
            # Set the current node we are looking at to the first node in the minheap
            # Thanks to using min heap the value we put into the heap will be the lowest f value
            # this way we don't have to take care of looking at the f values since the lowest one will be popped first
            # We will have to still look at if the g(h) value will be larger or smaller for tie breaker though
            curr = heapq.heappop(openList)[2]
            # print(curr)
            # Check if current node is the goal and if so we made it!
            if curr == goal:
                path = []
                # Create the path that was traveled to the goal to be returned for the next iteration of A*
                while curr in from_path:
                    path.append(curr)
                    curr = from_path[curr]
                # Now that we have the list we have to reverse it to get the correct order
                path = path[::-1]
                '''
                for i, j in path:
                    pygame.draw.rect(screen, pygame.Color(
                        'Yellow'), [j*5, i*5, 5, 5])
                '''
                return path
            # we have to keep searching for the end!
            closedList.append(curr)
            neighbors = self.get_neighbors(curr, gridspace)
            for neighbor in neighbors:
                curr_g_score = g_score[curr] + self.man_dist(curr, neighbor)
                if neighbor in closedList:
                    continue
                if neighbor not in [i[2] for i in openList]:
                    from_path[neighbor] = curr
                    g_score[neighbor] = curr_g_score
                    f_score[neighbor] = g_score[neighbor] + \
                        self.man_dist(neighbor, goal)
                    # counts the number of cells travled by the algorithm
                    self.counter += 1
                    # If we want to change the tie break we can just change the g_score to be negative
                    # NOTE That this will not change the actual gscore dictionary, its only use is to make sure that
                    # the larger g_score takes priority if that is the requested tiebreaking method
                    # negative = larger g_score wins
                    # nonnegative = smaller g_score wins
                    heapq.heappush(
                        openList, (f_score[neighbor], -g_score[neighbor], neighbor))

        return False

    # A* search that works with Adaptive A star, same as previous version except now returns and takes in g-score lists
    def RegAStar2(self, start, goal, gridspace, screen, old_g_score=None):
        # print(old_g_score)
        # List of spots that are open
        openList = []
        # List of nodes that have been visited
        closedList = []
        from_path = {}
        # g_score is given the starting node and since its also the current node the distance is 0
        g_score = {start: 0}
        # total tracel score starts at 0
        f_score = {start: self.man_dist(start, goal)}
        # We are pusing the following:
        #   (openList, (fscore[(0,0)], (0,0))
        heapq.heappush(openList, (f_score[start], g_score[start], start))
        # While there is an item in the open list
        while openList:
            # Set the current node we are looking at to the first node in the minheap
            # Thanks to using min heap the value we put into the heap will be the lowest f value
            # this way we don't have to take care of looking at the f values since the lowest one will be popped first
            # We will have to still look at if the g(h) value will be larger or smaller for tie breaker though
            curr = heapq.heappop(openList)[2]
            # print(curr)
            # Check if current node is the goal and if so we made it!
            if curr == goal:
                path = []
                # Create the path that was traveled to the goal to be returned for the next iteration of A*
                while curr in from_path:
                    path.append(curr)
                    curr = from_path[curr]
                # Now that we have the list we have to reverse it to get the correct order
                path = path[::-1]
                # print(g_score)
                '''
                for i, j in path:
                    pygame.draw.rect(screen, pygame.Color(
                        'Yellow'), [j*5, i*5, 5, 5])
                '''
                return (path, g_score)
            # we have to keep searching for the end!
            closedList.append(curr)
            neighbors = []
            neighbors = self.get_neighbors(curr, gridspace)
            for neighbor in neighbors:
                curr_g_score = g_score[curr] + self.man_dist(curr, neighbor)
                if neighbor in closedList:
                    continue
                if neighbor not in [i[2] for i in openList]:
                    self.counter += 1
                    # If the neightbor node is in the heuristic list
                    if neighbor in old_g_score:
                        # This emulates the tree pointer from the assignment where the neighbor will give the value of curr, its parent
                        from_path[neighbor] = curr
                        g_score[neighbor] = curr_g_score
                        f_score[neighbor] = g_score[neighbor] + \
                            old_g_score[neighbor]
                    else:
                        from_path[neighbor] = curr
                        g_score[neighbor] = curr_g_score
                        f_score[neighbor] = g_score[neighbor] + \
                            self.man_dist(neighbor, goal)
                    # If we want to change the tie break we can just change the g_score to be negative
                    # NOTE That this will not change the actual gscore dictionary, its only use is to make sure that
                    # the larger g_score takes priority if that is the requested tiebreaking method
                    # negative = larger g_score wins
                    # nonnegative = smaller g_score wins
                    heapq.heappush(
                        openList, (f_score[neighbor], -g_score[neighbor], neighbor))

        return (False, {})

    # Repeated Forward A star implementation
    def RepeatedFAStar(self, start, goal, screen):
        final_path = []
        path = []
        deadend = False
        self.counter = 0
        # First lets check if there is anything around the starting point
        self.update_blindgrid(start)
        # The first move of the agent
        path = self.RegAStar(start, goal, self.blindgrid, screen)
        # If the first move is blocked off
        if path == False:
            return False
        else:
            while path[0] != goal:
                # print(path[0])
                pygame.event.get()
                final_path.append(path[0])
                result = self.update_blindgrid(path[0])
                if result == True:
                    path = self.RegAStar(path[0], goal, self.blindgrid, screen)
                else:
                    path.pop(0)
                if path == False:
                    deadend = True
                    break
            # If there was deadend somewhere in the grid
            if(deadend == True):
                return False
            # Yay we made it to the goal
            else:
                for i, j in final_path:
                    pygame.draw.rect(screen, pygame.Color(
                        'Yellow'), [j*5, i*5, 5, 5])
                return final_path

    # Repeated Backward A star implementation
    def RepeatedBAStar(self, start, goal, screen):
        final_path = []
        path = []
        deadend = False
        self.counter = 0
        # First lets check if there is anything around the starting point
        self.update_blindgrid(start)
        # The first move of the agent
        path = self.RegAStar(goal, start, self.blindgrid, screen)
        # If the first move is blocked off
        if path == False:
            return False
        else:
            path = path[::-1]
            path.pop(0)
            while path[0] != goal:
                pygame.event.get()
                final_path.append(path[0])
                result = self.update_blindgrid(path[0])
                if result == True:
                    path = self.RegAStar(goal, path[0], self.blindgrid, screen)
                    if path == False:
                        deadend = True
                        break
                    else:
                        path = path[::-1]
                        path.pop(0)
                        if len(path) == 0:
                            for i, j in final_path:
                                pygame.draw.rect(screen, pygame.Color(
                                    'Yellow'), [j*5, i*5, 5, 5])
                            return final_path
                else:
                    path.pop(0)
                    if len(path) == 0:
                        for i, j in final_path:
                            pygame.draw.rect(screen, pygame.Color(
                                'Yellow'), [j*5, i*5, 5, 5])
                        return final_path
                if path == False:
                    deadend = True
                    break
            # If there was deadend somewhere in the grid
            if(deadend == True):
                return False
            # Yay we made it to the goal
            else:
                for i, j in final_path:
                    pygame.draw.rect(screen, pygame.Color(
                        'Yellow'), [j*5, i*5, 5, 5])
                return final_path

    def AdaptiveAStar(self, start, goal, screen):
        final_path = []
        path = []
        deadend = False
        self.counter = 0
        # First lets check if there is anything around the starting point
        self.update_blindgrid(start)
        # The first move of the agent
        path, g_score_list = self.RegAStar2(
            start, goal, self.blindgrid, screen, {})
        # If the first move is blocked off
        if path == False:
            return False
        else:
            heuristic_list = self.new_heuristic(g_score_list, len(path))
            while path[0] != goal:
                # print(heuristic_list)
                pygame.event.get()
                final_path.append(path[0])
                result = self.update_blindgrid(path[0])
                if result == True:
                    path, g_score_list = self.RegAStar2(
                        path[0], goal, self.blindgrid, screen, heuristic_list)
                    if(path == False):
                        deadend = True
                        break
                    else:
                        heuristic_list = self.new_heuristic(
                            g_score_list, len(path))

                else:
                    path.pop(0)
                if path == False:
                    deadend = True
                    break
            # If there was deadend somewhere in the grid
            if(deadend == True):
                return False
            # Yay we made it to the goal
            else:
                for i, j in final_path:
                    pygame.draw.rect(screen, pygame.Color(
                        'Yellow'), [j*5, i*5, 5, 5])
                return final_path
