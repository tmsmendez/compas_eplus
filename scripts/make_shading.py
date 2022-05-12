import os
import compas_energyplus
from compas_energyplus.datastructures import Shading
from compas.datastructures import Mesh

for i in range(50): print('')

w = 5.
l = 3.
d = 2.
h = 3.

w_ = w / 2.
h_ = h / 2.

v0 = [w_, 0, h_]
v1 = [w_ *  2, 0, h_]
v2 = [w_ * 2, 0, h_ * 2]
v3 = [w_, 0, h_ * 2]

v0_ = [w_, -d, h_]
v1_ = [w_ *  2, -d, h_]
v2_ = [w_ * 2, -d, h_ * 2]
v3_ = [w_, -d, h_ * 2]

vertices = [v0, v1, v2, v3, v0_, v1_, v2_, v3_]
f1 = [0, 4, 7, 3]
f2 = [3, 7, 6, 2]
f3 = [2, 1, 5, 6]
faces = [f1, f2, f3]

win = Shading()
win.name = 's1'
win.mesh = Mesh.from_vertices_and_faces(vertices, faces)
win.to_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'shading1.json'))
