from Modulos.pygame.CF_object import *

import pygame
#import sys
from pygame.locals import *




# Resoluciones:
# 1024x576
# 960x540
# 128x72
# Información de juego
title = 'Cuadrado Feliz 2'

disp_width = 1024
disp_height = 576
DISPLAY_SIZE = (disp_width, disp_height)
grid_square = disp_width//32

fps = 30

# Establecer información del juego
pygame.init()
pygame.display.set_caption( title )
display = pygame.display.set_mode( DISPLAY_SIZE )
clock = pygame.time.Clock()




# Sección objetos
player = Player(
    size=grid_square,
    position=(disp_width//2-grid_square//2, disp_height//2-grid_square//2)
)

Stone(
    size=grid_square,
    position=(disp_width//4-grid_square//2, disp_height//4-grid_square//2)
)




# Bucle
loop_game = True
while loop_game:
    # Eventos pygame, telcado, botones de ventana
    for event in pygame.event.get():
        if event.type == QUIT:
            loop_game = False
    
    # Mostrar fondo
    display.fill( (0, 0, 0) )
    
    # Función Jugador
    player.move()
    player.update()
    
    # Mostrar sprites
    for sprite in layer_all_sprites.sprites():
        display.blit(sprite.image, sprite.rect)

    # Fin | Mostrar todo y bloquear fps
    pygame.display.update()
    clock.tick(fps)

pygame.quit()