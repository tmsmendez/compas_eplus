from __future__ import print_function
import compas_energyplus

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
from compas.datastructures import Mesh
from compas_energyplus.datastructures import Zone

for i in range(50): print('')

w = 5
l = 3
h = 3

v0 = [0, 0, 0]
v1 = [w, 0, 0]
v2 = [w, l, 0]
v3 = [0, l, 0]
v4 = [0, 0, h]
v5 = [w, 0, h]
v6 = [w, l, h]
v7 = [0, l, h]

f0 = [0, 3, 2, 1]
# f0 = [0, 1, 2, 3]
f1 = [4, 5, 6, 7]
f2 = [0, 1, 5, 4]
f3 = [1, 2, 6, 5]
f4 = [2, 3, 7, 6]
f5 = [3, 0, 4, 7]

vertices = [v0, v1, v2, v3, v4, v5, v6, v7]
faces = [f0, f1, f2, f3, f4, f5]

name = 'zone1'
mesh = Mesh.from_vertices_and_faces(vertices, faces)
zone = Zone()
zone.name = name
zone.add_surfaces(mesh)
zone.to_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'zone1.json'))


w = 5
l = 3
h = 3
h_base = 3

v0 = [0, 0, 0 + h_base]
v1 = [w, 0, 0 + h_base]
v2 = [w, l, 0 + h_base]
v3 = [0, l, 0 + h_base]
v4 = [0, 0, h + h_base]
v5 = [w, 0, h + h_base]
v6 = [w, l, h + h_base]
v7 = [0, l, h + h_base]

f0 = [0, 3, 2, 1]
# f0 = [0, 1, 2, 3]
f1 = [4, 5, 6, 7]
f2 = [0, 1, 5, 4]
f3 = [1, 2, 6, 5]
f4 = [2, 3, 7, 6]
f5 = [3, 0, 4, 7]

vertices = [v0, v1, v2, v3, v4, v5, v6, v7]
faces = [f0, f1, f2, f3, f4, f5]

name = 'zone2'
mesh = Mesh.from_vertices_and_faces(vertices, faces)
zone = Zone()
zone.name = name
zone.add_surfaces(mesh)
zone.to_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'zone2.json'))


w = 5
l = 3
h = 3
h_base = 0
l_base = l

v0 = [0, 0 + l_base, 0 + h_base]
v1 = [w, 0 + l_base, 0 + h_base]
v2 = [w, l + l_base, 0 + h_base]
v3 = [0, l + l_base, 0 + h_base]
v4 = [0, 0 + l_base, h + h_base]
v5 = [w, 0 + l_base, h + h_base]
v6 = [w, l + l_base, h + h_base]
v7 = [0, l + l_base, h + h_base]

f0 = [0, 3, 2, 1]
# f0 = [0, 1, 2, 3]
f1 = [4, 5, 6, 7]
f2 = [0, 1, 5, 4]
f3 = [1, 2, 6, 5]
f4 = [2, 3, 7, 6]
f5 = [3, 0, 4, 7]

vertices = [v0, v1, v2, v3, v4, v5, v6, v7]
faces = [f0, f1, f2, f3, f4, f5]

name = 'zone3'
mesh = Mesh.from_vertices_and_faces(vertices, faces)
zone = Zone()
zone.name = name
zone.add_surfaces(mesh)
zone.to_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'zone3.json'))