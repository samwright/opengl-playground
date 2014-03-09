import numpy as np
from pyglet.gl import *

from core.polygon import Polygon


__author__ = 'eatmuchpie'


class GLPolygon(Polygon):
    def __init__(self, vertices=None, triangles_indices=None, to_clone=None):
        """
        Creates a GLPolygon from the supplied vertices and triangles, or
        shallow-copies the supplied GLPolygon.

        :param vertices: numpy.ndarray([[x1,y1,z1], [x2,y2,z2], ...])
        :param triangles_indices: numpy.ndarray([[a1,b1,c1], [a2,b2,c2], ...])
        :param to_clone: the triangle strip to copy
        """
        if to_clone is not None:
            self.gl_list = to_clone.gl_list
            super(GLPolygon, self).__init__(to_clone=to_clone)
        else:
            super(GLPolygon, self).__init__()

            # Remove unused vertices
            all_vertices = set(range(len(vertices)))
            unused_vertices = all_vertices
            for triangle_indices in triangles_indices:
                unused_vertices.difference_update(triangle_indices)
            sorted_unused_vertices = sorted(unused_vertices)
            vertices = np.delete(vertices, sorted_unused_vertices, 0)

            # Calculate index corrections
            def corrected_index(index):
                for n, deleted_index in enumerate(sorted_unused_vertices):
                    if index < deleted_index:
                        return index - n
                return index - len(sorted_unused_vertices)

            # Correct the triangle indices
            triangles_indices = np.vectorize(corrected_index)(triangles_indices)

            # Calculate sum of normals for each vertex
            normal_sums_per_vertex = np.zeros([len(vertices), 3])
            for triangle in triangles_indices:
                a, b, c = [vertices[i] for i in triangle]
                ab = b - a
                bc = c - a
                normal = np.cross(ab, bc)
                normal /= np.linalg.norm(normal)
                for i in triangle:
                    normal_sums_per_vertex[i] += normal

            # Replace sum of normals for each vertex with average by normalising
            for i in range(len(vertices)):
                length = np.linalg.norm(normal_sums_per_vertex[i])
                normal_sums_per_vertex[i] /= length

            # Linearise the arrays
            vertices = np.concatenate(vertices).tolist()
            normals = np.concatenate(normal_sums_per_vertex).tolist()
            triangles_indices = np.concatenate(triangles_indices).tolist()

            # Convert arrays to c_type arrays
            vertices = (GLfloat * len(vertices))(*vertices)
            normals = (GLfloat * len(normals))(*normals)
            triangles_indices = (GLuint * len(triangles_indices))(*triangles_indices)

            # Generate and save OpenGl command list
            self.gl_list = glGenLists(1)
            glNewList(self.gl_list, GL_COMPILE)

            glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_NORMAL_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, vertices)
            glNormalPointer(GL_FLOAT, 0, normals)
            glDrawElements(GL_TRIANGLES, len(triangles_indices), GL_UNSIGNED_INT, triangles_indices)
            glPopClientAttrib()

            glEndList()

    def draw(self):
        if self.gl_list is None:
            raise Exception("GLObject has no vertices defined")

        self.transform()

        try:
            glCallList(self.gl_list)
        finally:
            self.untransform()

    def clone(self):
        return GLPolygon(to_clone=self)

    @staticmethod
    def triangle_strip(vertices=None, triangle_strip_indices=None, to_clone=None):
        """
        Creates a Polygon from the supplied triangle strip.

        :param vertices: numpy.ndarray([[x1,y1,z1], [x2,y2,z2], ...])
        :param triangle_strip_indices: [1, 2, 3, 4, ...]
        :param to_clone: the triangle strip to copy
        """
        if to_clone is not None:
            return GLPolygon(to_clone=to_clone)
        else:
            triangles = []
            for i in range(len(triangle_strip_indices) - 2):
                if i % 2 == 0:
                    triangles.append(triangle_strip_indices[i: i + 3])
                else:
                    triangles.append(triangle_strip_indices[i + 2: i - 1: -1])

            return GLPolygon(vertices, triangles)
