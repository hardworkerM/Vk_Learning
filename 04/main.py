class CustomMeta(type):

    def __new__(mcs, name, bases, class_dict, **kwargs):
        new_class_dict = {}
        for key in class_dict:
            if key[:2] == '__' and key[-2:] == '__':
                new_class_dict[key] = class_dict[key]
            else:
                new_class_dict['custom_' + key] = class_dict[key]
        new_class_dict['__setattr__'] = mcs.set_attribute
        cls = super().__new__(mcs, name, bases, new_class_dict, **kwargs)
        return cls

    def __init__(cls, name, bases, class_dict, **kwargs):
        super().__init__(name, bases, class_dict, **kwargs)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    def set_attribute(self, key, value):
        key = 'custom_' + key
        object.__setattr__(self, key, value)


class Integer:
    def __get__(self, obj, objtype):
        if '_val' in self.__dict__:
            return self._val
        else:
            raise AttributeError('There is no such attribute')

    def __set__(self, obj, val):
        if isinstance(val, int):
            self._val = val
        else:
            raise TypeError(f'Attribute must be integer')

    def __delete__(self, obj):
        del self._val


class String:
    def __get__(self, obj, objtype):
        if '_val' in self.__dict__:
            return self._val
        else:
            raise AttributeError('There is no such attribute')

    def __set__(self, obj, val):
        if isinstance(val, str):
            self._val = val
        else:
            raise TypeError(f'Attribute must be string')

    def __delete__(self, obj):
        del self._val


class PositiveInteger:
    def __get__(self, obj, objtype):
        if '_val' in self.__dict__:
            return self._val
        else:
            raise AttributeError('There is no such attribute')

    def __set__(self, obj, val):
        print('set', val)
        if isinstance(val, int) and val < 0:
            self._val = val
        else:
            raise TypeError(f'Attribute must be integer and negative')

    def __delete__(self, obj):
        del self._val
