from .object_with_physics import ObjectWithPhysics

class Character(ObjectWithPhysics):
    def __init__( self, *args, hp=100, speed: int=None, jump_force:int=None,  **kwargs ):
        super().__init__( *args, **kwargs )

        self._SPANW_HP = hp
        self._SPAWN_JUMP_FORCE = jump_force or max(self.rect.size)*23
        self._SPAWN_SPEED = speed or max(self.rect.size)*16

        self.hp = self._SPANW_HP
        self.jump_force = self._SPAWN_JUMP_FORCE
        self.speed = self._SPAWN_SPEED
        self._WALKING_SPEED_MULTIPLIER = 0.5

        # Para moverse
        self.move_walk = False
        self.move_left = False
        self.move_right = False
        self.move_jump = False

    def get_speed(self, dt:float, multiplier:float ):
        return self.speed * multiplier * dt

    def get_running_speed(self, dt=1 ):
        return self.get_speed(dt, 1)

    def get_walking_speed(self, dt=1 ):
        return self.get_speed(dt, self._WALKING_SPEED_MULTIPLIER)

    def jump(self, dt=1, multiplier=1 ):
        self.current_vertical_force = -( self.jump_force*multiplier )

    def jump_on_the_ground(self, dt=1, multiplier=1):
        if self.on_the_ground():
            self.jump( dt=dt, multiplier=multiplier )

    def move(self, dt=1):
        if self.move_walk:
            speed = self.get_walking_speed(dt)
        else:
            speed = self.get_running_speed(dt)

        if self.move_left:
            self.flip_x = True
            self.moving_xy[0] = -speed
        elif self.move_right:
            self.flip_x = False
            self.moving_xy[0] = speed
        else:
            self.moving_xy[0] = 0

        if self.move_jump:
            self.jump_on_the_ground( dt )
