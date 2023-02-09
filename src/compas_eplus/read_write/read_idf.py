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
    
    find_lights(filepath, data)
    find_people(filepath, data)
    find_electric_equipment(filepath, data)
    find_zone_control_thermostat(filepath, data)
    find_thermostat_setpoint(filepath, data)
    find_ideal_air_loads(filepath, data)
    find_infiltration(filepath, data)
    find_equipment_list(filepath, data)
    find_equipment_connections(filepath, data)
    find_zone_lists(filepath, data)
    find_node_lists(filepath, data)

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
            ut = ''
        else:
            nt = lines[i + 4].split(',')[0].strip()
            ut = lines[i + 5].split(';')[0].strip()

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
                                   'sunday':sund,
                                   'monday':mond,
                                   'tuesday':tues,
                                   'wednesday':wedn,
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


def find_lights(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'lights':
            i_lines.append(i)
    
    data['lights'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        znam = lines[i + 2].split(',')[0].strip()
        snam = lines[i + 3].split(',')[0].strip()
        calm = lines[i + 4].split(',')[0].strip()
        ligl = lines[i + 5].split(',')[0].strip()
        wzfa = lines[i + 6].split(',')[0].strip()
        wppe = lines[i + 7].split(',')[0].strip()
        rafr = lines[i + 8].split(',')[0].strip()
        frad = lines[i + 9].split(',')[0].strip()
        fvis = lines[i + 10].split(',')[0].strip()
        frep = lines[i + 11].split(',')[0].strip()
        euct = lines[i + 12].split(';')[0].strip()

        data['lights'][name] = {'name':name,
                                'zone_name': znam,
                                'schedule_name': snam,
                                'design_level_calculation_method': calm,
                                'lighting_level': ligl,
                                'watts_per_zone_floor_area': wzfa,
                                'watts_per_person': wppe,
                                'return_air_fraction': rafr,
                                'fraction_radiant': frad,
                                'fraction_visible': fvis,
                                'fraction_replaceable': frep,
                                'end_use_subcategory': euct,
                                }


def find_people(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'people':
            i_lines.append(i)
    
    data['people'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        znam = lines[i + 2].split(',')[0].strip()
        snam = lines[i + 3].split(',')[0].strip()
        calm = lines[i + 4].split(',')[0].strip()
        nump = lines[i + 5].split(',')[0].strip()
        ppfa = lines[i + 6].split(',')[0].strip()
        fapp = lines[i + 7].split(',')[0].strip()
        frad = lines[i + 8].split(',')[0].strip()
        shfr = lines[i + 9].split(',')[0].strip()
        alsn = lines[i + 10].split(';')[0].strip()

        data['people'][name] = {'name':name,
                                'zone_name': znam,
                                'schedule_name': snam,
                                'calculation_method': calm,
                                'number_of_people': nump,
                                'people_per_floor_area': ppfa,
                                'floor_area_per_person': fapp,
                                'fraction_radiant': frad,
                                'sensible_heat_fraction':shfr,
                                'activity_level_schedule_name': alsn,
                                }


def find_electric_equipment(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'electricequipment':
            i_lines.append(i)
    
    data['electric_equipment'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        znam = lines[i + 2].split(',')[0].strip()
        snam = lines[i + 3].split(',')[0].strip()
        calm = lines[i + 4].split(',')[0].strip()
        desl = lines[i + 5].split(',')[0].strip()
        wzfa = lines[i + 6].split(',')[0].strip()
        wppe = lines[i + 7].split(',')[0].strip()
        flat = lines[i + 8].split(',')[0].strip()
        frad = lines[i + 9].split(',')[0].strip()
        flst = lines[i + 10].split(',')[0].strip()
        eusc = lines[i + 11].split(';')[0].strip()

        data['electric_equipment'][name] = {'name': name,
                                            'zone_name': znam,
                                            'schedule_name': snam,
                                            'calculation_method': calm,
                                            'design_level': desl,
                                            'watts_per_zone_floor_area': wzfa,
                                            'watts_per_person': wppe,
                                            'fraction_latent': flat,
                                            'fraction_radiant': frad,
                                            'fraction_lost': flst,
                                            'end_use_subcategory': eusc,
                                            }


def find_zone_control_thermostat(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'zonecontrol:thermostat':
            i_lines.append(i)
    
    data['zone_control_thermostat'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        znam = lines[i + 2].split(',')[0].strip()
        snam = lines[i + 3].split(',')[0].strip()
        ct1t = lines[i + 4].split(',')[0].strip()
        ct1n = lines[i + 5].split(',')[0].strip()
        ct2t = lines[i + 6].split(',')[0].strip()
        ct2n = lines[i + 7].split(',')[0].strip()
        ct3t = lines[i + 8].split(',')[0].strip()
        ct3n = lines[i + 9].split(',')[0].strip()
        ct4t = lines[i + 10].split(',')[0].strip()
        ct4n = lines[i + 11].split(',')[0].strip()
        tmpd = lines[i + 12].split(';')[0].strip()

        data['zone_control_thermostat'][name] = {'name': name,
                                                 'zone_name': znam,
                                                 'schedule_name': snam,
                                                 'control1_object_type': ct1t,
                                                 'control1_object_name': ct1n,
                                                 'control2_object_type': ct2t,
                                                 'control2_object_name': ct2n,
                                                 'control3_object_type': ct3t,
                                                 'control3_object_name': ct3n,
                                                 'control4_object_type': ct4t,
                                                 'control4_object_name': ct4n,
                                                 'temperature_difference': tmpd,
                                                } 


def find_thermostat_setpoint(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'thermostatsetpoint:dualsetpoint':
            i_lines.append(i)
    
    data['setpoint'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        htsp = lines[i + 2].split(',')[0].strip()
        clsp = lines[i + 3].split(';')[0].strip()

        data['setpoint'][name] = {'name': name,
                                  'heating_setpoint': htsp,
                                  'cooling_setpoint': clsp,
                                   }


def find_ideal_air_loads(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'zonehvac:idealloadsairsystem':
            i_lines.append(i)
    
    data['ideal_air_load'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        avsn = lines[i + 2].split(',')[0].strip()
        zsan = lines[i + 3].split(',')[0].strip()
        zean = lines[i + 4].split(',')[0].strip()
        sian = lines[i + 5].split(',')[0].strip()
        mhat = lines[i + 6].split(',')[0].strip()
        mcat = lines[i + 7].split(',')[0].strip()
        mhhr = lines[i + 8].split(',')[0].strip()
        mchr = lines[i + 9].split(',')[0].strip()
        hlim = lines[i + 10].split(',')[0].strip()
        mhaf = lines[i + 11].split(',')[0].strip()
        mshc = lines[i + 12].split(',')[0].strip()
        clim = lines[i + 13].split(',')[0].strip()
        mcaf = lines[i + 14].split(',')[0].strip()
        mtcc = lines[i + 15].split(',')[0].strip()
        hasn = lines[i + 16].split(',')[0].strip()
        casn = lines[i + 17].split(',')[0].strip()
        dhct = lines[i + 18].split(',')[0].strip()
        cshr = lines[i + 19].split(',')[0].strip()
        hmct = lines[i + 20].split(',')[0].strip()
        dsoa = lines[i + 21].split(',')[0].strip()
        oain = lines[i + 22].split(',')[0].strip()
        dcvt = lines[i + 23].split(',')[0].strip()
        oaet = lines[i + 24].split(',')[0].strip()
        hrty = lines[i + 25].split(',')[0].strip()
        shre = lines[i + 26].split(',')[0].strip()
        lhre = lines[i + 27].split(';')[0].strip()


        data['ideal_air_load'][name] = {'name': name,
                                        'availability_schedule_name': avsn,
                                        'zone_supply_air_node_name': zsan,
                                        'zone_exhaust_air_node_name': zean,
                                        'system_inlet_air_node_name': sian,
                                        'max_heating_supply_temperature': mhat,
                                        'min_cooling_supply_temperature': mcat,
                                        'max_heating_supply_humidity_ratio': mhhr,
                                        'min_cooling_supply_humidity_ratio': mchr,
                                        'heating_limit': hlim,
                                        'max_heating_air_flow_rate': mhaf,
                                        'max_sensible_heating_capacity': mshc,
                                        'cooling_limit': clim,
                                        'maximum_cooling_air_flow_rate': mcaf,
                                        'maximum_total_cooling_capacity': mtcc,
                                        'heating_availability_schedule_name': hasn,
                                        'cooling_availability_schedule_name': casn,
                                        'dehimidification_control_type': dhct,
                                        'cooling_sensible_heat_ratio': cshr,
                                        'humidification_control_type': hmct,
                                        'desing_specification_outdoor_air_name': dsoa,
                                        'outdoor_inlet_node_name': oain,
                                        'demand_controlled_ventilation_type': dcvt,
                                        'outdoor_air_economizer_type': oaet,
                                        'heat_recovery_type': hrty,
                                        'sensible_heat_recovery_effectiveness': shre,
                                        'latent_heat_revovery_effectiveness': lhre,
                                        } 


def find_infiltration(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'zoneinfiltration:designflowrate':
            i_lines.append(i)
    
    data['infiltration'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        znam = lines[i + 2].split(',')[0].strip()
        snam = lines[i + 3].split(',')[0].strip()
        dfcm = lines[i + 4].split(',')[0].strip()
        dfrt = lines[i + 5].split(',')[0].strip()
        fpza = lines[i + 6].split(',')[0].strip()
        fpes = lines[i + 7].split(',')[0].strip()
        acph = lines[i + 8].split(',')[0].strip()
        ctco = lines[i + 9].split(',')[0].strip()
        ttco = lines[i + 10].split(',')[0].strip()
        vtco = lines[i + 11].split(',')[0].strip()
        vstc = lines[i + 12].split(';')[0].strip()


        data['infiltration'][name] = {'name': name,
                                      'zone_name': znam,
                                      'schedule_name': snam,
                                      'design_flow_rate_calculation_method': dfcm,
                                      'design_flow_rate': dfrt,
                                      'flow_per_zone_floor_area': fpza,
                                      'flow_per_exterior_area': fpes, 
                                      'air_changes_per_hour': acph,
                                      'constant_term_coefficient': ctco,
                                      'temperature_term_coefficient': ttco,
                                      'velocity_term_coefficient': vtco,
                                      'velocity_squared_term_coefficient': vstc,
                                       }


def find_equipment_list(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'zonehvac:equipmentlist':
            i_lines.append(i)
    
    data['equipment_list'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        lsch = lines[i + 2].split(',')[0].strip()
        zeo1 = lines[i + 3].split(',')[0].strip()
        zen1 = lines[i + 4].split(',')[0].strip()
        zec1 = lines[i + 5].split(',')[0].strip()
        zeh1 = lines[i + 6].split(',')[0].strip()
        zsc1 = lines[i + 7].split(',')[0].strip()
        zsh1 = lines[i + 8].split(';')[0].strip()

        data['equipment_list'][name] = {'name': name,
                                        'load_distribution_scheme': lsch,
                                        'zone_equipment_object_type1': zeo1, 
                                        'zone_equipment_name1': zen1,
                                        'zone_equipment_cooling_sequence': zec1, 
                                        'zone_equipment_heating_sequence': zeh1, 
                                        'zone_equipment_sequenctial_cooling_fraction_schedule': zsc1,
                                        'zone_equipment_sequential_heating_fraction_schedule': zsh1,
                                        }


def find_equipment_connections(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'zonehvac:equipmentconnections':
            i_lines.append(i)
    
    data['equipment_connection'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        zcel = lines[i + 2].split(',')[0].strip()
        zain = lines[i + 3].split(',')[0].strip()
        zaen = lines[i + 4].split(',')[0].strip()
        zann = lines[i + 5].split(';')[0].strip()

        data['equipment_connection'][name] = {'name': name,
                                              'zone_conditioning_equipment_list': zcel,
                                              'zone_air_inlet_node': zain,
                                              'zone_air_exhaust_node': zaen,
                                              'zone_air_node': zann,
                                               }


def find_zone_lists(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'zonelist':
            i_lines.append(i)
    
    data['zone_lists'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        zones = {}
        for j in range(100):
            zone = lines[i + 2 + j]
            if ';' in zone: 
                zone = zone.split(';')[0].strip()
                zones[str(j)] = zone
                break
            else:
                zone = zone.split(',')[0].strip()
                zones[str(j)] = zone
        data['zone_lists'][name] = {'name': name,
                                    'zones': zones,}

def find_node_lists(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'nodelist':
            i_lines.append(i)
    
    data['node_lists'] = {}

    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        nodes = {}
        for j in range(100):
            node = lines[i + 2 + j]
            if ';' in node: 
                node = node.split(';')[0].strip()
                nodes[str(j)] = node
                break
            else:
                node = node.split(',')[0].strip()
                nodes[str(j)] = node
        data['node_lists'][name] = {'name': name,
                                    'nodes': nodes,}


if __name__ == '__main__':
    import os
    import compas_eplus

    for i in range(50): print('')

    file = 'teresa_example_apt.idf'
    path = os.path.join(compas_eplus.DATA, 'idf_examples', file)

    data = get_idf_data(path)
    # print(data.keys())

    object = 'node_lists'

    for k in data[object]:
        print(k)
        for j in data[object][k]:
            print(j)
        print(data[object][k]['nodes'])
        print('')