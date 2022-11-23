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
    find_no_mass_materials(filepath, data)
    find_gas_materials(filepath, data)
    find_glazing_materials(filepath, data)
    find_constructions(filepath, data)
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
                               'surfaces': {}
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


        data['zones'][zone]['surfaces'][name] = {'name': name,
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
    

def find_no_mass_materials(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'material:nomass':
            i_lines.append(i)

    data['materials_no_mass'] = {}
    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        rough = lines[i + 2].split(',')[0].strip()
        thres  = float(lines[i + 3].split(',')[0])
        thabs = float(lines[i + 4].split(',')[0])
        slra = float(lines[i + 5].split(',')[0])
        visa = float(lines[i + 6].split(';')[0])

        data['materials_no_mass'][name] = {'name': name,
                                           'roughness': rough,
                                           'thermal_resistance': thres,
                                           'thermal_absoptance': thabs,
                                           'solar_absorptance': slra,
                                           'visible_absorptance': visa,
                                          }


def find_gas_materials(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'windowmaterial:gas':
            i_lines.append(i)

    data['materials_gas'] = {}
    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        gtype = lines[i + 2].split(',')[0].strip()
        thick  = float(lines[i + 3].split(';')[0])

        data['materials_gas'][name] = {'name': name,
                                       'gas_type': gtype,
                                       'thickness': thick,
                                          }


def find_glazing_materials(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'windowmaterial:glazing':
            i_lines.append(i)

    data['materials_glazing'] = {}
    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        odtype = lines[i + 2].split(',')[0].strip()
        thick  = float(lines[i + 4].split(',')[0])
        soltr = float(lines[i + 5].split(',')[0])
        fref = float(lines[i + 6].split(',')[0])
        bref = float(lines[i + 7].split(',')[0])
        vtrs = float(lines[i + 8].split(',')[0])
        fvtr = float(lines[i + 9].split(',')[0])
        bvtr = float(lines[i + 10].split(',')[0])
        inftr = float(lines[i + 11].split(',')[0])
        finfhem = float(lines[i + 12].split(',')[0])
        binfhem = float(lines[i + 13].split(',')[0])
        cond = float(lines[i + 14].split(',')[0])
        dirt = float(lines[i + 15].split(',')[0])
        soldif = lines[i + 16].split(';')[0].strip()

        data['materials_glazing'][name] = {'name': name,
                                           'optical_data_type': odtype,
                                           'thickness': thick,
                                           'solar_transmittance': soltr,
                                           'front_solar_reflectance': fref,
                                           'back_solar_reflectance': bref,
                                           'visible_transmittance': vtrs,
                                           'front_visible_transmittance': fvtr,
                                           'back_visible_transmittance': bvtr,
                                           'infrared_transmittance': inftr,
                                           'front_infrared_emissivity': finfhem, 
                                           'back_infrared_emissivity': binfhem, 
                                           'conductivity': cond,
                                           'dirt_correction': dirt,
                                           'solar_diffusing': soldif,
                                          }


def find_constructions(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'construction':
            i_lines.append(i)

    data['construction'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        layers = []
        for j in range(100):
            layer = lines[i + 1 + j]

            if ';' in layer: 
                layer = layer.split(';')[0].strip()
                layers.append(layer)
                break
            else:
                layer = layer.split(',')[0].strip()
                layers.append(layer)
        data['construction'][name] = {'name': name, 'layers': layers}



if __name__ == '__main__':
    import os
    import compas_eplus

    for i in range(50): print('')

    file = 'teresa_example.idf'
    path = os.path.join(compas_eplus.DATA, 'idf_examples', file)

    data = get_idf_data(path)
    print(data.keys())
    print(data['construction']['Generic Double Pane'])