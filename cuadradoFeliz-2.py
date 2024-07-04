# Importar | Información de juego
from Modulos.pygame.CF_info import *

# Importar | Objetos
from Modulos.pygame.CF_object import *

# Importar | Pygame y necesario
import pygame
#import sys
from pygame.locals import *




# Establecer información del juego
pygame.display.set_caption( title )
display = pygame.display.set_mode( DISPLAY_SIZE )
clock = pygame.time.Clock()

# Para Escalar todo en pantalla
display_scale = pygame.Surface( (disp_width*1, disp_height*1) )




# Sección objetos
player = Player(
    size=grid_square,
    position=(disp_width//2-grid_square//2, disp_height-grid_square*8)
)

Stone(
    size=grid_square,
    position=(disp_width//2-grid_square*7.5, disp_height-grid_square*12)
)

Stone(
    size=grid_square,
    position=(disp_width//2-grid_square*7.5, disp_height-grid_square*8)
)

Stone(
    size=grid_square,
    position=(disp_width//2-grid_square//2, disp_height-grid_square*5)
)


floor_count = 0
for x in range(1, 33):
    position_x = grid_square*floor_count
    Stone(
        size=grid_square,
        position=(position_x, disp_height-grid_square)
    )
    floor_count += 1




# Función Scroll/Camara
scroll_float = [0,0]




# Bucle
loop_game = True
while loop_game:
    # Eventos pygame, telcado, botones de ventana
    for event in pygame.event.get():
        if event.type == QUIT:
            loop_game = False
    
    
    
    
    # Mostrar fondo
    display_scale.fill( (0, 0, 0) )
    
    # Función Jugador
    player.move()
    player.update()
    
    # Función Objetos que tienen que actualizarse
    # Aninaciones, Solidos.
    for obj in update_objects:
        obj.update()
    
    # Función Scroll/Camara
    scroll_float[0] += (player.rect.x -scroll_float[0] -disp_width/2)/4
    scroll_float[1] += (player.rect.y -scroll_float[1] -disp_height/2)/4
    scroll_int = [int(scroll_float[0]), int(scroll_float[1])]
    
    # Función | Para establecer transparensia a los objetos
    for sprite in transparency_all_sprites:
        sprite.transparency_collide = 0
        sprite.transparency_sprite = 255
    
    # Mostrar sprites
    for sprite in layer_all_sprites.sprites():
        display_scale.blit(
            sprite.surf, 
            (
                sprite.rect.x -scroll_int[0],
                sprite.rect.y -scroll_int[1]
            )
        )
    
    
    
    
    # Mostrar todo en la pantalla escalada
    surf = pygame.transform.scale(display_scale, DISPLAY_SIZE)
    display.blit( surf, (0,0) )

    # Fin | Mostrar todo y bloquear fps
    pygame.display.update()
    clock.tick(fps)

pygame.quit()