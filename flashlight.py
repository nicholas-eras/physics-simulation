import pygame, math, random

pygame.init()

width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Capturar Movimento do Mouse")

mouse_pos = (0, 0)

background_color = (30, 30, 30)
line_color = (225, 193, 110)
num_lines = 100

angle_step = 2 * math.pi  / num_lines
   
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
    
    screen.fill(background_color)
    
    for i in range(num_lines):
        pos_x = (width / 2) * (math.cos(angle_step * i)) + width / 2
        pos_y = (- height / 2) * math.sin(angle_step * i) + height / 2    
        
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
    
        pygame.draw.line(screen, line_color, mouse_pos, (pos_x, pos_y), 2)
        # pygame.draw.line(screen, line[1], mouse_pos, line[0], 2)
    
    pygame.draw.circle(screen, (255, 255, 255), (600, 800), 100)

    pygame.display.flip()

pygame.quit()
