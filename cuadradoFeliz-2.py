# Importar | Información de juego
from data.CF_info import *

# Importar | Objetos
from logic.pygame.CF_object import *

# Importar | Funciones especificas para este juego
from logic.pygame.CF_functions import *

# Importar | Pygame y necesario
import pygame
#import sys
from pygame.locals import *




# Establecer información del juego
pygame.display.set_caption( title )
display = pygame.display.set_mode( data_CF.disp )
clock = pygame.time.Clock()



# Fuentes de texto
size_font_normal = int(data_CF.grid_square/2)
size_font_big = int(data_CF.grid_square*2)
font_str = 'monospace'
font_normal = pygame.font.SysFont( font_str, size_font_normal )
font_big = pygame.font.SysFont( font_str, size_font_big )




# Para Escalar todo en pantalla
display_scale = pygame.Surface( (data_CF.disp[0]*1, data_CF.disp[1]*1) )



# Función color de fondo
background_color = pygame.Surface( (data_CF.disp[0], data_CF.disp[1]), pygame.SRCALPHA )
background_image = get_image(image='background')




# Función, generar un mapa a partir de un archivo de texto
class RenderMap():
    def __init__( self, x=None, y=None, path_main=None, map=None, grid_square=data_CF.grid_square ):
        '''
        Esta función en base un archivo de texto, se posicionaran objetos en la pantalla.

        Equivalencia de caracteres:
        p = Jugador
        f = Piso
        . = Espacio
        | = Limitador de camara
        [ = Escalaera horizontal Izq
        ] = Escalaera horizontal Der

        Parametros adicionales del mapa:
        $path = Directorio de trabajo, Si esta en None, se establecera uno defaul "./data/maps/"
        $next_level = Al colisionar con checkpoint del mapa se redicionara o otro mapa o se terminara el juego.
        $climate = Clima del juego.
        $message_start = Mostrar un mensaje al iniciar el mapa.
        $message_end = Mostrar un mensaje al terminar el mapa.
        '''
        super().__init__()
        
        # Player y spawn
        self.player = None
        self.player_spawn_xy = None
        
        # Obtener objeto mapa | Información necesaria del mapa
        obj_map = Map()
        read_map( obj_map, path_main=path_main, map=map)
        
        self.path = obj_map.path
        self.next_level = obj_map.next_level
        self.climate = obj_map.climate
        self.message_start = obj_map.message_start
        self.message_end = obj_map.message_end
        
        # Agregar objetos dependiendo del caracter de texto
        y_multipler = 0
        for line in obj_map.list_map:
            x_multipler = 0
            for char in line:            
                # Agregar objeto
                if char == 'p':
                    # Player
                    if self.player == None:
                        self.player_spawn_xy = [ 
                            (grid_square*x_multipler)+grid_square*0.25,
                            (grid_square*y_multipler) 
                        ]
                        self.player = Player(
                            size=grid_square,
                            position=(self.player_spawn_xy[0], self.player_spawn_xy[1])
                        )
                elif char == 'f':
                    # Piso
                    #print( (grid_square*x_multipler), (grid_square*y_multipler) )
                    Stone(
                        size=grid_square,
                        position=(
                            (grid_square*x_multipler), (grid_square*y_multipler)
                        )
                    )
                elif char == '|':
                    # Limite de la camara
                    Limit(
                        size=grid_square,
                        position=(
                            (grid_square*x_multipler), (grid_square*y_multipler)
                        )
                    )

                elif char == 'b':
                    # Caja
                    Box(
                        size=[grid_square, grid_square],
                        position=(
                            (grid_square*x_multipler), (grid_square*y_multipler)
                        )
                    )
                
                elif char == '[':
                    # Esclara horizontal Izq
                    Stair(
                        size=grid_square,
                        position=(
                            (grid_square*x_multipler), (grid_square*y_multipler)
                        ), direction='left'
                    )
                elif char == ']':
                    # Esclara horizontal Izq
                    Stair(
                        size=grid_square,
                        position=(
                            (grid_square*x_multipler), (grid_square*y_multipler)
                        ), direction='right'
                    )

                # Aumentar Coordenada x
                x_multipler += 1

            # Aumentar coordenada y
            y_multipler += 1
            print(line)
        print(x_multipler, y_multipler)
map_current = RenderMap( map='level-1' )
player = map_current.player
player_spawn_xy = map_current.player_spawn_xy




# Función tiempos de ejecución
object_player_dead = None
time_dead = data_CF.fps*4
time_count_dead = 0




# Clima
color_backgraund = GradiantColor( 
    color=[155, 168, 187], divider=16, start_with_max_power=True, time=data_CF.fps*120
)
if data_CF.show_sprite == True:
    color_backgound_transparency = 127
else:
    color_backgound_transparency = 255




# Función Scroll/Camara
scroll_float = [0,0]


# Función Scroll/Camara | Posicionar camara en donde esta el jugador
def start_camera(player):
    scroll_float = [0,0]
    scroll_float[0] += (player.rect.x -scroll_float[0] -data_CF.disp[0]/2)
    scroll_float[1] += (player.rect.y -scroll_float[1] -data_CF.disp[1]/2)
    
    return [int(scroll_float[0]), int(scroll_float[1])]

scroll_float = start_camera(player=player)



# Limite del mapa
limit_xy = [ [], [] ]
for obj in limit_objects:
    limit_xy[0].append( obj.rect.x )
    limit_xy[1].append( obj.rect.y )
limit_xy = [ max(limit_xy[0]),  max(limit_xy[1]) ]




