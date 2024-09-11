from data.CF_info import *
from data.CF_data import *
from logic.Modulo_Text import *
from logic.pygame.pygame_general_function import *
import pygame, os, random




# Sonidos
all_sounds = {
    'steps':
    [
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/steps/step-1.ogg') ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/steps/step-2.ogg') ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/steps/step-3.ogg') )
    ],

    'jump':
    pygame.mixer.Sound( os.path.join(dir_audio, 'effects/jump.ogg') ),
    
    'hits':
    [
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/hits/hit-1.ogg') ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/hits/hit-2.ogg') ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/hits/hit-3.ogg') )
    ],
    
    'hits-missed':
    [
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/hits_missed/hit-missed_1.ogg') ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/hits_missed/hit-missed_2.ogg') ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/hits_missed/hit-missed_3.ogg') )
    ],
    
    'dead':
    [
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/dead/dead-1.ogg') ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/dead/dead-2.ogg') ),
        pygame.mixer.Sound( os.path.join(dir_audio, 'effects/dead/dead-3.ogg') )
    ],
}
for key in all_sounds.keys():
    sound_or_sounds = all_sounds[key]
    if type( sound_or_sounds ) == list:
        for sound in sound_or_sounds:
            sound.set_volume( data_CF.volume )
    else:
        sound_or_sounds.set_volume( data_CF.volume )


# Sonido | Función para devolver un sonido
def get_sound( sound=None, number=None ):
    # Detectar que los parametros esten correctos
    error = False
    if sound == None:
        error = True
    else:
        sound_good = False
        for key in all_sounds.keys():
            if sound == key:
                if sound_good == False:
                    sound_good = True
            
        if sound_good == False:
            error = True

    if not number == None:
        if number < 0:
            error = True
    
    if error == True:
        sound = 'steps'
        number = 0
    
    # Devolver sonido | Establecer sonido final
    if type( all_sounds[sound] ) == list:
        if number == None:
            sound_final = random.choice( all_sounds[sound] )
        else:
            sounds_number = len(all_sounds)-1
            if number > sounds_number:
                number = sounds_number
            sound_final = all_sounds[sound][number]
    else:
        sound_final = all_sounds[sound]
    
    return sound_final




# Sprites
all_images = {}

all_images.update( {
    'background':
    pygame.transform.scale(
        pygame.image.load( os.path.join(dir_sprites, 'background.png') ), 
        (data_CF.disp[0], data_CF.disp[1])
    ),

    'stone':
    pygame.transform.scale(
        pygame.image.load( os.path.join(dir_sprites, 'floor/stone.png') ), 
        (data_CF.grid_square, data_CF.grid_square)
    ),
    
    'elevator':
    pygame.transform.scale(
        pygame.image.load( os.path.join(dir_sprites, 'floor/elevator.png') ), 
        (data_CF.grid_square, data_CF.grid_square)
    ),
    
    'box':
    pygame.transform.scale(
        pygame.image.load( os.path.join(dir_sprites, 'floor/box.png') ), 
        (data_CF.grid_square, data_CF.grid_square)
    ),
    
    'player':
    Anim_sprite_set(
        sprite_sheet = pygame.transform.scale(
            pygame.image.load( os.path.join(dir_sprites, 'player/player.png') ),
            (data_CF.grid_square*4, data_CF.grid_square)
        ),
        current_frame=None
    ),
    
    'player_hit-type':
    Anim_sprite_set(
        sprite_sheet = pygame.transform.scale(
            pygame.image.load( os.path.join(dir_sprites, 'player/player_hit-type.png') ),
            (data_CF.grid_square*8, data_CF.grid_square*2)
        ),
        current_frame=None
    ),
    
    'item-coin':
    pygame.transform.scale(
        pygame.image.load( os.path.join(dir_sprites, 'items/coin.png') ),
        (data_CF.grid_square, data_CF.grid_square)
    )

} )

def get_image(image=None, number=None):
    # Detectar si la imagen es buena o no
    error = False
    if image == None:
        error = True
    else:
        image_good = False
        for key in all_images.keys():
            if key == image:
                if image_good == False:
                    image_good = True
        
        if image_good == False:
            error = True
    
    if not number == None:
        if number < 0:
            error = True
    
    if error == True:
        image = 'player_not-move'
        number = 0
    
    
    # Devolver imagen | Establecer imagen
    if type(all_images[image]) == list:
        image_number = len( all_images[image] ) -1
        if not number == None:
            if number > image_number:
                number = image_number
            final_image = all_images[image][number]
        else:
            final_image = random.choice(
                all_images[image]
            )
    else:    
        final_image = all_images[image]

    return final_image




# Funciones de colisiones
def collision_detect(rect, grids):
    '''
    Si rect colisiona con uno o mas coliders/grids, estas se agregaran a la lista de hits "hit_list"
    Devuelve una lista
    '''
    hit_list = []
    for grid in grids:
        if rect.colliderect(grid):
            hit_list.append(grid)
    return hit_list


