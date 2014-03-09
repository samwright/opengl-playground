from nose.tools import assert_equals
import numpy as np
from core.transformable import Transformable
from core.utility import ObservableArray

__author__ = 'eatmuchpie'


class TestTransformable(object):

    def setup(self):
        self.obj = Transformable()
        self.callback_args = []

        def callback(*args):
            self.callback_args.append(args)

        self.obj.callbacks = [callback]

    def test_change_size(self):
        new_size = [1., 2., 3.]
        self.obj.size[:] = [1., 2., 3.]
        assert np.array_equal(new_size, self.obj.size)

        assert [(self.obj, 'size')] == self.callback_args, "callback args = " + str(self.callback_args)

    def test_replace_size(self):
        new_size = [1., 2., 3.]
        self.obj.size = ObservableArray.like(new_size)
        assert np.array_equal(new_size, self.obj.size)