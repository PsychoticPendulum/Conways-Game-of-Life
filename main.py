import pygame
import random

# Initialize pygame
pygame.init()
screen_size = [1600, 900]
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
clock = pygame.time.Clock()
pygame.display.set_caption("Game of Life")
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)


# Class for Game Variables
class Game:
    running = True
    paused = False
    speed = 15  # Frame rate of the game


# Class for Cursor Variables
class Cursor:
    x = 0
    y = 0
    click = False
    rect = pygame.Rect(x, y, 4, 4)


# Class for game settings
# Be sure that size is evenly divisible by screen_size[0] and screen_size[1] to avoid graphics glitches
class Grid:
    size = 100
    total = size * size
    res = screen_size[0] / size


class Cell:
    id = 0
    x = 0
    y = 0
    active = False


class Colors:
    r = 255
    g = 0
    b = 0
    v = 1


class Cell:
    id = 0
    x = 0
    y = 0
    w = Grid.res
    neighbours = 0
    active = False
    rect = pygame.Rect(x, y, w, w)


def create_grid():
    grid_array = []
    id = 0
    for i in range(Grid.size):
        for j in range(Grid.size):
            grid_array.append(Cell())
            grid_array[id].x = j * Grid.res
            grid_array[id].y = i * Grid.res
            grid_array[id].id = id
            id += 1
    return grid_array


cell_array = [create_grid(), create_grid()]
# Create two grids, one to be drawn and one to put in the old grid
# cell_array[0] will be drawn
# cell_array[1] will be the one to calculate on


def update_cursor_pos():
    Cursor.x, Cursor.y = pygame.mouse.get_pos()
    Cursor.rect = pygame.Rect(Cursor.x, Cursor.y, 1, 1)


# Draw Functions
def draw_box(x, y, w, h, c, o):
    if o:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, w, h))
    pygame.draw.rect(screen, c, pygame.Rect(x+1, y+1, w-2, h-2))


# Loop through different colors
def rainbow():
    if Colors.r == 255 and Colors.b == 0:
        Colors.g += Colors.v
    if Colors.g == 255 and Colors.r > 0:
        Colors.r -= Colors.v
    if Colors.g == 255 and Colors.r == 0:
        Colors.b += Colors.v
    if Colors.b == 255 and Colors.g > 0:
        Colors.g -= Colors.v
    if Colors.b == 255 and Colors.g == 0:
        Colors.r += Colors.v
    if Colors.r == 255 and Colors.b > 0:
        Colors.b -= Colors.v


# Draw a pause button
def paused():
    if Game.paused:
        draw_box(screen_size[0] / 2 - 20, screen_size[1] / 2 - 25, 15, 50, (194, 194, 194), True)
        draw_box(screen_size[0] / 2 + 5, screen_size[1] / 2 - 25, 15, 50, (194, 194, 194), True)


# Set all cells to inactive (Press c on keyboard)
def clear():
    for i in range(2):
        for cell in cell_array[i]:
            cell.active = False


# Set all cells randomly and enjoy the view (Press s on keyboard)
def randomize():
    clear()
    for cell in cell_array[0]:
        cell.active = random.randint(0, 1)


# Handle all the user input, keyboard or mouse
def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not Game.paused:
                    Game.paused = True
                else:
                    Game.paused = False
            if event.key == pygame.K_s:
                randomize()
            if event.key == pygame.K_c:
                clear()
        if event.type == pygame.MOUSEBUTTONDOWN:
            Cursor.click = True
        if event.type == pygame.MOUSEBUTTONUP:
            Cursor.click = False


# Actually draw all the cells
def render_field(x, y, active):
    c = [0, 0, 0]
    if active:
        c[0] = Colors.r
        c[1] = Colors.g
        c[2] = Colors.b
    else:
        c = [32, 32, 32]
    draw_box(x, y, Grid.res, Grid.res, c, True)


# Flush neighbours from last frame
def flush_neighbours():
    for i in range(2):
        for cell in cell_array[0]:
            cell.neighbours = 0


# Get current neighbours from background grid
def get_neighbours():
    for cell in cell_array[0]:
        # Getting the amount of active neighbours a cell has
        # Check that neighbour cell is actually a cell and not out of array
        if cell.id - 1 >= 0:
            if cell_array[1][cell.id - 1].active:
                cell.neighbours += 1
        if cell.id + 1 < Grid.total:
            if cell_array[1][cell.id + 1].active:
                cell.neighbours += 1
        if cell.id - Grid.size >= 0:
            if cell_array[1][cell.id - Grid.size].active:
                cell.neighbours += 1
        if cell.id + Grid.size < Grid.total:
            if cell_array[1][cell.id + Grid.size].active:
                cell.neighbours += 1
        if cell.id - Grid.size - 1 >= 0:
            if cell_array[1][cell.id - Grid.size - 1].active:
                cell.neighbours += 1
        if cell.id - Grid.size + 1 >= 0:
            if cell_array[1][cell.id - Grid.size + 1].active:
                cell.neighbours += 1
        if cell.id + Grid.size - 1 < Grid.total:
            if cell_array[1][cell.id + Grid.size - 1].active:
                cell.neighbours += 1
        if cell.id + Grid.size + 1 < Grid.total:
            if cell_array[1][cell.id + Grid.size + 1].active:
                cell.neighbours += 1


# Copy current grid to background grid
def copy_grid():
    for cell in cell_array[0]:
        cell_array[1][cell.id].active = cell.active


# Render main function
def render():
    # Loop through all cells and draw them
    for cell in cell_array[0]:
        render_field(cell.x, cell.y, cell.active)

    paused()


# Update main function
def update():
    update_cursor_pos()
    rainbow()

    copy_grid()
    flush_neighbours()
    get_neighbours()

    # Loop through all cells
    for cell in cell_array[0]:
        # Create a rect for each cell and check for collision with cursor
        cell.rect = pygame.Rect(cell.x, cell.y, cell.w, cell.w)
        if cell.rect.colliderect(Cursor.rect) and Cursor.click:
            cell.active = True

        if not Game.paused:
            # Implement reproduction logic
            if cell.neighbours < 2:
                cell.active = False
            if cell.neighbours == 3:
                cell.active = True
            if cell.neighbours > 3:
                cell.active = False


# Main Loop
while Game.running:
    handle_input()
    screen.fill((192, 192, 192))

    update()
    render()

    pygame.display.update()
    clock.tick(Game.speed)

pygame.quit()

