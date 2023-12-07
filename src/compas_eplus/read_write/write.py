from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


# TODO: the write_construction should eventually use saved layer names, not make up new ones
# TODO: write functions should work in ironpython, use old format statement


def write_idf_from_building(building):
    """
    Writes the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'w')
    fh.close()
    write_pre(building)
    write_building(building)
    write_global_vars(building)
    write_run_period(building)
    write_zones(building)
    write_windows(building)
    write_layers(building)
    write_constructions(building)
    write_shadings(building)
    write_spaces(building)
    write_space_lists(building)

    write_simulation_control(building)
    write_schedules(building)
    # write_schedule_type_limits(building)
    write_internal_gains(building)
    write_infiltration_rates(building)
    write_thermostats(building)
    write_hvac(building)
    write_node_lists(building)
    write_outdoor_airs(building)
    write_daylight(building)

    write_output_items(building)


def write_pre(building):
    """
    Writes the preamble to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    fh.write('\n') 
    fh.write('Version,\n')
    fh.write('  {};\t\t\t\t\t!- Version Identifier\n'.format(building.ep_version))
    fh.write('\n')
    fh.write('Timestep,\n')
    fh.write('  {};\t\t\t\t\t!- Number of Timesteps per Hour\n'.format(building.num_timesteps))  
    fh.write('\n')
    fh.close()


def write_building(building):
    """
    Writes the building basic data to the .idf file from the building datastructure.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    fh.write('Building,\n')
    fh.write('  {},\t\t\t\t\t!- Name\n'.format(building.name))
    fh.write('  0,\t\t\t\t\t !- North Axis (deg)\n')
    fh.write('  {},\t\t\t\t\t!- Terrain\n'.format(building.terrain))
    fh.write('  ,\t\t\t\t\t !- Loads Convergence Tolerance Value (W)\n')
    fh.write('  ,\t\t\t\t\t !- Temperature Convergence Tolerance Value (deltaC)\n')
    fh.write('  {},\t\t\t\t\t!- Solar Distribution\n'.format(building.solar_distribution))
    fh.write('  ,\t\t\t\t\t !- Maximum Number of Warmup Days\n')
    fh.write('  ;\t\t\t\t\t !- Minimum Number of Warmup Days\n')
    fh.write('\n')
    fh.close()


def write_global_vars(building):
    """
    Writes the global variables to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    fh.write('\n') 
    fh.write('GlobalGeometryRules,\n')
    fh.write('  UpperLeftCorner,\t\t\t\t\t!- Starting Vertex Position\n')
    fh.write('  CounterClockWise,\t\t\t\t\t!- Vertex Entry Direction\n')
    fh.write('  World;\t\t\t\t\t!- Coordinate System\n')
    fh.write('\n')           
    fh.close()


def write_run_period(building):
    """
    Writes the run period  to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    fh.write('  RunPeriod,\n')
    fh.write('    Run Period 1,            !- Name\n')
    fh.write('    1,                       !- Begin Month\n')
    fh.write('    1,                       !- Begin Day of Month\n')
    fh.write('    ,                        !- Begin Year\n')
    fh.write('    12,                      !- End Month\n')
    fh.write('    31,                      !- End Day of Month\n')
    fh.write('    ,                        !- End Year\n')
    fh.write('    Tuesday,                 !- Day of Week for Start Day\n')
    fh.write('    Yes,                     !- Use Weather File Holidays and Special Days\n')
    fh.write('    Yes,                     !- Use Weather File Daylight Saving Period\n')
    fh.write('    No,                      !- Apply Weekend Holiday Rule\n')
    fh.write('    Yes,                     !- Use Weather File Rain Indicators\n')
    fh.write('    Yes;                     !- Use Weather File Snow Indicators\n')
    fh.write('\n')
    fh.close()


def write_zones(building):
    """
    Writes all zones to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    
    Returns
    -------
    None
    """
    for zkey in building.zones:
        zone = building.zones[zkey]
        write_zone(building, zone)
        write_zone_surfaces(building, zone)
    write_all_zone_list(building)
    write_zone_lists(building)


def write_all_zone_list(building):
    fh = open(building.idf_filepath, 'a')
    fh.write('ZoneList,\n')
    fh.write('  all_zones_list, !- Name\n')
    for i, zkey in enumerate(building.zones):
        zone = building.zones[zkey]
        if i == len(building.zones) - 1:
            divider = ';'
        else:
            divider = ','
        fh.write('  {}{} !- Zone {} Name\n'.format(zone.name, divider, i))
    fh.write('\n')
    fh.write('\n')
    fh.close()


def write_zone_lists(building):
    fh = open(building.idf_filepath, 'a')

    for zlk in building.zone_lists:
        zl = building.zone_lists[zlk]
        zones = building.zone_lists[zlk].zones
        fh.write('ZoneList,\n')
        fh.write('  {},     !- Name\n'.format(zl.name))
        for i, zk in enumerate(zones):
            if i == len(zones) - 1:
                sep = ';'
            else:
                sep = ','
            fh.write('  {}{}        !- Zone Name {}\n'.format(zones[zk], sep, i + 1))
        fh.write('\n')
        fh.close()


def write_zone(building, zone):
    """
    Writes a single zone to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    zone: object
        The zone object to be written
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    fh.write('Zone,\n')
    fh.write('  {},         !- Name\n'.format(zone.name))
    fh.write('  0,          !- Direction of Relative North (deg)\n')
    fh.write('  {},          !- X Origin (m)\n'.format(zone.origin[0]))
    fh.write('  {},          !- Y Origin (m)\n'.format(zone.origin[1]))
    fh.write('  {},          !- Z Origin (m)\n'.format(zone.origin[2]))
    fh.write('  1,          !- Type\n')
    fh.write('  1,          !- Multiplier\n')
    fh.write('  {},           !- Ceiling Height (m)\n'.format(zone.height))
    fh.write('  {},           !- Volume (m3)\n'.format(zone.volume))
    fh.write('  ,           !- Floor Area (m2)\n')
    fh.write('  ,           !- Zone Inside Convection Algorithm\n')
    fh.write('  ,           !- Zone Outside Convection Algorithm\n')
    fh.write('  Yes;        !- Part of Total Floor Area\n')
    fh.write('\n')
    fh.close()


