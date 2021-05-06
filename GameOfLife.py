#! /bin/python3

###################
##### IMPORTS #####
###################

import pygame
import random
import math


#######################
##### INIT MODULE #####
#######################

pygame.init()
screenInfo = pygame.display.Info()
screen_size = [screenInfo.current_w, screenInfo.current_h]
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", int(screen_size[0] / 100))
pygame.display.set_caption("Conways Game of Life")

###################
##### CLASSES #####
###################

class Game:
    running = True
    paused = True
    debug = False
    infinity = True
    tick = 0
    maxFPS = 20
    c = [0, 35, 19]


class Cursor:
    x = 0
    y = 0
    lclick = False
    rclick = False
    rect = pygame.Rect(x,y,1,1)


class Colors:
    r = 255
    g = 0
    b = 0


class Cell:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

    resolution = 15 
    active = False
    neighbors = 0
    x = 0
    y = 0
    w = resolution
    h = w
    
    rect = pygame.Rect(x,y,w,h)
    c = [0,19,35]

    in_row = int(screen_size[0] / resolution)
    in_column = int(screen_size[1] / resolution)
    total = in_row * in_column

cells = []
bg_cells = []


#################
##### MATHS #####
#################

def is_prime(num):
    i = 2
    while (i <= math.sqrt(num)):
        i += 1
        if num % i == 0:
            return False
    return True


def get_distance(x1,y1,x2,y2):
    xdst = x1-x2
    ydst = y1-y2
    return math.sqrt(xdst*xdst+ydst*ydst)


###################
##### DRAWING #####
###################

def RGB():
    if Colors.r == 255 and Colors.b == 0:
        Colors.g += 1
    if Colors.g == 255 and Colors.r > 0:
        Colors.r -= 1
    if Colors.g == 255 and Colors.r == 0:
        Colors.b += 1
    if Colors.b == 255 and Colors.g > 0:
        Colors.g -= 1
    if Colors.b == 255 and Colors.g == 0:
        Colors.r += 1
    if Colors.r == 255 and Colors.b > 0:
        Colors.b -= 1


def gradient(id):
    value = id / Cell.total * 768


def draw_box(x, y, w, h, c, o):
    if o:
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(x,y,w,h))
    pygame.draw.rect(screen, c, pygame.Rect(x+1,y+1,w-2,h-2))


def draw_circle(x, y, r, c, f):
    xs = x-r
    ys = y-r
    d = r*2+2
    for i in range(d):
        for j in range(d):
            if f:
                if (int(get_distance(x,y,xs+j,ys+i))) <= r:
                    draw_box(xs+j,ys+i,1,1,c,False)
            else:
                if (int(get_distance(x,y,xs+j,ys+i))) == r:
                    draw_box(xs+j,ys+i,1,1,c,False)


def draw_line(x1, y1, x2, y2, c, t):
    pygame.draw.line(screen, c, [x1,y1], [x2,y2], t)


def draw_rect(x, y, w, h, c, t):
    draw_line(x, y, x+w, y, c, t)
    draw_line(x, y, x, y+h, c, t)
    draw_line(x, y+h, x+w, y+h, c, t)
    draw_line(x+w, y, x+w, y+h, c, t)


def draw_text(x,y,c,text):
    screen.blit(font.render(text, True, c), (x,y))


def paused():
    if Game.paused:
        draw_box(screen_size[0] / 2 - 20, screen_size[1] / 2 - 25, 15, 50, (192,192,192), True)
        draw_box(screen_size[0] / 2 + 5, screen_size[1] / 2 - 25, 15, 50, (192,192,192), True)
        pygame.mouse.set_visible(True)
    else:
        pygame.mouse.set_visible(False)


########################
##### KEYFUNCTIONS #####
########################

def clear():
    for cell in cells:
        cell.active = False


def randomize():
    for cell in cells:
        cell.active = random.randint(0,1)


def half():
    for cell in cells:
        if cell.id >= Cell.total / 2 - 1:
            cell.active = True
        if cell.id == Cell.total / 2 - Cell.in_row:
            cell.active = True


def fizzbuzz():
    for cell in cells:
        if cell.id % 3 == 0 or cell.id % 5 == 0:
            cell.active = True

def negative():
    for cell in cells:
        if cell.active:
            cell.active = False
        else:
            cell.active = True


