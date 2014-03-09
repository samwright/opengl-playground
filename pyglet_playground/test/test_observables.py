from nose.tools import assert_equals
from core.utility import ObservableProperties, ObservableMethods

__author__ = 'eatmuchpie'


@ObservableProperties('a', 'b')
@ObservableMethods('func_a', 'func_b')
class Obs(object):
    def func_a(self):
        return 'a'

    def func_b(self):
        return 'b'


class TestObservables(object):

    def setup(self):
        self.obj = Obs()
        self.callback_args = []

        def callback(*args):
            self.callback_args.append(args)

        self.obj.callbacks = [callback]


    def test_change_properties(self):
        self.obj.a = 5
        assert_equals(5, self.obj.a, "Didn't save 'a'")
        self.obj.b = 6
        assert_equals(6, self.obj.b, "Didn't save 'b'")

        assert_equals(2, len(self.callback_args), "Callback called {0} times "
                              "instead of twice".format(len(self.callback_args)))

        assert_equals((self.obj, 'a'), self.callback_args[0], "Wrong callback args")
        assert_equals((self.obj, 'b'), self.callback_args[1], "Wrong callback args")

    def test_call_method(self):
        assert_equals('a', self.obj.func_a())
        assert_equals('b', self.obj.func_b())

        assert_equals(2, len(self.callback_args))

        assert_equals((self.obj, 'func_a'), self.callback_args[0])
        assert_equals((self.obj, 'func_b'), self.callback_args[1])

    def test_mutate_properties(self):
        self.obj.a = Obs()
        self.callback_args = []
        self.obj.a.a = 3

        assert_equals(3, self.obj.a.a, "Nested object's setter didnt work")
        assert self.callback_args == [(self.obj, 'a')]