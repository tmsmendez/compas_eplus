from __future__ import print_function


__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import json
import compas_energyplus
from compas_energyplus.datastructures import Material


m1 = Material()
m1.name                = 'ExtFraming'
m1.roughness           = 'MediumRough'
m1.thickness           = 0.0254
m1.conductivity        = 1.802
m1.density             = 2255
m1.specific_heat       = 750
m1.thermal_absorptance = 0.9
m1.solar_absorptance   = 0.7
m1.visible_absorptance = 0.7


m2 = Material()
m2.name                = 'FacadeCladding'
m2.roughness           = 'MediumRough'
m2.thickness           = 0.0006
m2.conductivity        = 70
m2.density             = 2700
m2.specific_heat       = 870
m2.thermal_absorptance = 0.9
m2.solar_absorptance   = 0.7
m2.visible_absorptance = 0.7


m2 = Material()
m2.name                = 'Generic 25mm Insulation'
m2.roughness           = 'MediumRough'
m2.thickness           = 0.05
m2.conductivity        = 0.03
m2.density             = 43
m2.specific_heat       = 1210
m2.thermal_absorptance = 0.9
m2.solar_absorptance   = 0.7
m2.visible_absorptance = 0.7


m3 = Material()
m3.name                = 'Generic 25mm Wood'
m3.roughness           = 'MediumSmooth'
m3.thickness           = 0.0254
m3.conductivity        = 0.15
m3.density             = 608
m3.specific_heat       = 1630
m3.thermal_absorptance = 0.9
m3.solar_absorptance   = 0.5
m3.visible_absorptance = 0.5


m4 = Material()
m4.name                = 'Generic 50mm Insulation'
m4.roughness           = 'MediumRough'
m4.thickness           = 0.05
m4.conductivity        = 0.03
m4.density             = 43
m4.specific_heat       = 1210
m4.thermal_absorptance = 0.9
m4.solar_absorptance   = 0.7
m4.visible_absorptance = 0.7


m5 = Material()
m5.name                = 'Generic Acoustic Tile'
m5.roughness           = 'MediumSmooth'
m5.thickness           = 0.02
m5.conductivity        = 0.06
m5.density             = 368
m5.specific_heat       = 590
m5.thermal_absorptance = 0.9
m5.solar_absorptance   = 0.2
m5.visible_absorptance = 0.2


m6 = Material()
m6.name                = 'Generic Brick'
m6.roughness           = 'MediumRough'  
m6.thickness           = 0.1
m6.conductivity        = 0.9
m6.density             = 1920
m6.specific_heat       = 790
m6.thermal_absorptance = 0.9
m6.solar_absorptance   = 0.65
m6.visible_absorptance = 0.65


m7 = Material()
m7.name                = 'Generic Ceiling Air Gap'
m7.roughness           = 'Smooth'                
m7.thickness           = 0.1
m7.conductivity        = 0.556
m7.density             = 1.28
m7.specific_heat       = 1000
m7.thermal_absorptance = 0.9
m7.solar_absorptance   = 0.7 
m7.visible_absorptance = 0.7

m6 = Material()
m6.name                = 'Generic Gypsum Board'
m6.roughness           = 'MediumSmooth'       
m6.thickness           = 0.0127
m6.conductivity        = 0.16
m6.density             = 800
m6.specific_heat       = 1090
m6.thermal_absorptance = 0.9
m6.solar_absorptance   = 0.5
m6.visible_absorptance = 0.5

m7 = Material()
m7.name                = 'Generic LW Concrete'
m7.roughness           = 'MediumRough'
m7.thickness           = 0.1
m7.conductivity        = 0.53
m7.density             = 1280
m7.specific_heat       = 840
m7.thermal_absorptance = 0.9
m7.solar_absorptance   = 0.8
m7.visible_absorptance = 0.8


m8 = Material()
m8.name                = 'Generic Painted Metal'
m8.roughness           = 'Smooth'              
m8.thickness           = 0.0015
m8.conductivity        = 45
m8.density             = 7690
m8.specific_heat       = 410
m8.thermal_absorptance = 0.9
m8.solar_absorptance   = 0.5
m8.visible_absorptance = 0.5


m9 = Material()
m9.name                = 'Generic Roof Membrane'
m9.roughness           = 'MediumRough'
m9.thickness           = 0.01
m9.conductivity        = 0.16
m9.density             = 1120
m9.specific_heat       = 1460
m9.thermal_absorptance = 0.9
m9.solar_absorptance   = 0.65
m9.visible_absorptance = 0.65


m10 = Material()
m10.name                = 'Generic Wall Air Gap'
m10.roughness           = 'Smooth'
m10.thickness           = 0.1
m10.conductivity        = 0.667
m10.density             = 1.28
m10.specific_heat       = 1000
m10.thermal_absorptance = 0.9
m10.solar_absorptance   = 0.7
m10.visible_absorptance = 0.7

m11 = Material()
m11.name                = 'Material 1'
m11.roughness           = 'Smooth'  
m11.thickness           = 0.1
m11.conductivity        = 0.1
m11.density             = 0.1
m11.specific_heat       = 100
m11.thermal_absorptance = 0.9
m11.solar_absorptance   = 0.65
m11.visible_absorptance = 0.65


m12 = Material()
m12.name                = 'Material 2'
m12.roughness           = 'Smooth'
m12.thickness           = 0.1
m12.conductivity        = 0.1
m12.density             = 0.1
m12.specific_heat       = 100
m12.thermal_absorptance = 0.9
m12.solar_absorptance   = 0.8
m12.visible_absorptance = 0.8


materials = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12]
data = {}
for mat in materials:
    data[mat.name] = mat.data

filepath = os.path.join(compas_energyplus.DATA, 'materials', 'material_library1.json')
with open(filepath, 'w+') as fp:
    json.dump(data, fp)

