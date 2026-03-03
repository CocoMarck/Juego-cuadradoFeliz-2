from .scene import Scene
import pygame

from entities.game_object import GameObject
from entities.object_with_physics import ObjectWithPhysics
from entities.sticky_sprite import StickySprite
from entities.animated_sticky_sprite import AnimatedStickySprite
from entities.player import Player
from core.pygame.graphics_utils import surface_with_background
from controllers.animation_controller import AnimationController


GRID_SIZE = 16
player_surf = pygame.Surface( (GRID_SIZE*0.8, GRID_SIZE*0.5), pygame.SRCALPHA )
player_surf.blit(
    surface_with_background( (GRID_SIZE*0.5, GRID_SIZE*0.5), "white"),
    (0,0)
)
player_surf.blit(
    surface_with_background( (GRID_SIZE*0.3, GRID_SIZE*0.1), "white"),
    (GRID_SIZE*0.5,0)
)

def get_surf( color, angle=0 ):
    surf = player_surf.copy()

    mask = pygame.Surface( surf.get_size() ).convert_alpha()
    mask.fill(color)

    surf.blit( mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT )
    if angle != 0:
        return pygame.transform.rotate( surf, angle )

    return surf


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
        render_resolution=(512, 288)
        super().__init__( *args, render_resolution=render_resolution, name=name, groups=groups, **kwargs )

        self.grid_size = self.render_resolution[0]//32


    def init_objects(self):
        example_object = GameObject(
            surf=surface_with_background( (self.grid_size*0.5, self.grid_size), "purple" )
        )
        self.layers.add( example_object, layer=4 )

        basic_physics = ObjectWithPhysics(
            surf=surface_with_background( (self.grid_size, self.grid_size*0.5), "purple" ),
        )
        self.groups["physical"].add( basic_physics )
        self.layers.add( basic_physics, layer=4 )

        for x in range(0, 20):
            solid = GameObject(
                surf=surface_with_background( (self.grid_size, self.grid_size), "grey" ),
                position=( self.grid_size*x, (self.render_resolution[1]-self.grid_size) )
            )
            self.groups['solids'].add( solid )
            self.layers.add( solid, layer=4 )

        self.player = Player(
            surf=pygame.Surface( (self.grid_size*0.5, self.grid_size) ), alpha=31
        )
        self.groups["physical"].add( self.player )
        self.groups["characters"].add( self.player )
        self.layers.add( self.player, layer=4 )

        # Animations
        player_animations = {
            'idle': (
                [
                    get_surf("blue"),
                    get_surf("red"),
                    get_surf("purple"),
                ], 1
            ),
            'move': (
                [
                    get_surf("white"),
                    get_surf("grey", 10),
                    get_surf("black", -10),
                ], 0.1
            ),
            'move-walk': (
                [
                    get_surf("white"),
                    get_surf("grey", 5),
                    get_surf("black", -5),
                ], 0.2
            ),
            'jumping-idle': (
                [
                    get_surf("skyblue", 10),
                ], 1
            ),
            'falling-idle': (
                [
                    get_surf("pink", -10),
                ], 1
            ),
            'jumping-move': (
                [
                    get_surf("red", 20),
                ], 1
            ),
            'falling-move': (
                [
                    get_surf("yellow", -20),
                ], 1
            )
        }
        anim_player = AnimatedStickySprite(
            surf=player_animations['idle'][0][0],
            game_object=self.player, center=True,
            animation_controller=AnimationController( player_animations, state='idle' )
        )
        self.groups["sticky"].add( anim_player )
        self.groups["animated"].add( anim_player )

        for sprite in self.groups["sticky"]:
            self.layers.add( sprite, layer=1 )


    def update(self, dt, key_get_pressed):
        self.player.handle_input( key_get_pressed )

        for sprite in self.groups["characters"]:
            sprite.move()

        for sprite in self.groups["physical"]:
            sprite.update(dt, self.groups["solids"])

        for sprite in self.groups["sticky"]:
            sprite.stick()

        for sprite in self.groups["animated"]:
            sprite.update(dt)

