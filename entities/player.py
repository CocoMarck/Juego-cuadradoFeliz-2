from .character import Character

import pygame

class Player(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(args, **kwargs)

    def handle_input(self, dt=1, keys=None):
        if keys[pygame.K_LEFT]:
            self.moving_xy[0] = -(self.speed) * dt
        elif keys[pygame.K_RIGHT]:
            self.moving_xy[0] = self.speed * dt
        else:
            self.moving_xy[0] = 0

        if keys[pygame.K_SPACE] and self.on_the_ground():
            self.current_vertical_force = -(self.jump_force)
