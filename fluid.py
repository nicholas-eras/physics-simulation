from textwrap import indent
import pygame, math, random

pygame.init()

width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fluid movement")

mouse_pos = (0, 0)

water_blocks = []
grid_size = 15
last_time = 0
time_step = 100 #100ms

background_color = (30, 30, 30)
running = True

num_grids = (width // grid_size) * (height // grid_size)
grid_empty_color = (0, 0, 0)
grids = []
waters = []

class Water(pygame.Rect):
    def __init__(self, x, y, size):
        super().__init__(pygame.Rect(x, y, size, size))
        self.is_moving_sideways_already = False
        self.direction = 1

def move_water_blocks():
    occupied_position = {(water.x, water.y) for water in waters}

    for water in waters:
        move_water_vertically = True
        move_water_horizontally = False

        if water.y + grid_size == height:
            move_water_vertically = False

        if water.x == 0 or water.x + grid_size == width:
            move_water_horizontally = False   
                
        if ((water.x, water.y + grid_size) in occupied_position):
            move_water_vertically = False
            if (water.x +water.direction* grid_size, water.y) not in occupied_position:
                if water.direction == 1:
                    if water.x +water.direction* grid_size >= width:
                        continue
                if water.direction == -1:
                    if water.x +water.direction* grid_size < 0:
                        continue
                move_water_horizontally = True

        if move_water_vertically:
            water.y += grid_size

        if move_water_horizontally:
            if not water.is_moving_sideways_already:
                moviment_direction = random.choice([1, -1])
                water.is_moving_sideways_already = True
                water.direction = moviment_direction
            water.x = water.x +  water.direction*grid_size 

for y in range(height // grid_size):
    row = []
    for x in range(width // grid_size):            
        
        grid = pygame.Rect(
            grid_size * x,
            grid_size * y,
            grid_size,
            grid_size,
        )
        row.append(grid)
    grids.append(row)

while running:
    screen.fill(background_color)
        
    for row in grids:
        for grid in row:
            pygame.draw.rect(screen, (10, 10, 10), grid, 1)
    for water in waters:
        pygame.draw.rect(screen, (0, 0, 120), water)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        column = mouse_pos[0] // grid_size
        row = mouse_pos[1] // grid_size
        water = Water(grid_size * column, grid_size * row, grid_size)
        waters.append(water)                                
    
    current_time = pygame.time.get_ticks()
    if current_time - last_time >= time_step:
        move_water_blocks()
        last_time = current_time

 
    pygame.display.flip()

pygame.quit()
