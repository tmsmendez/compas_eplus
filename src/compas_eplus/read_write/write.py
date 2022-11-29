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

    write_separator(building)

    write_simulation_control(building)
    write_schedules(building)
    write_schedule_type_limits(building)
    write_internal_gains(building)
    write_infiltration_rates(building)
    write_thermostats(building)
    write_hvac(building)

    write_output_items(building)

def write_separator(building):
    fh = open(building.idf_filepath, 'a')
    fh.write('\n') 
    fh.write('\n') 
    fh.write('\n') 
    fh.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
    fh.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
    fh.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
    fh.write('!         From here on this is new code\n')
    fh.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
    fh.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
    fh.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
    fh.write('\n') 
    fh.write('\n') 
    fh.write('\n') 
    fh.close()

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
    write_zone_list(building)

def write_zone_list(building):
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
    fh.write('  0,          !- X Origin (m)\n')
    fh.write('  0,          !- Y Origin (m)\n')
    fh.write('  0,          !- Z Origin (m)\n')
    fh.write('  1,          !- Type\n')
    fh.write('  1,          !- Multiplier\n')
    fh.write('  ,           !- Ceiling Height (m)\n')
    fh.write('  ,           !- Volume (m3)\n')
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
    # this version is from Eplus documentation

    # fh.write('SimulationControl,\n')
    # fh.write('  Yes,      !- Do Zone Sizing Calculation\n')
    # fh.write('  No,       !- Do System Sizing Calculation\n')
    # fh.write('  No,       !- Do Plant Sizing Calculation\n')
    # fh.write('  Yes,      !- Run Simulation for Sizing Periods\n')
    # fh.write('  Yes,      !- Run Simulation for Weather File Run Periods\n')
    # fh.write('  No,       !- Do HVAC Sizing Simulation for Sizing Periods\n')
    # fh.write('  2;        !- Maximum Number of HVAC Sizing Simulation Passes\n')
    # fh.write('  \n')
    # fh.write('  \n')
    # fh.close()

    # this version is from Teresa's E+ class

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

    for sk in building.schedules:
        write_schedule(building, building.schedules[sk])

    fh = open(building.idf_filepath, 'a')

    fh.write('Schedule:Constant,\n')
    fh.write('    Always On,               !- Name\n')
    fh.write('    Any Number,              !- Schedule Type Limits Name\n')
    fh.write('    1;                       !- Hourly Value\n')
    fh.write('  \n')

    fh.write('Schedule:Compact,\n')
    fh.write('  Htg-SetP-Sch,            !- Name\n')
    fh.write('  Temperature,             !- Schedule Type Limits Name\n')
    fh.write('  Through: 12/31,          !- Field 1\n')
    fh.write('  For: SummerDesignDay,    !- Field 2\n')
    fh.write('  Until: 24:00,16.7,       !- Field 3\n')
    fh.write('  For: WinterDesignDay,    !- Field 5\n')
    fh.write('  Until: 24:00,22.2,       !- Field 6\n')
    fh.write('  For: WeekDays,           !- Field 8\n')
    fh.write('  Until: 6:00,16.7,        !- Field 9\n')
    fh.write('  Until: 20:00,22.2,       !- Field 11\n')
    fh.write('  Until: 24:00,16.7,       !- Field 13\n')
    fh.write('  For: WeekEnds Holiday,   !- Field 15\n')
    fh.write('  Until: 24:00,16.7,       !- Field 16\n')
    fh.write('  For: AllOtherDays,       !- Field 18\n')
    fh.write('  Until: 24:00,16.7;       !- Field 19\n')
    fh.write('  \n')

    fh.write('Schedule:Compact,\n')
    fh.write('  Clg-SetP-Sch,            !- Name\n')
    fh.write('  Temperature,             !- Schedule Type Limits Name\n')
    fh.write('  Through: 12/31,          !- Field 1\n')
    fh.write('  For: SummerDesignDay,    !- Field 2\n')
    fh.write('  Until: 24:00,23.9,       !- Field 3\n')
    fh.write('  For: WinterDesignDay,    !- Field 5\n')
    fh.write('  Until: 24:00,29.4,       !- Field 6\n')
    fh.write('  For: WeekDays,           !- Field 8\n')
    fh.write('  Until: 6:00,29.4,        !- Field 9\n')
    fh.write('  Until: 20:00,23.9,       !- Field 11\n')
    fh.write('  Until: 24:00,29.4,       !- Field 13\n')
    fh.write('  For: WeekEnds Holiday,   !- Field 15\n')
    fh.write('  Until: 24:00,29.4,       !- Field 16\n')
    fh.write('  For: AllOtherDays,       !- Field 18\n')
    fh.write('  Until: 24:00,29.4;       !- Field 19\n')
    fh.write('\n')

    fh.close()

