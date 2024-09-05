import os
from pathlib import Path as pathlib

dir_game = pathlib().absolute()
dir_data = os.path.join(dir_game, 'data')
dir_maps = os.path.join(dir_data, 'maps')

# Subdirectorios
# dir_data es el directorio data.
dir_sprites = os.path.join(dir_data, 'sprites')
dir_audio = os.path.join(dir_data, 'audio')