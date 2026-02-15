from controllers.animation_controller import AnimationController

class AnimatedStickySprite(StickySprite):
    '''
    Usando un controller, establece el cambio de frames, remplazando surf dependiendo del parametro `state` de update.
    '''
    def __init__(self, *args, animation_controller: AnimationController, **kwargs)
        super().__init__(*args, **kwargs)

        self.animation_controller = animation_controller

    def update(self, dt, state: str):
        self.animation_controller.update(dt, state)
        self.surf = self.animation_controller.get_current_frame()


