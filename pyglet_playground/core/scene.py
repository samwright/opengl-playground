import pyglet
from pyglet.gl import *
import numpy as np
from aperture import Aperture

from core.composite_polygon import CompositePolygon
from core.utility import vec


__author__ = 'eatmuchpie'


class Scene(CompositePolygon):
    def __init__(self, polygons=[]):
        super(Scene, self).__init__()

        try:
            # Try and create a window with multisampling (antialiasing)
            config = Config(sample_buffers=1, samples=4,
                            depth_size=16, double_buffer=True, )
            self.window = pyglet.window.Window(resizable=True, config=config)
        except pyglet.window.NoSuchConfigException:
            # Fall back to no multisampling for old hardware
            self.window = pyglet.window.Window(resizable=True)
        self.window.set_handler("on_resize", self.on_resize)
        self.window.set_handler("on_draw", self.draw)
        pyglet.clock.schedule(self.update)
        self.gl_setup()

    def on_resize(self, width, height):
        # Override the default on_resize handler to create a 3D projection
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60., width / float(height), .1, 1000.)
        glMatrixMode(GL_MODELVIEW)
        return pyglet.event.EVENT_HANDLED

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        super(Scene, self).draw()

    def gl_setup(self):
        # One-time GL setup
        glClearColor(1, 1, 1, 1)
        glColor3f(1, 0, 0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_NORMALIZE)

        # Uncomment this line for a wireframe view
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
        # but this is not the case on Linux or Mac, so remember to always
        # include it.
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)

        # Define a simple function to create ctypes arrays of floats:

        glLightfv(GL_LIGHT0, GL_POSITION, vec(.5, .5, 1, 0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, vec(.5, .5, 1, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))
        glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, .5, 0))
        glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .5, .5, 1))
        glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 1, 1, 1))

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0, 0.3, 1))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)

    def exec_(self):
        pyglet.app.run()


if __name__ == "__main__":
    def slowly_rotate(obj, dt):
        obj.orientation[:] += np.array([20, 50, 90]) * dt

    # cube = Cube()
    # cube.position[2] = -5.

    # torus = Torus(1, 0.3, 50, 30)
    # torus.position[2] = -4.

    aperture = Aperture()
    aperture.position[2] = -10
    aperture.size[:] = [2., 2., 2.]
    aperture.hole.size[:2] = [1., 1.]
    # aperture.lbox.size[0] = 0.2
    aperture.on_update = slowly_rotate
    # aperture.callback(aperture, 'no reason')

    scene = Scene()
    scene._polygons = {'aperture': aperture}
    scene.exec_()