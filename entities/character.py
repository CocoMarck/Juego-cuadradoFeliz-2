from .object_with_physics import ObjectWithPhysics

class Character(ObjectWithPhysics):
    def __init__( self, *args, hp=100, speed: int=None, jump_force:int=None,  **kwargs ):
        super().__init__( *args, **kwargs )

        self._SPANW_HP = hp
        self._SPAWN_JUMP_FORCE = jump_force or max(self.rect.size)*15
        self._SPAWN_SPEED = speed or max(self.rect.size)*16

        self.hp = self._SPANW_HP
        self.jump_force = self._SPAWN_JUMP_FORCE
        self.speed = self._SPAWN_SPEED
