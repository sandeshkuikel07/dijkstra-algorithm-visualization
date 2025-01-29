from tkinter import messagebox, Tk
import pygame
import sys
import math
from collections import deque

# Window settings
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
COLUMNS = 8
ROWS = 8
BOX_WIDTH = WINDOW_WIDTH // COLUMNS
BOX_HEIGHT = WINDOW_HEIGHT // ROWS
NODE_RADIUS = BOX_WIDTH // 3  # Increased node size

# Colors
BLACK = (0, 0, 0)
WHITE = (252, 255, 233)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)  # Changed path color
GREEN = (0, 255, 0)
PINK= (255, 105, 180)  # Changed target color

class Node:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.x = i * BOX_WIDTH + BOX_WIDTH // 2
        self.y = j * BOX_HEIGHT + BOX_HEIGHT // 2
        self.start = False
        self.target = False
        self.visited = False
        self.queued = False
        self.prior = None
        self.neighbors = {}

    def set_neighbors(self, grid):
        directions = {
            'right': (1, 0),
            'down': (0, 1),
            'left': (-1, 0),
            'up': (0, -1)
        }
        for direction, (dx, dy) in directions.items():
            new_i = self.i + dx
            new_j = self.j + dy
            if 0 <= new_i < COLUMNS and 0 <= new_j < ROWS:
                neighbor = grid[new_i][new_j]
                self.neighbors[direction] = {'node': neighbor, 'blocked': False}

def create_grid():
    grid = []
    for i in range(COLUMNS):
        row = []
        for j in range(ROWS):
            node = Node(i, j)
            row.append(node)
        grid.append(row)
    for i in range(COLUMNS):
        for j in range(ROWS):
            grid[i][j].set_neighbors(grid)
    return grid

def distance_point_to_segment(px, py, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx*dx + dy*dy)
    t = max(0, min(1, t))
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    return math.hypot(px - closest_x, py - closest_y)

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer")
    
    grid = create_grid()
    queue = deque()
    path = []
    
    begin_search = False
    start_node_set = False
    target_node_set = False
    searching = False
    start_node = None
    target_node = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not begin_search:
                if event.button == 3:  # Right click to set start/target
                    x, y = pygame.mouse.get_pos()
                    for i in range(COLUMNS):
                        for j in range(ROWS):
                            node = grid[i][j]
                            dx = x - node.x
                            dy = y - node.y
                            if dx**2 + dy**2 <= NODE_RADIUS**2:
                                if not start_node_set:
                                    if node.target:
                                        continue
                                    if start_node:
                                        start_node.start = False
                                    node.start = True
                                    start_node = node
                                    start_node_set = True
                                elif not target_node_set and not node.start:
                                    if target_node:
                                        target_node.target = False
                                    node.target = True
                                    target_node = node
                                    target_node_set = True
                                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_node_set and target_node_set and not begin_search:
                    begin_search = True
                    searching = True
                    queue.append(start_node)
                    start_node.queued = True
                elif event.key == pygame.K_r:
                    grid = create_grid()
                    queue = deque()
                    path = []
                    begin_search = False
                    start_node_set = False
                    target_node_set = False
                    searching = False
                    start_node = None
                    target_node = None

        # Handle edge blocking with mouse drag
        if not begin_search and pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            min_dist = 5
            edge_to_block = None
            
            for i in range(COLUMNS):
                for j in range(ROWS):
                    node = grid[i][j]
                    if 'right' in node.neighbors:
                        neighbor = node.neighbors['right']['node']
                        dist = distance_point_to_segment(x, y, node.x, node.y, neighbor.x, neighbor.y)
                        if dist < min_dist:
                            edge_to_block = (node, 'right', neighbor, 'left')
                            min_dist = dist
                    if 'down' in node.neighbors:
                        neighbor = node.neighbors['down']['node']
                        dist = distance_point_to_segment(x, y, node.x, node.y, neighbor.x, neighbor.y)
                        if dist < min_dist:
                            edge_to_block = (node, 'down', neighbor, 'up')
                            min_dist = dist
            
            if edge_to_block:
                node, dir1, neighbor, dir2 = edge_to_block
                if not node.neighbors[dir1]['blocked']:
                    node.neighbors[dir1]['blocked'] = True
                    neighbor.neighbors[dir2]['blocked'] = True

        if begin_search and searching:
            if queue:
                current_node = queue.popleft()
                current_node.visited = True

                if current_node == target_node:
                    searching = False
                    path.clear()
                    current = current_node
                    while current.prior is not None:
                        path.append(current)
                        current = current.prior
                    path.append(start_node)
                    path.reverse()
                else:
                    for direction in current_node.neighbors:
                        neighbor_info = current_node.neighbors[direction]
                        neighbor_node = neighbor_info['node']
                        is_blocked = neighbor_info['blocked']
                        if not is_blocked and not neighbor_node.visited and not neighbor_node.queued:
                            neighbor_node.queued = True
                            neighbor_node.prior = current_node
                            queue.append(neighbor_node)
            elif searching:
                searching = False
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There is no solution!")

        window.fill(WHITE)

        # Draw edges
        for i in range(COLUMNS):
            for j in range(ROWS):
                node = grid[i][j]
                if 'right' in node.neighbors:
                    neighbor = node.neighbors['right']['node']
                    blocked = node.neighbors['right']['blocked']
                    color = WHITE if blocked else BLACK
                    pygame.draw.line(window, color, (node.x, node.y), (neighbor.x, neighbor.y), 2)
                if 'down' in node.neighbors:
                    neighbor = node.neighbors['down']['node']
                    blocked = node.neighbors['down']['blocked']
                    color = WHITE if blocked else BLACK
                    pygame.draw.line(window, color, (node.x, node.y), (neighbor.x, neighbor.y), 2)

        # Draw nodes
        for i in range(COLUMNS):
            for j in range(ROWS):
                node = grid[i][j]
                color = BLACK
                if node.start:
                    color = GREEN
                elif node.target:
                    color = PURPLE
                elif node.visited:
                    color = RED
                elif node.queued:
                    color = PURPLE
                pygame.draw.circle(window, color, (node.x, node.y), NODE_RADIUS)

        # Draw path in yellow
        if path:
            for i in range(len(path)-1):
                start = path[i]
                end = path[i+1]
                pygame.draw.line(window, BLUE, (start.x, start.y), (end.x, end.y), 5)

        pygame.display.flip()

if __name__ == "__main__":
    main()