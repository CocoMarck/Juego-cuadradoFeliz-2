from core.game.scene import Scene
from core.game.window import Window

game_scene = Scene(
    render_resolution=[16,9], groups={}, name="game"
)
window = Window(
    window_size=[960,540], fps=100, scene=game_scene, title="Ventana"
)

if __name__ == "__main__":
    window.run()
