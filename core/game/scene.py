import pygame

class Scene():
    '''
    La escena de juego. Todo se guardara en el `RenderSurface`.
    '''
    def __init__(
        self, render_resolution:list, groups:dict, name:str,
    ):
        self.render_resolution = render_resolution
        self.render_surface = pygame.Surface( self.render_resolution )
        self.name = name

        # Grupos de lógica de sprites, y capas para renderizado de sprites.
        self.groups = groups
        self.layers = pygame.sprite.LayeredUpdates()

        # Señales de juego.
        self.signals = {
            "loop": True
        }

    def init_objects(self):
        '''
        Usando grops y layers.
        '''
        pass

    def handle_events(self, events ):
        '''
        Eventos de teclado.
        '''
        for event in events:
            if event.type == pygame.QUIT:
                self.signals["loop"] = False

    def update(self, dt):
        '''
        Actualizar eventos, normalmente solo usando groups.
        Normalmente es, los `"update"`, reciben `sprite.update()`.
        '''
        print( self.groups.keys() )

    def render(self):
        '''
        Renderizado, utilizando layers.
        '''
        self.render_surface.fill( 'green' )
        for sprite in self.layers.sprites():
            self.render_surface.blit( sprite.surf, sprite.rect )
