from contextlib import contextmanager
import numpy as np

from pyglet.gl import GLfloat

__author__ = 'eatmuchpie'


class Singleton(object):
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)

        return self.instance


def vec(*args):
    return (GLfloat * len(args))(*args)


class ObservableMethods(object):
    def __init__(self, *observed_method_names):
        self.observed_method_names = observed_method_names

    def __call__(self, cls):
        # Wrap class constructor to create callbacks list
        _add_callback_to_class(cls)

        def make_method_observable(method_name):
            original_method = getattr(cls, method_name)

            def replacement_method(inner_self, *args, **kwargs):
                result = original_method(inner_self, *args, **kwargs)
                inner_self.callback(inner_self, method_name)
                return result

            setattr(cls, method_name, replacement_method)

        # Wrap observed methods to run callbacks
        for observed_method_name in self.observed_method_names:
            make_method_observable(observed_method_name)

        return cls


def _add_callback_to_class(cls):
    original_init = cls.__init__

    def replacement_init(inner_self, *args, **kwargs):
        if not hasattr(inner_self, 'callbacks'):
            inner_self.callbacks = set()
            inner_self._is_calling_back = False
        original_init(inner_self, *args, **kwargs)

    def callback(inner_self, object, reason):
        if not inner_self._is_calling_back:
            inner_self._is_calling_back = True
            try:
                for callback_func in inner_self.callbacks:
                    callback_func(object, reason)
            finally:
                inner_self._is_calling_back = False


    @contextmanager
    def delayed_callback(inner_self, reason):
        """
        Delay callbacks to this object, then do one callback at the end.
        """
        if inner_self._is_calling_back:
            # For now, raise an exception
            raise Exception(
                "tried a delayed_callback during a delayed_callback or callback")
        inner_self._is_calling_back = True
        yield
        inner_self._is_calling_back = False
        inner_self.callback(inner_self, reason)

    cls.__init__ = replacement_init
    cls.callback = callback
    cls.delayed_callback = delayed_callback


class ObservableProperties(object):
    """
    Add properties to the decorated class.

    If the properties are replaced, the funtions in self.callbacks are called
    (by self.callback()). The functions are given two arguments: the changed
    object (self) and the name of the replaced property.

    If the new property value is observable itself (i.e. it has an obj.callbacks
    set) then any internal mutations to the new object will trigger
    self.callback(). The arguments given to the self.callbacks functions are
    the same as in the above paragraph.

    Whilst self.callback() is running, modifications won't trigger another
    self.callback(). If you want to run another code block without triggering
    self.callback(), you can run it inside a self.delayed_callback()
    with-block, after which self.callback() will be called, e.g.:

    with self.delayed_callback():
        code_block()
    """

    def __init__(self, *observable_properties):
        self.observable_properties = observable_properties

    def __call__(self, cls):
        _add_callback_to_class(cls)

        def add_observable_property_to_class(prop):
            hidden_property = '_' + prop
            setattr(cls, hidden_property, None)

            def setter(inner_self, value):
                setattr(inner_self, hidden_property, value)
                if hasattr(value, 'callbacks'):
                    value.callbacks.add(
                        lambda x, y: inner_self.callback(inner_self, prop))
                inner_self.callback(inner_self, prop)

            def getter(inner_self):
                return getattr(inner_self, hidden_property)

            setattr(cls, prop, property(getter, setter))


        for observable_property in self.observable_properties:
            add_observable_property_to_class(observable_property)

        return cls


@ObservableMethods('__setitem__', '__setslice__')
class ObservableArray(np.ndarray):
    @staticmethod
    def like(input_array):
        input_array = np.array(input_array)
        new_array = ObservableArray(np.array(input_array).shape)
        new_array[:] = input_array
        return new_array