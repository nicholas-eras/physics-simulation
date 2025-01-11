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

def move_water_blocks():
    for water_index, water in enumerate(waters):
        move_water = True
        if water.y + grid_size == height:
            move_water = False   
        
        if water_index > 0:
            for water_below in waters:
                if water_below != water:
                    if water.y + grid_size == water_below.y and water.x == water_below.x:
                        move_water = False

        if move_water:
            water.y += grid_size

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                column = mouse_pos[0] // grid_size
                row = mouse_pos[1] // grid_size
                water = pygame.Rect(grid_size * column, grid_size * row, grid_size, grid_size)
                waters.append(water)                                
    
    current_time = pygame.time.get_ticks()
    if current_time - last_time >= time_step:
        move_water_blocks()
        last_time = current_time

 
    pygame.display.flip()

pygame.quit()
