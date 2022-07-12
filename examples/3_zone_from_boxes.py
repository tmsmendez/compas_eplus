for i in range(50): print('')

import os
import json

import compas_eplus

from compas_eplus.building import Building
from compas_eplus.building import Zone
from compas_eplus.building import Window
from compas_eplus.building import Shading

from compas_eplus.viewers import BuildingViewer

data = compas_eplus.DATA

path = os.path.join(compas_eplus.TEMP)
wea = os.path.join(data, 'weather_files', 'USA_WA_Seattle-Tacoma.Intl.AP.727930_TMY3.epw')
# wea = os.path.join(data, 'weather_files', 'USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw')
b = Building(path, wea)

z1 = Zone.from_json(os.path.join(compas_eplus.DATA, 'building_parts', 'zone1.json'))
b.add_zone(z1)

z2 = Zone.from_json(os.path.join(compas_eplus.DATA, 'building_parts', 'zone2.json'))
b.add_zone(z2)

z3 = Zone.from_json(os.path.join(compas_eplus.DATA, 'building_parts', 'zone3.json'))
b.add_zone(z3)

w1 = Window.from_json(os.path.join(compas_eplus.DATA, 'building_parts', 'w1.json'))
b.add_window(w1)

w2 = Window.from_wall_and_wwr(z3, 3, .6, 'Generic Double Pane')
b.add_window(w2)

s1 = Shading.from_json(os.path.join(compas_eplus.DATA, 'building_parts', 'shading1.json'))
b.add_shading(s1)

filepath = os.path.join(compas_eplus.DATA, 'materials', 'material_library_simple.json')
with open(filepath, 'r') as fp:
    lib = json.load(fp)
b.add_materials_from_lib(lib)

filepath = os.path.join(compas_eplus.DATA, 'constructions', 'construction_library_simple.json')
with open(filepath, 'r') as fp:
    lib = json.load(fp)
b.add_constructions_from_lib(lib)

b.write_idf()
# b.analyze(exe='/Applications/EnergyPlus-9-6-0/energyplus')
b.analyze(exe='/Applications/EnergyPlus/energyplus')
for i in range(50): print('')
b.load_results()
b.plot_mean_zone_temperatures(plot_type='scatter')

v = BuildingViewer(b)
v.show()

b.to_json(os.path.join(compas_eplus.DATA, 'buildings', '1zone_building.json'))