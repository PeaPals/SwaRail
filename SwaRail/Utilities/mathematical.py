import math

def coordinate_distance(coordinate_1, coordinate_2):
        return (
            (coordinate_2[0] - coordinate_1[0]) ** 2 + (coordinate_2[1] - coordinate_2[1]) ** 2
        ) ** 0.5


def coordinate_slope(coordinate_1, coordinate_2, format="rad"):
    slope = (coordinate_2[1] - coordinate_1[1]) / (coordinate_2[0] - coordinate_1[0])

    if format == "rad":
        return math.degrees(math.atan(slope))

    return slope