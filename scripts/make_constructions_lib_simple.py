from __future__ import print_function


__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import json
import compas_energyplus
from compas_energyplus.datastructures import Construction


c1 = Construction()
c1.name = 'R13WALL'
c1.layers = ['R13LAYER',
             ]

c2 = Construction()
c2.name = 'FLOOR'
c2.layers = ['C5 - 4 IN HW CONCRETE',
             ]

c3 = Construction()
c3.name = 'ROOF31'
c3.layers = ['R31LAYER',
             ]

c4 = Construction()
c4.name = 'Generic Double Pane'
c4.layers = ['Generic Low-e Glass',
             'Generic Window Air Gap',
             'Generic Clear Glass',
             ]


constructions = [c1, c2, c3, c4]
data = {}
for con in constructions:
    data[con.name] = con.data

filepath = os.path.join(compas_energyplus.DATA, 'constructions', 'construction_library_simple.json')
with open(filepath, 'w+') as fp:
    json.dump(data, fp)

