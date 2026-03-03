from core.game.scene import Scene
from core.game.cuadrado_feliz_dos_scene import CuadradoFelizDosScene
from core.game.window import Window

game_scene = CuadradoFelizDosScene()

window = Window(
    window_size=[960,540], fps=100, scene=game_scene, title="Ventana"
)
window.init_pygame()
game_scene.init_objects()

if __name__ == "__main__":
    window.run()
