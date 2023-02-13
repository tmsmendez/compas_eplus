for i in range(50): print('')

import os
import json

import compas_eplus

from compas_eplus.building import Building
from compas_eplus.building import Zone
from compas_eplus.building import Window
# from compas_eplus.building import Shading
from compas_eplus.building import EquipmentList
from compas_eplus.building import EquipmentConnection
from compas_eplus.building import NodeList
from compas_eplus.building import IdealAirLoad

from compas_eplus.viewers import BuildingViewer
from compas_eplus.viewers import ResultsViewer

from compas.datastructures import Mesh
from compas_eplus.read_write import get_idf_data

data = compas_eplus.DATA

path = os.path.join(compas_eplus.TEMP)
wea = compas_eplus.SEATTLE




file = 'doe_midrise_apt.idf'
filepath = os.path.join(compas_eplus.DATA, 'idf_examples', file)
path = compas_eplus.TEMP
wea = compas_eplus.SEATTLE


w = 20
l = 10
h = 4

vertices = [[0, 0, 0],
            [w, 0, 0],
            [w, l, 0],
            [0, l, 0],
            [0, 0, h],
            [w, 0, h],
            [w, l, h],
            [0, l, h]]
faces = [[0, 3, 2, 1],
         [4, 5, 6, 7],
         [0, 1, 5, 4],
         [1, 2, 6, 5],
         [2, 3, 7, 6],
         [3, 0, 4, 7]]

b = Building(path, wea)

num_stories = 4
meshes = []
for i in range(num_stories):
    for v in vertices[:4]:
        v[2] = h * i
    for v in vertices[4:]:
        v[2] = h * (i + 1) 
    meshes.append(Mesh.from_vertices_and_faces(vertices, faces))

for i, mesh in enumerate(meshes):
    z = Zone.from_mesh(mesh, 'zone_{}'.format(i))
    b.add_zone(z)

points = [[w / 4., 0, h / 4.],
            [w / 2., 0, h / 4. ],
            [w / 2., 0, h / 2.],
            [w / 4., 0, h / 2.]
            ]

w = Window.from_points_and_zone(points, b.zones[0])
w.construction = 'Generic Double Pane'
b.add_window(w)

data = get_idf_data(filepath)
b.add_data_from_idf(data)


rules = {'Wall': 'Typical Insulated Steel Framed Exterior Wall-R16',
         'Window': 'Generic Double Pane',
         'Floor': 'Generic Interior Floor',
         'Roof': 'Generic Roof'}

b.assign_constructions_from_rules(rules)

b.set_zone_systems()

v = BuildingViewer(b)
v.show()

b.write_idf()
b.analyze(exe='/Applications/EnergyPlus/energyplus')
b.load_results()

v = ResultsViewer(b)
v.show('total')
