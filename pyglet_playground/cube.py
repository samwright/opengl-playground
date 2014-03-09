import numpy as np

from core.composite_polygon import CompositePolygon
from core.trianglestrip import TriangleStrip


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

    polygons = {'top': TriangleStrip(vertices, [0, 2, 1, 3]),
                'bottom': TriangleStrip(vertices, [4, 5, 6, 7]),
                'lower': TriangleStrip(vertices, [0, 1, 4, 5]),
                'upper': TriangleStrip(vertices, [2, 6, 3, 7]),
                'left': TriangleStrip(vertices, [0, 4, 2, 6]),
                'right': TriangleStrip(vertices, [1, 3, 5, 7])}

    return CompositePolygon(polygons)
