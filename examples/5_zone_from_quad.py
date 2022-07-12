import os
import json
import compas_eplus

from compas_eplus.viewers import BuildingViewer

from compas_eplus.building import Building

for i in range(50): print('')

path = compas_eplus.TEMP
wea = compas_eplus.SEATTLE

quad = [[0,0,0],
        [30,0,0],
        [30,10,0],
        [0,10,0],
        ]
zone_depth = [3., 6, 3, 6]
b = Building.from_quad(path, wea, quad, zone_depth, height=3)

filepath = os.path.join(compas_eplus.DATA, 'materials', 'material_library_simple.json')
with open(filepath, 'r') as fp:
    lib = json.load(fp)
b.add_materials_from_lib(lib)

filepath = os.path.join(compas_eplus.DATA, 'constructions', 'construction_library_simple.json')
with open(filepath, 'r') as fp:
    lib = json.load(fp)
b.add_constructions_from_lib(lib)

v = BuildingViewer(b)
v.show()
