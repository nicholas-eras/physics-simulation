import pygame
import math
import random

pygame.init()
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fluid movement")

mouse_pos = (0, 0)
water_blocks = []
water_size = 10
last_time = 0
time_step = 100  # 100ms
background_color = (30, 30, 30)
running = True

class Water(pygame.Rect):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.is_moving = True
        self.direction = 0  # 0: down, -1: left, 1: right
        self.moved_this_frame = False

def draw_water():
    mouse_pos = pygame.mouse.get_pos()
    new_water = Water(
        mouse_pos[0] - water_size / 2,
        mouse_pos[1] - water_size / 2,
        water_size,
    )
    draw_water = True
    for water in water_blocks:
        if water.colliderect(new_water):
            draw_water = False
    if draw_water:
        water_blocks.append(new_water)

def can_move_down(water, water_blocks):
    if water.y + water_size >= height:
        return False
    
    for other_water in water_blocks:
        if other_water != water:
            if (water.x == other_water.x and 
                water.y + water_size == other_water.y):
                return False
    return True

def try_move_sideways(water, water_blocks, direction):
    current_x = water.x
    while True:
        new_x = current_x + (water_size * direction)
        
        # Check wall collision
        if new_x < 0 or new_x + water_size > width:
            return current_x
        
        # Check water collision
        collision = False
        for other_water in water_blocks:
            if other_water != water:
                test_rect = pygame.Rect(new_x, water.y, water_size, water_size)
                if test_rect.colliderect(other_water):
                    collision = True
                    break
        
        if collision:
            return current_x
            
        # Check if can fall at this position
        test_rect = pygame.Rect(new_x, water.y + water_size, water_size, water_size)
        can_fall = True
        if test_rect.bottom > height:
            can_fall = True
        else:
            for other_water in water_blocks:
                if other_water != water and test_rect.colliderect(other_water):
                    can_fall = False
                    break
        
        if can_fall:
            return new_x
            
        current_x = new_x

def move_water_blocks():
    # Reset moved flag for all blocks
    for water in water_blocks:
        water.moved_this_frame = False
    
    for water in water_blocks:
        if water.moved_this_frame:
            continue
            
        if not water.is_moving:
            continue

        # Try to move down first
        if can_move_down(water, water_blocks):
            water.y += water_size
            water.moved_this_frame = True
            continue

        # If can't move down, try both sides
        left_pos = try_move_sideways(water, water_blocks, -1)
        right_pos = try_move_sideways(water, water_blocks, 1)
        
        # Move to the furthest possible position
        if abs(left_pos - water.x) > abs(right_pos - water.x):
            water.x = left_pos
        else:
            water.x = right_pos
            
        # Check if can fall after moving sideways
        if can_move_down(water, water_blocks):
            water.y += water_size
            
        water.moved_this_frame = True
        
        # If couldn't move at all, stop moving
        if water.x == water.x and not can_move_down(water, water_blocks):
            water.is_moving = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                draw_water()

    current_time = pygame.time.get_ticks()
    if current_time - last_time >= time_step:
        move_water_blocks()
        last_time = current_time

    screen.fill(background_color)
    for water in water_blocks:
        pygame.draw.rect(screen, (0, 0, 160), water)
    pygame.display.flip()

pygame.quit()