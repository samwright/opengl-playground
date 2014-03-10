import numpy as np
from pyglet.gl import *
from core.utility import ObservableProperties, ObservableArray


__author__ = 'eatmuchpie'


@ObservableProperties('orientation', 'size', 'position')
class Transformable(object):
    """
    An object that has three transformable properties - its orientation, size,
    and position.

    Those properties can be set to be automatically applied in the 3D space, or
    that responsibility can be delegated to the subclass, as defined in
    self.auto_transform.
    """
    class BadTransformation(Exception):
        pass

    def __init__(self, to_clone=None):
        """
        Create a new Transformable object, optionally cloning the
        transformations of the supplied Transformable object.
        """
        if to_clone is not None:
            self.orientation = ObservableArray.like(to_clone.orientation)
            self.size = ObservableArray.like(to_clone.size)
            self.position = ObservableArray.like(to_clone.position)
            self.auto_transform = dict(to_clone.auto_transform)
        else:
            self.orientation = ObservableArray.like([0., 0., 0.])
            self.size = ObservableArray.like([1., 1., 1.])
            self.position = ObservableArray.like([0., 0., 0.])
            self.auto_transform = {
                'size': True,
                'orientation': True,
                'position': True
            }

        self.check_arrays()
        self.callbacks.add(self.check_arrays)

    def check_arrays(self, object=None, reason=None):
        for array in self.orientation, self.position, self.size:
            if not isinstance(array, ObservableArray):
                raise Transformable.BadTransformation("Array must be ObservableArray")
            if array.shape != (3,):
                raise Transformable.BadTransformation(
                    "Array needs shape of (3), not {0}".format(array.shape))

    def transform(self):
        """
        Perform the automated transformations (if desired).

        This is done by pushing a cloned modelview matrix to the stack, then
        applying the transformations to it. The matrix stays on the stack after
        this function returns. It can be removed with the self.untransform()
        method.
        """
        glPushMatrix()

        if self.auto_transform['position']:
            glTranslatef(*self.position)

        if self.auto_transform['orientation']:
            glRotatef(self.orientation[0], 0, 0, 1)
            glRotatef(self.orientation[1], 0, 1, 0)
            glRotatef(self.orientation[2], 1, 0, 0)

        if self.auto_transform['size']:
            glScalef(*self.size)

    def untransform(self):
        """
        Undo the transformation applied in self.transform().

        This pops the matrix from the modelview stack.
        """
        glPopMatrix()


