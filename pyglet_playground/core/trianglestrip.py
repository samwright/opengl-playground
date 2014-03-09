import numpy as np

from core.gl_polygon import GLPolygon


__author__ = 'eatmuchpie'


class TriangleStrip(GLPolygon):


    def __init__(self, vertices=None, triangle_strip_indices=None, to_clone=None):
        """
        Creates a Polygon from the supplied triangle strip.

        :param vertices: numpy.ndarray([[x1,y1,z1], [x2,y2,z2], ...])
        :param triangle_strip_indices: [1, 2, 3, 4, ...]
        :param to_clone: the triangle strip to copy
        """
        if to_clone is not None:
            super(TriangleStrip, self).__init__(to_clone=to_clone)
        else:
            triangles = []
            for i in range(len(triangle_strip_indices) - 2):
                if i % 2 == 0:
                    triangles.append(triangle_strip_indices[i: i + 3])
                else:
                    triangles.append(triangle_strip_indices[i + 2: i - 1: -1])

            super(TriangleStrip, self).__init__(vertices, triangles)
