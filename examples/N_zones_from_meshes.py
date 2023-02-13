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
faces = [[0, 1, 2, 3],
         [4, 7, 6, 5],
         [0, 4, 5, 1],
         [1, 5, 6, 2],
         [2, 6, 7, 3],
         [3, 7, 4, 0]]

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

# w = Window.from_wall_and_wwr()



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
