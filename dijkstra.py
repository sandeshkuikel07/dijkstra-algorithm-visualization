from tkinter import messagebox, Tk
import pygame
import sys

window_width = 700
window_height = 700

window = pygame.display.set_mode((window_width, window_height))

columns = 50
rows = 50

box_width = window_width // columns
box_height = window_height // rows

grid = []
queue = []
path = []


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
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width-1, box_height-1))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


# Create Grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

# Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)


def main():
    begin_search = False
    start_box_set = False
    target_box_set = False
    searching = True
    start_box = None
    target_box = None

    while True:
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Draw Wall
                if event.buttons[0] and not begin_search:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                # Set Start Box
                if event.buttons[2] and not begin_search and not start_box_set:
                    i = x // box_width
                    j = y // box_height
                    start_box = grid[i][j]
                    start_box.start = True
                    start_box_set = True
                # Set Target Box after Start Box is set
                if event.buttons[2] and not begin_search and start_box_set and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    if target_box != start_box:  # Ensure target box is not the same as the start box
                        target_box.target = True
                        target_box_set = True
            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False
                    # Return control back to the Pygame loop
                    return

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (252, 255, 233))  # FCFFE9

                if box.queued:
                    box.draw(window, (200, 0, 0))  # red
                if box.visited:
                    box.draw(window, (128, 0, 128))  # purple
                if box in path:
                    box.draw(window, (0, 0, 200))  # blue
                if box.start:
                    box.draw(window, (0, 255, 0))  # green
                if box.wall:
                    box.draw(window, (10, 10, 10))  # grey4
                if box.target:
                    box.draw(window, (255, 0, 0))  # navy blue

        pygame.display.flip()


if __name__ == "__main__":
    main()

