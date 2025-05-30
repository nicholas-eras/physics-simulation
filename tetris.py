import pygame
import os

pygame.init()

largura = 600
altura = 900
square_size = 50

number_rows = altura // square_size
number_cols = largura // square_size

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Cria a janela
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("MyTetris")

fundo = (30, 30, 30)
cinza = (120, 120, 120)
vermelho = (180, 0, 0)
azul = (0, 0, 180)
verde = (0, 180, 0)
roxo = (180, 0, 180)
amarelo = (180, 180, 0)

x = (largura - square_size) // 2
y = (altura - square_size) // 2

tile_types = {
    "o":{
        "blocks":[
            {
                "x_index": 0,
                "y_index": 0,
            },
            {
                "x_index": 0,
                "y_index": 1,
            },
            {
                "x_index": 1,
                "y_index": 0,
            },
            {
                "x_index": 1,
                "y_index": 1,
            },
        ],
        "y_index_offset": 1,
        "color": vermelho
    },
    "i":{
        "blocks":[
            {
                "x_index": 0,
                "y_index": 0,
            },
            {
                "x_index": 0,
                "y_index": 1,
            },
            {
                "x_index": 0,
                "y_index": 2,
            },
            {
                "x_index": 0,
                "y_index": 3,
            },
        ],
        "y_index_offset": 1,
        "color": amarelo
    },
    # "s":{
    #     "blocks":[
    #         {
    #             "x_index": -1,
    #             "y_index": 1,
    #         },
    #         {
    #             "x_index": 0,
    #             "y_index": 1,
    #         },
    #         {
    #             "x_index": 0,
    #             "y_index": 0,
    #         },
    #         {
    #             "x_index": 1,
    #             "y_index": 0,
    #         },
    #     ],
    #     "y_index_offset": 1,
    #     "color": azul
    # },
    # "l":{
    #     "blocks":[
    #         {
    #             "x_index": 0,
    #             "y_index": 0,
    #         },
    #         {
    #             "x_index": 0,
    #             "y_index": 1,
    #         },
    #         {
    #             "x_index": 0,
    #             "y_index": 2,
    #         },
    #         {
    #             "x_index": 1,
    #             "y_index": 2,
    #         },
    #     ],
    #     "y_index_offset": 1,
    #     "color": verde
    # },
    # "t":{
    #     "blocks":[
    #         {
    #             "x_index": -1,
    #             "y_index": 0,
    #         },
    #         {
    #             "x_index": 0,
    #             "y_index": 0,
    #         },
    #         {
    #             "x_index": 1,
    #             "y_index": 0,
    #         },
    #         {
    #             "x_index": 0,
    #             "y_index": 1,
    #         },
    #     ],
    #     "y_index_offset": 1,
    #     "color": roxo
    # },
}

tiles_types_list = [type for type in tile_types]

class Tile:
    tile_id = 0

    def __init__(self, cor, x_index, y_index, type):
        self.cor = cor
        self.x_index = x_index 
        self.y_index = y_index
        self.type = type
        Tile.tile_id += 1
        self.tile_id = Tile.tile_id
        self.is_moving = True
        self.tile_types_copy = tile_types[type].copy()

    def blocks(self):
        return [{"x_index": block["x_index"] + self.x_index,"y_index": block["y_index"] + self.y_index } for block in self.tile_types_copy["blocks"]]
    
    def y_index_offset(self):
        return tile_types[self.type]["y_index_offset"] + self.y_index
    
    def occupied_blocks(self):
        return [[b["x_index"], b["y_index"], self.tile_id] for b in self.blocks()]
    
    def lowest_point(self):
        return max([index["y_index"] for index in self.tile_types_copy["blocks"]]) + self.y_index
    
    def get_y_positions(self):
        return {b["y_index"] for b in self.blocks()}
    
    def __str__(self):
        print(self.blocks())
        return f"{self.tile_id}"

tiles = []

ultimo_movimento = pygame.time.get_ticks()  
tempo_unitario = 100  

rodando = True

tile_type_index = len(tiles)
def increment_tile_type(index):
    while index >= len(tiles_types_list):
        index -= len(tiles_types_list)
    while index < 0:
        index += len(tiles_types_list)
    return index