def collision_move_original(rect, movement, grids):
    ''''
    Cuando "rect" colisione con algun "grid", dependiendo de la dirección de su colision, el "rect" se posicionara de forma inversa a la dirección de colisión.
    - Si rect colisiona del lado derecho del tile, este se movera a su lado izquierdo.
    - Si rect colisiona del lado izquiedo del tile, este se movera a su lado derecho.
    - Si rect colisiona del lado inferior del tile, este se movera a su lado superior.
    - Si rect colisiona del lado superior del tile, este se movera a su lado inferior.
    '''
    collision_types = {'top':False, 'bottom':False, 'right':False, 'left': False}

    # Movimiento dimención x
    rect.x += movement[0]
    hit_list = collision_detect(rect, grids)
    for grid in hit_list:
        if movement[0] > 0:
            rect.right = grid.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = grid.right
            collision_types['left'] = True
    
    # Movimiento dimención y
    rect.y += movement[1]
    hit_list = collision_detect(rect, grids)
    for grid in hit_list:
        if movement[1] > 0:
            rect.bottom = grid.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = grid.bottom
            collision_types['top'] = True
    
    return rect, collision_types




def collide_and_move( obj=None, obj_movement=[0,0], solid_objects=None):
    '''
    Esta función collisiona y mueve un objeto tipo "pygame.sprite.Sprite()"
    
    Para esta función se necesita del siguiente objeto, con estos atributos:
    Objeto tipo "pygame.sprite.Sprite"
    self.rect
    Este objeto lo utilizaremos para el parametro:
    obj=objeto

    Tambien se necesita una lista de dos valores, que haran la función de movimiento del jugador.
    obj_movement = [0, 0]
    El primer valor de la lista seria el movimiento "x" y el segundo valor de la lista el movimiento "y"
    
    solid_objects, es una lista de objetos que teinen los siguientes atributos:
    Objetos tipo pygame.sprite.Sprite()
    self.rect
    solid_objects = lista_de_objetos
    


    Cuando "obj" colisione con algun "solid_objects", dependiendo de la dirección de su colision, el "obj" se posicionara de forma inversa a la dirección de colisión.
    Primero obj se mueve en dirección "x" si obj_movement[0] es menor o meyor a cero.
    Y se determina lo siguiente:
    - Si obj colisiona del lado derecho del solid_object, este se movera a su lado izquierdo.
    - Si obj colisiona del lado izquiedo del solid_object, este se movera a su lado derecho.
    
    Despues obj se mueve en dirección "y" si obj_movement[1] es menor o meyor a cero, y se determina lo siguiente:
    Y se determina lo siguiente:
    - Si obj colisiona del lado inferior del solid_object, este se movera a su lado superior.
    - Si obj colisiona del lado superior del solid_object, este se movera a su lado inferior.
    '''
    collided_side = None

    obj.rect.x += obj_movement[0]
    for solid in solid_objects:
        if obj.rect.colliderect( solid.rect ):
            if obj_movement[0] > 0:
                obj.rect.right = solid.rect.left
                collided_side = 'right'
            elif obj_movement[0] < 0:
                obj.rect.left = solid.rect.right
                collided_side = 'left'
        
    obj.rect.y += obj_movement[1]
    for solid in solid_objects:
        if obj.rect.colliderect( solid.rect ):
            if obj_movement[1] > 0:
                obj.rect.bottom = solid.rect.top
                collided_side = 'bottom'
            elif obj_movement[1] < 0:
                obj.rect.top = solid.rect.bottom
                collided_side = 'top'
    
    return collided_side




def detect_limit(
    obj, player, player_spawn_xy=None, scroll_float=None,
    not_scroll_xy=None, grid_square=None, disp_width=None, disp_height=None
):
    '''
    Función objetos que limitan la camara/scroll, para detectar la posición del limite y detectar si el scroll esta sobrepasando el limite y entonces parar el scroll.
    '''
    # Limite positivo x
    if obj.rect.x >= disp_width:
        if scroll_float[0] >= obj.rect.x-(disp_width):
            if player.moving_xy[0] < 0:
                # Cuando quiere salir del limite positivo
                if not player.rect.x <= obj.rect.x-(disp_width/2):
                    not_scroll_xy[0] = True
            else:
                # Cuando llega al limite positivo
                not_scroll_xy[0] = True
                
    # Limite negativo x
    if obj.rect.x <= 0:
        if scroll_float[0] <= obj.rect.x:
            if player.moving_xy[0] > 0:
                # Cuando quiere salir del limite negativo
                if not player.rect.x >= obj.rect.x+disp_width/2:
                    not_scroll_xy[0] = True
            else:
                # Cuando llega al limite negativo
                not_scroll_xy[0] = True
    
    
    # Limite positivo y
    if obj.rect.y >= disp_height-grid_square:
        if scroll_float[1] >= obj.rect.y-(disp_height):
            if player.moving_xy[1] < 0:
                # Cuando quiere salir del limite positivo
                if not player.rect.y <= obj.rect.y-(disp_height/2):
                    not_scroll_xy[1] = True
            else:
                # Cuando llega al limite positivo
                not_scroll_xy[1] = True
                
    # Limite negativo y
    if obj.rect.y <= 0:
        if scroll_float[1] <= obj.rect.y:
            if player.moving_xy[1] > 0:
                # Cuando quiere salir del limite negativo
                if not player.rect.y >= obj.rect.y+disp_height/2:
                    not_scroll_xy[1] = True
            else:
                # Cuando llega al limite negativo
                not_scroll_xy[1] = True

    # Restablecer camara al spawn
    # volver a anlizar los limites, para que se acomode al 100% bien
    if player.rect.x == player_spawn_xy[0] and player.rect.y == player_spawn_xy[1]:
        not_scroll_xy = [False, False]
    
    # Devolver el mover el scroll en x o en y.
    return not_scroll_xy




