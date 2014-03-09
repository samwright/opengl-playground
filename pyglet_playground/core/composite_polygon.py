from core.polygon import Polygon

__author__ = 'eatmuchpie'


class CompositePolygon(Polygon):
    def __init__(self, polygons={}, to_clone=None):
        super(CompositePolygon, self).__init__(to_clone)
        if to_clone is not None:
            self._polygons = dict((k, v.clone())
                                  for k, v in to_clone._polygons.iteritems())
        else:
            self._polygons = dict(polygons)

    def draw(self):
        self.transform()

        for polygon in self._polygons.values():
            polygon.draw()

        self.untransform()

    def clone(self):
        return CompositePolygon(to_clone=self)

    def update(self, dt):
        super(CompositePolygon, self).update(dt)
        for polygon in self._polygons.values():
            polygon.update(dt)
