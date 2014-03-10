import numpy as np

from core.composite_polygon import CompositePolygon
from core.gl_polygon import GLPolygon

__author__ = 'eatmuchpie'


def create_unit_cube():
    vertices = np.array([
        [0., 0., 0.],
        [1., 0., 0.],
        [0., 1., 0.],
        [1., 1., 0.],
        [0., 0., 1.],
        [1., 0., 1.],
        [0., 1., 1.],
        [1., 1., 1.],
    ])

    polygons = {'top': GLPolygon.triangle_strip(vertices, [0, 2, 1, 3]),
                'bottom': GLPolygon.triangle_strip(vertices, [4, 5, 6, 7]),
                'lower': GLPolygon.triangle_strip(vertices, [0, 1, 4, 5]),
                'upper': GLPolygon.triangle_strip(vertices, [2, 6, 3, 7]),
                'left': GLPolygon.triangle_strip(vertices, [0, 4, 2, 6]),
                'right': GLPolygon.triangle_strip(vertices, [1, 3, 5, 7])}

    return CompositePolygon(polygons)
