import pygame
from .CF_functions import *




class Player(pygame.sprite.Sprite):
    def __init__(
        self, size=32, position=(0,0),
        show_collide=False, show_sprite=True, color_sprite=(153, 252, 152)
    ):
        super().__init__()
        
        size_ready = (size//2, size)
        
        # Collider
        surf = pygame.Surface( size_ready, pygame.SRCALPHA )
        surf.fill(color_sprite)
        self.image = surf
        self.rect = surf.get_rect(
            topleft=position
        )
        layer_all_sprites.add(self, layer=1)
        
        
        # Movimiento Teclas/Botones
        self.__pressed_left = pygame.K_LEFT
        self.__pressed_right = pygame.K_RIGHT
        self.__pressed_up = pygame.K_UP
        self.__pressed_down = pygame.K_DOWN
        self.__pressed_run = pygame.K_LSHIFT

        self.__pressed_jump = pygame.K_SPACE
        
        
        # Movimiento Variables
        self.moving_xy = [0, 0]
        self.__speed_run = size//2
        self.__speed_walk = size//8

        self.gravity_power = size*0.05
        self.__gravity_limit = size*0.75
        self.__gravity_current = 0
        self.__air_count = 0
        self.jump_power = size*0.59
        
        self.__jump_count = 0
        self.__jump_power = size//2
        self.__jump_max_height = size*4
        self.__jump_ready = False
        self.__jump_continue = False

    
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
        
        # Accionar movimiento
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.move_jump = False
        self.__walking = False

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
            self.move_jump = True
        
    def update(self):
        '''
        Para que el jugador pueda interactuar
        '''
        # Para establecer la velocidad actual, dependiendo si el jugador camina o no.
        if self.__walking == True:
            self.speed_current = self.__speed_walk
        else:
            self.speed_current = self.__speed_run

        # Mover al jugador
        self.moving_xy = [0, 0]
        if self.move_left == True:
            self.moving_xy[0] -= self.speed_current
        if self.move_right == True:
            self.moving_xy[0] += self.speed_current

        '''
        if self.move_up == True:
            self.moving_xy[1] -= self.speed_current
        if self.move_down == True:
            self.moving_xy[1] += self.speed_current
        '''
        '''
        if self.move_jump == True:
            if self.__air_count == 0:
                #self.moving_xy[1] -= 128
                self.__gravity_current -= self.jump_power#19
            
        # Gravedad
        self.moving_xy[1] += self.__gravity_current
        if self.__gravity_current <= self.__gravity_limit:
            # Gravedad dentro del limite
            self.__gravity_current += self.gravity_power
        else:
            # Gravedad supero el limite
            self.__gravity_current = self.__gravity_limit
        '''
        if self.move_jump == True:
            self.__jump_ready = True

        self.moving_xy[1] += self.__gravity_current
        if self.__gravity_current <= self.__gravity_limit:
            # Gravedad dentro del limite
            self.__gravity_current += self.gravity_power
        else:
            # Gravedad supero el limite
            self.__gravity_current = self.__gravity_limit

        if self.__air_count <= 0:
            print('sin gravedad muchacho')
            if self.__jump_ready == True and self.__jump_continue == False:
                print('saltito')
                #self.moving_xy[1] = 0
                self.__gravity_current = 0
                self.__jump_count += self.__jump_power
                #self.__jump_ready = False
                self.__jump_continue = True
                self.moving_xy[1] -= self.__jump_power
        else:
            print('con gravedad muchacho')
            if self.__jump_continue == True:
                print('saltando')
                #self.moving_xy[1] = 0
                self.__gravity_current = 0
                self.__jump_ready = False
                self.__jump_count += self.__jump_power
                if self.__jump_count <= self.__jump_max_height:
                    self.moving_xy[1] -= self.__jump_power
                    self.__jump_continue = True
                else:
                    self.__jump_count = 0
                    self.__jump_continue = False
        print(self.__jump_count)

        self.__air_count += 1
        

        # Colsion Solidos
        collide_direction = None
        
        
        self.rect.x += self.moving_xy[0]
        for obj in solid_objects:
            if self.rect.colliderect(obj.rect):
                if self.moving_xy[0] > 0:
                    self.rect.right = obj.rect.left
                    collide_direction = 'right'
                elif self.moving_xy[0] < 0:
                    self.rect.left = obj.rect.right
                    collide_direction = 'left'
        
        self.rect.y += self.moving_xy[1]
        for obj in solid_objects:
            if self.rect.colliderect(obj.rect):
                if self.moving_xy[1] > 0:
                    self.rect.bottom = obj.rect.top
                    collide_direction = 'bottom'
                elif self.moving_xy[1] < 0:
                    self.rect.top = obj.rect.bottom
                    collide_direction = 'top'
        
        if type(collide_direction) == str:
            print(collide_direction)
        
        if collide_direction == 'bottom':
            self.__gravity_current = 0
            self.__air_count = 0
        else:
            self.__air_count += 1
        
        if collide_direction == 'top':
            self.__gravity_current = 0
            
            self.__jump_continue = False
            self.__jump_count = 0




class Stone(pygame.sprite.Sprite):
    def __init__(self, size=32, position=(0,0)):
        super().__init__()
        
        size_ready = (size, size)
        self.image = pygame.Surface( size_ready, pygame.SRCALPHA )
        self.image.fill( (127, 127, 127) )
        self.rect = self.image.get_rect(
            topleft=position
        )
        layer_all_sprites.add(self, layer=0)
        solid_objects.add(self)




# Grupos de sprites
layer_all_sprites = pygame.sprite.LayeredUpdates()

solid_objects = pygame.sprite.Group()