# Funcion del clima
class GradiantColor():
    def __init__(
        self, color=[155, 168, 187], transparency=255, divider=2, start_with_max_power=False, time=0
    ):
        '''
        Divide un color rgb y con la funcion update, actualiza el color a uno de la lista, dependiendo si se ánade mas color, o se disminulle el color. Esto esta pensado para utilizarse en un bucle.
        
        color = [int, int, int] (min 0, max 255)
        divider = int or float (recomend int)
        start_with_max_power = bool
        time = int
        '''
        super().__init__()
        
        # Listar colores | Obtener color de inico y color de fin
        self.__color_list = divider_color_rgb( color=color, divider=divider )
        self.__number_list = len(self.__color_list)-1
        self.start_color = self.__color_list[0]
        self.end_color = self.__color_list[self.__number_list]
        
        # Reducir colores
        if start_with_max_power == True:
            self.__color_number = self.__number_list
            self.__reduce_color = True
        else:
            self.__color_number = 0
            self.___reduce_color = False
        self.current_color = self.__color_list[ self.__color_number ]
        
        # Tiempo de ejecución
        self.__current_time = 0

        self.__time = calculate_multiplier( number_start=divider, number_fin=time )
    
    def update(self):
        # Tiempo de ejecución
        self.__current_time += 1
        if self.__current_time >= self.__time:
            self.__current_time = 0
            
            # Cambiar color
            self.current_color = self.__color_list[self.__color_number]
            
            # Aumentar color
            if self.__reduce_color == False:
                self.__color_number += 1
                if self.__color_number >= self.__number_list:
                    self.__reduce_color = True

            # Disminuir color
            elif self.__reduce_color == True:
                self.__color_number -= 1
                if self.__color_number <= 0:
                    self.__reduce_color = False





def divider_color_rgb(color=[255,255,255], divider=2):
    '''
    Dividir un color rgb, en varios colores rgb.
    color = [int, int, int] (min 0, max 255)
    divider = int or float (recomend int)
    '''
    # Detectar que el color rgb sea una lita aceptable, para cada valor en la lista
    number = 0
    for c in color:
        if c < 0 or c > 255:
            color[index] = 255
        number += 1

    if number < 0 or number > 3:
        color = [255, 255, 255]
    
    # Detectar que divisor sea un valor aceptable, para cada valor en el rgb
    for c in color:
        if divider < 0 or divider> c:
            divider = 1
        else:
            pass
    
    # Dividir valores | Lista de colores rgb
    color_list = []

    multipler = 0
    for x in range(0, divider):
        multipler += 1

        # Agregar nuevo color rgb a la lista de colores final.
        new_color = []
        for c in color:
            new_color.append( (c/divider)*multipler )
        color_list.append( new_color )
    
    # Devuelve la lista de colores rgb final
    return color_list


#print( divider_color_rgb(color=[155, 168, 187], divider=16) )





def detect_collision( obj, obj_movement=[0,0], colliders=None, dimension=None ):
    '''
    Detecta la direccion en la que colisiona un objeto con otro
    Y Dependiendo de eso, posiciona el jugador en un lado o en otro.
    '''
    collided_side = None
    
    if dimension == 'x' or dimension == None:
        for collide in colliders:
            if obj.rect.colliderect( collide.rect ):
                if obj_movement[0] > 0:
                    collided_side = 'right'
                elif obj_movement[0] < 0:
                    collided_side = 'left'

    if dimension == 'y' or dimension == None:
        for collide in colliders:
            if obj.rect.colliderect( collide.rect ):
                if obj_movement[1] > 0:
                    collided_side = 'top'
                elif obj_movement[1] < 0:
                    collided_side = 'bottom'
                    if obj.rect.y > collide.rect.y+obj.rect.height:
                        obj.rect.bottom = collide.rect.bottom+obj.rect.height
    
    return collided_side