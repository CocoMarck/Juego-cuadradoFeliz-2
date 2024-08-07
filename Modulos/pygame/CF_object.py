from .CF_info import *
from .CF_functions import *
from .pygame_general_function import *
import random



class Player(pygame.sprite.Sprite):
    def __init__(
        self, size=32, position=(0,0),
        show_collide=True, show_sprite=True, color_sprite=(153, 252, 152)
    ):
        super().__init__()
        
        size_ready = (size//2, size)
        
        # Collider
        surf = pygame.Surface( size_ready, pygame.SRCALPHA )
        surf.fill(color_sprite)
        self.surf = surf
        self.rect = surf.get_rect(
            topleft=position
        )
        layer_all_sprites.add(self, layer=2)
        
        # Variables de transparencia de collider y sprite
        self.transparency_collide = 255
        self.transparency_sprite = 255
        self.__transparency_sprite = self.transparency_sprite
        transparency_all_sprites.add(self)
        
        
        # Movimiento Teclas/Botones
        self.__pressed_left = K_LEFT
        self.__pressed_right = K_RIGHT
        self.__pressed_up = K_UP
        self.__pressed_down = K_DOWN
        self.__pressed_run = K_LSHIFT

        self.__pressed_jump = K_SPACE
        
        self.__key_hit_normal = K_a
        self.__key_hit_power = K_s
        self.__move_x_positive = True
        
        # Coliders adicionales
        self.collide_hit = None
        self.__hit_framesCount = 0
        
        
        # Movimiento Variables
        self.moving_xy = [0, 0]
        self.hp = 100
        self.__speed_run = size*0.3125 # Porsentaje 30.25 %
        self.__speed_walk = size*0.1250 # Porsentaje 12.50 %

        self.gravity_power = size*0.025
        self.__gravity_limit = size*0.75
        self.__gravity_current = -self.gravity_power # Negativo, para que empieze en 0 poder de gravedad
        self.__air_count = 8 # 8 Para que inicie en caida.
        self.jump_power = size*0.59
        
        self.__jump_count = 0
        self.__jump_power = size/2
        self.__jump_max_height = size*4
        self.__jumping = False
        
        
        # Sprite
        self.__sprite = pygame.sprite.Sprite()
        self.__sprite.surf = get_image('player', 0)
        self.__sprite.rect = self.__sprite.surf.get_rect( 
            topleft=(
                self.rect.x -(self.rect.width*1.5),
                self.rect.y -(self.rect.height)
            )
        )
        layer_all_sprites.add( self.__sprite, layer=1)
        self.__sprite_current_frame = 0
        self.sprite_angle = 0
        
        
        # Sonido Contador de pasos
        self.__step_count = 0
        self.__collide_in_floor = 'wait'

    
    def change_speed( self, speed=8, change_walk=False ):
        self.__speed_run = speed

        if change_walk == True:
            self.__speed_walk = speed//4
    
    
    def move(self):
        '''
        Para llamar al movimiento del jugador
        '''
        # Teclas de movimiento
        pressed_keys = pygame.key.get_pressed()
        pressed_left = pressed_keys[self.__pressed_left]
        pressed_right = pressed_keys[self.__pressed_right]
        pressed_run = pressed_keys[self.__pressed_run]

        pressed_up = pressed_keys[self.__pressed_up]
        pressed_down = pressed_keys[self.__pressed_down]

        pressed_jump = pressed_keys[self.__pressed_jump]
        
        pressed_hit_normal = pressed_keys[self.__key_hit_normal]
        pressed_hit_power = pressed_keys[self.__key_hit_power]
        
        # Accionar movimiento
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.move_jump = False
        self.__walking = False
        self.hit_normal = False
        self.hit_power = False

        if pressed_left:
            self.move_left = True
        if pressed_right:
            self.move_right = True

        if pressed_up:
            self.move_up = True
        if pressed_down:
            self.move_down = True
            
        if pressed_run:
            self.__walking = True
        
        if pressed_jump:
            self.jump()
        
        # Acciónar Golpes
        if pressed_hit_normal:
            self.hit_normal = True
        if pressed_hit_power:
            self.hit_power = True
    
    def jump(self):
        if self.__gravity_current <= 0:
            self.move_jump = False
        else:
            self.move_jump = True
            

    def update(self):
        '''
        Para que el jugador pueda interactuar
        '''
        # HP | Si la hp esta en cero:
        # Dejar de moverse y de verse
        # Dejar de interactuar con los objetos.
        if self.hp <= 0:
            dead = True
            
            self.move_left = False
            self.move_right = False
            self.move_up = False
            self.move_down = False
            self.move_jump = False
            self.__walking = False
            self.hit_normal = False
            self.hit_power = False
            
            self.__jump_count = self.__jump_max_height
            self.__gravity_current = 0
            
            self.transparency_sprite = 0
            self.__sprite.surf.set_alpha( 0 )
        else:
            self.transparency_sprite = self.__transparency_sprite
            dead = False
        
        # Variables de daño
        damage = 0
        damage_effect = False
        
        
        # Detectar si esta en el piso o no. 
        # Esto se determina dependiendo la cantidad de frames en las que el jugador esta en el aire.
        if self.__air_count <= 2: # 5 para que funcione en la resolucion mas baja "128x72"
            # En el piso | Sin gravedad
            fall = False
            if self.__collide_in_floor == 'wait':
                self.__collide_in_floor = 'yes'
            elif self.__collide_in_floor == 'yes':
                self.__collide_in_floor = 'no'
                
        else:
            # En caida | Con gravedad
            fall = True
            self.__collide_in_floor = 'wait'
        #print(self.__air_count)
        
        
        # Para establecer la velocidad actual, dependiendo si el jugador camina o no.
        if self.__walking == True:
            self.speed_current = self.__speed_walk
        else:
            self.speed_current = self.__speed_run


        # Mover al jugador
        self.moving_xy = [0, 0]
        if self.move_left == True:
            self.moving_xy[0] -= self.speed_current
            self.__move_x_positive = False
        if self.move_right == True:
            self.moving_xy[0] += self.speed_current
            self.__move_x_positive = True
        if self.move_jump == True:
            if fall == False:
                #print('Iniciar Salto')
                self.__jumping = True
                get_sound( 'jump', None ).play()
                #self.__gravity_current = -(
                    #self.rect.height*(self.gravity_power+(self.gravity_power/self.rect.height))
                    #self.rect.height*0.425
                #)


        # Gravedad | Agregar gravedad
        # Esto dependera si la función de salto no cancelo la gravedad, ya que la función de salto puede establecer la gravedad en 0
        # if dead == False:
        self.moving_xy[1] += self.__gravity_current
        #print(self.moving_xy[1])

        # Gravedad | Caida
        # Estas variables seran adicionadas a la dimención "y" del jugador "moving_xy[1]"
        if self.__gravity_current < self.__gravity_limit:
            # Gravedad dentro del limite
            self.__gravity_current += self.gravity_power
        else:
            # Gravedad supero el limite
            self.__gravity_current = self.__gravity_limit

                
        # Gravedad | Salto
        if self.__jumping == True:
            #print('saltando')
            self.__gravity_current, self.moving_xy[1] = 0, 0
            self.__jump_count += self.__jump_power
            if self.__jump_count <= self.__jump_max_height:
                self.moving_xy[1] -= self.__jump_power
                self.__jumping = True
            else:
                self.__jumping = False
        else:
            self.__jump_count = 0
        
        
        # Golpes | Tipo de golpe
        # Una lista que contiene los datos necesarios, para saber que golpe usara el jugador.
        hit_type = [None, None, None, 'on_floor']
        hit_framesMultipler = 0
        if self.moving_xy[0] > 0: # Golpe Derecha
            hit_type[1], hit_type[2] = 'dash', 'right'
            hit_framesMultipler += 0.05
        elif self.moving_xy[0] < 0: # Golpe Izquierda
            hit_type[1], hit_type[2] = 'dash', 'left'
            hit_framesMultipler += 0.05

        else:
            if self.__move_x_positive == True:
                hit_type[1], hit_type[2] = 'neutral', 'right'
            else:
                hit_type[1], hit_type[2] = 'neutral', 'left'
                
        if fall == True:
            hit_type[3] = 'jump_or_fall'
        else:
            hit_type[3] = 'on_floor'
        
        if self.move_down == True:
            hit_type[0] = 'legs'
            hit_framesMultipler += 0.5
        elif self.move_up == True:
            hit_type[0] = 'head'
            hit_framesMultipler += 0.5
        else:
            hit_type[0] = 'arms'
            hit_framesMultipler += 0.3


        # Golpes | Tiempo hasta golpear
        '''
        El tiempo hasta llegar al golpe esta basado en la multiplicación de los "fps" del juego por la variable "hit_framesMultipler".
        fps = 30
        hit_framesMultipler = 0.3
        tiempo = fps*hit_framesMultipler = 9
        '''
        if self.hit_normal == True:
            self.__hit_framesCount += 1
            self.hit_normal = False
            
            # Mover al lanzar golpe
            if hit_type[3] == 'on_floor':
                if hit_type[1] == 'dash':
                    if hit_type[2] == 'right':
                        self.moving_xy[0] = self.__speed_run*0.2
                    else:
                        self.moving_xy[0] = -1*(self.__speed_run*0.2)
                else:
                    self.moving_xy[0] = 0
                if hit_type[0] == 'head':
                    self.moving_xy[0] = 0
        else:
            if self.__hit_framesCount > 0:
                self.__hit_framesCount += 1
                self.hit_normal = False

        if self.__hit_framesCount >= 30*hit_framesMultipler:#fps*hit_framesMultipler
            self.__hit_framesCount = 0
            self.hit_normal = True

            # Mover al lanzar golpe
            if (
                hit_type[3] == 'on_floor' and
                (not hit_type[0] == 'head')
            ):
                if hit_type[1] == 'neutral':
                    if hit_type[2] == 'right':
                        self.moving_xy[0] += self.__speed_run*0.25
                    else:
                        self.moving_xy[0] -= self.__speed_run*0.25
                if hit_type[1] == 'dash':
                    if hit_type[2] == 'right':
                        self.moving_xy[0] = self.__speed_run*0.5
                    else:
                        self.moving_xy[0] = -1*(self.__speed_run*0.5)
        

        # Golpes | Crear y posicionar en medio el colider
        hit = False
        if not self.collide_hit == None:
           #if fall == True or self.hit_normal == False: #Si el jugador esta callendo/saltando
            if self.hit_normal == False:
                self.collide_hit.kill()
                self.collide_hit = None
            else:
                self.collide_hit.rect.x = self.rect.x+self.moving_xy[0]+self.collide_hit.rect.width/2
                self.collide_hit.rect.y = self.rect.y+self.moving_xy[1]

                hit = True

        else:
           #if fall == False and self.hit_normal == True: #Si el jugador esta callendo/saltando
            if self.hit_normal == True:
                size = self.rect.height//4
                self.collide_hit = hit_object( 
                    size=size, position=(
                        self.rect.x+self.moving_xy[0] + size//2,
                        self.rect.y+self.moving_xy[1]
                    ),
                    damage=1
                )
                self.collide_hit.surf.fill( (255,0,0, self.transparency_collide) )

                hit = True
        
        # Golpes | Posicionar golpes y establecer su daño.
        if hit == True:
            get_sound( 'hits', None ).play()
            # Posicionar golpe y esablecer daño
            multipler_position_xy = [0, 0]
            kill_collide_hit = False
            if hit_type[0] == 'arms':
                multipler_position_xy[1] = 0.5
                if hit_type[1] == 'neutral':
                    self.collide_hit.damage = 10
                    multipler_position_xy[0] = 3

                elif hit_type[1] == 'dash':
                    self.collide_hit.damage = 20
                    multipler_position_xy[0] = 4

            elif hit_type[0] == 'legs':
                multipler_position_xy[1] = 2.25
                if hit_type[1] == 'neutral':
                    self.collide_hit.damage = 25
                    multipler_position_xy[0] = 4

                elif hit_type[1] == 'dash':
                    self.collide_hit.damage = 40
                    multipler_position_xy[0] = 5
                    
                if hit_type[3] == 'jump_or_fall':
                    self.collide_hit.damage = self.collide_hit.damage*0.25
                    multipler_position_xy[1] = 4.75
                    multipler_position_xy[0] = multipler_position_xy[0]*0.5
                    

            elif hit_type[0] == 'head':
                self.collide_hit.damage = 30
                
                if hit_type[3] == 'jump_or_fall':
                    multipler_position_xy[1] = -2
                else:
                    multipler_position_xy[1] = -1
                
            #if hit_type[3] == 'jump_or_fall':
            #    kill_collide_hit = True

            if hit_type[2] == 'right':
                self.collide_hit.rect.x += self.collide_hit.rect.width * multipler_position_xy[0]
            elif hit_type[2] == 'left':
                self.collide_hit.rect.x -= self.collide_hit.rect.width * multipler_position_xy[0]
            self.collide_hit.rect.y += self.collide_hit.rect.width * multipler_position_xy[1]
            
            if kill_collide_hit == True:
                self.collide_hit.kill()
                hit = False
        

        # Colsion Solidos
        collided_side = collide_and_move(obj=self, obj_movement=self.moving_xy, solid_objects=solid_objects)
        
        # Dependendiendo la colisión actual, la gravedad se restablecera a 0.
        #if type(collided_side) == str:
        #    print(collided_side)
        
        if collided_side == 'bottom':
            self.__gravity_current = 0
            self.__air_count = 0
        else:
            self.__air_count += 1
        
        if collided_side == 'top':
            self.__gravity_current = 0
            
            self.__jumping = False
            self.__jump_count = 0
        
        # Colisión | Pantalla
        display_collision = obj_not_see(disp_width, disp_height, obj=self, difference=0, reduce_positive=False)
        if not display_collision == None:
            self.hp = 0
            #self.rect.x = disp_width//2
            #self.rect.y = disp_height//2
        

        # Daño | Colisionar Solido | Establecer daño al colisionar con el piso de un solido
        if collided_side == 'bottom' and self.moving_xy[1] >= self.__gravity_limit:
            damage = 5
            damage_effect = True
        

        # Sprite | Animar | Establecer sprite actual
        # Collider | Colorear | Saltar o caer
        # Sprite | Animar | Saltar o caer 
        sprite_angle = 0
        sprite_add_xy = [0, 0]
        if self.__jumping == True:
            #print('Saltando')
            self.surf.fill( generic_colors('blue', self.transparency_collide) )
            if (
                (self.move_right == False and self.move_left == False) or
                (self.moving_xy[0] == 0)
            ):
                self.__sprite.surf = get_image('player', 1)
            else:
                self.__sprite.surf = get_image('player', 3)
                sprite_angle = 20
        else:
            if fall == True:
                #print('Con gravedad')
                self.surf.fill( generic_colors('sky_blue', self.transparency_collide) )
                if (
                    (self.move_right == False and self.move_left == False) or
                    (self.moving_xy[0] == 0)
                ):
                    self.__sprite.surf = get_image('player', 2)
                else:
                    self.__sprite.surf = get_image('player', 3)
                    sprite_angle = -11
            else:
                #print('Sin gravedad')
                self.surf.fill( generic_colors('green', self.transparency_collide) )
                if (
                    (self.move_right == False and self.move_left == False) or
                    (self.moving_xy[0] == 0)
                ):
                    self.__sprite.surf = get_image('player', 0)
                else:
                    self.__sprite.surf = get_image('player', 3)
        

        # Sonido | Contador de pasos | Caida
        # Sprite | Animar | Moverse en eje x, correr o caminar.
        if fall == False and self.moving_xy[0] != 0:
            if self.__hit_framesCount == 0:
                if self.__walking == False:
                    self.__sprite_current_frame += 0.75
                else:
                    self.__sprite_current_frame += 0.25
                
                # Cambiar Angulo de sprite
                if self.__sprite_current_frame >= 8:
                    self.__sprite_current_frame = 0
                    # Reiniciar
                else:
                    # Cambiar angulo, en base al valor del "sprite_current_frame"
                    if self.__sprite_current_frame < 4:
                        sprite_angle += self.__sprite_current_frame*4
                        sprite_add_xy[1] -= self.rect.height*0.025 * self.__sprite_current_frame
                    elif self.__sprite_current_frame > 4:
                        sprite_angle -= self.__sprite_current_frame*2
                        sprite_add_xy[1] -= self.rect.height*0.0125 * self.__sprite_current_frame
    
                self.__sprite.surf = get_image('player', 3)

            # Contador de pasos
            # Contar, Basado en la velocidad el jugador
            if self.moving_xy[0] < 0:
                number_ready = (self.moving_xy[0] / self.rect.height) *-4
            else:
                number_ready = (self.moving_xy[0] / self.rect.height) *4
            self.__step_count += number_ready
        
            if self.__step_count >= 8:
                get_sound( 'steps', None ).play()
                self.__step_count = 0

        else:
            # Reiniciar contador de pasos
            self.__step_count = 0
            
        if self.__collide_in_floor == 'yes':
            get_sound( 'steps', None ).play()
        

        # Sprite | Animar | Golpear a la gente.
        if self.__hit_framesCount > 0:
            # Prepararse para dar un golpe
            if fall == True:
                self.__sprite.surf = get_image('player', 3)
                sprite_angle = -5
            else:
                self.__sprite.surf = get_image('player', 3)

        if hit == True:
            # Golpes
            if hit_type[1] == 'neutral':
                if hit_type[0] == 'arms':
                    self.__sprite.surf = get_image('player', 3)
                    sprite_angle = -11
                    sprite_add_xy[0] = self.rect.width/3
                elif hit_type[0] == 'legs':
                    self.__sprite.surf = get_image('player', 3)
                    sprite_angle = 25
                    if fall == False and self.__jumping == False:
                        sprite_add_xy[0] = self.rect.width/2
                    else:
                        sprite_angle = -sprite_angle
                        sprite_add_xy[0] = self.rect.width*0.25
                        sprite_add_xy[1] = self.rect.width*0.25

            elif hit_type[1] == 'dash':
                if hit_type[0] == 'arms':
                    self.__sprite.surf = get_image('player', 3)
                    sprite_angle = -25
                    sprite_add_xy[0] = self.rect.width*0.5

                elif hit_type[0] == 'legs':
                    self.__sprite.surf = get_image('player', 3)
                    sprite_angle = 25
                    if fall == False and self.__jumping == False:
                        sprite_add_xy[0] = self.rect.width
                    else:
                        sprite_angle = -sprite_angle
                        sprite_add_xy[0] = self.rect.width*0.5
                        sprite_add_xy[1] = self.rect.width*0.5
                    
            if hit_type[0] == 'head':
                self.__sprite.surf = get_image('player', 3)
                sprite_angle = 2
                sprite_add_xy[1] = -self.rect.height*0.25
        
        # Sprite | Voltear
        if self.__move_x_positive == True:
            self.__sprite.surf = pygame.transform.flip( self.__sprite.surf, False, False )
        else:
            self.__sprite.surf = pygame.transform.flip( self.__sprite.surf, True, False )
            sprite_angle = -sprite_angle
            sprite_add_xy[0] = - sprite_add_xy[0]
        
        # Sprite | Posicionar
        if sprite_angle != 0:
            # Sprite | Rotar imagen, solo si el agulo no es cero.
            obj_rotate_image(
                obj=self.__sprite,
                image=self.__sprite.surf,
                rotate_number=sprite_angle,
                center=False
            )
            
        # Sprite | Obtener rectangulo actual, debido a constantes cambios de dimenciones
        self.__sprite.rect = self.__sprite.surf.get_rect()
        
        # Sprite | Centrar en x el sprite en el collider
        # Sprite | Añadir sprite_add_xy, ya que esto permite cambiar la posicion dependiendo de la animación
        self.__sprite.rect.x = (
            self.rect.x + sprite_add_xy[0]
            -(self.__sprite.rect.width -self.rect.width)/2
        )
        self.__sprite.rect.y = (
            self.rect.y + sprite_add_xy[1]
            -(self.__sprite.rect.height -self.rect.height)/2
        )
        

        # Sprite | Graverdad alta | Rotar imagen
        if self.__gravity_current == self.__gravity_limit:
            self.rotate(multipler=10)
        else:
            self.sprite_angle = 0
        
        
        # Daño | Establecer daño y hacer o no hacer el efecto de daño
        if damage != 0:
            self.hp -= damage
            if damage_effect == True:
                # Mover al jugador aleatoriamente:
                # Su valor de movimiento sera en base al valor de altura multiplicado por daño probocado multiplicado por 0.01. Ya que el hp inicial es de 100, y 100 por 0.01 = 1
                # Ejemplo: 32 * (10*0.01) = 3.2
                move_value = self.rect.height*(damage*0.01)
                self.moving_xy = [ 
                    random.choice([move_value,-move_value]) , random.choice([move_value,-move_value])
                ]

                # Colsion Solidos | Moverse debido al daño recivido
                collided_side = collide_and_move(obj=self, obj_movement=self.moving_xy, solid_objects=solid_objects)
                
                if collided_side == 'bottom':
                    self.__gravity_current = 0
                    self.__air_count = 0
                else:
                    self.__air_count += 1
                
                if collided_side == 'top':
                    self.__gravity_current = 0
                    
                    self.__jumping = False
                    self.__jump_count = 0

            get_sound( 'hits', None ).play()
            
            
            
        # Sprite | Establecer transparencia al sprite
        self.__sprite.surf.set_alpha( self.transparency_sprite )

    
    
    def rotate(self, multipler=1):
        image=get_image('player', 3)
        if self.__move_x_positive == True:
            value = -1
        else:
            value = 1
            image = pygame.transform.flip( image, True, False )

        self.sprite_angle = obj_rotate_image( 
            obj=self.__sprite, image=image, rotate_number=self.sprite_angle, center=True
        ) 
        self.sprite_angle += value*multipler





class Stone(pygame.sprite.Sprite):
    def __init__(self, size=grid_square, position=(0,0)):
        super().__init__()
        
        # Transparencias
        self.transparency_collide = 255
        self.transparency_sprite = 255
        
        # Collider
        size_ready = (size, size)
        self.surf = pygame.Surface( size_ready, pygame.SRCALPHA )
        self.surf.fill( generic_colors('grey', self.transparency_collide) )
        self.rect = self.surf.get_rect(
            topleft=position
        )
        layer_all_sprites.add(self, layer=2)
        transparency_all_sprites.add(self)
        solid_objects.add(self)
        update_objects.add(self)
        
        # Sprite
        self.__sprite = pygame.sprite.Sprite()
        self.__sprite.surf = get_image('stone')
        self.__sprite.rect = self.rect
        layer_all_sprites.add(self.__sprite, layer=0)
        
        # Estadisticas del solido
        self.hp = 200
    
    def update(self):
        self.surf.fill( generic_colors('grey', self.transparency_collide) )

        destroy = False
        if self.hp <= 0:
            destroy = True
        
        # Quitar vida al solido, solo si los golpes destruyen solidos.
        # Destruir solido si se le acabo el hp.
        if destroy == False:
            for obj in damage_objects:
                if self.rect.colliderect( obj.rect ):
                    if obj.destroy_solids == True:
                        self.hp -= obj.damage
                        print(self.hp)
        else:
            self.__sprite.kill()
            self.kill()




class hit_object(pygame.sprite.Sprite):
    def __init__(self, size=8, position=(0,0), damage=4):
        super().__init__()
        '''
        Collider que hace daño, sus parametros determinaran su daño y a que le hace daño.
        '''
        
        size_ready = (size, size)

        self.surf = pygame.Surface( size_ready, pygame.SRCALPHA )
        self.rect = self.surf.get_rect( topleft=position )
        self.surf.fill( (255, 0, 0) )
        self.damage = damage
        self.destroy_solids = True
        layer_all_sprites.add(self, layer=2)
        update_objects.add(self)
        damage_objects.add(self)
    
    def update(self):
        for solid in solid_objects:
            if self.rect.colliderect( solid.rect ):
                print(f'Quita -{self.damage}')




class box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        '''
        Una caja que puede rotarse y ser destruida a trancazos.
        '''
        self.sprite_angle = 0
    
    
    def update(self):
        pass
    
    def rotate(self):
        pass




# Grupos de sprites
layer_all_sprites = pygame.sprite.LayeredUpdates()
transparency_all_sprites = pygame.sprite.Group()
update_objects = pygame.sprite.Group()
anim_objects = pygame.sprite.Group()

solid_objects = pygame.sprite.Group()
damage_objects = pygame.sprite.Group()