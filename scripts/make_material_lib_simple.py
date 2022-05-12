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
from compas_energyplus.datastructures import MaterialNoMass
from compas_energyplus.datastructures import WindowMaterialGlazing
from compas_energyplus.datastructures import WindowMaterialGas


m1 = Material()
m1.name                = 'C5 - 4 IN HW CONCRETE'
m1.roughness           = 'MediumRough'         
m1.thickness           = 0.1014984           
m1.conductivity        = 1.729577            
m1.density             = 2242.585            
m1.specific_heat       = 836.8000            
m1.thermal_absorptance = 0.9000000           
m1.solar_absorptance   = 0.6500000           
m1.visible_absorptance = 0.6500000           

m2 = MaterialNoMass()
m2.name                      = 'R13LAYER'
m2.roughness                 = 'Rough'
m2.thermal_resistance        = 2.290965
m2.thermal_absorptance       = 0.9000000
m2.solar_absorptance         = 0.7500000
m2.visible_absorptance       = 0.7500000

m3 = MaterialNoMass()
m3.name                      = 'R31LAYER'
m3.roughness                 = 'Rough'
m3.thermal_resistance        = 5.456
m3.thermal_absorptance       = 0.900000000
m3.solar_absorptance         = 0.750000000
m3.visible_absorptance       = 0.750000000


m4 = WindowMaterialGlazing()
m4.name                                    = 'Generic Low-e Glass'
m4.optical_data_type                       = 'SpectralAverage'
m4.win_glass_spectral_data_name            = ''
m4.thickness                               = 0.006
m4.solar_transmittance                     = 0.45
m4.front_solar_reflectance                 = 0.36
m4.back_solar_reflectance                  = 0.36
m4.visible_transmittance                   = 0.71
m4.front_visible_reflectance               = 0.21
m4.back_visible_reflectance                = 0.21
m4.infrared_transmittance                  = None
m4.front_infrared_hemispherical_emissivity = 0.84
m4.back_infrared_hemispherical_emissivity  = 0.047
m4.conductivity                            = 1
m4.dirt_correction_factor                  = 1
m4.solar_diffusing                         = 'No'



m5 = WindowMaterialGlazing()
m5.name                                    = 'Generic Clear Glass'
m5.optical_data_type                       = 'SpectralAverage'
m5.win_glass_spectral_data_name            = ''
m5.thickness                               = 0.006
m5.solar_transmittance                     = 0.77
m5.front_solar_reflectance                 = 0.07
m5.back_solar_reflectance                  = 0.07
m5.visible_transmittance                   = 0.88
m5.front_visible_reflectance               = 0.08
m5.back_visible_reflectance                = 0.08
m5.infrared_transmittance                  = None
m5.front_infrared_hemispherical_emissivity = 0.84
m5.back_infrared_hemispherical_emissivity  = 0.84
m5.conductivity                            = 1
m5.dirt_correction_factor                  = 1
m5.solar_diffusing                         = 'No'


m6 = WindowMaterialGas()
m6.name      = 'Generic Window Air Gap'
m6.gas_type  = 'Air'
m6.thickness = 0.0127

materials = [m1, m2, m3, m4, m5, m6]
data = {}
for mat in materials:
    data[mat.name] = mat.data

filepath = os.path.join(compas_energyplus.DATA, 'materials', 'material_library_simple.json')
with open(filepath, 'w+') as fp:
    json.dump(data, fp)

