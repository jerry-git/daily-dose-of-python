from typing import TypeVar

TShape = TypeVar("TShape", bound="Shape")


class Shape:
    def set_scale(self: TShape, scale: float) -> TShape:
        self.scale = scale
        return self


class Circle(Shape):
    def set_radius(self, radius: float) -> Circle:
        self.radius = radius
        return self
