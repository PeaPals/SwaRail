import math


class Vec2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, coordinate):
        return Vec2(self.x + coordinate.x, self.y + coordinate.y)

    def __sub__(self, coordinate):
        return Vec2(self.x - coordinate.x, self.y - coordinate.y)

    def __truediv__(self, coordinate):
        return Vec2(self.x / coordinate.x, self.y / coordinate.y)

    def __floordiv__(self, coordinate):
        return Vec2(self.x // coordinate.x, self.y // coordinate.y)

    def __mul__(self, coordinate):
        return Vec2(self.x * coordinate.x, self.y * coordinate.y)

    def __pow__(self, power):
        return Vec2(self.x ** power, self.y ** power)

    def __abs__(self, coordinate):
        return Vec2(abs(coordinate.x), abs(coordinate.y))

    def __eq__(self, coordinate):
        if not isinstance(coordinate, Vec2):
            return False

        return (self.x == coordinate.x) and (self.y == coordinate.y)

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"

    def __hash__(self):
        return hash(self.__repr__())


    @staticmethod
    def euclidian_distance(coordinate_1, coordinate_2):
        diff = (coordinate_2 - coordinate_1) ** 2
        return (diff.x + diff.y) ** 0.5


    @staticmethod
    def manhaten_distance(coordinate_1, coordinate_2):
        diff = abs(coordinate_2 - coordinate_1)
        return diff.x + diff.y


    @staticmethod
    def slope(coordinate_1, coordinate_2, format='rad'):
        diff = coordinate_2 - coordinate_1
        slope = diff.x / diff.y

        match format:
            case 'rad': math.degrees(math.atan(slope))
            case 'deg': return slope