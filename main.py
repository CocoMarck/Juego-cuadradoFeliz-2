import pygame
from entities.game_object import GameObject
from core.pygame.graphics_utils import surface_with_background



# Constantes
GAME_TITLE = 'Cuadrado Feliz 2'
FPS = 100

WINDOW_SIZE = (960, 540)
RENDER_RESOLUTION = (320, 180)
GRID_SIZE = RENDER_RESOLUTION[0]//32

# Rendrizado, y vistas jejej
window = pygame.display.set_mode( WINDOW_SIZE )
render_surface = pygame.Surface( RENDER_RESOLUTION )

# Delta time moment
clock = pygame.time.Clock()

# Información
pygame.display.set_caption( GAME_TITLE )



# Objetos
example_object = GameObject(
    surf=surface_with_background( (GRID_SIZE*0.5, GRID_SIZE), "purple" )
)
count = 0




# Bucle
loop = True
while loop:
    # FPS | Delta time
    dt = clock.tick(FPS) / 1000
    fps = clock.get_fps()

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    # Render
    ## Fondo, evitar bugs visuales
    render_surface.fill( 'green' )

    ## Objetos
    count += dt
    if count >= 0.01:
        count = 0
        example_object.angle += 5
        example_object.rotate_surface()
    render_surface.blit( example_object.surf, example_object.rect )

    ## Mostrar todo
    window.blit(
        pygame.transform.scale(render_surface, WINDOW_SIZE), (0,0)
    )
    pygame.display.update()

pygame.quit()
