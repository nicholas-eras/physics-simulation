import pygame, math, random

pygame.init()

width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fluid movement")

mouse_pos = (0, 0)

solid_blocks = []
solid_size = 10
last_time = 0
time_step = 100 #100ms

background_color = (30, 30, 30)
running = True


class Solid(pygame.Rect):
    def __init__(self,x, y, size):
        super().__init__(x, y, size, size)
        self.is_moving = True

def draw_solid():
    mouse_pos = pygame.mouse.get_pos()
    new_solid = Solid(
                mouse_pos[0] - solid_size / 2,
                mouse_pos[1] - solid_size / 2,
                solid_size,                 
            )
    draw_solid = True
    for solid in solid_blocks:                        
        if solid.colliderect(new_solid):
            draw_solid = False

    if draw_solid:
        solid_blocks.append(new_solid)

def move_solid_blocks():
    for solid_index, solid in enumerate(solid_blocks):
        if not solid.is_moving :
            continue

        solid_can_move = True

        if solid.y + solid_size >= height:
            solid.y = height - solid_size    
            solid.is_moving = False  
            continue

        if solid_index > 0:
            for next_solid_index, next_solid in enumerate(solid_blocks):
                if next_solid_index == solid_index:
                    break

                if solid.colliderect(next_solid) and next_solid.y > solid.y:
                    solid.y = next_solid.y - solid_size
                    if not next_solid.is_moving:
                        solid.is_moving = False
                        solid_can_move = False            

        if solid_can_move:
            solid.is_moving = True
            solid.y += solid_size

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                draw_solid()
    
    current_time = pygame.time.get_ticks()
    if current_time - last_time >= time_step:
        move_solid_blocks()
        last_time = current_time

    screen.fill(background_color)
    for solid in solid_blocks:
        pygame.draw.rect(screen, (0, 0, 160), solid)
 
    pygame.display.flip()

pygame.quit()
