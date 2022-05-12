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
c1.name = 'ExteriorWall_05cef855'
c1.layers = ['FacadeCladding',       
             'AirGap',               
             'ContExtInsulation',    
             'ExtFraming'
             ]

c2 = Construction()
c2.name = 'Generic Context'
c2.layers = ['Material 2']


c3 = Construction()
c3.name = 'Generic Double Pane'
c3.layers = ['Generic Low-e Glass',
             'Generic Window Air Gap',
             'Generic Clear Glass'
             ]


c4 = Construction()
c4.name = 'Generic Exposed Floor'
c4.layers = ['Generic Painted Metal',
             'Generic Ceiling Air Gap',
             'Generic 50mm Insulation',
             'Generic LW Concrete',
             ]


c5 = Construction()
c5.name = 'Generic Exterior Door'
c5.layers = ['Generic Painted Metal',
             'Generic 25mm Insulation',
             'Generic Painted Metal',
             ]


c6 = Construction()
c6.name = 'Generic Exterior Wall'
c6.layers = ['Generic Brick',
             'Generic LW Concrete',
             'Generic 50mm Insulation',
             'Generic Wall Air Gap',
             'Generic Gypsum Board',
             ]


c7 = Construction()
c7.name = 'Generic Ground Slab'
c7.layers = ['Generic 50mm Insulation',       
             'Generic HW Concrete',       
             ]


c8 = Construction()
c8.name = 'Generic Interior Ceiling'
c8.layers = ['Generic LW Concrete',    
             'Generic Ceiling Air Gap',    
             'Generic Acoustic Tile',    
             ]


c9 = Construction()
c9.name = 'Generic Interior Door'
c9.layers = ['Generic 25mm Wood',
             ]


c10 = Construction()
c10.name = 'Generic Interior Floor'
c10.layers = ['Generic Acoustic Tile',    
              'Generic Ceiling Air Gap',    
              'Generic LW Concrete',
             ]


c11 = Construction()
c11.name = 'Generic Interior Wall'
c11.layers = ['Generic Gypsum Board',  
              'Generic Wall Air Gap',    
              'Generic Gypsum Board',
              ]


c12 = Construction()
c12.name = 'Generic Roof'
c12.layers = ['Generic Roof Membrane',    
              'Generic 50mm Insulation',
              'Generic LW Concrete',
              'Generic Ceiling Air Gap',
              'Generic Acoustic Tile',
             ]


c13 = Construction()
c13.name = 'Generic Shade'
c13.layers = ['Material 1',
             ]


c14 = Construction()
c14.name = 'Generic Single Pane'
c14.layers = ['Generic Clear Glass',
             ]


c15 = Construction()
c15.name = 'Generic Underground Roof'
c15.layers = ['Generic 50mm Insulation',  
              'Generic HW Concrete',    
              'Generic Ceiling Air Gap',           
              'Generic Acoustic Tile',
             ]


c16 = Construction()
c16.name = 'Generic Underground Wall'
c16.layers = ['Generic 50mm Insulation',  
              'Generic HW Concrete', 
              'Generic Wall Air Gap',           
              'Generic Gypsum Board',
              ]


c17 = Construction()
c17.name = 'NGlass_7b80efc2'
c17.layers = ['wood_1e683bda',
             ]


c18 = Construction()
c18.name = 'SGlass_c3b30ffd'
c18.layers = ['wood_72070c24',
             ]

constructions = [c1, c2, c3, c4, c5, c6, c7, c8, c8, c10,
                 c11, c12, c13, c14, c15, c16, c17, c18]
data = {}
for con in constructions:
    data[con.name] = con.data

filepath = os.path.join(compas_energyplus.DATA, 'constructions', 'construction_library1.json')
with open(filepath, 'w+') as fp:
    json.dump(data, fp)

