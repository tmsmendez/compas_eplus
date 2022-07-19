import os
import json
import compas_eplus

from compas_eplus.viewers import BuildingViewer

from compas_eplus.building import Building
from compas_eplus.building import Window

for i in range(50): print('')

path = compas_eplus.TEMP
wea = compas_eplus.SEATTLE

quad = [[0,0,0],
        [30,0,0],
        [30,10,0],
        [0,10,0],
        ]
zone_depth = [3., 3, 3, 3]
b = Building.from_quad(path, wea, quad, zone_depth, height=3)


# zone = b.zones[0]
# w = Window.from_wall_and_wwr(zone, 2, .6, 'Generic Double Pane')
# b.add_window(w)


# # filepath = os.path.join(compas_eplus.DATA, 'materials', 'material_library_simple.json')
# # b.add_materials_from_json(filepath)

# filepath = os.path.join(compas_eplus.DATA, 'materials', 'materials.csv')
# b.add_materials_from_csv(filepath)

# filepath = os.path.join(compas_eplus.DATA, 'constructions', 'construction_library_simple.json')
# with open(filepath, 'r') as fp:
#     lib = json.load(fp)
# b.add_constructions_from_lib(lib)

v = BuildingViewer(b)
v.show()

# b.write_idf()
# b.analyze(exe='/Applications/EnergyPlus-9-6-0/energyplus')
# # b.analyze(exe='/Applications/EnergyPlus/energyplus')
# for i in range(50): print('')
# b.load_results()
# b.plot_mean_zone_temperatures(plot_type='scatter')
