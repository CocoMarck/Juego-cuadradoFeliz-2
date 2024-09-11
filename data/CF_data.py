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

# file
file_CF = os.path.join( dir_data, 'CF.dat' )


def get_data_text(list_mode=False):
    if list_mode == False:
        file_text = Text_Read( file_CF, option='ModeText' )
    else:
        file_text = Text_Read( file_CF, option='ModeList' )
    return file_text



def get_data_parameters():
    '''
    Obtiene los datos de CF.dat y los devuelve en un diccionario
    '''
    # Leer texto e ignorar comentarios
    file_text = get_data_text()
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




def read_CF( CF ) -> bool:
    dict_data = get_data_parameters()

    CF.disp = dict_data['disp']
    CF.grid_square = CF.disp[0]/32
    
    CF.volume = dict_data['volume']
    CF.fps = dict_data['fps']
    
    CF.music = dict_data['music']
    CF.climate_sound = dict_data['climate_sound']
    CF.show_clouds = dict_data['show_clouds']
    CF.show_collide = dict_data['show_collide']
    CF.show_sprite = dict_data['show_sprite']
    
    CF.current_level = dict_data['current_level']
    
    return True


def save_CF( CF ) -> bool:
    save = True
    
    # Verificar que disp sa una lista de dos numeros
    if type(CF.disp) == list:
        if len(CF.disp) == 2:
            if type(CF.disp[0]) == int and type(CF.disp[1]) == int:
                # Guardar disp
                print( 'pass disp' )
            else:
                save = False
        else:
            save = False
    else:
        save = False
    
    
    # Verificar volume
    if type(CF.volume) == float:
        if CF.volume >= 0 and CF.volume <= 1:
            # Guardar volumen
            print( 'pass volume' )
        else:
            save = False
    else:
        save = False
    
    # Verificar fps
    if type(CF.fps) == int:
        if CF.fps > 0:
            # Guardar fps
            print( 'pass fps' )
        else:
            save = False
    else:
        save = False
    
    
    # Verificar boleanos
    if (
        type(CF.music) == bool and
        type(CF.climate_sound) == bool and
        type(CF.show_collide) == bool and
        type(CF.show_sprite) == bool
    ):
        # Guardar boleanos
        print( 'pass bools' )
    else:
        save = False
    
    
    # Current level
    if type(CF.current_level) == str:
        if pathlib(CF.current_level).exists():
            # Guardar nivel
            print( 'pass nivel' )
        else:
            save = False
    else:
        save = False
        
    
    # Guardar todo
    if save == True:
        CF.grid_square = CF.disp[0]/32

        # Obtener archivo
        text = get_data_text(list_mode=True)
        
        # Cambiar parametros por los nuevos
        parameters = {
            'disp': f'{CF.disp[0]}x{CF.disp[1]}', 
            'volume': CF.volume, 
            'fps': CF.fps, 
            'music': CF.music,
            'climate_sound': CF.climate_sound,
            'show_clouds': CF.show_clouds,
            'show_collide': CF.show_collide,
            'show_sprite': CF.show_sprite
        }
        new_text = ''
        for line in text:
            for param in parameters.keys():
                if ( line.replace(' ', '') ).startswith( f'{param}='):
                    line = f'{param}={parameters[param]}'
            new_text += f'{line}\n'
        
        # Escribir datos
        with open( file_CF, 'w' ) as text:
            text.write( new_text[:-1] )
        
        return True
    else:
        return False




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
    #print(parameters)

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
    #print(file_text_prefix)


    # Objeto agregar todo
    obj.path = parameters['path']
    obj.next_level = parameters['next_level']
    obj.climate = parameters['climate']
    obj.message_start = parameters['message_start']
    obj.message_end = parameters['message_end']
    
    obj.list_map = file_text_prefix

    # Devolver
    return True