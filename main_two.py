from core.game.scene import Scene
from core.game.window import Window

scene = Scene(
    render_resolution=[16,9], grid_size=1, groups={}, name="game"
)
window = Window(
    window_size=[960,540], fps=100, scene=scene, title="Ventana"
)

if __name__ == "__main__":
    window.run()
