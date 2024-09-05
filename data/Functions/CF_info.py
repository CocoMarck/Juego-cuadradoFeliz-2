import os, pygame
from .CF_data import *

pygame.init()

# Resoluciones compatibles (16:9):
# 1920x1080 Funciona
# 1024x576 Funciona
# 960x540 Funciona
# 512x288
# 384x216
# 256x144
# 1440x810 (Bugeado, Salta como 1% mas alto el jugador)
# 480x270 (Bugeado, Salta como 1% mas alto el jugador, camina a la izquierda mas rapido que a la derecha)
# 128x72 (Bugeado, No camina a la derecha: x positivo)
# Información de juego
title = 'Cuadrado Feliz 2'

disp_width, disp_height = 1024,576
DISPLAY_SIZE = (disp_width, disp_height)
grid_square = disp_width/32

fps = 30
volume = 0.05


# Para mostrar o no sprite
show_collide = False
show_sprite = True
