import pygame
from .game_object import GameObject
from core.pygame.physics_utils import collide_and_move

class ObjectWithPhysics(GameObject):
    '''
    La furza de gravedad, es por px's por segundo.
    Es decir, cada 1 segundos, el player se movera `x pixles`.
    '''
    def __init__(self, *args, gravity_force=0.1, limit_of_gravity_force=None, **kwargs):
        super().__init__( *args, **kwargs )

        # Constantes
        self._SPAWN_GRAVITY_FORCE = gravity_force
        self._SPAWN_LIMIT_OF_GRAVITY_FORCE = limit_of_gravity_force or max(self.rect.size)-1

        # Gravedad
        self.current_gravity_force = 0
        self.limit_of_gravity_force = self._SPAWN_LIMIT_OF_GRAVITY_FORCE
        self.gravity_force = self._SPAWN_GRAVITY_FORCE


    def gravity(self, dt:float):
        '''
        En dalta time.
        Cada segundo se mueve `self.current_gravity_force` pixeles.
        `gravity_force` se acumula; Es relativo, por lo que la fuerza debe medirse en cada acumulación por segundo.

        # Recomendación.
        Cada 1 segundo se mueva: 10 rect max(size). Y como maximo 30 max(size)
        '''
        self.current_gravity_force += self.gravity_force*dt
        if self.current_gravity_force > self.limit_of_gravity_force:
            self.current_gravity_force = self.limit_of_gravity_force

        self.moving_xy[1] = self.current_gravity_force*dt

    def collide_and_move(self, solid_objects: list):
        '''
        Colisionar con objeto solido y moverse.
        '''
        return collide_and_move(
            self.rect, self.moving_xy, solid_objects
        )

    def update(self, dt=1, solid_objects: pygame.sprite.Group=[] ):
        self.gravity(dt)
        collision_side = self.collide_and_move( solid_objects )
        for x in collision_side.values():
            if x == True:
                #self.moving_xy[1] = 0
                break



