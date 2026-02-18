from .character import Character

import pygame

class Player(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(args, **kwargs)

    def handle_input(self, dt=1, keys=None):
        if keys[pygame.K_LSHIFT]:
            speed = self.get_walking_speed(dt)
        else:
            speed = self.get_running_speed(dt)

        if keys[pygame.K_LEFT]:
            self.flip_x = True
            self.moving_xy[0] = -speed
        elif keys[pygame.K_RIGHT]:
            self.flip_x = False
            self.moving_xy[0] = speed
        else:
            self.moving_xy[0] = 0

        if keys[pygame.K_SPACE]:
            self.jump_on_the_ground( dt )