def write_schedule_type_limits(building):
    fh = open(building.idf_filepath, 'a')

    fh.write('ScheduleTypeLimits,\n')
    fh.write('  Any Number;              !- Name\n')
    fh.write('  \n')

    fh.write('ScheduleTypeLimits,\n')
    fh.write('  Fraction,                !- Name\n')
    fh.write('  0.0,                     !- Lower Limit Value\n')
    fh.write('  1.0,                     !- Upper Limit Value\n')
    fh.write('  CONTINUOUS;              !- Numeric Type\n')
    fh.write('  \n')

    fh.write('ScheduleTypeLimits,\n')
    fh.write('  Temperature,             !- Name\n')
    fh.write('  -60,                     !- Lower Limit Value\n')
    fh.write('  200,                     !- Upper Limit Value\n')
    fh.write('  CONTINUOUS,              !- Numeric Type\n')
    fh.write('  Temperature;             !- Unit Type\n')
    fh.write('  \n')

    fh.write('ScheduleTypeLimits,\n')
    fh.write('  Control Type,            !- Name\n')
    fh.write('  0,                       !- Lower Limit Value\n')
    fh.write('  4,                       !- Upper Limit Value\n')
    fh.write('  DISCRETE;                !- Numeric Type\n')
    fh.write('  \n')

    # fh.write('ScheduleTypeLimits,\n')
    # fh.write('  On/Off,                  !- Name\n')
    # fh.write('  0,                       !- Lower Limit Value\n')
    # fh.write('  1,                       !- Upper Limit Value\n')
    # fh.write('  DISCRETE;                !- Numeric Type\n')
    # fh.write('  \n')

    # fh.write('ScheduleTypeLimits,\n')
    # fh.write('  FlowRate,                !- Name\n')
    # fh.write('  0.0,                     !- Lower Limit Value\n')
    # fh.write('  10,                      !- Upper Limit Value\n')
    # fh.write('  CONTINUOUS;              !- Numeric Type\n')


    fh.write('  \n')
    fh.write('  \n')
    fh.close()

def write_internal_gains(building):

    ppl_area = building.people_area[building.program]
    lgt_area = building.lights_area[building.program]
    lgt_frac = building.lights_fraction[building.program]
    eqp_area = building.equipment_area[building.program]

    fh = open(building.idf_filepath, 'a')
    fh.write('People,\n')
    fh.write('  All zones People,        !- Name\n')
    fh.write('  all_zones_list,          !- Zone or ZoneList Name\n')
    fh.write('  {}_occupancy,            !- Number of People Schedule Name\n'.format(building.name))
    fh.write('  people/area,             !- Number of People Calculation Method\n')
    fh.write('  ,                        !- Number of People\n')
    fh.write('  {},                      !- People per Zone Floor Area [person/m2]\n'.format(ppl_area))
    fh.write('  ,                        !- Zone Floor Area per Person [m2/person]\n')
    fh.write('  0.3,                     !- Fraction Radiant\n')
    fh.write('  ,                        !- Sensible Heat Fraction\n')
    fh.write('  {}_activity;             !- Activity Level Schedule Name\n'.format(building.name))
    fh.write('  \n')

    fh.write('Lights,\n')
    fh.write('  All zones Lights,        !- Name\n')
    fh.write('  all_zones_list,          !- Zone or ZoneList Name\n')
    fh.write('  {}_lights,                !- Schedule Name\n'.format(building.name))
    fh.write('  Watts/Area,              !- Design Level Calculation Method\n')
    fh.write('  ,                        !- Lighting Level [W]\n')
    fh.write('  {},                      !- Watts per Zone Floor Area [W/m2]\n'.format(lgt_area))
    fh.write('  ,                        !- Watts per Person {W/person}\n')
    fh.write('  0,                       !- Return Air Fraction\n')
    fh.write('  {},                    !- Fraction Radiant\n'.format(lgt_frac))
    fh.write('  0.2,                     !- Fraction Visible\n')
    fh.write('  0,                       !- Fraction Replaceable\n')
    fh.write('  GeneralLights;           !- End-Use Subcategory\n')
    fh.write('  \n')

    fh.write('ElectricEquipment,\n')
    fh.write('  All zones ElecEq,        !- Name\n')
    fh.write('  all_zones_list,          !- Zone or ZoneList Name\n')
    fh.write('  {}_equipment,                 !- Schedule Name\n'.format(building.name))
    fh.write('  Watts/Area,              !- Design Level Calculation Method\n')
    fh.write('  ,                        !- Design Level [W]\n')
    fh.write('  {},                       !- Watts per Zone Floor Area [W/m2]\n'.format(eqp_area))
    fh.write('  ,                        !- Watts per Person {W/person}\n')
    fh.write('  0,                       !- Fraction Latent\n')
    fh.write('  0.5,                     !- Fraction Radiant\n')
    fh.write('  0;                       !- Fraction Lost\n')
    fh.write('  \n')
    fh.write('  \n')
    fh.close()

