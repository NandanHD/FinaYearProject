Coverage Path Planning Algorithm for Robotic Automation
📌 Overview
This project implements a Coverage Path Planning (CPP) algorithm in a grid-based environment with both static and dynamic obstacles, enabling a robot to autonomously explore and cover an unknown region. The simulation is built in Python using Pygame for visualization.

The robot:

Starts at (0, 0) and must visit all reachable cells.

Avoids static and dynamic obstacles while maintaining efficient movement.

Uses a priority-based pathfinding algorithm for optimal coverage.

Updates the grid in real time, showing visited, unvisited, and retraced paths.

Applications of this algorithm include:

Autonomous cleaning robots

Lawn mowing robots

Mine-sweeping systems

Structural inspection

Precision farming

🚀 Features
Static obstacles: Fixed positions, predefined before simulation.

Dynamic obstacles: Move randomly each frame.

Priority-based pathfinding: Balances shortest distance and unexplored neighbors.

Real-time visualization with color-coded cells:

White: Unvisited

Light Green: Visited

Gray: Static obstacle

Red: Dynamic obstacle

Yellow: Retraced path

Blue: Robot position

Automatic stopping when the grid is fully explored.

🛠 Requirements
Python 3.8+ (Tested on Python 3.13)

Pygame
