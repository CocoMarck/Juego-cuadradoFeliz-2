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





# Relacionadas con la rotación:
def divisor_number_list(number=0, divisor=0, multipler=1):
    '''
    Divide un valor entero o flotante a una lista
    Ejemplo: dividir 8 en cuatro, devuelve = [2,2,2,2]
    
    multipler sirve para multiplicar un valor en cada numero de la lista
    Ejemplo: dividir 8 en cuatro y multipler = -1, devuelve = [-2,-2,-2,-2]
    
    number=int, or float
    divisor=int or float
    multipler=int or float
    
    Devuelve: list
    '''
    # Dividir el numero
    number_base = number/divisor
    
    # Listar el numero
    list_number = []
    for number in range(1, divisor+1):
        list_number.append( number_base*number*multipler )
    
    # Devolver la lista de numeros
    return list_number




def rotate(rotate_number=0):
    '''
    Función que determina el valor de rotación.

    Si esta función se pone en un bucle, el valor de rotación podra cambiar constantemente.
    Ya que iria de 0 al limite positivo 360 o al limite negativo -360, y al llegar al limite ya sea el positivo o el negativo, su valor de rotación regresara a cero. (Tambien podemos llamarlos limites laterales)
    
    rotate_number = int, angulo de rotación
    
    Devuelve: rotate_number, angulo de rotación
    rotate_number, puede cambiar al entrar en esta función
    '''
    # Determinar si el angulo de rotación no es igual a cero
    if rotate_number > 0 or rotate_number < 0:
        # Eestablecer limite valor minimo y maximo de angulo de rotación a: 360 y -360
        if rotate_number > 360:
            rotate_number = 360
        elif rotate_number < -360:
            rotate_number = -360
    
        # Determinar si el valor es igual al limite minimo o al maximo, establecer el angulo en cero.
        if rotate_number == 360 or rotate_number == -360:
            rotate_number = 0
    
    # Devolver el angulo de rotación
    return rotate_number




def rotate_to_good_angle(rotate_number=0, divisor=4):
    '''
    Establecer angulo a uno bueno-predeterminado, ejemplo:
    si el angulo es menor a 90 grados, posicionar en 90 grados
    si el angulo es menor a 180 grados, posicionar en 180 grados
    si el angulo esmenor a 270 grados, posicionar en 270 grados
    si el angulo es menor a 360 grados, posicionar en 360 grados
    
    divisor = int, divide 360 grados
    rotate_number = int or float, numero actual de rotación
    
    Cambiando o no el valor de rotate_number se
    Devuelve:
    rotate_number
    '''
    # Determina si el valor de rotación actual es positivo o negativo
    multipler = 1
    if rotate_number > 0:
        multipler = 1
    elif rotate_number < 0:
        multipler = -1

    # Divisor de angulos disponibles a establecer
    # divisor = divisor
    angles = divisor_number_list( number=360, divisor=divisor, multipler=multipler )
    angle_base = angles[0]
    '''
    angle_base = 360//divisor
    angles = []
    for number in range(1, divisor+1):
        angles.append( angle_base*number*multipler )
    '''
        
    # Determinar el angulo a posicionar
    change_angle = None
    if multipler == 1:
        if rotate_number != 0 and rotate_number < angles[0]:
            if change_angle == None:
                change_angle = angles[0]
        
        for number in range(0, divisor):
            if angles[number] != angle_base:
                if rotate_number > angles[number-1] and rotate_number < angles[number]:
                    if change_angle == None:
                        change_angle = angles[number]
        
        if not change_angle == None:
            rotate_number = change_angle

    elif multipler == -1:
        if rotate_number != 0 and rotate_number > angles[0]:
            if change_angle == None:
                change_angle = angles[0]
        
        for number in range(0, divisor):
            if angles[number] != angle_base:
                if rotate_number < angles[number-1] and rotate_number > angles[number]:
                    if change_angle == None:
                        change_angle = angles[number]
        
        if not change_angle == None:
            rotate_number = change_angle

    # Devolver el valor nuevo para el angulo
    return rotate_number




def obj_rotate_image( obj, image=None, rotate_number=0, center=True):
    '''
    Función para rotar imagen, centraliza y rota de forma adecuada la imagen
    obj = pygame.sprite.Sprite()
    obj.rect = pygame.Rect
    obj.surf = image
    image = pygame.image.load
    rotate_number = int or float
    
    - Esta función depende de la funciónes: rotate
    
    Devuelve, rotate_number
    '''
    # Establecer valor de rotación de forma correcta.
    rotate_number = rotate(rotate_number=rotate_number)

    # Rotar imagen
    if rotate_number != 0:
        # Rotar imagen
        obj.surf = pygame.transform.rotate( image, rotate_number )
    else:
        # No rotar imagen
        obj.surf = image
    
    # Posicionar correctamente la imagen
    if rotate_number != 0 or rotate_number != 360:
        if center == True:
            obj.rect = obj.surf.get_rect( center=obj.rect.center )
        else:
            obj.rect = obj.surf.get_rect( )
    
    # Devolver lo necesario
    return rotate_number




def obj_rotate_image_to_good_angle(obj, image=None, rotate_number=0, divisor=4):
    '''
    Posicionar en un lugar adecuado, por ejemplo:
    si el sprite esta en un angulo menor a 90 grados, posicionar en 90 grados
    si el sprite esta en un angulo menor a 180 grados, posicionar en 180 grados
    si el sprite esta en un angulo menor a 270 grados, posicionar en 270 grados
    si el sprite este en un angulo menor a 360 grados, posicionar en 360 grados
    
    - Esta función depende de la funciónes: rotate, rotate_to_good_angle, rotate_image
    
    obj = pygame.sprite.Sprite()
    divisor = int, divide 360 grados
    rotate_number = int or float, valor de rotación actual
    obj_surf, obj_rect = pygame.Surface, pygame.Rect
    image = pygame.image.load
    
    devuelve: rotate_number
    '''
    # Rotar a un buen angulo
    rotate_number = rotate_to_good_angle(divisor=divisor, rotate_number=rotate_number)

    # Rotar imagen ya con la posicion establecida
    rotate = obj_rotate_image(
        obj=obj, image=image, rotate_number=rotate_number
    )
    
    # Devolver lo necesario
    return rotate_number




# Funciones trigoneometricas
def get_hypotenuse( x=None, y=None, root_number=True ):
    '''
    x, y (int or float) = Cateto opuesto, Cateto adyasente 
    root_number = bool, para obtener el valor real o no de la hipotenusa
    
    Devolver: x^2 + y^2
    '''
    value = (x**2 + y**2)
    if root_number == True:
        value = value**(0.5)
    return value




def get_radian( angle=None, radio=None ):
    '''
    Angulo = int or float
    Radio el circulo = int or float

    En base al angulo de devolver el radian
    '''
    return (
        ( radio*(angle/180) * 3.1416 ) / radio
    )
    
    


# Funciones multiplos
def calculate_multiplier( number_start=1, number_fin=24 ):
    '''
    Obtener el multiplicador por el cual un numero llega a otro.

    Operación muy sencilla, dividir el numero desado por llegar por el numero de incio.
    '''
    if number_start == 0:
        raise ValueError('number_start no puede ser cero')

    return number_fin / number_start