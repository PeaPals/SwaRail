from ursina import *

from ursina import EditorCamera

UI = Ursina()

point = [Vec3(i / 31, curve.in_out_sine(i / 31), 0) for i in range(32)]

model = Entity(
    model=Mesh(vertices=point, mode='line', thickness=4)
)

UI.run()