def check_line_filled(y_index):
    global tiles, occupied_blocks
    counter = 0
    blocks_to_remove = set()

    for occupied_block in occupied_blocks:
        if occupied_block[1] ==  y_index:
            counter += 1            
            blocks_to_remove.add(occupied_block[2])
        if counter == number_cols:  
            occupied_blocks = []
            for tile in tiles:
                if tile.tile_id in blocks_to_remove:
                    teste = [block for block in tile.tile_types_copy["blocks"] if block["y_index"] + tile.y_index  != y_index ]
                    if tile.tile_id == 8:
                        print(tile)
                        print(blocks_to_remove, y_index)
                        print(teste)
                    tile.tile_types_copy["blocks"] = teste
                    occupied_blocks.extend(tile.occupied_blocks())

                if tile.tile_types_copy["blocks"] == []:
                    tiles.remove(tile)

while rodando:
    #Cliques
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = evento.pos
            x_index = mouse_x // square_size
            y_index = mouse_y // square_size

            tile_type_index = len(tiles)
            tile_type_index = increment_tile_type(tile_type_index)

            tile = Tile(tile_types[tiles_types_list[tile_type_index]]["color"], x_index, y_index, tiles_types_list[tile_type_index])
            tiles.append(tile)

    #Movimento dos tiles
    agora = pygame.time.get_ticks()
    if agora - ultimo_movimento > tempo_unitario:
        occupied_blocks = []
        for tile in tiles:
            occupied_blocks.extend(tile.occupied_blocks())
            tile_can_move = []

            for block in tile.blocks():
                block_can_move = False
                block_coordinate = [block["x_index"], block["y_index"], tile.tile_id]
                block_coordinate_future = [block["x_index"], block["y_index"] + 1, tile.tile_id]    
              
                if tile.lowest_point() < number_rows - 1 and tile.is_moving:
                 
                    if block_coordinate_future[:2] in [ob[:2] for ob in occupied_blocks if ob[2] != tile.tile_id]:                                         
                        tile.is_moving = False
                        block_can_move = False
                        for y_index in tile.get_y_positions():
                            check_line_filled(y_index)

                elif not block_can_move:
                    tile.is_moving = False
                    block_can_move = False
                    for y_index in tile.get_y_positions():
                        check_line_filled(y_index)

                if tile.lowest_point() >= number_rows - 1: 
                 
                    tile.is_moving = False
                    block_can_move = False

                for y_index in tile.get_y_positions():
                    check_line_filled(y_index)
        
                if block_coordinate_future[:2] not in [ob[:2] for ob in occupied_blocks if ob[2] != tile.tile_id] and not tile.lowest_point() >= number_rows - 1:                                         
                    block_can_move = True                    

                tile_can_move.append(block_can_move)
                
            if  tile.is_moving or (all(tile_can_move) and tile_can_move != []):
                tile.y_index += 1
                tile.is_moving = True
            else:
                tile.is_moving = False

        ultimo_movimento = agora

    #Desenho
    janela.fill(fundo)
    for row in range(number_rows):
        for col in range(number_cols):
            pygame.draw.rect(janela, cinza, (col * square_size, row * square_size, square_size, square_size), 1)
    
    tile_hover = tile_types[tiles_types_list[increment_tile_type(0 if len(tiles) == 0 else tile_type_index+1)]]
    mouse_index = pygame.mouse.get_pos()[0] // square_size, pygame.mouse.get_pos()[1] // square_size
    cor_com_opacidade = (*tile_hover['color'], 128)

    tile_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)

    for block in tile_hover["blocks"]:
        tile_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(tile_surface, cor_com_opacidade, (0, 0, square_size, square_size))
        janela.blit(
            tile_surface,
            ((block["x_index"] + mouse_index[0]) * square_size,
            (block["y_index"] + mouse_index[1]) * square_size)
        )

    for tile in tiles:
        for block in tile.tile_types_copy["blocks"]:
            pygame.draw.rect(janela, tile.cor, ((block["x_index"] + tile.x_index)* square_size, (block["y_index"] + tile.y_index) * square_size, square_size, square_size))

    pygame.display.flip()
pygame.quit()
