# 12-classdecor_bonus.py
from math import pi


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
    for name, value in cls.__annotations__.items():
        class Checker(TypeChecker):
            required_type = value
        setattr(cls, name, Checker(name))
    return cls


@typechecked
class Point:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __str__(self):
        return f'{self.x}, {self.y}'


@typechecked
class Circle:
    center: Point
    radius: int

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
