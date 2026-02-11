import pygame
from .game_object import GameObject
from core.pygame.physics_utils import collide_and_move

class ObjectWithPhysics(GameObject):
    '''
    La furza de gravedad, es por px's por segundo.
    Es decir, cada 1 segundos, el player se movera `x pixles`.
    '''
    def __init__(self, *args, vertical_force=0.1, vertical_force_limit=None, **kwargs):
        super().__init__( *args, **kwargs )

        # Constantes
        self._SPAWN_VERTICAL_FORCE = vertical_force
        self._SPAWN_VERTICAL_FORCE_LIMIT = vertical_force_limit or max(self.rect.size)-1

        # Gravedad
        self.current_vertical_force = 0
        self.vertical_force_limit = self._SPAWN_VERTICAL_FORCE_LIMIT
        self.vertical_force = self._SPAWN_VERTICAL_FORCE

        # Para salto
        self.air_dt_count = 1


    def apply_gravity(self, dt:float):
        '''
        En dalta time.
        Cada segundo se mueve `self.current_vertical_force` pixeles.
        `vertical_force` se acumula; Es relativo, por lo que la fuerza debe medirse en cada acumulación por segundo.

        # Recomendación.
        Cada 1 segundo se mueva: 10 rect max(size). Y como maximo 30 max(size)
        '''
        self.current_vertical_force += self.vertical_force*dt
        if self.current_vertical_force > self.vertical_force_limit:
            self.current_vertical_force = self.vertical_force_limit

        self.moving_xy[1] = self.current_vertical_force*dt


    def collide_and_move(self, solid_objects: list):
        '''
        Colisionar con objeto solido y moverse.
        '''
        return collide_and_move(
            self.rect, self.moving_xy, solid_objects
        )

    def on_the_ground(self, dt=1, collision_side=None):
        self.air_dt_count += dt

        if collision_side['bottom']:
            self.air_dt_count = 0

        return (
            self.air_dt_count <= 0.1 and
            self.current_vertical_force >= 0
        )


    def update(self, dt=1, solid_objects: pygame.sprite.Group=[] ):
        self.apply_gravity(dt)

        collision_side = self.collide_and_move( solid_objects )
        for x in collision_side.values():
            if x == True:
                self.current_vertical_force = 0
                self.moving_xy[1] = 0
                break

        on_the_ground = self.on_the_ground(dt, collision_side)
        print(on_the_ground)
        if on_the_ground:
            self.current_vertical_force -= 500




