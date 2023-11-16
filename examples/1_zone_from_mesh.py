for i in range(50): print('')

import os
import compas_eplus

from compas.datastructures import Mesh

from compas_eplus.building import Building
from compas_eplus.building import Zone
from compas_eplus.building import Window
from compas_eplus.building import Shading

from compas_eplus.read_write import get_idf_data

from compas_eplus.viewers import BuildingViewer
from compas_eplus.viewers import ResultsViewer

# making a mesh for the zone - - - - - - - - - - - - - - - - - - - - - - - - - - 

w = 10
l = 20
h = 10

v0 = [0, 0, 0]
v1 = [w, 0, 0]
v2 = [w, l, 0]
v3 = [0 ,l, 0]
v4 = [0, 0, h]
v5 = [w, 0, h]
v6 = [w, l, h]
v7 = [0 ,l, h]

f0 = [0, 3, 2, 1]
f1 = [4, 5, 6, 7]
f2 = [0, 1, 5, 4]
f3 = [1, 2, 6, 5]
f4 = [2, 3, 7, 6]
f5 = [0, 4, 7, 3]

vertices = [v0, v1, v2, v3, v4, v5, v6, v7]
faces = [f0, f1, f2, f3, f4, f5]

mesh = Mesh.from_vertices_and_faces(vertices, faces)

# making a building - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - 

path = compas_eplus.TEMP
wea = compas_eplus.SEATTLE

b = Building(path, wea)

# adding zone from mesh to building - - - -  - - - - - - - - - - - - - - - - - -

z = Zone.from_mesh(mesh, 'zone_0')
b.add_zone(z)


# adding window from points - - - - - - - - - - - - - - - - - - - - - - - - - - -

points = [[w / 6., 0, h / 4.],
          [w / 4., 0, h / 4. ],
          [w / 4., 0, h / 2.],
          [w / 6., 0, h / 2.]]

w1 = Window.from_points_and_zone(points, b.zones[0])
w1.construction = 'Generic Double Pane'
b.add_window(w1)

# adding a window from WWR with shading - - - - - - - - - - - - - - - - - - - 

w2 = Window.from_wall_and_wwr(z, 3, .5)
w2.construction = 'Generic Double Pane'
b.add_window(w2)

sh = Shading.from_window(w2, top=1, right=1)
b.add_shading(sh)


# adding all other data from IDF file - - - - - - - - - - - - - - - - - - - - 

file = 'doe_midrise_apt.idf'
filepath = os.path.join(compas_eplus.DATA, 'idf_examples', file)

data = get_idf_data(filepath)
b.add_data_from_idf(data)


rules = {'Wall': 'Typical Insulated Steel Framed Exterior Wall-R16',
         'Window': 'Generic Double Pane',
         'Floor': 'Generic Interior Floor',
         'Roof': 'Generic Roof'}

b.assign_constructions_from_rules(rules)

b.set_zone_systems()

# v = BuildingViewer(b)
# v.show()

b.write_idf()
b.analyze(exe='/Applications/EnergyPlus/energyplus')
b.load_results()

v = ResultsViewer(b)
v.show('total')