def write_layers(building):
    """
    Writes all layers to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    
    Returns
    -------
    None
    """
    
    for lk in building.layers:
        lay_name = building.layers[lk]['layer_name']
        mat_name = building.layers[lk]['material_name']
        mk = building.material_key_dict[mat_name]
        mat = building.materials[mk]
        thick = building.layers[lk]['thickness']
        if mat.__type__ == 'Material':
            write_material(building, mat, thick, lay_name)
        elif mat.__type__ == 'MaterialNoMass':
            write_materials_nomass(building, mat)
        elif mat.__type__ == 'WindowMaterialGlazing':
            write_material_glazing(building, mat, thick, lay_name)
        elif mat.__type__ == 'WindowMaterialGas':
            write_material_gas(building, mat, thick, lay_name)
        elif mat.__type__ == 'WindowMaterialGlazingSimple':
            write_materials_glazing_simple(building, mat)


def write_materials_glazing_simple(building, mat):
    fh = open(building.idf_filepath, 'a')
    fh.write('\n')
    fh.write('WindowMaterial:SimpleGlazingSystem,\n')
    fh.write('  {},             !- Name\n'.format(mat.name))
    fh.write('  {},             !- U-Factor (W/m2-K)\n'.format(mat.u_factor))
    fh.write('  {},             !- Solar Heat Gain Coefficient\n'.format(mat.solar_heat_gain_coefficient))
    fh.write('  {};             !- Visible Transmittance\n'.format(mat.visible_transmittance))
    fh.write('\n')
    fh.close()


def write_material_glazing(building, mat, thickness, layer_name):
    """
    Writes a glazing material to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    mat: object
        The material object to be written
    thickness: float
        The thickness of the material layer
    layer_name: str
        The name of the material layer, including the thickness modifier
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    fh.write('\n')
    fh.write('WindowMaterial:Glazing,\n')
    fh.write('  {},         !- Name\n'.format(layer_name))
    fh.write('  {},         !- Optical Data Type\n'.format(mat.optical_data_type))
    fh.write('  {},         !- Window Glass Spectral Data Set Name\n'.format(mat.win_glass_spectral_data_name))
    fh.write('  {},         !- Thickness (m)\n'.format(thickness))
    fh.write('  {},         !- Solar Transmittance at Normal Incidence\n'.format(mat.solar_transmittance))
    fh.write('  {},         !- Front Side Solar Reflectance at Normal Incidence\n'.format(mat.front_solar_reflectance))
    fh.write('  {},         !- Back Side Solar Reflectance at Normal Incidence\n'.format(mat.back_solar_reflectance))
    fh.write('  {},         !- Visible Transmittance at Normal Incidence\n'.format(mat.visible_transmittance))
    fh.write('  {},         !- Front Side Visible Reflectance at Normal Incidence\n'.format(mat.front_visible_reflectance))
    fh.write('  {},         !- Back Side Visible Reflectance at Normal Incidence\n'.format(mat.back_visible_reflectance))
    fh.write('  {},         !- Infrared Transmittance at Normal Incidence\n'.format(mat.infrared_transmittance))
    fh.write('  {},         !- Front Side Infrared Hemispherical Emissivity\n'.format(mat.front_infrared_hemispherical_emissivity))
    fh.write('  {},         !- Back Side Infrared Hemispherical Emissivity\n'.format(mat.back_infrared_hemispherical_emissivity))
    fh.write('  {},         !- Conductivity (W/m-K)\n'.format(mat.conductivity))
    fh.write('  {},         !- Dirt Correction Factor for Solar and Visible Transmittance\n'.format(mat.dirt_correction_factor))
    fh.write('  {};         !- Solar Diffusing\n'.format(mat.solar_diffusing))
    fh.write('\n')
    fh.close()


def write_material_gas(building, mat, thickness, layer_name):
    """
    Writes a gas material to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    mat: object
        The material object to be written
    thickness: float
        The thickness of the material layer
    layer_name: str
        The name of the material layer, including the thickness modifier
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    fh.write('\n')
    fh.write('WindowMaterial:Gas,\n')
    fh.write('  {},         !- Name\n'.format(layer_name))
    fh.write('  {},         !- Gas Type\n'.format(mat.gas_type ))
    fh.write('  {};         !- Thickness (m)\n'.format(thickness))
    fh.write('\n')
    fh.close()


def write_materials_nomass(building, mat):
    """
    Writes a no mass material to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    mat: object
        The material object to be written
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    fh.write('\n')
    fh.write('Material:NoMass,\n')
    fh.write('  {},     !- Name\n'.format(mat.name))
    fh.write('  {},     !- Roughness\n'.format(mat.roughness))
    fh.write('  {},     !- Thermal Resistance (m2-K/W)\n'.format(mat.thermal_resistance))
    fh.write('  {},     !- Thermal Absorptance\n'.format(mat.thermal_absorptance))
    fh.write('  {},     !- Solar Absorptance\n'.format(mat.solar_absorptance))
    fh.write('  {};     !- Visible Absorptance\n'.format(mat.visible_absorptance))
    fh.write('\n')
    fh.write('\n')
    fh.close()


def write_material(building, mat, thickness, layer_name):
    """
    Writes a material to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    mat: object
        The material object to be written
    thickness: float
        The thickness of the material layer
    layer_name: str
        The name of the material layer, including the thickness modifier
    
    Returns
    -------
    None
    """
    if thickness:
        fh = open(building.idf_filepath, 'a')
        fh.write('\n')
        fh.write('Material,\n')
        fh.write('  {},     !- Name\n'.format(layer_name))
        fh.write('  {},     !- Roughness\n'.format(mat.roughness))
        fh.write('  {},     !- Thickness (m)\n'.format(thickness))
        fh.write('  {},     !- Conductivity (W/m-K)\n'.format(mat.conductivity))
        fh.write('  {},     !- Density (kg/m3)\n'.format(mat.density))
        fh.write('  {},     !- Specific Heat (J/kg-K)\n'.format(mat.specific_heat))    
        fh.write('  {},     !- Thermal Absorptance\n'.format(mat.thermal_absorptance))
        fh.write('  {},     !- Solar Absorptance\n'.format(mat.solar_absorptance))
        fh.write('  {};     !- Visible Absorptance\n'.format(mat.visible_absorptance))
        fh.write('\n')
        fh.write('\n')
        fh.close()


def write_zone_surfaces(building, zone):
    """
    Writes all zone surfaces to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    zone: object
        The zone object to be written
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    for fk in zone.surfaces.faces():
        write_building_surface(building, zone, fk)
    fh.close()


