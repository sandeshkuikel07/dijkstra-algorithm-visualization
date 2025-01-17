from tkinter import messagebox, Tk
import pygame
import sys
from collections import deque  # More efficient than list for queue operations

# Window settings
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
COLUMNS = 50
ROWS = 50
BOX_WIDTH = WINDOW_WIDTH // COLUMNS
BOX_HEIGHT = WINDOW_HEIGHT // ROWS

# Colors
BLACK = (0, 0, 0)
WHITE = (252, 255, 233)
PURPLE = (128, 0, 128)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GREEN = (0, 255, 0)
WALL_COLOR = (10, 10, 10)
TARGET_COLOR = (255, 0, 0)

class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * BOX_WIDTH, self.y * BOX_HEIGHT, BOX_WIDTH-1, BOX_HEIGHT-1))

    def set_neighbours(self, grid):
        self.neighbours = []
        # Check all four directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < COLUMNS and 0 <= new_y < ROWS:
                self.neighbours.append(grid[new_x][new_y])

def create_grid():
    return [[Box(i, j) for j in range(ROWS)] for i in range(COLUMNS)]

def reset_path(grid, queue, path):
    for i in range(COLUMNS):
        for j in range(ROWS):
            box = grid[i][j]
            if not (box.start or box.wall or box.target):
                box.queued = False
                box.visited = False
                box.prior = None
    queue.clear()
    path.clear()

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer")
    
    grid = create_grid()
    # Set neighbours for all boxes
    for i in range(COLUMNS):
        for j in range(ROWS):
            grid[i][j].set_neighbours(grid)

    queue = deque()  # Use deque instead of list for better performance
    path = []
    
    begin_search = False
    start_box_set = False
    target_box_set = False
    searching = False
    start_box = None
    target_box = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                i = x // BOX_WIDTH
                j = y // BOX_HEIGHT
                
                # Left click to draw walls
                if event.button == 1 and not begin_search:
                    if not (grid[i][j].start or grid[i][j].target):
                        grid[i][j].wall = not grid[i][j].wall  # Toggle wall

                # Right click to set start and target
                elif event.button == 3 and not begin_search:
                    if not start_box_set:
                        start_box = grid[i][j]
                        start_box.start = True
                        start_box_set = True
                    elif not target_box_set and not grid[i][j].start:
                        target_box = grid[i][j]
                        target_box.target = True
                        target_box_set = True

            # Press SPACE to start search
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_box_set and target_box_set and not begin_search:
                    begin_search = True
                    searching = True
                    queue.append(start_box)
                    start_box.queued = True
                # Press 'R' to reset
                elif event.key == pygame.K_r:
                    grid = create_grid()
                    for i in range(COLUMNS):
                        for j in range(ROWS):
                            grid[i][j].set_neighbours(grid)
                    queue.clear()
                    path.clear()
                    begin_search = False
                    start_box_set = False
                    target_box_set = False
                    searching = False
                    start_box = None
                    target_box = None

        if begin_search and searching:
            if queue:
                current_box = queue.popleft()  # Use popleft() for deque
                current_box.visited = True

                if current_box == target_box:
                    searching = False
                    current = current_box
                    while current.prior != None:
                        path.append(current.prior)
                        current = current.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall and not neighbour.visited:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            elif searching:
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There is no solution!")
                searching = False

        # Draw grid
        window.fill(BLACK)
        for i in range(COLUMNS):
            for j in range(ROWS):
                box = grid[i][j]
                color = WHITE
                
                if box.queued:
                    color = PURPLE
                if box.visited:
                    color = RED
                if box in path:
                    color = BLUE
                if box.start:
                    color = GREEN
                if box.wall:
                    color = WALL_COLOR
                if box.target:
                    color = TARGET_COLOR
                
                box.draw(window, color)

        pygame.display.flip()

if __name__ == "__main__":
    main()