def write_infiltration_rates(building):
    fh = open(building.idf_filepath, 'a')
    fh.write('  ZoneInfiltration:DesignFlowRate,\n')
    fh.write('    All zones Infil 1,       !- Name\n')
    fh.write('    all_zones_list,          !- Zone or ZoneList Name\n')
    fh.write('    Always On,               !- Schedule Name\n')
    fh.write('    flow/exteriorwallarea,   !- Design Flow Rate Calculation Method\n')
    fh.write('    ,                        !- Design Flow Rate [m3/s]\n')
    fh.write('    ,                        !- Flow per Zone Floor Area [m3/s-m2]\n')
    fh.write('    {},                      !- Flow per Exterior Surface Area [m3/s-m2]\n'.format(building.infiltration_rate))
    fh.write('    ,                        !- Air Changes per Hour [1/hr]\n')
    fh.write('    0,                       !- Constant Term Coefficient\n')
    fh.write('    0,                       !- Temperature Term Coefficient\n')
    fh.write('    0,                  !- Velocity Term Coefficient\n')
    fh.write('    0;                       !- Velocity Squared Term Coefficient\n')
    fh.write('  \n')
    fh.write('  \n')
    fh.close()

def write_thermostats(building):
    fh = open(building.idf_filepath, 'a')
    fh.write('ZoneControl:Thermostat,\n')
    fh.write('  All zones Control,                  !- Name\n')
    fh.write('  all_zones_list,                     !- Zone or ZoneList Name\n')
    fh.write('  {}_control_type,            !- Control Type Schedule Name\n'.format(building.name))
    # fh.write('  ThermostatSetpoint:SingleCooling,   !- Control 1 Object Type\n')
    # fh.write('  CoolingSetPoint,                    !- Control 1 Name\n')
    # fh.write('  ThermostatSetpoint:SingleHeating,   !- Control 2 Object Type\n')
    # fh.write('  HeatingSetpoint,                    !- Control 2 Name\n')
    fh.write('  ThermostatSetpoint:DualSetpoint,    !- Control 3 Object Type\n')
    fh.write('  DualSetPoint;                       !- Control 3 Name\n')
    fh.write('  \n')
    
    # fh.write('ThermostatSetpoint:SingleHeating,\n')
    # fh.write('  HeatingSetpoint,         !- Name\n')
    # fh.write('  Htg-SetP-Sch;            !- Setpoint Temperature Schedule Name\n')
    # fh.write('  \n')

    # fh.write('ThermostatSetpoint:SingleCooling,\n')
    # fh.write('  CoolingSetpoint,         !- Name\n')
    # fh.write('  Clg-SetP-Sch;            !- Setpoint Temperature Schedule Name\n')
    # fh.write('  \n')

    fh.write('ThermostatSetpoint:DualSetpoint,\n')
    fh.write('  DualSetPoint,            !- Name\n')
    fh.write('  Htg-SetP-Sch,            !- Heating Setpoint Temperature Schedule Name\n')
    fh.write('  Clg-SetP-Sch;            !- Cooling Setpoint Temperature Schedule Name\n')
    
    fh.write('  \n')
    fh.write('  \n')
    fh.close()