def write_building_surface(building, zone, fk):
    """
    Writes a building surface to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    zone: object
        The zone object to be written
    fk: int
        The face key of the surface to the written
    
    Returns
    -------
    None
    """
    st = zone.surfaces.face_attribute(fk, 'surface_type')
    ct = zone.surfaces.face_attribute(fk, 'construction')
    ob = zone.surfaces.face_attribute(fk, 'outside_boundary_condition')

    if ob =='Adiabatic':
        se = 'NoSun'
        we = 'NoWind'
    else:
        se = 'SunExposed'
        we = 'WindExposed'

    num_vert = len(zone.surfaces.face_vertices(fk))

    sname = zone.surfaces.face_attribute(fk, 'name')

    fh = open(building.idf_filepath, 'a')
    fh.write('\n')
    fh.write('BuildingSurface:Detailed,\n')
    fh.write('  {},                    !- Name\n'.format(sname))
    # fh.write('  {},                    !- Name\n'.format(zone.name))
    fh.write('  {},                       !- Surface Type\n'.format(st))
    fh.write('  {},                       !- Construction Name\n'.format(ct))
    fh.write('  {},                       !- Zone Name\n'.format(zone.name))
    fh.write('  ,                         !- Space Name\n')
    fh.write('  {},                       !- Outside Boundary Condition\n'.format(ob))
    fh.write('  ,                         !- Outside Boundary Condition Object\n')
    fh.write('  {},                       !- Sun Exposure\n'.format(se))
    fh.write('  {},                       !- Wind Exposure\n'.format(we))
    fh.write('  0.0,                      !- View Factor to Ground\n')
    fh.write('  {},                       !- Number of Vertices\n'.format(num_vert))

    for i, vk in enumerate(zone.surfaces.face_vertices(fk)):
        x, y, z = zone.surfaces.vertex_coordinates(vk)
        if i == num_vert - 1:
            sep = ';'
        else:
            sep = ','
        fh.write('  {:.3f}, {:.3f}, {:.3f}{}\t\t\t\t\t!- X,Y,Z Vertex {}\n'.format(x, y, z, sep, i))
    fh.write('\n')
    fh.close()


def write_windows(building):
    """
    Writes all windows  to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    for wk in building.windows:
        win = building.windows[wk]
        con = win.construction
        bsn = win.building_surface

        fh.write('\n')
        fh.write('FenestrationSurface:Detailed,\n')
        fh.write('  {},                       !- Name\n'.format(win.name))
        fh.write('  Window,                   !- Surface Type\n')
        fh.write('  {},                       !- Construction Name\n'.format(con))
        fh.write('  {},                       !- Building Surface Name\n'.format(bsn))
        fh.write('  ,                         !- Outside Boundary Condition Object\n')
        fh.write('  ,                         !- View Factor to Ground\n')
        fh.write('  ,                         !- Frame and Divider Name\n')
        fh.write('  ,                         !- Multiplier\n')
        fh.write('  {},                         !- Number of Vertices\n'.format(len(win.nodes)))
        for i, nodes in enumerate(win.nodes):
            x, y, z = nodes
            if i == len(win.nodes) - 1:
                sep = ';'
            else:
                sep = ','
            fh.write('  {:.3f}, {:.3f}, {:.3f}{}\t\t\t\t\t!- X,Y,Z Vertex {} (m)\n'.format(x, y, z, sep, i))
        fh.write('\n')
    fh.write('\n')
    fh.close()


def write_constructions(building):
    """
    Writes all constructions to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    fh.write('\n')
    for ck in building.constructions:
        name = building.constructions[ck].name
        layers = [building.constructions[ck].layers[lk]['name'] for lk in building.constructions[ck].layers]
        types = [building.materials[building.material_key_dict[lname]].__type__ for lname in layers]
        thicks = [building.constructions[ck].layers[lk]['thickness'] for lk in building.constructions[ck].layers] 
        fh.write('Construction,\n')
        fh.write('  {},\t\t\t\t\t!- Name\n'.format(name))
        for i, layer in enumerate(layers):
            if i == len(layers) - 1:
                sep = ';'
            else:
                sep = ','
            if thicks[i] > 0:
                lname = '{} {}mm'.format(layer, round(thicks[i]*1000, 1))
            elif thicks[i] <= 0 and types[i] == 'Material':
                    continue
            else:
                lname = '{}'.format(layer)
            fh.write('  {}{}\t\t\t\t\t!- Layer {}\n'.format(lname, sep, i))
        fh.write('\n')
    fh.write('\n')
    fh.close()


def write_shadings(building):
    """
    Writes all shading devices to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    
    Returns
    -------
    None
    """
    for sk in building.shadings:
        write_shading(building, building.shadings[sk])


