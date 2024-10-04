import pygame
import math
import random

pygame.init()

# Window setup
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)

# Physics constants
G = 0.25
TIME_STEP = 0.25

class CelestialBody:
    def __init__(self, x, y, mass, radius, color, name, vx=0, vy=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.name = name
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.trail = []
        self.max_trail_length = 50

    def draw_vector(self, screen, start_pos, vx, vy, color, scale, thickness=2):
        if vx == 0 and vy == 0:
            return
        
        # Calculate magnitude
        magnitude = math.sqrt(vx*vx + vy*vy)
        
        # Normalize and scale the vector
        length = magnitude * scale
        if magnitude != 0:
            normalized_x = vx / magnitude
            normalized_y = vy / magnitude
        else:
            return
        
        # Calculate end point
        end_x = start_pos[0] + normalized_x * length
        end_y = start_pos[1] + normalized_y * length
        
        # Draw main line
        pygame.draw.line(screen, color, start_pos, (end_x, end_y), thickness)
        
        # Draw arrowhead
        arrow_size = 10
        angle = math.atan2(-normalized_y, normalized_x)
        arrow_angle = math.pi/6  # 30 degrees
        
        arrow_p1 = (end_x - arrow_size * math.cos(angle - arrow_angle),
                   end_y + arrow_size * math.sin(angle - arrow_angle))
        arrow_p2 = (end_x - arrow_size * math.cos(angle + arrow_angle),
                   end_y + arrow_size * math.sin(angle + arrow_angle))
        
        pygame.draw.line(screen, color, (end_x, end_y), arrow_p1, thickness)
        pygame.draw.line(screen, color, (end_x, end_y), arrow_p2, thickness)

    def draw(self, screen):
        # Draw trail
        if len(self.trail) > 1:
            pygame.draw.lines(screen, (self.color[0]//2, self.color[1]//2, self.color[2]//2), 
                            False, self.trail, 1)

        # Draw body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Calculate magnitudes
        v_magnitude = math.sqrt(self.vx**2 + self.vy**2)
        a_magnitude = math.sqrt(self.ax**2 + self.ay**2)
        
        # Draw vectors with proper arrows
        velocity_scale = 20
        accel_scale = 1000
        
        # Draw velocity vector (white)
        self.draw_vector(screen, (self.x, self.y), self.vx, self.vy, WHITE, velocity_scale)
        
        # Draw acceleration vector (green)
        self.draw_vector(screen, (self.x, self.y), self.ax, self.ay, GREEN, accel_scale)
        
        # Draw text information
        font = pygame.font.Font(None, 20)
        
        # Format text information
        info_lines = [
            f"{self.name}",
            f"Velocidade: {v_magnitude:.1f}",
            f"Aceleração: {a_magnitude:.3f}"
        ]
        
        # Position text blocks
        y_offset = -50
        for line in info_lines:
            text = font.render(line, True, WHITE)
            screen.blit(text, (self.x + self.radius + 5, self.y + y_offset))
            y_offset += 15

    def update_trail(self):
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

    def apply_gravity(self, bodies):
        self.ax = 0
        self.ay = 0
        
        for other in bodies:
            if other is not self:
                dx = other.x - self.x
                dy = other.y - self.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < self.radius + other.radius:
                    continue
                
                force = G * self.mass * other.mass / (distance * distance)
                angle = math.atan2(dy, dx)
                
                self.ax += (force * math.cos(angle)) / self.mass
                self.ay += (force * math.sin(angle)) / self.mass

    def update_position(self):
        self.vx += self.ax * TIME_STEP
        self.vy += self.ay * TIME_STEP
        self.x += self.vx * TIME_STEP
        self.y += self.vy * TIME_STEP
        self.vx *= 0.999
        self.vy *= 0.999
        self.update_trail()

def calculate_center_of_mass(bodies):
    total_mass = 0
    com_x = 0
    com_y = 0
    
    for body in bodies:
        total_mass += body.mass
        com_x += body.x * body.mass
        com_y += body.y * body.mass
    
    if total_mass > 0:
        com_x /= total_mass
        com_y /= total_mass
        
    return com_x, com_y

def draw_center_of_mass(screen, com_x, com_y):
    # Draw center of mass indicator
    pygame.draw.circle(screen, PURPLE, (int(com_x), int(com_y)), 5)
    font = pygame.font.Font(None, 24)
    com_text = font.render("Centro de Massa", True, PURPLE)
    screen.blit(com_text, (int(com_x) + 10, int(com_y) - 10))

def main():
    clock = pygame.time.Clock()
    bodies = create_simulation()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = mouse_x - WIDTH//2
                    dy = mouse_y - HEIGHT//2
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance == 0:
                        distance = 1
                    
                    vx = -dy/distance * random.randint(0, 5)
                    vy = dx/distance * random.randint(0, 5)
                    
                    mass_radius = random.uniform(20, 700)
                    new_body = CelestialBody(
                        mouse_x, mouse_y,
                        mass=mass_radius,
                        radius=0.1*mass_radius,
                        color=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                        name=f"Body {len(bodies)}",
                        vx=vx,
                        vy=vy
                    )
                    bodies.append(new_body)

        # Physics updates
        for body in bodies:
            body.apply_gravity(bodies)
        for body in bodies:
            body.update_position()

        # Drawing
        screen.fill(BLACK)
        
        # Draw bodies
        for body in bodies:
            body.draw(screen)
        
        # Draw center of mass last (on top)
        com_x, com_y = calculate_center_of_mass(bodies)
        draw_center_of_mass(screen, com_x, com_y)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def create_simulation():
    bodies = []
    
    sun = CelestialBody(WIDTH//2, HEIGHT//2, 5000, 80, YELLOW, "Sun")
    bodies.append(sun)
    
    earth = CelestialBody(
        WIDTH//2, HEIGHT//2 - 150,
        mass=50, 
        radius=15, 
        color=BLUE, 
        name="Earth",
        vx=4,
        vy=0
    )
    bodies.append(earth)
    
    mars = CelestialBody(
        WIDTH//2 + 250, HEIGHT//2,
        mass=30,
        radius=12,
        color=RED,
        name="Mars",
        vx=0,
        vy=3
    )
    bodies.append(mars)
    
    return bodies

if __name__ == "__main__":
    main()