# Función | Para establecer transparensia a los objetos
'''
Mejor, directamente cambiar la transparencia con un "set_alpha"
'''
if data_CF.show_collide == True:
    value_show_collide = 127
else:
    value_show_collide = 0

if data_CF.show_sprite == True:
    value_show_sprite = 255
else:
    value_show_sprite = 0

for sprite in transparency_all_sprites:
    sprite.transparency_collide = value_show_collide
    sprite.transparency_sprite = value_show_sprite




# Bucle
loop_game = True
while loop_game:
    # Eventos pygame, telcado, botones de ventana
    for event in pygame.event.get():
        if event.type == QUIT:
            loop_game = False
    
    
    
    
    # Mostrar fondo
    if data_CF.show_sprite == True:
        display_scale.blit( background_image, (0,0) )

    color = []
    for x in color_backgraund.current_color:
        color.append(x)
    color.append(color_backgound_transparency)
    background_color.fill( color )
    display_scale.blit( background_color, (0,0) )
    color_backgraund.update()
    
    # Función Jugador
    player.move()
    player.update()
    
    # Función Objetos que tienen que actualizarse
    # Aninaciones, Solidos.
    for obj in update_objects:
        obj.update()
        
        
    # Función objetos que limitan la camara
    not_scroll_xy = [False, False]
    for obj in limit_objects:
        not_scroll_xy = detect_limit(
            obj=obj, player=player, player_spawn_xy=player_spawn_xy,
            scroll_float=scroll_float, not_scroll_xy=not_scroll_xy,
            grid_square=data_CF.grid_square, disp_width=data_CF.disp[0], disp_height=data_CF.disp[1]
        )
                
    
    # Función Scroll/Camara
    if not_scroll_xy[0] == False:
        scroll_float[0] += (player.rect.x -scroll_float[0] -data_CF.disp[0]/2)/4

    if not_scroll_xy[1] == False:
        scroll_float[1] += (player.rect.y -scroll_float[1] -data_CF.disp[1]/2)/4

    scroll_int = [int(scroll_float[0]), int(scroll_float[1])]
    
    
    # Detectar el limite de la pantalla
    # Asi se haria
    #display_collision = obj_not_see(
    #    data_CF.disp[0]+scroll_int[0], data_CF.disp[1]+scroll_int[1], obj=obj, difference=0, reduce_positive=False
    #)      

    # Detectar si un objeto colisiona con el limite del mapa/juego 
    # Función si el jugador/personaje colisiona con el limite del mapa
    for char in char_objects:
        limit_collision = obj_not_see(
            limit_xy[0], limit_xy[1], obj=char, difference=0, reduce_positive=False
        )
        if not limit_collision == None:
            char.hp = 0
    
    # Función si se detacta que un objeto tipo item colisiona con el limite del mapa
    for item in item_objects:
        limit_collision = obj_not_see(
            limit_xy[0], limit_xy[1], obj=item, difference=0, reduce_positive=False
        )
        if not limit_collision == None:
            item.hp = -1
    
    
    # Función si el jugador muere, regresar al checkpoint
    if player.hp <= 0:
        # Reproducir sonido
        if time_count_dead == 0:
            get_sound( 'dead' ).play()
            if object_player_dead == None:
                #object_player_dead = Particle( 
                #    size=data_CF.grid_square, position=(player.rect.x -(player.rect.width*0.5), player.rect.y) 
                #)
                #object_player_dead.transparency_collide = value_show_collide
                #object_player_dead.transparency_sprite = value_show_sprite
                #object_player_dead.update()
                if data_CF.show_sprite == False:
                    object_player_dead = Player_dead(player=player, show_collide=True)
                else:
                    object_player_dead = Player_dead(player=player, show_collide=False)
        
        # Al terminarse el tiempo de visualización de muerte, restablecer en el checkpoint
        time_count_dead += 1
        if time_count_dead >= time_dead:
            time_count_dead = 0
            object_player_dead.kill()
            object_player_dead = None
            player.rect.x = player_spawn_xy[0]
            player.rect.y = player_spawn_xy[1]
            scroll_float = start_camera(player=player)
            player.hp = 100
    
    # Función | Establecer transparencia de sprites        
    for sprite in transparency_all_sprites:
        sprite.transparency_collide = value_show_collide
        sprite.transparency_sprite = value_show_sprite
    
    # Mostrar sprites
    for sprite in layer_all_sprites.sprites():
        display_scale.blit(
            sprite.surf, 
            (
                sprite.rect.x -scroll_int[0],
                sprite.rect.y -scroll_int[1]
            )
        )
    
    

    # Sección del texto del juego (Interfaz/HUD)
    text_hp = font_normal.render(
        str(player.hp), True, generic_colors('green')
    )
    display_scale.blit(
        text_hp, (
            (data_CF.disp[0])-(size_font_normal*3),
            size_font_normal
        )
    )
    
    text_stamina = font_normal.render(
        str(player.stamina), True, generic_colors('blue')
    )
    display_scale.blit(
        text_stamina, (
            (data_CF.disp[0])-(size_font_normal*3),
            size_font_normal*2
        )
    )
    
    text_score = font_normal.render(
        str(player.score), True, generic_colors('yellow')
    )
    display_scale.blit(
        text_score, (
            (data_CF.disp[0])-(size_font_normal*3),
            size_font_normal*3
        )
    )
    
    
    
    
    # Mostrar todo en la pantalla escalada
    surf = pygame.transform.scale(display_scale, data_CF.disp)
    display.blit( surf, (0,0) )

    # Fin | Mostrar todo y bloquear data_CF.fps
    pygame.display.update()
    clock.tick(data_CF.fps)

pygame.quit()