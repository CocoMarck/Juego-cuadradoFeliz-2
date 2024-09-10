from entities.entity import *
from logic.Modulo_Text import *

import os
from pathlib import Path as pathlib

dir_game = pathlib().absolute()
dir_data = os.path.join(dir_game, 'resources')
dir_maps = os.path.join(dir_data, 'maps')

# Subdirectorios
# dir_data es el directorio data.
dir_sprites = os.path.join(dir_data, 'sprites')
dir_audio = os.path.join(dir_data, 'audio')



def get_CFdat():
    '''
    Obtiene los datos de CF.dat y los devuelve en un diccionario
    '''
    # Leer texto e ignorar comentarios
    file_text = Text_Read( os.path.join( dir_data, 'CF.dat' ), option='ModeText' )
    file_text = Ignore_Comment( text=file_text, comment='#' )
    file_text = file_text.replace( ' ', '' ).lower()
    
    # Establecer lineas en diccionario
    dict_text = {}
    for line in file_text.split('\n'):
        line_split = line.split('=')
        if len(line_split) == 2:
            value = line_split[1]
            if line_split[1] == 'true':
                value = True
            elif line_split[1] == 'false':
                value = False
            else:
                if line_split[0] == 'disp':
                    disp = line_split[1].split('x')
                    value = [int(disp[0]), int(disp[1])]
                elif line_split[0] == 'fps':
                    value = int(line_split[1])
                elif line_split[0] == 'volume':
                    value = float(line_split[1])
            dict_text.update( {line_split[0] : value} )
    
    # Devolver el diccionario
    return dict_text
#input( get_CFdat() )



def read_CF( CF ):
    CF.disp = [1280, 720]
    CF.volume = 0.02
    CF.fps = 30
    CF.music = True
    CF.climate_sound = True
    CF.show_clouds = True
    CF.show_collide = False
    CF.current_level = None


def save_CF( CF ):
    print( CF )


def read_map( obj, path_main=None, map=None):
    # Leer archivo de texto
    prefix_map = 'cf_map'
    if map.startswith(prefix_map):
        if len(map)-3 >= 0:
            list_map = map.split()
            if (
                f'{list_map[len(map)-2]}{list_map[len(map)-1]}{list_map[len(map)]}' == 'txt'
            ):
                pass
    else:
        map = f'{prefix_map}_{map}.txt'
    
    if path_main == None:
        file_text = Text_Read( os.path.join( dir_maps, map ), option='ModeText' )
    else:
        file_text = Text_Read( os.path.join( path_main, map), option='ModeText' )


    # Ignorar comentarios y parametros tipo "$Parameter". 
    file_text_ignore = Ignore_Comment( text=file_text, comment='#' )
    

    # Agregar parametros en un diccionario.
    parameters = {}
    for line in file_text_ignore.split('\n'):
        if line.startswith('$'):
            with_value = False
            for char in line:
                if char == '=':
                    with_value = True

            if with_value == True:
                param = line.split('=')
                
                split_char = None
                for char in param[1]:
                    if char == ' ':
                        pass
                    else:
                        if split_char == None:
                            split_char = char
                param[1] = f'{split_char}{param[1].split(split_char)[1]}'
                        
                parameters.update(
                    {param[0].replace('$', '').replace(' ', '') : param[1]} 
                )
    print(parameters)

    # Ignorar comentarios y parametros tipo "$Parameter". 
    file_text_ignore = Ignore_Comment( text=file_text_ignore, comment='$' )
    file_text_ignore = file_text_ignore.split('\n')

    # Solo aceptar caracteres relacionados con los objetos
    '''
    | = Limitación
    . = Espacio
    p = Player
    f = Plataforma, Piso
    b = Caja
    [ = Escalara horizontal Izq
    ] = Escalara horizontal Der
    '''
    prefix_obj = '|.pfb[]'
    file_text_prefix = []
    for line in file_text_ignore:
        new_line = ''
        for char in line:
            for prefix_char in prefix_obj:
                if char == prefix_char:
                    new_line += char
        if not new_line == '':
            file_text_prefix.append(new_line)
    print(file_text_prefix)


    # Objeto agregar todo
    obj.path = parameters['path']
    obj.next_level = parameters['next_level']
    obj.climate = parameters['climate']
    obj.message_start = parameters['message_start']
    obj.message_end = parameters['message_end']
    
    obj.list_map = file_text_prefix

    # Devolver
    return True