def write_hvac(building):

    for zkey in building.zones:
        zone = building.zones[zkey]
        zname = zone.name

        fh = open(building.idf_filepath, 'a')

        fh.write('! Zone {} Idal air load system - - - - - - -\n'.format(zname))
        fh.write('!--------------------------------------------\n')
        fh.write('  \n')

        fh.write('ZoneHVAC:IdealLoadsAirSystem,\n')
        fh.write('  {} Ideal Loads System,              !- Name\n'.format(zname))
        fh.write('  Always On,                           !- Availability Schedule Name\n')
        fh.write('  {} Ideal Loads Supply Node,         !- Zone Supply Air Node Name \n'.format(zname))
        fh.write('  {} Ideal Loads Exhaust Node,         !- Zone Exhaust Air Node Name\n'.format(zname))
        fh.write('  ,                                   !- System Inlet Air Node Name\n')
        fh.write('  50,                                 !- Maximum Heating Supply Air Temperature [C]\n')
        fh.write('  13,                                 !- Minimum Cooling Supply Air Temperature [C]\n')
        fh.write('  0.0156,                             !- Maximum Heating Supply Air Humidity Ratio [kgWater/kgDryAir]\n')
        fh.write('  0.0077,                             !- Minimum Cooling Supply Air Humidity Ratio [kgWater/kgDryAir]\n')
        fh.write('  NoLimit,                            !- Heating Limit\n')
        fh.write('  ,                                   !- Maximum Heating Air Flow Rate [m3/s]\n')
        fh.write('  ,                                   !- Maximum Sensible Heating Capacity [W]\n')
        fh.write('  NoLimit,                            !- Cooling Limit\n')
        fh.write('  ,                                   !- Maximum Cooling Air Flow Rate [m3/s]\n')
        fh.write('  ,                                   !- Maximum Total Cooling Capacity [W]\n')
        fh.write('  ,                                   !- Heating Availability Schedule Name\n')
        fh.write('  ,                                   !- Cooling Availability Schedule Name\n')
        fh.write('  None,                               !- Dehumidification Control Type\n')
        fh.write('  0.7,                                !- Cooling Sensible Heat Ratio\n')
        fh.write('  None,                               !- Humidification Control Type\n')
        fh.write('  ,                                   !- Design Specification Outdoor Air Object Name\n')
        # fh.write('  {} Ideal Loads OA Inlet Node,       !- Outdoor Air Inlet Node Name\n'.format(zname))
        fh.write('  ,                                   !- Outdoor Air Inlet Node Name\n'.format(zname))
        fh.write('  None,                               !- Demand Controlled Ventilation Type\n')
        fh.write('  NoEconomizer,                       !- Outdoor Air Economizer Type\n')
        fh.write('  None,                               !- Heat Recovery Type\n')
        fh.write('  0.70,                               !- Sensible Heat Recovery Effectiveness\n')
        fh.write('  0.65;                               !- Latent Heat Recovery Effectiveness\n')
        fh.write('  \n')

        fh.write('ZoneHVAC:EquipmentList,\n')
        fh.write('  {}Equipment,                    !- Name\n'.format(zname))
        fh.write('  SequentialLoad,                 !- Load Distribution Scheme\n')
        fh.write('  ZoneHVAC:IdealLoadsAirSystem,   !- Zone Equipment 1 Object Type\n')
        fh.write('  {} Ideal Loads System,          !- Zone Equipment 1 Name\n'.format(zname))
        fh.write('  1,                              !- Zone Equipment 1 Cooling Sequence\n')
        fh.write('  1,                              !- Zone Equipment 1 Heating or No-Load Sequence\n')
        fh.write('  ,                               !- Zone Equipment 1 Sequential Cooling Fraction Schedule Name\n')
        fh.write('  ;                               !- Zone Equipment 1 Sequential Heating Fraction Schedule Name\n')
        fh.write('  \n')

        fh.write('ZoneHVAC:EquipmentConnections,\n')
        fh.write('  {},                             !- Zone Name\n'.format(zname))
        fh.write('  {}Equipment,                    !- List Name: Zone Equipment\n'.format(zname))
        fh.write('  {} Ideal Loads Supply Node,     !- List Name: Zone Air Inlet Nodes\n'.format(zname))
        fh.write('  {} Ideal Loads Exhaust Node,    !- List Name: Zone Air Exhaust Nodes\n'.format(zname))
        fh.write('  {}AirNode                       !- Zone Air Node Name\n'.format(zname))
        fh.write('  {} Ideal Loads Return Node;     !- Zone Return Air Node or NodeList Name\n'.format(zname))
        fh.write('  \n')
        fh.write('  \n')
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

    # fh.write('Output:Variable,\n')
    # fh.write('  ,                                       !- Key Value\n')
    # fh.write('  Zone Electric Equipment Electricity Energy, !- Variable Name\n')
    # fh.write('  Hourly;                                 !- Report\n')
    # fh.write('\n')

    # fh.write('Output:Variable,\n')
    # fh.write('  ,                                       !- Key Value\n')
    # fh.write('  Water Use Equipment Heating Energy,     !- Variable Name\n')
    # fh.write('  Hourly;                                 !- Reporting Frequency\n')
    # fh.write('\n')

    # fh.write('Output:Variable,\n')
    # fh.write('  ,                                       !- Key Value\n')
    # fh.write('  Water Heater Electricity Energy,        !- Variable Name\n')
    # fh.write('  Hourly;                                 !- Reporting Frequency\n')
    

    # Output:Table:Monthly,
    #   Air Loop System Energy and Water Use, !- Name
    #   , !- DigitsAfterDecimal Air System Hot Water Energy , SumOrAverage,
    #   Air System Steam Energy , SumOrAverage,
    #   Air System Chilled Water Energy, SumOrAverage,
    #   1.26. GROUP – AIR DISTRIBUTION 1083
    #   Air System Electricity Energy, SumOrAverage, Air System NaturalGas Energy, SumOrAverage,
    #   Air System Water Volume, SumOrAverage;


    fh.write('\n')
    fh.write('\n')

    fh.close()

if __name__ == '__main__':
    pass