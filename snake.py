import pygame, random

class Snake(pygame.Rect):
    position = 0
    def __init__(self, x, y, size, direction = "direita"):
        super().__init__(x, y, size, size)
        self.direction = direction
        self.previous_direction = direction
        self.changed_direction_at = None
        self.changed_direction_to = None
        Snake.position += 1
        self.position = Snake.position

    def get_pos(self):
        return (self.x, self.y)

    def __repr__(self):
        return (f"Snake(position={self.position}, x={self.x}, y={self.y}, size={self.width}, "
                f"direction={self.direction}, previous_direction={self.previous_direction}, "
                f"changed_direction_at={self.changed_direction_at}, "
                f"changed_direction_to={self.changed_direction_to})")

    def __str__(self):
        return (f"Snake(position={self.position}, x={self.x}, y={self.y}, size={self.width}, "
                f"direction={self.direction}, previous_direction={self.previous_direction}, "
                f"changed_direction_at={self.changed_direction_at}, "
                f"changed_direction_to={self.changed_direction_to}), "
                f"current_pos={self.get_pos()}")

pygame.init()

width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

mouse_pos = (0, 0)

grid_size = 30

background_color = (30, 30, 30)
running = True

num_grids = (width // grid_size) * (height // grid_size) - 2
grid_empty_color = (0, 0, 0)
grids = []
snake_color = (0, 180, 0)
snake = [
    Snake(width // 2, height // 2, grid_size),
    # Snake(width // 2 - 1 * grid_size, height // 2, grid_size),
    # Snake(width // 2- 2 * grid_size, height // 2, grid_size),
    # Snake(width // 2- 3 * grid_size, height // 2, grid_size),
    # Snake(width // 2- 4 * grid_size, height // 2, grid_size),
    # Snake(width // 2- 5 * grid_size, height // 2, grid_size),
    # Snake(width // 2- 6 * grid_size, height // 2, grid_size),
    # Snake(width // 2- 7 * grid_size, height // 2, grid_size),
    # Snake(width // 2- 8 * grid_size, height // 2, grid_size),
    # Snake(width // 2- 9 * grid_size, height // 2, grid_size)
    ]

last_time = 0
time_step = 100 #100ms
snake_directions = {"cima":0, "esquerda":1, "baixo":2, "direita":3}

while True:
    random_row = random.randint(1, width // grid_size)
    random_column =  random.randint(1, height // grid_size)
    if Snake((random_row-1)*grid_size, (random_column-1)*grid_size, grid_size) not in snake:
        food = pygame.Rect((random_row-1)*grid_size, (random_column-1)*grid_size, grid_size, grid_size)
        break

def move_snake(): 
    for snake_block in snake:  
        if snake_block.direction != snake_block.previous_direction:
            snake_block.changed_direction_at = snake_block.get_pos()
            snake_block.previous_direction = snake_block.direction
            snake_block.changed_direction_to = snake_block.direction

        match (snake_block.direction):
            case "cima":
                snake_block.y -= grid_size
            case "esquerda":    
                snake_block.x -= grid_size
            case "baixo":    
                snake_block.y += grid_size
            case "direita":    
                snake_block.x += grid_size                

def update_snake_blocks_direction():
    for i, snake_block in enumerate(snake):
        if i != 0:            
            if snake[i-1].changed_direction_at is not None and snake_block.get_pos() == snake[i-1].changed_direction_at:        
                snake_block.direction = snake[i-1].previous_direction

def change_head_direction_to(direction):
    if direction == "baixo" and snake[0].direction == "cima" or direction == "cima" and snake[0].direction == "baixo":
        return
    if direction == "direita" and snake[0].direction == "esquerda" or direction == "esquerda" and snake[0].direction == "direita":
        return
    snake[0].direction = direction

def check_if_new_body_out_screen(new_body_part_x, new_body_part_y):
    snake_body_parts_position = [(snake_body_part.x, snake_body_part.y) for snake_body_part in snake]
    if not 0 <= new_body_part_x < width or not 0 <= new_body_part_y < height:
        new_body_part_x = snake_last_body_part.x
        new_body_part_y = snake_last_body_part.y + grid_size
        if not 0 <= new_body_part_x < width or not 0 <= new_body_part_y < height or (new_body_part_x, new_body_part_y) in snake_body_parts_position:
            new_body_part_x = snake_last_body_part.x
            new_body_part_y = snake_last_body_part.y - grid_size
            if not 0 <= new_body_part_x < width or not 0 <= new_body_part_y < height or (new_body_part_x, new_body_part_y) in snake_body_parts_position:
                new_body_part_x = snake_last_body_part.x + grid_size
                new_body_part_y = snake_last_body_part.y
                if not 0 <= new_body_part_x < width or not 0 <= new_body_part_y < height or (new_body_part_x, new_body_part_y) in snake_body_parts_position:
                    new_body_part_x = snake_last_body_part.x - grid_size
                    new_body_part_y = snake_last_body_part.y
                
    return new_body_part_x, new_body_part_y

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
    current_time = pygame.time.get_ticks()
    if current_time - last_time >= time_step:
        move_snake()
        update_snake_blocks_direction()
        last_time = current_time

    screen.fill(background_color)
        
    for row in grids:
        for grid in row:
            pygame.draw.rect(screen, (10, 10, 10), grid, 1)

    for snake_body in snake:
        pygame.draw.rect(screen, snake_color, snake_body, 0)

    for i, snake_body in enumerate(snake):        
        if (snake_body.x >= width or snake_body.x < 0) or (snake_body.y > height or snake_body.y  < 0) :   

            running = False

        if snake_body is not snake[0]:
            if snake[0].colliderect(snake_body):
                running = False

    pygame.draw.rect(screen, (180, 0, 0), food)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        change_head_direction_to("cima")
    if keys[pygame.K_a]:
        change_head_direction_to("esquerda")        
    if keys[pygame.K_s]:
        change_head_direction_to("baixo")        
    if keys[pygame.K_d]:
        change_head_direction_to("direita")        

    if snake[0].colliderect(food):                    
        snake_last_body_part = snake[-1]            
        match snake_last_body_part.direction:
            case "cima":    
                new_body_part_x = snake_last_body_part.x
                new_body_part_y = snake_last_body_part.y + grid_size                        
            case "esquerda":    
                new_body_part_x = snake_last_body_part.x + grid_size
                new_body_part_y = snake_last_body_part.y 
            case "baixo":    
                new_body_part_x = snake_last_body_part.x
                new_body_part_y = snake_last_body_part.y - grid_size
            case "direita":    
                new_body_part_x = snake_last_body_part.x - grid_size
                new_body_part_y = snake_last_body_part.y

        new_body_part_x, new_body_part_y = check_if_new_body_out_screen(new_body_part_x, new_body_part_y)
        snake.append(Snake(new_body_part_x, new_body_part_y, grid_size, snake[-1].previous_direction))

        while True:
            if num_grids < 1:
                print("ganhooo")
                running = False
                break
                
            random_row = random.randint(1, width // grid_size)
            random_column =  random.randint(1, height // grid_size)
            if Snake((random_row-1)*grid_size, (random_column-1)*grid_size, grid_size) not in snake:                
                food = pygame.Rect((random_row - 1)*grid_size, (random_column-1)*grid_size, grid_size, grid_size)
                num_grids -= 1
                break
            

    pygame.display.flip()

pygame.quit()
