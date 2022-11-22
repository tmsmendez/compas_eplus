from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import re


def get_idf_data(filepath):
    data = {}
    find_zones(filepath, data)
    find_sufaces(filepath, data)
    find_windows(filepath, data)
    find_materials(filepath, data)
    return data


def find_zones(filepath, data):

    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'zone':
            i_lines.append(i)

    data['zones'] = {}    
    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        x = float(lines[i + 2].split(',')[0].strip())
        y = float(lines[i + 3].split(',')[0].strip())
        z = float(lines[i + 4].split(',')[0].strip())
        h = float(lines[i + 8].split(',')[0].strip())
        v = float(lines[i + 9].split(',')[0].strip())
        data['zones'][name] = {'origin': [x, y, z],
                               'height': h,
                               'volume':v,
                               }


def find_sufaces(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'buildingsurface:detailed':
            i_lines.append(i)
    data['surfaces']  = {}
    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        zone  = lines[i + 4].split(',')[0].strip()
        stype = lines[i + 2].split(',')[0].strip()
        cons  = lines[i + 3].split(',')[0].strip()
        outs = lines[i + 6].split(',')[0].strip()
        pts = []
        for j in range(4):
            xyz = lines[i + j + 12]
            xyz = re.split('; |, ', xyz)[:3]
            xyz = [float(x) for x in xyz]
            pts.append(xyz)


        data['surfaces'][name] = {'name': name,
                                           'surface_type': stype,
                                           'construction': cons,
                                           'outside_condition': outs,
                                           'surface_points': pts  
                                           }


def find_windows(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'fenestrationsurface:detailed':
            i_lines.append(i)
    
    data['windows'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        bs_name  = lines[i + 4].split(',')[0].strip()
        cons = lines[i + 3].split(',')[0].strip()
        stype = lines[i + 2].split(',')[0].strip()
        pts = []
        for j in range(4):
            xyz = lines[i + j + 10]
            xyz = re.split('; |, ', xyz)[:3]
            xyz = [float(x) for x in xyz]
            pts.append(xyz)

        data['windows'][name] = {'name': name,
                                 'building_surface': bs_name,
                                 'construction': cons,
                                 'surface_type': stype,
                                 'surface_points': pts  
                                 }


def find_materials(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'material':
            i_lines.append(i)

    data['materials'] = {}
    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        rough = lines[i + 2].split(',')[0].strip()
        thick  = float(lines[i + 3].split(',')[0])
        cond = float(lines[i + 4].split(',')[0])
        dens = float(lines[i + 5].split(',')[0])
        sphe = float(lines[i + 6].split(',')[0])
        thra = float(lines[i + 7].split(',')[0])
        slea = float(lines[i + 8].split(',')[0])
        vsba = float(lines[i + 9].split(';')[0])

        data['materials'][name] = {'name': name,
                                   'roughness': rough,
                                   'thickness': thick,
                                   'conductivity': cond,
                                   'density': dens,
                                   'specific_heat': sphe,
                                   'thermal_absoptance': thra,
                                   'solar_absorptance': slea,
                                   'visible_absorptance': vsba,
                                  }
    


# Material:NoMass,
#   Typical Carpet Pad,                     !- Name
#   VeryRough,                              !- Roughness
#   0.2164799871521,                        !- Thermal Resistance {m2-K/W}
#   0.9,                                    !- Thermal Absorptance
#   0.7,                                    !- Solar Absorptance
#   0.8;                                    !- Visible Absorptance





#   WindowMaterial:Gas,
#   AIR 13MM,                               !- Name
#   Air,                                    !- Gas Type
#   0.0127;                                 !- Thickness {m}



# WindowMaterial:Glazing,
#   CLEAR 6MM,                              !- Name
#   SpectralAverage,                        !- Optical Data Type
#   ,                                       !- Window Glass Spectral Data Set Name
#   0.00599999999999998,                    !- Thickness {m}
#   0.775,                                  !- Solar Transmittance at Normal Incidence
#   0.071,                                  !- Front Side Solar Reflectance at Normal Incidence
#   0.071,                                  !- Back Side Solar Reflectance at Normal Incidence
#   0.881,                                  !- Visible Transmittance at Normal Incidence
#   0.08,                                   !- Front Side Visible Reflectance at Normal Incidence
#   0.08,                                   !- Back Side Visible Reflectance at Normal Incidence
#   0,                                      !- Infrared Transmittance at Normal Incidence
#   0.84,                                   !- Front Side Infrared Hemispherical Emissivity
#   0.84,                                   !- Back Side Infrared Hemispherical Emissivity
#   0.899398119904063,                      !- Conductivity {W/m-K}
#   1,                                      !- Dirt Correction Factor for Solar and Visible Transmittance
#   No;                                     !- Solar Diffusing


# WindowMaterial:SimpleGlazingSystem,
#   U 0.36 SHGC 0.36 Simple Glazing,        !- Name
#   2.04408,                                !- U-Factor {W/m2-K}
#   0.36,                                   !- Solar Heat Gain Coefficient
#   0.6;                                    !- Visible Transmittance



# Construction,
#   Generic Context,                        !- Name
#   Material 2;                             !- Layer 1

# Construction,
#   Generic Double Pane,                    !- Name
#   Generic Low-e Glass,                    !- Layer 1
#   Generic Window Air Gap,                 !- Layer 2
#   Generic Clear Glass;                    !- Layer 3


if __name__ == '__main__':
    import os
    import compas_eplus

    for i in range(50): print('')

    file = 'teresa_example.idf'
    path = os.path.join(compas_eplus.DATA, 'idf_examples', file)

    data = get_idf_data(path)
    print(data['surfaces'])