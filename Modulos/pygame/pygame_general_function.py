import os, sys
from pathlib import Path as pathlib


import pygame, random
from pygame.locals import *




def obj_not_see(disp_width=None, disp_height=None, obj=None, difference=0, reduce_positive=False):
    '''
    Para detectar si esta en la pantalla el sprite, si esta fuera de la pantalla, devolvera un string indicador de la posición en la que no se ve. Y si esta adentro de la pantalla, devolvera un None.
    disp_width  =int, Ancho de pantalla
    disp_height =int, Altura de pantalla
    obj         =pygame.sprite.Sprite(), Objeto tipo sprite, con atributo rect

    difference  =int, Añade/Dismunille, la altura y anchura de pantalla establecida. 
    difference, es un parametro opcional. Los demas son necesarios
    
    '''
    # Diferencia para numero positivo (Ancho positivo, o Alto positivo de pantalla)
    if difference >= 0:
        if reduce_positive == True:
            difference_for_positive = -(round(difference*0.75))
        else:
            difference_for_positive = difference

    else:
        difference_for_positive = difference*2
    
    # Devolver un string si se detecta que se sobrepaso la pantalla
    direction = None
    if obj.rect.x > disp_width +(difference_for_positive):
        direction = 'width_positive'
    elif obj.rect.x < 0 -(difference):
        direction = 'width_negative'
    
    elif obj.rect.y > disp_height +(difference_for_positive):
        direction = 'height_positive'
    elif obj.rect.y < 0 -(difference):
        direction = 'height_negative'
    return direction




def generic_colors(color='green', transparency=255):
    '''
    Colores que considero genericos, estan bueno tenerlos en una función y obtenerlos de una forma rapida y consistente.
    
    color, Un string, escribe el nombre del color en ingles y minuscilas y te debolvera su valor rgb.
    colores: red, green, blue, white, black, grey, sky_blue, yellow.
    
    transparency, sirve para cambiar su transparencia; de 0 a 255, entre mas alto mas opaco. (Opcional)
    '''
    # Principales
    if color == 'red':
        return(255, 0, 0, transparency)
    if color == 'green':
        return (0, 255, 0, transparency)
    elif color == 'blue':
        return (0, 0, 255, transparency)

    # Escala de grises
    elif color == 'white':
        return (255, 255, 255, transparency)
    elif color == 'black':
        return (0, 0, 0, transparency)
    elif color == 'grey':
        return (128, 128, 128, transparency)
    
    # Otros
    elif color == 'sky_blue':
        return (0, 255, 255, transparency)
    
    elif color == 'yellow':
        return (255, 255, 0, transparency)




class Anim_sprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, position=(0,0) ):
        super().__init__()
        '''
        Para utilizar la animación de los sprites.
        '''
        
        # Cargar la hoja de sprites
        # Sprite sheet tiene que ser un pygame.image.load()
        rect_sheet = sprite_sheet.get_rect()
        
        # Dimenciones de cada cuadro de animación
        self.frame_square = rect_sheet.height
        self.frame_number = rect_sheet.width//rect_sheet.height
        
        # Lista para almacenar los cuardos de animación
        self.frames = []
        
        # Recortar la hoja de sprites en cuadros individuales
        for i in range(self.frame_number):
            frame = sprite_sheet.subsurface( 
                (i*self.frame_square, 0, self.frame_square, self.frame_square) 
            )
            self.frames.append(frame)
        
        # Índice para rastrear el cuadro de animación actual
        self.current_frame = 0
        
        # Configurar la imagen inicial
        self.surf = self.frames[self.current_frame]
        
        # Mostrar
        surf = pygame.Surface( (self.frame_square, self.frame_square) )
        self.rect = surf.get_rect( topleft=position )
    
    def anim(self):
        # Actualizar la animación
        self.current_frame = (self.current_frame +1) % len(self.frames)
        self.surf = self.frames[self.current_frame]
        



def Anim_sprite_set(sprite_sheet=None, current_frame=None):
    '''
    Establecer un frame de un srpite tipo animación
    '''
    # Cargar la hoja de sprites
    # Sprite sheet tiene que ser un pygame.image.load()
    rect_sheet = sprite_sheet.get_rect()
    
    # Dimenciones de cada cuadro de animación
    frame_square = rect_sheet.height
    frame_number = rect_sheet.width//rect_sheet.height
    
    # Lista para almacenar los cuardos de animación
    frames = []
    
    # Recortar la hoja de sprites en cuadros individuales
    for i in range(frame_number):
        frame = sprite_sheet.subsurface( 
            (i*frame_square, 0, frame_square, frame_square) 
        )
        frames.append(frame)
    
    # Índice para rastrear el cuadro de animación actual "current_frame"
    # Configurar la imagen inicial
    if not frames == []:
        if current_frame == None:
            return frames
        else:
            return( frames[current_frame] )




def Split_sprite(sprite_sheet, parts=4):
    """
    Divide un sprite en partes iguales.
    """
    parts = parts//2
    # Sprite sheet tiene que ser un pygame.image.load()
    rect_sheet = sprite_sheet.get_rect()

    # Dimensiones de cada cuadro de animación
    frame_width = rect_sheet.width // parts
    frame_height = rect_sheet.height // parts

    # Lista para almacenar los cuadros divididos
    frames = []

    # Recortar la hoja de sprites en cuadros individuales
    number = -1
    for _ in range(parts):
        number += 1
        for x in range(parts):
            frame = sprite_sheet.subsurface( 
                (x*frame_width, (frame_height*number), frame_width, frame_height) 
            )
            frames.append(frame)

    return frames



def obj_detect_collision(obj_main, obj_collide):
    collision_direction = None
    if obj_main.rect.y == obj_collide.rect.y-(obj_main.rect.height):
        # Colision arriba
        collision_direction = 'collide_up'
    elif obj_main.rect.y == obj_collide.rect.y+(obj_collide.rect.height):
        # Colision abajo
        collision_direction = 'collide_down'
    elif obj_main.rect.x == obj_collide.rect.x-(obj_main.rect.width):
        # Colision izquierda
        collision_direction = 'collide_left'
    elif obj_main.rect.x == obj_collide.rect.x+(obj_collide.rect.width):
        # Collide derecha
        collision_direction = 'collide_right'
    
    return collision_direction