def midline():
    for cell in cells:
        if cell.id < Cell.total - 1:
            if cell.id % Cell.in_row == 0: 
                cell.active = True
                cells[cell.id - 1].active = True
            if cell.id < Cell.in_row:
                cell.active = True
            if cell.id > Cell.total - Cell.in_row:
                cell.active = True


def infinity_mode():
    if Game.tick >= Game.maxFPS * 7:
        Game.tick = 0
        seed = random.randint(0,9)
        if seed == 0:
            half()
        else:
            midline()


##########################
##### CELL FUNCTIONS #####
##########################

def copy_cells():
    for cell in cells:
        bg_cells[cell.id].active = cell.active
        bg_cells[cell.id].neighbors = cell.neighbors


def flush_neighbors():
    for cell in cells:
        cell.neighbors = 0
        bg_cells[cell.id].neighbors = 0


def get_neighbors(id):
    # 1 2 3
    # 4 x 5
    # 6 7 8
    # Max neighbors = 8, right?
    
    # Edge Cases
    
    # Top Left
    if id == 0:
        # 5
        if bg_cells[id + 1].active:
            cells[id].neighbors += 1
        # 6
        if bg_cells[id + Cell.in_row - 1].active:
            cells[id].neighbors += 1
        # 7
        if bg_cells[id + Cell.in_row].active:
            cells[id].neighbors += 1
        # 8
        if bg_cells[id + Cell.in_row + 1].active:
            cells[id].neighbors += 1
        # 2
        if bg_cells[Cell.total - Cell.in_row + 1].active:
            cells[id].neighbors += 1
        # 3
        if bg_cells[Cell.total - 1].active:
            cells[id].neighbors += 1
        # 1
        if bg_cells[Cell.total - Cell.in_row].active:
            cells[id].neighbors += 1
        # 4
        if bg_cells[Cell.in_row * 2 - 1].active:
            cells[id].neighbors += 1
    # Top Right
    elif id == Cell.in_row - 1:
        # 6
        if bg_cells[id + 1].active:
            cells[id].neighbors += 1
        # 4
        if bg_cells[id - 1].active:
            cells[id].neighbors += 1
        # 7
        if bg_cells[id + Cell.in_row].active:
            cells[id].neighbors += 1
        # 6
        if bg_cells[id + Cell.in_row - 1].active:
            cells[id].neighbors += 1
        # 8
        if bg_cells[Cell.total - Cell.in_row].active:
            cells[id].neighbors += 1
        # 5
        if bg_cells[0].active:
            cells[id].neighbors += 1
        # 1
        if bg_cells[Cell.total - 2].active:
            cells[id].neighbors += 1
        # 2
        if bg_cells[Cell.total - 1].active:
            cells[id].neighbors += 1
    # Bottom Left
    elif id == Cell.total - Cell.in_row:
        # 5
        if bg_cells[id + 1].active:
            cells[id].neighbors += 1
        # 2
        if bg_cells[id - Cell.in_row].active:
            cells[id].neighbors += 1
        # 3
        if bg_cells[id - Cell.in_row + 1].active:
            cells[id].neighbors += 1
        # 4
        if bg_cells[Cell.total - 1].active:
            cells[id].neighbors += 1
        # 1
        if bg_cells[Cell.total - Cell.in_row - 1].active:
            cells[id].neighbors += 1
        # 7
        if bg_cells[0].active:
            cells[id].neighbors += 1
        # 8
        if bg_cells[1].active:
            cells[id].neighbors += 1
        # 6
        if bg_cells[Cell.in_row - 1].active:
            cells[id].neighbors += 1
    # Bottom Right
    elif id == Cell.total - 1:
        # 5
        if bg_cells[Cell.total - Cell.in_row].active:
            cells[id].neighbors += 1
        # 4
        if bg_cells[id - 1].active:
            cells[id].neighbors += 1
        # 2
        if bg_cells[Cell.total - Cell.in_row - 1].active:
            cells[id].neighbors += 1
        # 1
        if bg_cells[Cell.total - Cell.in_row - 2].active:
            cells[id].neighbors += 1
        # 3
        if bg_cells[Cell.total - Cell.in_row * 2].active:
            cells[id].neighbors += 1
        # 8
        if bg_cells[0].active:
            cells[id].neighbors += 1
        # 7
        if bg_cells[Cell.in_row - 1].active:
            cells[id].neighbors += 1
        # 6
        if bg_cells[Cell.in_row - 2].active:
            cells[id].neighbors += 1
    # Top Row
    elif id < Cell.in_row:
        # 4
        if bg_cells[id - 1].active:
            cells[id].neighbors += 1
        # 5
        if bg_cells[id + 1].active:
            cells[id].neighbors += 1
        # 7
        if bg_cells[id + Cell.in_row].active:
            cells[id].neighbors += 1
        # 6
        if bg_cells[id + Cell.in_row - 1].active:
            cells[id].neighbors += 1
        # 8
        if bg_cells[id + Cell.in_row + 1].active:
            cells[id].neighbors += 1
        # 2
        if bg_cells[id + Cell.total - Cell.in_row].active:
            cells[id].neighbors += 1
        # 1
        if bg_cells[id + Cell.total - Cell.in_row - 1].active:
            cells[id].neighbors += 1
        # 3
        if bg_cells[id + Cell.total - Cell.in_row + 1].active:
            cells[id].neighbors += 1
    # Bottom Row
    elif Cell.total - Cell.in_row < id:
        # 4
        if bg_cells[id - 1].active:
            cells[id].neighbors += 1
        # 5
        if bg_cells[id + 1].active:
            cells[id].neighbors += 1
        # 2
        if bg_cells[id - Cell.in_row].active:
            cells[id].neighbors += 1
        # 1
        if bg_cells[id - Cell.in_row - 1].active:
            cells[id].neighbors += 1
        # 3
        if bg_cells[id - Cell.in_row + 1].active:
            cells[id].neighbors += 1
        # 7
        if bg_cells[id - Cell.total + Cell.in_row].active:
            cells[id].neighbors += 1
        # 6
        if bg_cells[id - Cell.total + Cell.in_row - 1].active:
            cells[id].neighbors += 1
        # 8
        if bg_cells[id - Cell.total + Cell.in_row + 1].active:
            cells[id].neighbors += 1
    # Left Column
    elif id % Cell.in_row == 0:
        # 5
        if bg_cells[id + 1].active:
            cells[id].neighbors += 1
        # 4
        if bg_cells[id + Cell.in_row - 1].active:
            cells[id].neighbors += 1
        # 6
        if bg_cells[id + Cell.in_row * 2 - 1].active:
            cells[id].neighbors += 1
        # 7
        if bg_cells[id + Cell.in_row].active:
            cells[id].neighbors += 1
        # 8
        if bg_cells[id + Cell.in_row + 1].active:
            cells[id].neighbors += 1
        # 1
        if bg_cells[id - 1].active:
            cells[id].neighbors += 1
        # 2
        if bg_cells[id - Cell.in_row].active:
            cells[id].neighbors += 1
        # 3
        if bg_cells[id - Cell.in_row + 1].active:
            cells[id].neighbors += 1
    elif id % Cell.in_row  == Cell.in_row - 1:
        # 4
        if bg_cells[id - 1].active:
            cells[id].neighbors += 1
        # 2
        if bg_cells[id - Cell.in_row].active:
            cells[id].neighbors += 1
        # 1
        if bg_cells[id - Cell.in_row - 1].active:
            cells[id].neighbors += 1
        # 6
        if bg_cells[id + Cell.in_row - 1].active:
            cells[id].neighbors += 1
        # 7
        if bg_cells[id + Cell.in_row].active:
            cells[id].neighbors += 1
        # 8
        if bg_cells[id + 1].active:
            cells[id].neighbors += 1
        # 3
        if bg_cells[id - Cell.in_row * 2 + 1].active:
            cells[id].neighbors += 1
        # 5
        if bg_cells[id - Cell.in_row + 1].active:
            cells[id].neighbors += 1
    # Any cell that isn't special
    else:
        #1
        if id - Cell.in_row - 1 >= 0:
            if bg_cells[id - Cell.in_row - 1].active:
                cells[id].neighbors += 1
        # 2
        if id - Cell.in_row >= 0:
            if bg_cells[id - Cell.in_row].active:
                cells[id].neighbors += 1
        # 3
        if id - Cell.in_row + 1 >= 0:
            if bg_cells[id - Cell.in_row + 1].active:
                cells[id].neighbors += 1
        # 4
        if id - 1 >= 0:
            if bg_cells[id - 1].active:
                cells[id].neighbors += 1
        # 5
        if id + 1 < Cell.total:
            if bg_cells[id + 1].active:
                cells[id].neighbors += 1
        # 6
        if id + Cell.in_row - 1 < Cell.total:
            if bg_cells[id + Cell.in_row - 1].active:
                cells[id].neighbors += 1
        # 7
        if id + Cell.in_row < Cell.total:
            if bg_cells[id + Cell.in_row].active:
                cells[id].neighbors += 1
        # 8
        if id + Cell.in_row + 1 < Cell.total:
            if bg_cells[id + Cell.in_row + 1].active:
                cells[id].neighbors += 1



