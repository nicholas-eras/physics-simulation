import pygame, math, random

pygame.init()

width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ray Tracing")

mouse_pos = (0, 0)

background_color = (30, 30, 30)
line_color = (225, 193, 110)
line_length = 1000
num_lines = 100

angle_step = 2 * math.pi  / num_lines

num_polygon = 1
polygon_size = 100
polygons = []
for _ in range(num_polygon):
    # polygon_position = (random.randint(0, width - polygon_size), random.randint(0, height - polygon_size))
    polygon_position = (400, 300)
    polygon_vertices = [
        polygon_position,
        (polygon_position[0], polygon_position[1] + polygon_size),
        (polygon_position[0] + polygon_size, polygon_position[1] + polygon_size),
        (polygon_position[0] + polygon_size, polygon_position[1])
        ]
    polygons.append(polygon_vertices)


def obtain_quadrant(x, y):
    if x > 0 and y > 0:
        return 1
    if x < 0 and y > 0:
        return 2
    if x < 0 and y < 0:
        return 3
    if x > 0 and y < 0:
        return 4

def is_mouse_inside_polygon(mouse_pos, polygon):    
    if polygon[0][0] < mouse_pos[0] < polygon[2][0] and polygon[0][1] < mouse_pos[1] < polygon[1][1]:
        return True
    return False

def calculate_min_max_angle_polygon(mouse_pos, polygon):
        pos_x, pos_y = mouse_pos[0], mouse_pos[1]
        
        angles_vertice = []
        for vertice in polygon:
            angle = math.degrees(math.atan2(vertice[1] - pos_y, vertice[0] - pos_x))
            if angle < 0:
                angle += 360  
            quadrante = obtain_quadrant(vertice[0] - pos_x, vertice[1] - pos_y)
            distance = math.sqrt((vertice[1] - pos_y)**2 + (vertice[0] - pos_x)** 2)
            angles_vertice.append({"angle": angle, "vertice": vertice, "quadrant": quadrante, "distance": distance})
        
        if (polygon[1][1] > mouse_pos[1] and polygon[0][1] < mouse_pos[1]):
            angles_vertice.sort(key= lambda obj: obj["distance"])
        else:
            angles_vertice.sort(key= lambda obj: obj["angle"])

        if pos_x > polygon[3][0] and pos_y > polygon[2][1]:            
            angles_vertice.sort(key= lambda obj: obj["distance"])            
            return angles_vertice[1], angles_vertice[2], angles_vertice                
        
        if pos_x > polygon[3][0] and pos_y < polygon[2][1]:            
            angles_vertice.sort(key= lambda obj: obj["distance"])            
            return angles_vertice[1], angles_vertice[2], angles_vertice                
        
        if pos_x > polygon[2][0]:
            return angles_vertice[1], angles_vertice[2], angles_vertice                
        
        if (polygon[1][1] > mouse_pos[1] and polygon[0][1] < mouse_pos[1] and pos_x < polygon[0][0]): 
            return angles_vertice[0], angles_vertice[1], angles_vertice
        
        return angles_vertice[0], angles_vertice[-1], angles_vertice

def is_angle_between(angulo, min_angle, max_angle, polygon, mouse_pos):     
    if min_angle > max_angle:
        min_angle, max_angle = max_angle, min_angle
    
    if angulo == 0 and mouse_pos[0] < polygon[0][0] and ( polygon[0][1] < mouse_pos[1] < polygon[1][0]):
        return True

    if (mouse_pos[0] < polygon[0][0]) and (polygon[1][1] > mouse_pos[1] and polygon[0][1] < mouse_pos[1]):
        if angulo < 90:
            return angulo < min_angle
        else:
            return 360 - angulo < 360 - max_angle
    

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
        pygame.draw.polygon(screen, line_color, polygon, not is_mouse_inside_polygon(mouse_pos, polygon))

    for i in range(num_lines):
        pos_x = line_length * math.cos(angle_step * i) + mouse_pos[0]
        pos_y = line_length * math.sin(angle_step * i) + mouse_pos[1]
        
        draw_line = True
        for polygon in polygons:
            if is_mouse_inside_polygon(mouse_pos, polygon):
                draw_line = False
                continue

            vertice_menor, vertice_maior, angles_2 = calculate_min_max_angle_polygon(mouse_pos, polygon)      
            
            angulo_menor = vertice_menor["angle"]
            angulo_maior = vertice_maior["angle"]

            if ((pos_x - mouse_pos[0]) == 0):
                angulo_line_horizontal = 0
            else:
                angulo_line_horizontal = math.degrees(math.atan2(pos_y - mouse_pos[1], pos_x - mouse_pos[0]))

            if angulo_line_horizontal < 0:
                angulo_line_horizontal += 360 
           
            if is_angle_between(angulo_line_horizontal, angulo_menor, angulo_maior, polygon, mouse_pos):
                angle_until_center = math.atan2((polygon[0][1] + polygon_size / 2) - mouse_pos[1],(polygon[0][0] + polygon_size / 2) - mouse_pos[0])
                if angulo_line_horizontal > angle_until_center:
                    pos_x = polygon[0][0]
                    pos_y = math.tan(angulo_line_horizontal) * (pos_x - mouse_pos[0])
                elif angulo_line_horizontal == angle_until_center:
                    pos_x = polygon[0][0]
                    pos_y = polygon[2][1]
                else:
                    pos_y = polygon[2][1]
                    if math.tan(angulo_line_horizontal) == 0:
                        pos_x = polygon[0][0]
                    else:
                        pos_x =  (mouse_pos[1] - pos_y) / math.tan(angulo_line_horizontal)
                draw_line = False                             
    
        if not draw_line:        
            continue
        
        pygame.draw.line(screen, line_color, mouse_pos, (pos_x, pos_y), 1)
        

    pygame.display.flip()

pygame.quit()
