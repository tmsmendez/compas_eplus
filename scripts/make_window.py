import os
import compas_energyplus
from compas_energyplus.datastructures import Window

for i in range(50): print('')

w = 5
# l = 3
h = 3

w_ = w / 2
h_ = h / 2

v0 = [w_, 0, h_]
v1 = [w_ *  2, 0, h_]
v2 = [w_ * 2, 0, h_ * 2]
v3 = [w_, 0, h_ * 2]

win = Window()
win.name = 'w1'
win.nodes = [v0, v1, v2, v3]
win.building_surface = 'zone1_2'
win.construction = 'Generic Double Pane'
win.to_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'w1.json'))
