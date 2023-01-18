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
    find_glazing_material_simple(filepath, data)
    find_constructions(filepath, data)
    find_schedule_compact(filepath, data)
    find_schedule_type_limits(filepath, data)
    find_schedule_day_interval(filepath, data)
    find_schedule_week_daily(filepath, data)
    find_schedule_year(filepath, data)
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
        name = lines[i + 1].split(',')[0].strip().lower()
        x = float(lines[i + 2].split(',')[0].strip())
        y = float(lines[i + 3].split(',')[0].strip())
        z = float(lines[i + 4].split(',')[0].strip())
        h = float(lines[i + 8].split(',')[0].strip())
        v = float(lines[i + 9].split(',')[0].strip())
        data['zones'][name] = {'name': name,
                               'origin': [x, y, z],
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
        zone  = lines[i + 4].split(',')[0].strip().lower()
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
        # bs_name = bs_name.replace('.', '')
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
                                 'nodes': pts  
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

        data['materials'][name] = {'__type__': 'Material',
                                   'name': name,
                                   'roughness': rough,
                                   'thickness': thick,
                                   'conductivity': cond,
                                   'density': dens,
                                   'specific_heat': sphe,
                                   'thermal_absorptance': thra,
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

    # data['materials_no_mass'] = {}
    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        rough = lines[i + 2].split(',')[0].strip()
        thres  = float(lines[i + 3].split(',')[0])
        thabs = float(lines[i + 4].split(',')[0])
        slra = float(lines[i + 5].split(',')[0])
        visa = float(lines[i + 6].split(';')[0])

        data['materials'][name] = {'__type__': 'MaterialNoMass',
                                   'name': name,
                                   'roughness': rough,
                                   'thermal_resistance': thres,
                                   'thermal_absorptance': thabs,
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

    # data['materials_gas'] = {}
    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        gtype = lines[i + 2].split(',')[0].strip()
        thick  = float(lines[i + 3].split(';')[0])

        data['materials'][name] = {'__type__': 'WindowMaterialGas',
                                   'name': name,
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

    # data['materials_glazing'] = {}
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

        data['materials'][name] = {'__type__': 'WindowMaterialGlazing',
                                   'name': name,
                                   'optical_data_type': odtype,
                                   'thickness': thick,
                                   'solar_transmittance': soltr,
                                   'front_solar_reflectance': fref,
                                   'back_solar_reflectance': bref,
                                   'visible_transmittance': vtrs,
                                   'front_visible_reflectance': fvtr,
                                   'back_visible_reflectance': bvtr,
                                   'infrared_transmittance': inftr,
                                   'front_infrared_hemispherical_emissivity': finfhem, 
                                   'back_infrared_hemispherical_emissivity': binfhem, 
                                   'conductivity': cond,
                                   'dirt_correction_factor': dirt,
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

    data['constructions'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        layers = {}
        for j in range(100):
            layer = lines[i + 2 + j]
            if ';' in layer: 
                layer = layer.split(';')[0].strip()
                layers[str(j)] = layer
                break
            else:
                layer = layer.split(',')[0].strip()
                layers[str(j)] = layer
        data['constructions'][name] = {'name': name, 'layers': layers}


def find_glazing_material_simple(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'windowmaterial:simpleglazingsystem':
            i_lines.append(i)

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        ufac  = float(lines[i + 2].split(',')[0])
        solh  = float(lines[i + 3].split(',')[0])
        vist  = lines[i + 4].split(';')[0]

        data['materials'][name] = {'__type__': 'WindowMaterialGlazingSimple',
                                   'name':name,
                                   'u_factor': ufac,
                                   'solar_heat_gain_coefficient': solh,
                                   'visible_transmittance': vist,
                                    }


def find_schedule_compact(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'schedule:compact':
            i_lines.append(i)
    
    data['schedules'] = {}
    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        stl = lines[i + 2].split(',')[0].strip()
        th = lines[i + 3].split(',')[0].split(':')[1].strip()
        fo = lines[i + 4].split(',')[0].split(':')[1].strip()
        un = lines[i + 5].split(',')[0].split(':')[1].strip()
        value = float(lines[i + 6].split(';')[0].strip())

        data['schedules'][name] = {'__type__': 'compact',
                                   'name': name,
                                   'schedule_type_limits': stl,
                                   'through': th,
                                   'for': fo,
                                   'until': un,
                                   'value': value,
                                  }


def find_schedule_type_limits(filepath, data):

    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'scheduletypelimits':
            i_lines.append(i)

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        low = lines[i + 2].split(',')[0].strip()
        if low:
            low = float(low)
        else:
            low = ''
        up = lines[i + 3].split(',')[0].strip()
        if up:
            up = float(up)
        else:
            up = ''
        if ';' in lines[i + 4]:
            nt = lines[i + 4].split(';')[0].strip()
            ut = None
        else:
            nt = lines[i + 4].split(',')[0].strip()
            ut = lines[i + 4].split(';')[0].strip()
        print(nt)

        data['schedules'][name] = {'__type__': 'schedule_type_limits',
                                   'name': name, 
                                   'lower_limit': low,
                                   'upper_limit': up,
                                   'numeric_type': nt,
                                   'unit_type': ut, 
                                    }


def find_schedule_day_interval(filepath, data):

    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'schedule:day:interval':
            i_lines.append(i)

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        stl = lines[i + 2].split(',')[0].strip()
        itt = lines[i + 3].split(',')[0].strip()

        time_values = {}
        count = 0
        for j in range(100):
            time = lines[i + 4 + count]
            time = time.split(',')[0].strip()
            value = lines[i + 5 + count]
            if ';' in value: 
                value = float(value.split(';')[0].strip())
                time_values[str(j)] = {'time': time, 'value': value}
                break
            else:
                value = float(value.split(',')[0].strip())
                time_values[str(j)] = {'time': time, 'value': value}
            count += 2

        data['schedules'][name] = {'__type__': 'day_interval',
                                   'name': name,
                                   'schedule_type_limits': stl,
                                   'interpolate_timestep': itt,
                                   'time_values': time_values,
                                  }


def find_schedule_week_daily(filepath, data):

    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'schedule:week:daily':
            i_lines.append(i)

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        sund = lines[i + 2].split(',')[0].strip()
        mond = lines[i + 3].split(',')[0].strip()
        tues = lines[i + 4].split(',')[0].strip()
        wedn = lines[i + 5].split(',')[0].strip()
        thur = lines[i + 6].split(',')[0].strip()
        frid = lines[i + 7].split(',')[0].strip()
        satu = lines[i + 8].split(',')[0].strip()
        holi = lines[i + 9].split(',')[0].strip()
        summ = lines[i + 10].split(',')[0].strip()
        wint = lines[i + 11].split(',')[0].strip()
        cus1 = lines[i + 12].split(',')[0].strip()
        cus2 = lines[i + 13].split(';')[0].strip()

        data['schedules'][name] = {'__type__': 'week_daily',
                                   'name': name,
                                   'sund':sund,
                                   'monday':mond,
                                   'tuesday':tues,
                                   'wednesdat':wedn,
                                   'thursday':thur,
                                   'friday':frid,
                                   'saturday':satu,
                                   'holiday':holi,
                                   'summer_design_day':summ,
                                   'winter_design_day':wint,
                                   'custom_day1':cus1,
                                   'custom_day2':cus2,
                                   }


def find_schedule_year(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'schedule:year':
            i_lines.append(i)

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        stln = lines[i + 2].split(',')[0].strip()
        swn1 = lines[i + 3].split(',')[0].strip()
        stm1 = lines[i + 4].split(',')[0].strip()
        std1 = lines[i + 5].split(',')[0].strip()
        enm1 = lines[i + 6].split(',')[0].strip()
        end1 = lines[i + 7].split(';')[0].strip()

        data['schedules'][name] = {'__type__': 'year',
                                   'name': name,
                                   'schedule_type_limits': stln,
                                   'schedule_week_name1': swn1,
                                   'start_month_1': stm1,
                                   'start_day1': std1,
                                   'end_month1': enm1,
                                   'end_dat1': end1,
                                  }



if __name__ == '__main__':
    import os
    import compas_eplus

    for i in range(50): print('')

    file = 'teresa_example.idf'
    path = os.path.join(compas_eplus.DATA, 'idf_examples', file)

    data = get_idf_data(path)
    print(data.keys())

    for k in data['schedules']:
        print(k)
        print(data['schedules'][k]['__type__'])
        print('')