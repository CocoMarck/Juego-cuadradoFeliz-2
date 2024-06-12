import pygame




class Player(pygame.sprite.Sprite):
    def __init__(
        self, size=32, position=(0,0),
        show_collide=False, show_sprite=True, color_sprite=(153, 252, 152)
    ):
        super().__init__()
        
        size_ready = (size, size)
        
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
        #self.__walking = False
        self.__speed_run = size//2
        self.__speed_walk = self.__speed_run//2
        self.speed_current = self.__speed_walk

        #self.move_left = False
        #self.move_right = False
        #self.move_up = False
        #self.move_down = False
    
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
        
        # Accionar movimiento
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
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
        
    def update(self):
        '''
        Para que el jugador pueda interactuar
        '''
        # Para establecer la velocidad actual, dependiendo si el jugador camina o no.
        if self.__walking == False:
            self.speed_current = self.__speed_run
        else:
            self.speed_current = self.__speed_walk

        # Colsion Solidos
        for obj in solid_objects:
            if self.rect.colliderect(obj.rect):
                print('colision')

        # Mover al jugador
        if self.move_left == True:
            self.rect.x -= self.speed_current
        if self.move_right == True:
            self.rect.x += self.speed_current

        if self.move_up == True:
            self.rect.y -= self.speed_current
        if self.move_down == True:
            self.rect.y += self.speed_current




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