def write_shading(building, shading):
    """
    Writes a single shading device to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    shading: object
        The shading object to be written
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    fh.write('\n')
    sname = shading.name
    mesh = shading.mesh
    for fk in mesh.faces():
        fh.write('Shading:Building:Detailed,\n')
        fh.write('  Shading {}-{}, !- Detached Shading\n'.format(sname, fk))
        fh.write('  , !- Shadowing Transmittance & Schedule\n')
        vertices = mesh.face_vertices(fk)
        fh.write('  {}, !-Number of verrices\n'.format(len(vertices)))
        for i, vk in enumerate(vertices):
            if i == len(vertices) - 1:
                sep = ';'
            else:
                sep = ','
            x, y, z = mesh.vertex_coordinates(vk)
            fh.write('  {}, {}, {}{} ! Vertex {}\n'.format(x, y, z, sep, i))
        fh.write('\n')
    fh.write('\n')
    fh.close()


def write_simulation_control(building):

    fh = open(building.idf_filepath, 'a')
    fh.write('SimulationControl,\n')
    fh.write('  No,       !- Do Zone Sizing Calculation\n')
    fh.write('  No,       !- Do System Sizing Calculation\n')
    fh.write('  No,       !- Do Plant Sizing Calculation\n')
    fh.write('  No,       !- Run Simulation for Sizing Periods\n')
    fh.write('  Yes,      !- Run Simulation for Weather File Run Periods\n')
    fh.write('  No,       !- Do HVAC Sizing Simulation for Sizing Periods\n')
    fh.write('  1;        !- Maximum Number of HVAC Sizing Simulation Passes\n')
    fh.write('  \n')
    fh.write('  \n')
    fh.close()


def write_schedule(building, schedule):
    if schedule.alldays:
        add = schedule.alldays
        addks = sorted(add.keys())

        fh = open(building.idf_filepath, 'a')
        fh.write('Schedule:Compact,\n')
        fh.write('  {},                !- Name\n'.format(schedule.name))
        fh.write('  {},                !- Schedule Type Limits Name\n'.format(schedule.type_limits))
        fh.write('  Through: 12/31,          !- Field 1\n')
        fh.write('  For: AllDays,            !- Field 2\n')
        for h in addks:
            fh.write('  Until: {}:00,{},         !- Field n \n'.format(h, add[h]))
        fh.write('  ;\n')
        fh.write('  \n')
        fh.write('  \n')
        fh.close()

    else:
        wd = schedule.weekdays
        wdks = sorted(wd.keys())

        wed = schedule.weekends
        wedks = sorted(wed.keys())

        if schedule.summer_design_day:
            sddd = schedule.summer_design_day
            sdddls = sorted(sddd.keys())


        fh = open(building.idf_filepath, 'a')
        fh.write('Schedule:Compact,\n')
        fh.write('  {},                !- Name\n'.format(schedule.name))
        fh.write('  {},                !- Schedule Type Limits Name\n'.format(schedule.type_limits))
        fh.write('  Through: 12/31,    !- Field 1\n')
        fh.write('  For: WeekDays SummerDesignDay CustomDay1 CustomDay2, !- Field 2\n')
        for h in wdks:
            fh.write('  Until: {}:00,{},         !- Field n \n'.format(h, wd[h]))

        fh.write('  For: Weekends WinterDesignDay Holiday, !- Field n \n')
        for h in wedks:
            fh.write('  Until: {}:00,{},         !- Field n \n'.format(h, wed[h]))
        fh.write('  ;\n')
        fh.write('  \n')
        fh.write('  \n')
        fh.close()


def write_schedules(building):
    # building.find_set_schedules()
    # for sk in building.set_schedules:
    for sk in building.schedules:
        schedule = building.schedules[sk]
        stype = schedule.type
        if stype == 'compact':
            write_schedule_compact(building, schedule)
        elif stype == 'day_interval':
            write_schedule_day_interval(building, schedule)
        elif stype == 'week_daily':
            write_schedule_week_daily(building, schedule)
        elif stype == 'year':
            write_schedule_year(building, schedule)
        elif stype == 'schedule_type_limits':
            write_schedule_type_limits(building, schedule)


def write_schedule_compact(building, schedule):
    fh = open(building.idf_filepath, 'a')
    fh.write('Schedule:Compact,\n')
    fh.write('  {},  !- Name\n'.format(schedule.name))
    fh.write('  {}, !- Schedule Type Limits Name\n'.format(schedule.type_limits))
    fh.write('  Through: {}, !- Field 1\n'.format(schedule.through))
    fh.write('  For: {},     !- Field 2\n'.format(schedule.for_))
    fh.write('  Until: {}:00,   !- Field 3\n'.format(schedule.until))
    fh.write('  {};          !- Field 4\n'.format(schedule.value))
    fh.write('\n')
    fh.close()


def write_schedule_day_interval(building, schedule):

    time_values = schedule.time_values
    sep = ','
    fh = open(building.idf_filepath, 'a')
    fh.write('Schedule:Day:Interval,\n')
    fh.write('  {},   !- Name\n'.format(schedule.name))
    fh.write('  {},   !- Schedule Type Limits Name\n'.format(schedule.type_limits))
    fh.write('  {},   !- Interpolate to Timestep\n'.format(schedule.interpolate_timestep))
    for i, tk in enumerate(time_values):
        fh.write('  {},    !- Time {} [hh:mm]\n'.format(time_values[tk]['time'], i + 1))
        if i == len(time_values) - 1:
            sep = ';'
        fh.write('  {}{}    !- Value Until Time {}\n'.format(time_values[tk]['value'], sep, i + 1))
    fh.write('\n')
    fh.close()


def write_schedule_week_daily(building, schedule):
    fh = open(building.idf_filepath, 'a')
    fh.write('Schedule:Week:Daily,\n')

    fh.write('  {},         !- Name\n'.format(schedule.name))
    fh.write('  {},         !- Sunday Schedule:Day Name\n'.format(schedule.sunday))
    fh.write('  {},         !- Monday Schedule:Day Name\n'.format(schedule.monday))
    fh.write('  {},         !- Tuesday Schedule:Day Name\n'.format(schedule.tuesday))
    fh.write('  {},         !- Wednesday Schedule:Day Name\n'.format(schedule.wednesday))
    fh.write('  {},         !- Thursday Schedule:Day Name\n'.format(schedule.thursday))
    fh.write('  {},         !- Friday Schedule:Day Name\n'.format(schedule.friday))
    fh.write('  {},         !- Saturday Schedule:Day Name\n'.format(schedule.saturday))
    fh.write('  {},         !- Holiday Schedule:Day Name\n'.format(schedule.holiday))
    fh.write('  {},         !- SummerDesignDay Schedule:Day Name\n'.format(schedule.summer_design_day))
    fh.write('  {},         !- WinterDesignDay Schedule:Day Name\n'.format(schedule.winter_design_day))
    fh.write('  {},         !- CustomDay1 Schedule:Day Name\n'.format(schedule.custom_day1))
    fh.write('  {};         !- CustomDay2 Schedule:Day Name\n'.format(schedule.custom_day2))
    fh.write('\n')
    fh.close()


def write_schedule_year(building, schedule):
    fh = open(building.idf_filepath, 'a')

    fh.write('Schedule:Year,\n')
    fh.write('  {},     !- Name\n'.format(schedule.name))
    fh.write('  {},     !- Schedule Type Limits Name\n'.format(schedule.type_limits))
    fh.write('  {},     !- Schedule:Week Name 1\n'.format(schedule.schedule_week_name1))
    fh.write('  {},     !- Start Month 1\n'.format(schedule.start_month_1))
    fh.write('  {},     !- Start Day 1\n'.format(schedule.start_day1))
    fh.write('  {},     !- End Month 1\n'.format(schedule.end_month1))
    fh.write('  {};     !- End Day 1\n'.format(schedule.end_day1))
    fh.write('  \n')
    fh.write('  \n')
    fh.close()


def write_schedule_type_limits(building, schedule):
    fh = open(building.idf_filepath, 'a')
    fh.write('ScheduleTypeLimits,\n')
    fh.write('  {},     !- Name\n'.format(schedule.name))
    fh.write('  {},     !- Lower Limit Value\n'.format(schedule.lower_limit))
    fh.write('  {},     !- Upper Limit Value\n'.format(schedule.upper_limit))
    fh.write('  {},     !- Numeric Type\n'.format(schedule.numeric_type))
    fh.write('  {};     !- Unit Type\n'.format(schedule.unit_type))
    fh.write('  \n')

    # fh.write('ScheduleTypeLimits,\n')
    # fh.write('  Any Number;              !- Name\n')
    # fh.write('  \n')

    # fh.write('ScheduleTypeLimits,\n')
    # fh.write('  Fraction,                !- Name\n')
    # fh.write('  0.0,                     !- Lower Limit Value\n')
    # fh.write('  1.0,                     !- Upper Limit Value\n')
    # fh.write('  CONTINUOUS;              !- Numeric Type\n')
    # fh.write('  \n')

    # fh.write('ScheduleTypeLimits,\n')
    # fh.write('  Temperature,             !- Name\n')
    # fh.write('  -60,                     !- Lower Limit Value\n')
    # fh.write('  200,                     !- Upper Limit Value\n')
    # fh.write('  CONTINUOUS,              !- Numeric Type\n')
    # fh.write('  Temperature;             !- Unit Type\n')
    # fh.write('  \n')

    # fh.write('ScheduleTypeLimits,\n')
    # fh.write('  Control Type,            !- Name\n')
    # fh.write('  0,                       !- Lower Limit Value\n')
    # fh.write('  4,                       !- Upper Limit Value\n')
    # fh.write('  DISCRETE;                !- Numeric Type\n')
    # fh.write('  \n')

    fh.write('  \n')
    fh.write('  \n')
    fh.close()


def write_internal_gains(building):

    for pk in building.peoples:
        p = building.peoples[pk]
        fh = open(building.idf_filepath, 'a')
        fh.write('People,\n')
        fh.write('  {},     !- Name\n'.format(p.name))
        fh.write('  {},     !- Zone or ZoneList Name\n'.format(p.zone_name))
        fh.write('  {},     !- Number of People Schedule Name\n'.format(p.schedule_name))
        fh.write('  {},     !- Number of People Calculation Method\n'.format(p.calculation_method))
        fh.write('  {},     !- Number of People\n'.format(p.number_of_people))
        fh.write('  {},     !- People per Zone Floor Area [person/m2]\n'.format(p.people_per_floor_area))
        fh.write('  {},     !- Zone Floor Area per Person [m2/person]\n'.format(p.floor_area_per_person))
        fh.write('  {},     !- Fraction Radiant\n'.format(p.fraction_radiant))
        fh.write('  {},     !- Sensible Heat Fraction\n'.format(p.sensible_heat_fraction))
        fh.write('  {};     !- Activity Level Schedule Name\n'.format(p.activity_level_schedule_name))
        fh.write('  \n')


    for lk in building.lights:
        l = building.lights[lk]
        fh.write('Lights,\n')
        fh.write('  {},     !- Name\n'.format(l.name))
        fh.write('  {},     !- Zone or ZoneList Name\n'.format(l.zone_name))
        fh.write('  {},     !- Schedule Name\n'.format(l.schedule_name))
        fh.write('  {},     !- Design Level Calculation Method\n'.format(l.design_level_calculation_method))
        fh.write('  {},     !- Lighting Level [W]\n'.format(l.lighting_level))
        fh.write('  {},     !- Watts per Zone Floor Area [W/m2]\n'.format(l.watts_per_zone_floor_area))
        fh.write('  {},     !- Watts per Person [W/person]\n'.format(l.watts_per_person))
        fh.write('  {},     !- Return Air Fraction\n'.format(l.return_air_fraction))
        fh.write('  {},     !- Fraction Radiant\n'.format(l.fraction_radiant))
        fh.write('  {},     !- Fraction Visible\n'.format(l.fraction_visible))
        fh.write('  {},     !- Fraction Replaceable\n'.format(l.fraction_replaceable))
        fh.write('  {};     !- End-Use Subcategory\n'.format(l.end_use_subcategory))
        fh.write('  \n')

    for ek in building.electric_equipments:
        e = building.electric_equipments[ek]
        fh.write('ElectricEquipment,\n')
        fh.write('  {},     !- Name\n'.format(e.name))                              
        fh.write('  {},     !- Zone or ZoneList Name\n'.format(e.zone_name))             
        fh.write('  {},     !- Schedule Name\n'.format(e.schedule_name))                     
        fh.write('  {},     !- Design Level Calculation Method\n'.format(e.calculation_method))       
        fh.write('  {},     !- Design Level [W]\n'.format(e.design_level))                  
        fh.write('  {},     !- Watts per Zone Floor Area [W/m2]\n'.format(e.watts_per_zone_floor_area))  
        fh.write('  {},     !- Watts per Person [W/person]\n'.format(e.watts_per_person))           
        fh.write('  {},     !- Fraction Latent\n'.format(e.fraction_latent))                   
        fh.write('  {},     !- Fraction Radiant\n'.format(e.fraction_radiant))                  
        fh.write('  {},     !- Fraction Lost\n'.format(e.fraction_lost))   
        fh.write('  {};     !- End-Use Subcategory\n'.format(e.end_use_subcategory))
        fh.write('  \n')
        fh.write('  \n')
        fh.close()


def write_infiltration_rates(building):
    for ik in building.infiltrations:
        i = building.infiltrations[ik]

        fh = open(building.idf_filepath, 'a')
        fh.write('  ZoneInfiltration:DesignFlowRate,\n')
        fh.write('    {},       !- Name\n'.format(i.name))
        fh.write('    {},       !- Zone or ZoneList Name\n'.format(i.zone_name))
        fh.write('    {},       !- Schedule Name\n'.format(i.schedule_name))
        fh.write('    {},       !- Design Flow Rate Calculation Method\n'.format(i.design_flow_rate_calculation_method))
        fh.write('    {},       !- Design Flow Rate [m3/s]\n'.format(i.design_flow_rate))
        fh.write('    {},       !- Flow per Zone Floor Area [m3/s-m2]\n'.format(i.flow_per_zone_floor_area))
        fh.write('    {},       !- Flow per Exterior Surface Area [m3/s-m2]\n'.format(i.flow_per_exterior_area))
        fh.write('    {},       !- Air Changes per Hour [1/hr]\n'.format(i.air_changes_per_hour))
        fh.write('    {},       !- Constant Term Coefficient\n'.format(i.constant_term_coefficient))
        fh.write('    {},       !- Temperature Term Coefficient\n'.format(i.temperature_term_coefficient))
        fh.write('    {},       !- Velocity Term Coefficient\n'.format(i.velocity_term_coefficient))
        fh.write('    {};       !- Velocity Squared Term Coefficient\n'.format(i.velocity_squared_term_coefficient))
        fh.write('  \n')
        fh.write('  \n')
        fh.close()


def write_thermostats(building):

    for tk in building.zone_control_thermostats:
        t = building.zone_control_thermostats[tk]

        fh = open(building.idf_filepath, 'a')
        fh.write('ZoneControl:Thermostat,\n')
        fh.write('  {},    !- Name\n'.format(t.name))
        fh.write('  {},    !- Zone or ZoneList Name\n'.format(t.zone_name))
        fh.write('  {},    !- Control Type Schedule Name\n'.format(t.schedule_name))
        fh.write('  {},    !- Control 1 Object Type\n'.format(t.control1_object_type))
        fh.write('  {},    !- Control 1 Name\n'.format(t.control1_object_name))
        fh.write('  {},    !- Control 2 Object Type\n'.format(t.control2_object_type))
        fh.write('  {},    !- Control 2 Name\n'.format(t.control2_object_name))
        fh.write('  {},    !- Control 3 Object Type\n'.format(t.control3_object_type))
        fh.write('  {},    !- Control 3 Name\n'.format(t.control3_object_name))
        fh.write('  {},    !- Control 4 Object Type\n'.format(t.control4_object_type))
        fh.write('  {},    !- Control 4 Name\n'.format(t.control4_object_name))
        fh.write('  {};    !- Temperature Difference Between Cutout And Setpoint [deltaC]\n'.format(t.temperature_difference))
        fh.write('  \n')

    
    for sk in building.setpoints:
        s = building.setpoints[sk]
        fh.write('ThermostatSetpoint:DualSetpoint,\n')
        fh.write('  {},     !- Name\n'.format(s.name))
        fh.write('  {},     !- Heating Setpoint Temperature Schedule Name\n'.format(s.heating_setpoint))
        fh.write('  {};     !- Cooling Setpoint Temperature Schedule Name\n'.format(s.cooling_setpoint))
        fh.write('  \n')

    fh.write('  \n')
    fh.close()


def write_hvac(building):

    for ik in building.ideal_air_loads:
        i = building.ideal_air_loads[ik]
        fh = open(building.idf_filepath, 'a')
        fh.write('ZoneHVAC:IdealLoadsAirSystem,\n')
        fh.write('  {},     !- Name\n'.format(i.name))
        fh.write('  {},     !- Availability Schedule Name\n'.format(i.availability_schedule_name))
        fh.write('  {},     !- Zone Supply Air Node Name \n'.format(i.zone_supply_air_node_name))
        fh.write('  {},     !- Zone Exhaust Air Node Name\n'.format(i.zone_exhaust_air_node_name))
        fh.write('  {},     !- System Inlet Air Node Name\n'.format(i.system_inlet_air_node_name))
        fh.write('  {},     !- Maximum Heating Supply Air Temperature [C]\n'.format(i.max_heating_supply_temperature))
        fh.write('  {},     !- Minimum Cooling Supply Air Temperature [C]\n'.format(i.min_cooling_supply_temperature))
        fh.write('  {},     !- Maximum Heating Supply Air Humidity Ratio [kgWater/kgDryAir]\n'.format(i.max_heating_supply_humidity_ratio))
        fh.write('  {},     !- Minimum Cooling Supply Air Humidity Ratio [kgWater/kgDryAir]\n'.format(i.min_cooling_supply_humidity_ratio))
        fh.write('  NoLimit,     !- Heating Limit\n')
        # fh.write('  {},     !- Heating Limit\n'.format(i.heating_limit))
        fh.write('  {},     !- Maximum Heating Air Flow Rate [m3/s]\n'.format(i.max_heating_air_flow_rate))
        fh.write('  ,       !- Maximum Sensible Heating Capacity [W]\n')
        # fh.write('  {},     !- Maximum Sensible Heating Capacity [W]\n'.format(i.max_sensible_heating_capacity))
        fh.write('  LimitFlowRate,     !- Cooling Limit\n')
        # fh.write('  {},     !- Cooling Limit\n'.format(i.cooling_limit))
        fh.write('  ,       !- Maximum Cooling Air Flow Rate [m3/s]\n')
        fh.write('  ,       !- Maximum Total Cooling Capacity [W]\n')
        # fh.write('  {},     !- Maximum Cooling Air Flow Rate [m3/s]\n'.format(i.maximum_cooling_air_flow_rate))
        # fh.write('  {},     !- Maximum Total Cooling Capacity [W]\n'.format(i.maximum_total_cooling_capacity))
        fh.write('  {},     !- Heating Availability Schedule Name\n'.format(i.heating_availability_schedule_name))
        fh.write('  {},     !- Cooling Availability Schedule Name\n'.format(i.cooling_availability_schedule_name))
        fh.write('  {},     !- Dehumidification Control Type\n'.format(i.dehimidification_control_type))
        fh.write('  {},     !- Cooling Sensible Heat Ratio\n'.format(i.cooling_sensible_heat_ratio))
        fh.write('  {},     !- Humidification Control Type\n'.format(i.humidification_control_type))
        # fh.write('  ,     !- Design Specification Outdoor Air Object Name\n')
        fh.write('  {},     !- Design Specification Outdoor Air Object Name\n'.format(i.desing_specification_outdoor_air_name))
        fh.write('  {},     !- Outdoor Air Inlet Node Name\n'.format(i.outdoor_inlet_node_name))
        fh.write('  {},     !- Demand Controlled Ventilation Type\n'.format(i.demand_controlled_ventilation_type))
        fh.write('  NoEconomizer,     !- Outdoor Air Economizer Type\n'.format(i.outdoor_air_economizer_type))
        # fh.write('  {},     !- Outdoor Air Economizer Type\n'.format(i.outdoor_air_economizer_type))
        fh.write('  Enthalpy,     !- Heat Recovery Type\n'.format(i.heat_recovery_type))
        # fh.write('  {},     !- Heat Recovery Type\n'.format(i.heat_recovery_type))
        fh.write('  0.7,     !- Sensible Heat Recovery Effectiveness\n'.format(i.sensible_heat_recovery_effectiveness))
        # fh.write('  {},     !- Sensible Heat Recovery Effectiveness\n'.format(i.sensible_heat_recovery_effectiveness))
        fh.write('  0.7;     !- Latent Heat Recovery Effectiveness\n'.format(i.latent_heat_revovery_effectiveness))
        # fh.write('  {};     !- Latent Heat Recovery Effectiveness\n'.format(i.latent_heat_revovery_effectiveness))
        fh.write('  \n')
        fh.write('  \n')
        fh.close()


    for ek in building.equipment_lists:
        el = building.equipment_lists[ek]
        fh = open(building.idf_filepath, 'a')
        fh.write('ZoneHVAC:EquipmentList,\n')
        fh.write('  {},     !- Name\n'.format(el.name))
        fh.write('  {},     !- Load Distribution Scheme\n'.format(el.load_distribution_scheme))
        fh.write('  {},     !- Zone Equipment 1 Object Type\n'.format(el.zone_equipment_object_type1))
        fh.write('  {},     !- Zone Equipment 1 Name\n'.format(el.zone_equipment_name1))
        fh.write('  {},     !- Zone Equipment 1 Cooling Sequence\n'.format(el.zone_equipment_cooling_sequence))
        fh.write('  {},     !- Zone Equipment 1 Heating or No-Load Sequence\n'.format(el.zone_equipment_heating_sequence))
        fh.write('  {},     !- Zone Equipment 1 Sequential Cooling Fraction Schedule Name\n'.format(el.zone_equipment_sequenctial_cooling_fraction_schedule))
        fh.write('  {};     !- Zone Equipment 1 Sequential Heating Fraction Schedule Name\n'.format(el.zone_equipment_sequential_heating_fraction_schedule))
        fh.write('  \n')
        fh.write('  \n')
        fh.close()


    for ek in building.equipment_connections:
        ec = building.equipment_connections[ek]
        fh = open(building.idf_filepath, 'a')
        fh.write('ZoneHVAC:EquipmentConnections,\n')
        fh.write('  {},     !- Zone Name\n'.format(ec.name))
        fh.write('  {},     !- Zone Conditioning Equipment List Name\n'.format(ec.zone_conditioning_equipment_list))
        fh.write('  {},     !- Zone Air Inlet Node or NodeList Name\n'.format(ec.zone_air_inlet_node))
        fh.write('  {},     !- Zone Air Exhaust Node or NodeList Name\n'.format(ec.zone_air_exhaust_node))
        fh.write('  {};     !- Zone Air Node Name\n'.format(ec.zone_air_node))
        fh.write('  \n')
        fh.write('  \n')
        fh.close()


def write_node_lists(building):
    fh = open(building.idf_filepath, 'a')

    for nlk in building.node_lists:
        nl = building.node_lists[nlk]
        nodes = building.node_lists[nlk].nodes
        fh.write('NodeList,\n')
        fh.write('  {},     !- Name\n'.format(nl.name))
        for i, nk in enumerate(nodes):
            if i == len(nodes) - 1:
                sep = ';'
            else:
                sep = ','
            fh.write('  {}{}        !- Node Name {}\n'.format(nodes[nk], sep, i + 1))
        fh.write('\n')
    fh.close()


def write_outdoor_airs(building):
    fh = open(building.idf_filepath, 'a')
    for oak in building.outdoor_airs:
        oa = building.outdoor_airs[oak]
        fh.write('DesignSpecification:OutdoorAir,\n')
        fh.write('  {},       !- Name\n'.format(oa.name))
        fh.write('  {},       !- Outdoor Air Method\n'.format(oa.outdoor_air_method))
        fh.write('  {},       !- Outdoor Air Flow per Person [m3/s-person]\n'.format(oa.outdoor_air_flow_per_person))
        fh.write('  {},       !- Outdoor Air Flow per Zone Floor Area [m3/s-m2]\n'.format(oa.outdoor_air_flow_zone_area))
        fh.write('  {},       !- Outdoor Air Flow per Zone [m3/s]\n'.format(oa.outdoor_air_zone))
        fh.write('  {};       !- Outdoor Air Flow Air Changes per Hour [1/hr]\n'.format(oa.outdoor_air_flow_air_changes_per_hour))
        fh.write('\n')
    fh.close()


def write_daylight(building):
    fh = open(building.idf_filepath, 'a')
    for dck in building.daylighting_controls:
        dc = building.daylighting_controls[dck]
        fh.write('Daylighting:Controls,\n')
        fh.write('  {},     !- Name\n'.format(dc.name))
        fh.write('  {},     !- Zone or Space Name\n'.format(dc.zone_name))
        fh.write('  {},     !- Daylighting Method\n'.format(dc.daylighting_method))
        fh.write('  {},     !- Availability Schedule Name\n'.format(dc.availability_schedule))
        fh.write('  {},     !- Lighting Control Type\n'.format(dc.lighting_control_type))
        fh.write('  {},     !- Minimum Input Power Fraction for Continuous or ContinuousOff Dimming Control\n'.format(dc.min_input_power_fraction))
        fh.write('  {},     !- Minimum Light Output Fraction for Continuous or ContinuousOff Dimming Control\n'.format(dc.min_light_output_fraction))
        fh.write('  {},     !- Number of Stepped Control Steps\n'.format(dc.num_stepped_control_steps))
        fh.write('  {},     !- Probability Lighting will be Reset When Needed in Manual Stepped Control\n'.format(dc.probability_lighting_reset))
        fh.write('  {},     !- Glare Calculation Daylighting Reference Point Name\n'.format(dc.glare_reference_point))
        fh.write('  {},     !- Glare Calculation Azimuth Angle of View Direction Clockwise from Zone y-Axis [deg]\n'.format(dc.glare_azimut_angle))
        fh.write('  {},     !- Maximum Allowable Discomfort Glare Index\n'.format(dc.max_allowable_discomfort_glare_index))
        fh.write('  {},     !- DElight Gridding Resolution [m2]\n'.format(dc.delight_gridding_resolution))
        for rpk in building.daylighting_controls[dck].reference_points:
            rpt = building.daylighting_controls[dck].reference_points[rpk]
            rpt_name = rpt['ref_pt_name']
            rpt_frac = rpt['ref_pt_fraction']
            rpt_illm = rpt['illuminance_setpt']
            sep = ';'
            # print(rpt_name)
            fh.write('  {}, !- Daylighting Reference Point Name {}\n'.format(rpt_name, rpk + 1))
            fh.write('  {},  !- Fraction of Lights Controlled by Reference Point {}\n'.format(rpt_frac, rpk + 1))
            fh.write('  {}{}  !- Illuminance Setpoint at Reference Point {} [lux]\n'.format(rpt_illm, sep, rpk + 1))
        fh.write('\n')

    for drpk in building.daylighting_reference_points:
        rpt = building.daylighting_reference_points[drpk]
        fh.write('Daylighting:ReferencePoint,\n')
        fh.write('  {},           !- Name\n'.format(rpt.name))
        fh.write('  {},           !- Zone or Space Name\n'.format(rpt.zone_name))
        fh.write('  {},           !- X-Coordinate of Reference Point [m]\n'.format(rpt.x))
        fh.write('  {},           !- Y-Coordinate of Reference Point [m]\n'.format(rpt.y))
        fh.write('  {};           !- Z-Coordinate of Reference Point [m]\n'.format(rpt.z))
        fh.write('\n')
    fh.close()

def write_spaces(building):
    fh = open(building.idf_filepath, 'a')
    for spk in building.spaces:
        sp = building.spaces[spk]
        fh.write('Space,\n')
        fh.write('{},                               !- Name\n'.format(sp.name))
        fh.write('{},                               !- Zone Name\n'.format(sp.zone_name))
        fh.write('{},                               !- Ceiling Height [m]\n'.format(sp.height))
        fh.write('{},                               !- Volume [m3]\n'.format(sp.volume))
        fh.write('{},                               !- Floor Area [m2]\n'.format(sp.floor_area))
        fh.write('{};                               !- Space Type\n'.format(sp.space_type))
        fh.write('\n')
    fh.write('\n')
    fh.close()

def write_space_lists(building):
    fh = open(building.idf_filepath, 'a')

    for slk in building.space_lists:
        sl = building.space_lists[slk]
        spaces = building.space_lists[slk].spaces
        fh.write('SpaceList,\n')
        fh.write('  {},     !- Name\n'.format(sl.name))
        for i, sk in enumerate(spaces):
            if i == len(spaces) - 1:
                sep = ';'
            else:
                sep = ','
            fh.write('  {}{}        !- Space Name {}\n'.format(spaces[sk], sep, i + 1))
        fh.write('\n')
        fh.close()


def write_output_items(building):
    """
    Writes the output items to the .idf file from the building data.
    Parameters
    ----------
    building: object
        The building datastructure containing the data to be used
    
    Returns
    -------
    None
    """
    fh = open(building.idf_filepath, 'a')
    fh.write('Output:Variable,*,Zone Mean Air Temperature,timestep;\n')
    fh.write('\n')
    
    fh.write('OutputControl:Table:Style,\n')
    fh.write('    CommaAndHTML;                    !- Column Separator\n')
    fh.write('\n')

    fh.write('Output:Table:SummaryReports,\n')
    fh.write('    AllSummary;              !- Report 1 Name\n')
    fh.write('\n')

    fh.write('Output:Variable,\n')
    fh.write('  ,                                       !- Key Value\n')
    fh.write('  Zone Ideal Loads Supply Air Total Cooling Energy, !- Variable Name\n')
    fh.write('  Hourly;                                 !- Reporting Frequency\n')
    fh.write('\n')

    fh.write('Output:Variable,\n')
    fh.write('  ,                                       !- Key Value\n')
    fh.write('  Zone Ideal Loads Supply Air Total Heating Energy, !- Variable Name\n')
    fh.write('  Hourly;                                 !- Reporting Frequency\n')
    fh.write('\n')

    fh.write('Output:Variable,\n')
    fh.write('  ,                                       !- Key Value\n')
    fh.write('  Zone Lights Electricity Energy,         !- Variable Name\n')
    fh.write('  Hourly;                                 !- Reporting Frequency\n')
    fh.write('\n')
    fh.write('\n')
    fh.write('\n')

    fh.close()


if __name__ == '__main__':
    pass