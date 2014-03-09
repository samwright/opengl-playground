from math import pi, sin, cos
import numpy as np
from core.composite_polygon import CompositePolygon
from core.gl_polygon import GLPolygon

from core.trianglestrip import TriangleStrip
from core.utility import ObservableProperties, ObservableArray
from cube import create_unit_cube

__author__ = 'eatmuchpie'


@ObservableProperties('hole', 'lbox', 'rbox', 'tbox', 'bbox', 'scale_hole')
class Aperture(CompositePolygon):
    def __init__(self, smoothness=400, to_clone=None):
        if to_clone is not None:
            super(Aperture, self).__init__(to_clone=to_clone)
            with self.delayed_callback('cloning'):
                self.scale_hole = to_clone.scale_hole
                for box in 'hole', 'lbox', 'rbox', 'tbox', 'bbox':
                    setattr(self, box, self._polygons[box].clone())
        else:
            with self.delayed_callback('init'):
                self.hole = Aperture._create_hole(smoothness)
                self.lbox = create_unit_cube()
                self.lbox.size[0] = 0
                self.rbox = self.lbox.clone()
                self.tbox = create_unit_cube()
                self.tbox.size[1] = 0
                self.bbox = self.tbox.clone()

                polygons = {
                    'hole': self.hole,
                    'lbox': self.lbox,
                    'rbox': self.rbox,
                    'tbox': self.tbox,
                    'bbox': self.bbox
                }

                super(Aperture, self).__init__(polygons)
                self.auto_transform['size'] = False
                self.scale_hole = True
                self.hole.position[:] = [0.5, 0.5, 0.]
                self.callbacks.add(self.handle_change)

    def handle_change(self, changed_object=None, reason=None):
        # _ __ _
        #! !__! !
        #! !__! !
        #!_!__!_!

        if reason.endswith('box'):
            # A box was changed, so update self and aperture accordingly
            self.size[0] = self.lbox.size[0] + self.rbox.size[0] + self.hole.size[0]
            self.size[1] = self.tbox.size[1] + self.bbox.size[1] + self.hole.size[1]
            self.hole.position[0] = self.lbox.size[0] + (self.hole.size[0] / 2)
            self.hole.position[1] = self.bbox.size[1] + (self.hole.size[1] / 2)
        elif reason == 'hole':
            # Aperture changed: nothing to do
            pass
        elif reason in ['size', 'scale_hole']:
            # self.size was changed
            previous_size = self.lbox.size + [self.hole.size[0] + self.rbox.size[0], 0., 0.]
            scale_required = self.size / previous_size
            if self.scale_hole:
                self.hole.position *= scale_required
                self.hole.size *= scale_required

        hole_end = self.hole.position[:2] + (self.hole.size[:2] / 2)
        hole_start = self.hole.position[:2] - (self.hole.size[:2] / 2)

        assert np.all(self.size[:2] >= hole_end), "Hole extends out of aperture"

        # Fill space around hole with padding
        self.lbox.position[:] = [0., 0., 0.]
        self.lbox.size[:] = [hole_start[0], self.size[1], self.size[2]]
        self.rbox.position[:] = [hole_end[0], 0., 0.]
        self.rbox.size[:] = [self.size[0] - hole_end[0], self.size[1], self.size[2]]
        self.bbox.position[:] = [hole_start[0], 0., 0.]
        self.bbox.size[:] = [self.hole.size[0], hole_start[1], self.size[2]]
        self.tbox.position[:] = [self.lbox.size[0], hole_end[1], 0.]
        self.tbox.size[:] = [self.hole.size[0], self.size[1] - hole_end[1], self.size[2]]

        # Make sure hole is still as deep as the aperture
        self.hole.size[2] = self.size[2]
        self.hole.position[2] = 0.

    @staticmethod
    def _create_hole(smoothness):
        # calculate vertices of square
        square_vertices = np.array([
            [0.5, 0.5, 0.],
            [-0.5, 0.5, 0.],
            [-0.5, -0.5, 0.],
            [0.5, -0.5, 0.],
        ])

        # calculate vertices of circular aperture (from +x axis going ccw)
        front_circle_vertices = np.zeros((smoothness, 3))
        for i in range(smoothness):
            angle = 2 * pi * i / smoothness
            radial_line = np.array([cos(angle), sin(angle), 0.]) * 0.5
            front_circle_vertices[i][:] = radial_line

        # The square vertices will be appended to the circular vertices
        front_vertices = np.append(front_circle_vertices, square_vertices, 0)

        # Create front face of aperture
        triangle_indices = []
        for i in range(len(front_circle_vertices)):
            quadrant = int(4 * float(i) / smoothness)
            closest_corner_index = len(front_circle_vertices) + quadrant
            triangle_indices.append(
                [closest_corner_index, i, (i + 1) % len(front_circle_vertices)])

        front_face = GLPolygon(front_vertices, triangle_indices)

        # Create back face
        back_face = front_face.clone()
        back_face.orientation[1] = 180.
        back_face.position[2] = 1.

        # Create cylinder between faces - starting by creating the circular vertices
        # of the back face...
        back_circular_vertices = np.array(front_circle_vertices)
        back_circular_vertices[:, 2] += 1.
        back_circle_start_index = len(front_circle_vertices)
        circle_vertices = np.append(front_circle_vertices,
                                    back_circular_vertices,
                                    0)

        # ...and now create the cylinder triangles
        triangle_indices = []
        for front_vertex in range(len(front_circle_vertices)) + [0]:
            back_vertex = front_vertex + back_circle_start_index
            triangle_indices.extend([front_vertex, back_vertex])
        cylinder = GLPolygon.triangle_strip(circle_vertices, triangle_indices)

        return CompositePolygon({'front_face': front_face,
                                 'back_face': back_face,
                                 'cylinder': cylinder})
