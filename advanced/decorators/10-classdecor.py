# 10-classdecor.py
import inspect
from math import pi
from numbers import Number


class TypeChecker:
    required_type = object

    def __init__(self, name):
        self.ivar_name = f'_{name}'

    def __get__(self, instance, owner=None):
        return instance.__dict__[self.ivar_name]

    def __set__(self, instance, value):
        # Beware: bool is a subclass of int (for historical reasons)
        if not isinstance(value, self.required_type) or \
                (self.required_type != bool and isinstance(value, bool)):
            raise TypeError(f'expecting a {self.required_type.__name__}')
        instance.__dict__[self.ivar_name] = value


def typechecked(cls):
    for name, attribute in vars(cls).items():
        if inspect.isclass(attribute) and issubclass(attribute, TypeChecker):
            setattr(cls, name, attribute(name))
    return cls


class NumberType(TypeChecker):
    required_type = Number


@typechecked
class Point:
    x = NumberType
    y = NumberType

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __str__(self):
        return f'{self.x}, {self.y}'


class PointType(TypeChecker):
    required_type = Point


@typechecked
class Circle:
    radius = NumberType
    center = PointType

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    @property
    def area(self):
        return pi * self.radius ** 2

    def __repr__(self):
        return f'Circle({self.center!r}, {self.radius!r})'

    def __str__(self):
        return f'Circle of radius {self.radius} at {self.center}'
