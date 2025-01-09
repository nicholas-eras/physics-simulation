import pygame, math, random

pygame.init()

width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ray Tracing")

mouse_pos = (0, 0)

background_color = (30, 30, 30)
line_color = (225, 193, 110)
line_length = 1000
num_lines = 500

angle_step = 2 * math.pi  / num_lines

num_polygon = 3
polygon_size = 100
polygons = []
for _ in range(num_polygon):
    polygon_position = (random.randint(0, width - polygon_size), random.randint(0, height - polygon_size))
    polygon_vertices = [polygon_position, (polygon_position[0], polygon_position[1] + polygon_size), (polygon_position[0] + polygon_size, polygon_position[1] + polygon_size), (polygon_position[0] + polygon_size, polygon_position[1])]
    polygons.append(polygon_vertices)

def calculate_min_max_angle_polygon(mouse_pos, polygon):
        pos_x, pos_y = mouse_pos[0], mouse_pos[1]
        
        angles_vertice = []
        for vertice in polygon:
            angle = math.atan2(vertice[1] - pos_y, vertice[0] - pos_x)
            angles_vertice.append({"angle": angle, "vertice": vertice})

        angles_vertice.sort(key= lambda obj: obj["angle"])

        return angles_vertice[0], angles_vertice[-1]

def is_angle_between(angulo, min_angle, max_angle):    
     return angulo >= min_angle and angulo <= max_angle

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
    
    screen.fill(background_color)
    for polygon in polygons:
        pygame.draw.polygon(screen, line_color, polygon, 1)

    for i in range(num_lines):
        pos_x = line_length * math.cos(angle_step * i) + mouse_pos[0]
        pos_y = line_length * math.sin(angle_step * i) + mouse_pos[1]
        
        draw_line = True
        for polygon in polygons:
            vertice_menor, vertice_maior = calculate_min_max_angle_polygon(mouse_pos, polygon)      
            
            angulo_menor = vertice_menor["angle"]
            angulo_maior = vertice_maior["angle"]

            if ((pos_x - mouse_pos[0]) == 0):
                angulo_line_horizontal = 0
            else:
                angulo_line_horizontal = math.atan2(pos_y - mouse_pos[1], pos_x - mouse_pos[0])    

            if is_angle_between(angulo_line_horizontal, angulo_menor, angulo_maior):
                media_angulo = (angulo_maior + angulo_menor)/2
                if angulo_line_horizontal >= media_angulo:
                    pos_x = vertice_maior["vertice"][0]
                    pos_y = mouse_pos[1] -  math.tan(angulo_line_horizontal) * (mouse_pos[0] - pos_x)
                else:
                    pos_y = vertice_menor["vertice"][1]
                    if math.tan(angulo_line_horizontal) == 0:
                        pos_x = vertice_maior["vertice"][0]
                    else:
                        pos_x = mouse_pos[0] -  (mouse_pos[1] - pos_y) / math.tan(angulo_line_horizontal)
                # draw_line = False

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        
        if not draw_line:
            continue

        pygame.draw.line(screen, line_color, mouse_pos, (pos_x, pos_y), 1)
        
    pygame.display.flip()

pygame.quit()
