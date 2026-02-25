import pygame

SECOND_TO_MILLISECONDS = 1000

class CuadradoFelizDos:
    def __init__(self, window_size, render_resolution, fps, title):
        self.title = title
        self.window_size = window_size
        self.render_resolution = render_resolution
        self.fps = fps

        self.render_surface = pygame.Surface( self.render_resolution )
        self.loop = True

        # Init pygame
        self.window = None
        self.clock = None

        # Grupo de sprites
        self.layers = pygame.sprite.LayeredUpdates()
        self.solids = pygame.sprite.Group()
        self.stickies = pygame.sprite.Group()
        self.animateds = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()

        # Inicializar objetos
        self.init_pygame()
        self.init_objects()

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption( self.title )
        self.window = pygame.display.set_mode( self.window_size )

        self.clock = pygame.time.Clock()

    def init_objects(self):
        pass

    def handle_events(self, events):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False

    def update(self, dt, player):
        player.handle_input( pygame.key.get_pressed() )

        for character in self.characters:
            character.move()
            character.update(dt)

        for sprite in sticky_sprites:
            sprite.stick()

        for sprite in animated_sprites:
            sprite.update(dt)

    def render(self):
        self.render_surface.fill( 'green' )
        for sprite in self.layers.sprites():
            self.render_surface.blit( sprite.surf, sprite.rect )
        self.window.blit(
            pygame.transform.scale(self.render_surface, self.window_size), (0,0)
        )
        pygame.display.update()

    def run(self, player):
        while self.loop:
            dt = self.clock.tick(self.fps) / SECOND_TO_MILLISECONDS
            fps = self.clock.get_fps()

            self.handle_events()

            self.update(dt, player)

            self.render()


        pygame.quit()
