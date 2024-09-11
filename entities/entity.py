'''
Asi se importan:
from entities.entity import *

data = CF()
if type(data) == CF:
    print('Data tipo CF')
'''

# Entidad CF.dat
class CF():
    def __init__(self):
        super().__init__()
        '''
        Contiene datos del juego
        '''
        
        self.disp = [int, int]
        self.grid_square = int

        self.volume = float
        self.fps = int

        self.music = bool
        self.climate_sound = bool
        self.show_clouds = bool
        self.show_collide = bool
        self.show_sprite = bool

        self.current_level = str




# Entidad map
class Map():
    def __init__(self):
        super().__init__()
        '''
        Contiene datos del mapa
        '''
        self.list_map = list

        self.path = str
        self.next_level = str
        self.climate = str
        self.message_start = str
        self.message_end = str