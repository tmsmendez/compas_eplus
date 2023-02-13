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


b = Building.from_quad_5zone(path, wea, quad, height=height, zone_depth=depth/4.)
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

eqc = b.equipment_connections['generic_zone']
eql = b.equipment_lists['doe_midrise_apt_equipment_list']
inl = b.node_lists['doe_midrise_apt_inlet_node_list']
enl = b.node_lists['doe_midrise_apt_exhaust_node_list']
ial = b.ideal_air_loads['doe_midrise_apt_ideal_loads']

from copy import deepcopy

for zk in b.zones:
    zname = b.zones[zk].name

    b.node_lists[zk] = NodeList.from_data(deepcopy(inl.data))
    inlname = '{}_{}'.format(b.node_lists[zk].name, zname)
    b.node_lists[zk].name = inlname
    b.node_lists[zk].nodes['0'] = 'inlet_node_{}'.format(zname)

    b.node_lists[zname] = NodeList.from_data(deepcopy(enl.data))
    enlname = '{}_{}'.format(b.node_lists[zname].name, zname)
    b.node_lists[zname].name = enlname
    b.node_lists[zname].nodes['0'] = 'exhaust_node_{}'.format(zname)

    b.ideal_air_loads[zk] = IdealAirLoad.from_data(deepcopy(ial.data))
    ialname = '{} {}'.format(zname, b.ideal_air_loads[zk].name)
    b.ideal_air_loads[zk].name = ialname
    b.ideal_air_loads[zk].zone_supply_air_node_name = inlname
    b.ideal_air_loads[zk].zone_exhaust_air_node_name = enlname

    b.equipment_lists[zk] = EquipmentList.from_data(eql.data)
    elname =  '{}_{}'.format(b.equipment_lists[zk].name, zname)
    b.equipment_lists[zk].name = elname
    b.equipment_lists[zk].zone_equipment_name1 = ialname

    b.equipment_connections[zk] = EquipmentConnection.from_data(eqc.data)
    b.equipment_connections[zk].name = zname
    b.equipment_connections[zk].zone_conditioning_equipment_list = elname
    b.equipment_connections[zk].zone_air_inlet_node = inlname
    b.equipment_connections[zk].zone_air_exhaust_node = enlname
    b.equipment_connections[zk].zone_air_node += '_{}'.format(zname)

del b.equipment_connections['generic_zone']
del b.equipment_lists['doe_midrise_apt_equipment_list']
del b.node_lists['doe_midrise_apt_inlet_node_list']
del b.node_lists['doe_midrise_apt_exhaust_node_list']
del b.ideal_air_loads['doe_midrise_apt_ideal_loads']


v = BuildingViewer(b)
v.show()

b.write_idf()
b.analyze(exe='/Applications/EnergyPlus/energyplus')
b.load_results()

v = ResultsViewer(b)
v.show('total')

#TODO: why is the deep copy needed!!!!