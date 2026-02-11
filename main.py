import pygame
from entities.game_object import GameObject
from entities.object_with_physics import ObjectWithPhysics
from core.pygame.graphics_utils import surface_with_background



# Constantes
GAME_TITLE = 'Cuadrado Feliz 2'
FPS = 100
SECOND_TO_MILLISECONDS = 1000

WINDOW_SIZE = (960, 540)
RENDER_RESOLUTION = (1920, 1080)
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

basic_physics = ObjectWithPhysics(
    surf=surface_with_background( (GRID_SIZE, GRID_SIZE*0.5), "purple" ),
    gravity_force=GRID_SIZE*10, limit_of_gravity_force=GRID_SIZE*30
)
solid_objects = []

solid = GameObject(
    surf=surface_with_background( (GRID_SIZE, GRID_SIZE), "grey" ),
    position=( 0, RENDER_RESOLUTION[1]-GRID_SIZE )
)
solid_objects.append(solid)




# Bucle
loop = True
while loop:
    # FPS | Delta time
    dt = clock.tick(FPS) / SECOND_TO_MILLISECONDS
    fps = clock.get_fps()

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    # Render
    ## Fondo, evitar bugs visuales
    render_surface.fill( 'green' )

    ## Objetos
    ### Eventos de objetos
    example_object.angle += 100 * dt # Cien grados cada segundo.
    example_object.rotate_surface()

    #basic_physics.moving_xy = [0,0]
    basic_physics.update( dt, solid_objects )
    print(basic_physics.moving_xy )

    ### Objetos | Rederizado
    render_surface.blit( example_object.surf, example_object.rect )
    render_surface.blit( basic_physics.surf, basic_physics.rect )
    render_surface.blit( solid.surf, solid.rect )

    #
    count += dt
    #if count >= 1.75:
    #    loop = False
    #    print(f'Segundos actuales: {count}')
    #    input()


    ## Mostrar todo
    window.blit(
        pygame.transform.scale(render_surface, WINDOW_SIZE), (0,0)
    )
    pygame.display.update()

pygame.quit()