##################
##### UPDATE #####
##################

def update_cursor():
    Cursor.x, Cursor.y = pygame.mouse.get_pos()
    Cursor.rect = pygame.Rect(Cursor.x, Cursor.y, 1, 1)
    for cell in cells:
        # Cursor
        if cell.rect.colliderect(Cursor.rect):
            if Cursor.lclick:
                cell.active = True
            elif Cursor.rclick:
                cell.active = False


def update_cells():
    copy_cells()
    flush_neighbors()

    for cell in cells:
        # Rect
        cell.rect = pygame.Rect(cell.x, cell.y, cell.w, cell.h)
        # Color
        if cell.active:
            cell.c = [Colors.r, Colors.g, Colors.b]
        else:
            cell.c = [0,19,35]

        get_neighbors(cell.id)

        if not Game.paused:
            # Rules
            if cell.neighbors < 2:
                cell.active = False
            elif cell.neighbors > 3:
                cell.active = False
            if cell.neighbors == 3:
                cell.active = True


def update():
    RGB()
    update_cursor()
    update_cells()

    if not Game.paused and Game.infinity:
        infinity_mode()


##################
##### RENDER #####
##################

def render_cells():
    for cell in cells:
        c = [0,19,35]
        if cell.active:
            c = [Colors.r, Colors.g, Colors.b]
        if cell.rect.colliderect(Cursor.rect) and Game.paused:
            c = [192,192,192]
        draw_box(cell.x, cell.y, cell.w, cell.h, c, True)
        if Game.debug:
            draw_text(cell.x, cell.y, (192,192,192), str(cell.neighbors))
            draw_text(cell.x, cell.y + cell.h / 2, (192,192,192), str(cell.id))

