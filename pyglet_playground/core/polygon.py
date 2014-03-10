import abc

from core.transformable import Transformable


__author__ = 'eatmuchpie'


class Polygon(Transformable):
    """
    A 2D surface in 3D space.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, to_clone=None):
        super(Polygon, self).__init__(to_clone=to_clone)
        self.on_update = None

    @abc.abstractmethod
    def draw(self):
        """
        Draw the object to screen.
        """
        pass

    @abc.abstractmethod
    def clone(self):
        """
        Clone this object.
        """
        pass

    def update(self, dt):
        """
        Called before this object is drawn, with the amount of time that has
        passed since the last update.

        :param dt: the time that has passed since the last update.
        """
        pass

