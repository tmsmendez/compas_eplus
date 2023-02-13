import os
import compas_eplus
from compas_eplus.building import Building
from compas_eplus.viewers import BuildingViewer
from compas_eplus.viewers import ResultsViewer
from compas_eplus.building import Window
from compas_eplus.read_write import get_idf_data


from compas_eplus.building import EquipmentList
from compas_eplus.building import EquipmentConnection
from compas_eplus.building import NodeList
from compas_eplus.building import IdealAirLoad


for i in range(50): print('')

file = 'doe_midrise_apt.idf'
filepath = os.path.join(compas_eplus.DATA, 'idf_examples', file)
path = compas_eplus.TEMP
wea = compas_eplus.SEATTLE

width = 20
depth = 10
height = 3

quad = [[0, 0, 0], [width, 0, 0],[width, depth, 0],[0, depth, 0]]


b = Building.from_quad_2zone(path, wea, quad, height=height)
data = get_idf_data(filepath)
b.add_data_from_idf(data)


zone = b.zones[0]
w = Window.from_wall_and_wwr(zone, 2, .6)
w.construction = 'Generic Double Pane'
b.add_window(w)

zone = b.zones[1]
w = Window.from_wall_and_wwr(zone, 2, .2)
w.construction = 'Generic Double Pane'
b.add_window(w)

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

#TODO: why is the deep copy needed!!!!