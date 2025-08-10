import pygame
import random
import heapq

class RobotNavigation:
    def __init__(self, width, height, obstacles):
        """
        Initialize grid environment with efficient navigation
        """
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        
        # Cell states
        self.UNVISITED = 0
        self.VISITED = 1
        self.OBSTACLE = 2
        self.ROBOT = 3
        self.RETRACED_PATH = 4
        self.DYNAMIC_OBSTACLE = 5
        
        # Robot navigation parameters
        self.robot_pos = [0, 0]
        self.visited_cells = set([(0, 0)])
        self.unvisited_cells = set((x, y) for x in range(width) 
                                   for y in range(height) 
                                   if (x, y) != (0, 0))
        
        # Place static obstacles
        for x, y in obstacles:
            self.grid[y][x] = self.OBSTACLE
            if (x, y) in self.unvisited_cells:
                self.unvisited_cells.remove((x, y))
        
        # Place dynamic obstacles
        self.dynamic_obstacles = []
        for _ in range(3):  # Add 3 dynamic obstacles
            while True:
                obstacle = [random.randint(0, width - 1), random.randint(0, height - 1)]
                if self.grid[obstacle[1]][obstacle[0]] == self.UNVISITED:
                    self.grid[obstacle[1]][obstacle[0]] = self.DYNAMIC_OBSTACLE
                    self.dynamic_obstacles.append(obstacle)
                    break
        
        # Mark initial robot position
        self.grid[0][0] = self.ROBOT
    
    def move_dynamic_obstacles(self):
        """
        Move the dynamic obstacles randomly
        """
        for i, obstacle in enumerate(self.dynamic_obstacles):
            x, y = obstacle
            self.grid[y][x] = self.UNVISITED  # Clear current position
            
            # Choose a random valid direction
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < self.width and 
                    0 <= new_y < self.height and 
                    self.grid[new_y][new_x] in [self.UNVISITED, self.VISITED]):
                    self.dynamic_obstacles[i] = [new_x, new_y]
                    self.grid[new_y][new_x] = self.DYNAMIC_OBSTACLE
                    break
    
    def find_most_efficient_path(self):
        """
        Find the most efficient path to an unvisited cell
        """
        start = tuple(self.robot_pos)
        
        # Priority queue for efficient path finding
        open_set = []
        heapq.heappush(open_set, (0, start, []))
        visited = set([start])
        
        while open_set:
            priority, current, path = heapq.heappop(open_set)
            
            # Check neighboring cells for unvisited cells
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                # Check grid boundaries and obstacles
                if (0 <= neighbor[0] < self.width and 
                    0 <= neighbor[1] < self.height and 
                    self.grid[neighbor[1]][neighbor[0]] not in [self.OBSTACLE, self.DYNAMIC_OBSTACLE] and
                    neighbor not in visited):
                    
                    new_path = path + [neighbor]
                    
                    # If unvisited cell found, return path
                    if neighbor in self.unvisited_cells:
                        return new_path
                    
                    # Add to exploration queue
                    visited.add(neighbor)
                    
                    # Priority based on distance and unexplored neighbors
                    unexplored_neighbors = sum(
                        1 for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                        if (0 <= neighbor[0]+dx < self.width and 
                            0 <= neighbor[1]+dy < self.height and 
                            self.grid[neighbor[1]+dy][neighbor[0]+dx] == self.UNVISITED)
                    )
                    
                    priority = len(new_path) - unexplored_neighbors
                    heapq.heappush(open_set, (priority, neighbor, new_path))
        
        return None
    
    def move_robot(self, path):
        """
        Move robot along the calculated path
        """
        if not path:
            return False
        
        # Retrace path coloring
        for x, y in path[:-1]:
            if self.grid[y][x] == self.VISITED:
                self.grid[y][x] = self.RETRACED_PATH
        
        # Move to final cell
        x, y = path[-1]
        
        # Update grid
        self.grid[self.robot_pos[1]][self.robot_pos[0]] = self.VISITED
        self.grid[y][x] = self.ROBOT
        
        # Update robot position
        self.robot_pos = [x, y]
        
        # Update visited and unvisited cells
        if (x, y) in self.unvisited_cells:
            self.unvisited_cells.remove((x, y))
        self.visited_cells.add((x, y))
        
        return True
    
    def is_exploration_complete(self):
        """
        Check if entire grid is explored
        """
        return len(self.unvisited_cells) == 0 and all(
            cell != self.UNVISITED for row in self.grid for cell in row
        )

class GridVisualization:
    def __init__(self, width, height):
        """
        Initialize Pygame visualization
        """
        pygame.init()
        
        # Dynamic cell sizing
        self.CELL_SIZE = max(20, min(800 // max(width, height), 40))
        self.SCREEN_WIDTH = width * self.CELL_SIZE
        self.SCREEN_HEIGHT = height * self.CELL_SIZE
        
        # Colors
        self.COLORS = {
            0: (255, 255, 255),  # Unvisited - White
            1: (200, 255, 200),  # Visited - Light Green
            2: (100, 100, 100),  # Obstacle - Dark Gray
            3: (0, 0, 255),      # Robot - Blue
            4: (255, 255, 0),    # Retraced Path - Yellow
            5: (255, 0, 0)       # Dynamic Obstacle - Red
        }
        
        # Create screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Efficient Robot Grid Navigation')
    
    def draw_grid(self, robot_nav):
        """
        Render grid state
        """
        for y in range(robot_nav.height):
            for x in range(robot_nav.width):
                rect = pygame.Rect(
                    x * self.CELL_SIZE, 
                    y * self.CELL_SIZE, 
                    self.CELL_SIZE, 
                    self.CELL_SIZE
                )
                pygame.draw.rect(
                    self.screen, 
                    self.COLORS[robot_nav.grid[y][x]], 
                    rect
                )
                pygame.draw.rect(
                    self.screen, 
                    (0, 0, 0), 
                    rect, 
                    1
                )

def run_simulation(width, height, obstacles):
    """
    Main simulation runner
    """
    # Initialize components
    robot_nav = RobotNavigation(width, height, obstacles)
    visualization = GridVisualization(width, height)
    
    # Pygame setup
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Move dynamic obstacles
        robot_nav.move_dynamic_obstacles()
        
        # Find most efficient path to unvisited cell
        path = robot_nav.find_most_efficient_path()
        
        # Move robot
        if path:
            robot_nav.move_robot(path)
        
        # Check exploration completion
        if robot_nav.is_exploration_complete():
            print("Grid fully explored!")
            break
        
        # Visualize grid
        visualization.screen.fill((255, 255, 255))
        visualization.draw_grid(robot_nav)
        pygame.display.flip()
        
        # Control simulation speed
        clock.tick(2.5)
    
    # Keep window open until closed
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    
    pygame.quit()

def main():
    width = 10
    height = 10
    obstacles = [(2, 2), (3, 4), (7, 7)]  # Static obstacles
    run_simulation(width, height, obstacles)

if __name__ == "__main__":
    main()
