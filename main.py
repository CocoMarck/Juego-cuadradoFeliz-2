import pygame
from entities.game_object import GameObject
from entities.object_with_physics import ObjectWithPhysics
from entities.player import Player
from core.pygame.graphics_utils import surface_with_background



# Constantes
GAME_TITLE = 'Cuadrado Feliz 2'
FPS = 100
SECOND_TO_MILLISECONDS = 1000

WINDOW_SIZE = (960, 540)
RENDER_RESOLUTION = (960, 540)
GRID_SIZE = RENDER_RESOLUTION[0]//32

# Rendrizado, y vistas jejej
window = pygame.display.set_mode( WINDOW_SIZE )
render_surface = pygame.Surface( RENDER_RESOLUTION )

# Delta time moment
clock = pygame.time.Clock()

# Información
pygame.display.set_caption( GAME_TITLE )



# Renderizado de objetos
layers_of_all_sprites = pygame.sprite.LayeredUpdates()
solid_objects = pygame.sprite.Group()


# Objetos
count = 0

example_object = GameObject(
    surf=surface_with_background( (GRID_SIZE*0.5, GRID_SIZE), "purple" )
)
layers_of_all_sprites.add( example_object, layer=0 )

basic_physics = ObjectWithPhysics(
    surf=surface_with_background( (GRID_SIZE, GRID_SIZE*0.5), "purple" ),
)
layers_of_all_sprites.add( basic_physics, layer=0 )

for x in range(0, 20):
    solid = GameObject(
        surf=surface_with_background( (GRID_SIZE, GRID_SIZE), "grey" ),
        position=( GRID_SIZE*x, (RENDER_RESOLUTION[1]-GRID_SIZE) )
    )
    layers_of_all_sprites.add( solid, layer=0 )
    solid_objects.add( solid )

player = Player(
    surf=surface_with_background( (GRID_SIZE, GRID_SIZE*0.5), "blue" ),
)
layers_of_all_sprites.add( player, layer=0 )




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
    ### Contador
    count += dt

    ### Eventos de objetos
    example_object.angle += 100 * dt # Cien grados cada segundo.
    example_object.rotate_surface()

    #basic_physics.moving_xy = [0,0]
    basic_physics.update( dt, solid_objects )
    if round(count) == 5:
        basic_physics.set_spawn_position()
        solid.set_spawn_position()

    #if count > 2 and (not count >= 5):
    #    solid.moving_xy[0] = GRID_SIZE*4
    #else:
    #    solid.moving_xy[0] = 0
    solid.update(dt)

    player.update(dt, solid_objects)
    player.handle_input(dt, pygame.key.get_pressed() )

    ### Objetos | Rederizado
    for sprite in layers_of_all_sprites.sprites():
        render_surface.blit( sprite.surf, sprite.rect )

    # Parar loop
    #if count >= 8:
        #loop = False
        #print(f'Segundos actuales: {count}')
        #input()


    ## Mostrar todo
    window.blit(
        pygame.transform.scale(render_surface, WINDOW_SIZE), (0,0)
    )
    pygame.display.update()

pygame.quit()
