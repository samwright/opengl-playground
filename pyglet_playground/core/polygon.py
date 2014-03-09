import abc

from core.transformable import Transformable


__author__ = 'eatmuchpie'


class Polygon(Transformable):
    __metaclass__ = abc.ABCMeta

    def __init__(self, to_clone=None):
        super(Polygon, self).__init__(to_clone=to_clone)
        self.on_update = None

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def clone(self):
        pass

    def update(self, dt):
        if self.on_update is not None:
            self.on_update(self, dt)

