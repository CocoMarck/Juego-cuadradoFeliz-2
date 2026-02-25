from .scene import Scene
import pygame

from entities.game_object import GameObject
from entities.object_with_physics import ObjectWithPhysics
from entities.sticky_sprite import StickySprite
from entities.animated_sticky_sprite import AnimatedStickySprite
from entities.player import Player
from core.pygame.graphics_utils import surface_with_background
from controllers.animation_controller import AnimationController


class CuadradoFelizDosScene(Scene):
    def __init__(self, *args, **kwargs):
        name = "game"
        groups = {
            "solids": pygame.sprite.Group(),
            "physical": pygame.sprite.Group(),
            "characters": pygame.sprite.Group(),
            "sticky": pygame.sprite.Group(),
            "animated": pygame.sprite.Group()
        }
        super().__init__( *args, name=name, groups=groups, **kwargs )

        self.grid_size = self.render_resolution[0]//32


    def init_objects(self):
        example_object = GameObject(
            surf=surface_with_background( (self.grid_size*0.5, self.grid_size), "purple" )
        )
        self.layers.add( example_object, layer=0 )

        basic_physics = ObjectWithPhysics(
            surf=surface_with_background( (self.grid_size, self.grid_size*0.5), "purple" ),
        )
        self.groups["physical"].add( basic_physics )
        self.layers.add( basic_physics, layer=0 )

        for x in range(0, 20):
            solid = GameObject(
                surf=surface_with_background( (self.grid_size, self.grid_size), "grey" ),
                position=( self.grid_size*x, (self.render_resolution[1]-self.grid_size) )
            )
            self.groups['solids'].add( solid )
            self.layers.add( solid, layer=0 )

        self.player = Player(
            surf=pygame.Surface( (self.grid_size*0.5, self.grid_size) ), alpha=255
        )
        self.groups["physical"].add( self.player )
        self.groups["characters"].add( self.player )
        self.layers.add( self.player, layer=0 )


    def update(self, dt, key_get_pressed):
        self.player.handle_input( key_get_pressed )

        for sprite in self.groups["characters"]:
            sprite.move()

        for sprite in self.groups["physical"]:
            sprite.update(dt, self.groups["solids"])
