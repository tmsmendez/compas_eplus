import os
import json
import compas_eplus

from compas_eplus.viewers import BuildingViewer

from compas_eplus.building import Building
from compas_eplus.building import Window
from compas_eplus.building import Construction

for i in range(50): print('')

path = compas_eplus.TEMP
wea = compas_eplus.SEATTLE

width = 20
depth = 10
height = 3

quad = [[0, 0, 0],
        [width, 0, 0],
        [width, depth, 0],
        [0, depth, 0]]


zone_depth = [3., 3., 3., 3.]
b = Building.from_quad(path, wea, quad, zone_depth, height=height)


zone = b.zones[0]
w = Window.from_wall_and_wwr(zone, 2, .6)
w.construction = 'double_glazing'
b.add_window(w)

zone = b.zones[1]
w = Window.from_wall_and_wwr(zone, 2, .4)
w.construction = 'double_glazing'
b.add_window(w)

zone = b.zones[2]
w = Window.from_wall_and_wwr(zone, 2, .2)
w.construction = 'double_glazing'
b.add_window(w)

zone = b.zones[3]
w = Window.from_wall_and_wwr(zone, 2, .1)
w.construction = 'double_glazing'
b.add_window(w)

c = Construction()
c.name = 'ext_wall'
c.layers = {0: {'name': 'Generic Painted Metal', 'thickness':.003},
            1: {'name': 'Generic Wall Air Gap', 'thickness':.03},
            2: {'name': 'Generic Insulation', 'thickness':.006},
            3: {'name': 'Generic Gypsum Board', 'thickness':.012},
            }
b.add_construction(c)

c = Construction()
c.name = 'double_glazing'
c.layers = {0: {'name': 'Generic Low-e Glass', 'thickness':.006},
            1: {'name': 'Generic Window Air Gap', 'thickness':.0127},
            2: {'name': 'Generic Clear Glass', 'thickness':.006}}
b.add_construction(c)

# these should be updated ------------------------------------------------------
c = Construction()
c.name = 'cieling'
c.layers = {0: {'name': 'Generic Painted Metal', 'thickness':.003},
            1: {'name': 'Generic Wall Air Gap', 'thickness':.03},
            2: {'name': 'Generic Insulation', 'thickness':.006},
            3: {'name': 'Generic Gypsum Board', 'thickness':.012},
            }
b.add_construction(c)

c = Construction()
c.name = 'floor'
c.layers = {0: {'name': 'Generic Painted Metal', 'thickness':.003},
            1: {'name': 'Generic Wall Air Gap', 'thickness':.03},
            2: {'name': 'Generic Insulation', 'thickness':.006},
            3: {'name': 'Generic Gypsum Board', 'thickness':.012},
            }
b.add_construction(c)
# ------------------------------------------------------------------------------

filepath = os.path.join(compas_eplus.DATA, 'materials', 'materials.csv')
b.add_materials_from_csv(filepath)

rules = {'wall': 'ext_wall', 'window': 'double_glazing', 'floor': 'floor', 'ceiling': 'cieling'}
b.assign_constructions_from_rules(rules)


v = BuildingViewer(b)
v.show()

b.write_idf()
b.analyze(exe='/Applications/EnergyPlus-9-6-0/energyplus')
# b.analyze(exe='/Applications/EnergyPlus/energyplus')
for i in range(50): print('')
b.load_results()
b.plot_mean_zone_temperatures(plot_type='scatter')
b.to_json(os.path.join(compas_eplus.DATA, 'buildings', '5_zone.json'))


