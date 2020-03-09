Assignment 1 README for CS440
Things needed to run:
-Python 3.7.1
-install pygame module for python (used for visualizing the gridworld, the final path, and adding user keyboard button input)
	-pip install pygame
	-https://www.pygame.org/wiki/GettingStarted

Included Python files:
GridBuilder.py:
-Python script used to generate 50 gridworlds (0-49), there is already 50 worlds included with this submission
FindPath.py
-Used to store the AStar class and handles the operations behind A* and its many variations
Main.py
-The file that is actually used to run the project

How to use Main.py
-When first opening up Main.py enter the gridworld number into the console
-once the pygame board pops up the user is free to use the arrow keys to execute each version of A*:
	-Left == Repeated Backwards A*
	-Right == Repeated Forwards A*
	-Up == Adaptive A*
	-Down == Clear board

Quick Notes about the Program:
-Once each run is complete the information on the console will return the length of the path and the time spent processing
-The program by default is in favor of larger g-value tiebreaker. If you want to change this you can go to the line 133 to change tie-breaking for Forward and Backward and to line 204 for Adaptive in the FindPath.py file. Further instructions are in the comments above those lines.
-Once an A* search is complete please clear the board in order to clearly see the next version of A* called
-Please only click the arrow keys once and allow the program to finish running before touching the other arrow keys
-If pygame window shows not responding that is not the program crashing as the operations are just taking a longer time. For me the runtime was at max 1.5min and averaged 10-30sec for backwards and adaptive