def render():
    render_cells()
    paused()


#################
##### INPUT #####
#################

def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Quit Game
            if event.key == pygame.K_q:
                Game.running = False
            # Pause Game
            if event.key == pygame.K_SPACE:
                if Game.paused:
                    Game.paused = False
                else:
                    Game.paused = True
            # Clear
            if event.key == pygame.K_c:
                clear()
            # Randomize
            if event.key == pygame.K_s:
                randomize()
            # Half
            if event.key == pygame.K_r:
                half()
            # Fivths
            if event.key == pygame.K_f:
                fizzbuzz()
            # Negative
            if event.key == pygame.K_n:
                negative()
            # Midline
            if event.key == pygame.K_m:
                midline()
            # Infinity Mode
            if event.key == pygame.K_i:
                if Game.infinity:
                    clear()
                    Game.infinity = False
                else:
                    clear()
                    half()
                    midline()
                    Game.tick = 0
                    Game.infinity = True
            # Debugmode
            if event.key == pygame.K_d:
                if Game.debug:
                    Game.debug = False
                else:
                    Game.debug = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Cursor.lclick = True
            if event.button == 3:
                Cursor.rclick = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                Cursor.lclick = False
            if event.button == 3:
                Cursor.rclick = False


################
##### INIT #####
################

def create_grid():
    id = 0
    for i in range(Cell.in_column):
        for j in range(Cell.in_row):
            cells.append(Cell(j * Cell.w, i * Cell.h, id))
            bg_cells.append(Cell(j + Cell.w, i * Cell.h, id))
            id += 1


def init_game():
    create_grid()

init_game()


#####################
##### MAIN LOOP #####
#####################

while Game.running:
    handle_input()
    screen.fill(Game.c)

    update()
    render()

    pygame.display.update()
    Game.tick += 1
    clock.tick(Game.maxFPS)


################
##### EXIT #####
################

pygame.quit()
quit()
