import pygame

class GameObject(pygame.sprite.Sprite):
    '''
    Objeto de juego con los atributos necesarios para eventos básicos del juego.
    '''
    def __init__(
        self, name='object', group="generic", 
        surf: pygame.Surface, alpha=255, flip_x=False, flip_y=False, position=(0,0), 
        volume=float(1), angle=int(0)
    ):
        # Evitar hacer wrappers al surface o al rect, nada de eso.
        super().__init()

        # Constantes
        self._SPAWN_POSITION = position
        self._SPAWN_VOLUME = volume
        self._SPAWN_ANGLE = angle
        self._SPAWN_SURF = surf
        self._SPAWN_ALPHA = alpha

        # Variables | Para sonido
        self._volume = volume

        # Variables | Relacionado con movimiento
        self.angle = angle
        self.moving_xy = [0,0]
        self.flip_x = flip_x
        self.flip_y = flip_y

        # Varialbes | Releciondas con herencia, o tipo de objeto
        self.name = name
        self.group = group

        # Superficie
        self.surf = surf.copy()
        self.rect = surf.get_rect( position=self.position )

    def flip_surface(self):
        self.surf = pygame.transform.flip( self._SPAWN_SURF, self.flip_x, self.flip_y )

    def resize_rect(self):
        if self.surf.get_size() != self.rect.size:
            self.surf = pygame.transform.scale(self._SURF_BASE, self.rect.size)

    def set_alpha(self, alpha: int ):
        self.surf.set_alpha( alpha )

    def set_spawn_alpha(self):
        self.set_alpha( self._SPAWN_ALPHA )

    def rotate_surface(self):
        pass

    def get_volume(self):
        pass

    def set_volume(self):
        pass

    def set_spawn_volume(self):
        pass
