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
    fh.write('  {},\t\t\t\t\t !- Name\n'.format(zone.name))
    fh.write('  0,\t\t\t\t\t !- Direction of Relative North (deg)\n')
    fh.write('  0,\t\t\t\t\t !- X Origin (m)\n')
    fh.write('  0,\t\t\t\t\t !- Y Origin (m)\n')
    fh.write('  0,\t\t\t\t\t !- Z Origin (m)\n')
    fh.write('  ,\t\t\t\t\t !- Type\n')
    fh.write('  1,\t\t\t\t\t !- Multiplier\n')
    fh.write('  ,\t\t\t\t\t !- Ceiling Height (m)\n')
    fh.write('  ,\t\t\t\t\t !- Volume (m3)\n')
    fh.write('  ,\t\t\t\t\t !- Floor Area (m2)\n')
    fh.write('  ,\t\t\t\t\t !- Zone Inside Convection Algorithm\n')
    fh.write('  ,\t\t\t\t\t !- Zone Outside Convection Algorithm\n')
    fh.write('  Yes;\t\t\t\t\t !- Part of Total Floor Area\n')
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

    fh = open(building.idf_filepath, 'a')
    fh.write('\n')
    fh.write('BuildingSurface:Detailed,\n')
    fh.write('  {}_{},                    !- Name\n'.format(zone.name, fk))
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
        fh.write('{},                       !- Name\n'.format(win.name))
        fh.write('Window,                   !- Surface Type\n')
        fh.write('{},                       !- Construction Name\n'.format(con))
        fh.write('{},                       !- Building Surface Name\n'.format(bsn))
        fh.write(',                         !- Outside Boundary Condition Object\n')
        fh.write(',                         !- View Factor to Ground\n')
        fh.write(',                         !- Frame and Divider Name\n')
        fh.write(',                         !- Multiplier\n')
        fh.write('{},                         !- Number of Vertices\n'.format(len(win.nodes)))
        for i, nodes in enumerate(win.nodes):
            x, y, z = nodes
            if i == len(win.nodes) - 1:
                sep = ';'
            else:
                sep = ','
            fh.write('{:.3f}, {:.3f}, {:.3f}{}\t\t\t\t\t!- X,Y,Z Vertex {} (m)\n'.format(x, y, z, sep, i))
        fh.write('\n')
    fh.write('\n')
    fh.close()

def write_zone_thermo_schedule(building, zone):
    """
    Writes a zone thermostat schedule to the .idf file from the building data.
    THIS FUNCTION IS NOT YET OPERATIONAL, CURRENTLY HARDCODED. 

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
    fh.write('\n')
    fh.write('ZoneControl:Thermostat,\n')
    fh.write('  {} Thermostat,         !- Name\n'.format(zone.name))
    fh.write('  {},                    !- Zone or ZoneList Name\n'.format(zone.name))
    fh.write('  {} Thermostat Schedule, !- Control Type Schedule Name\n'.format(zone.name))
    fh.write('  ThermostatSetpoint:DualSetpoint,        !- Control 1 Object Type\n')
    fh.write('  Thermostat Setpoint Dual Setpoint 1,    !- Control 1 Name\n')
    fh.write('  ,                                       !- Control 2 Object Type\n')
    fh.write('  ,                                       !- Control 2 Name\n')
    fh.write('  ,                                       !- Control 3 Object Type\n')
    fh.write('  ,                                       !- Control 3 Name\n')
    fh.write('  ,                                       !- Control 4 Object Type\n')
    fh.write('  ,                                       !- Control 4 Name\n')
    fh.write('  0;                                      !- Temperature Difference Between Cutout And Setpoint (deltaC)\n')
    fh.write('\n')
    fh.write('Schedule:Compact,\n')
    fh.write('  {} Thermostat Schedule, !- Name\n'.format(zone.name))
    fh.write('  {} Thermostat Schedule Type Limits, !- Schedule Type Limits Name\n'.format(zone.name))
    fh.write('  Through: 12/31,                         !- Field 1\n')
    fh.write('  For: AllDays,                           !- Field 2\n')
    fh.write('  Until: 24:00,                           !- Field 3\n')
    fh.write('  4;                                      !- Field 4\n')
    fh.write('\n')
    fh.write('ScheduleTypeLimits,\n')
    fh.write('  {} Thermostat Schedule Type Limits, !- Name\n'.format(zone.name))
    fh.write('  0,                                      !- Lower Limit Value (BasedOnField A3)\n')
    fh.write('  4,                                      !- Upper Limit Value (BasedOnField A3)\n')
    fh.write('  DISCRETE;                               !- Numeric Type\n')
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
        fh.write('{},\t\t\t\t\t!- Name\n'.format(name))
        for i, layer in enumerate(layers):
            if i == len(layers) - 1:
                sep = ';'
            else:
                sep = ','
            lname = '{} {}mm'.format(layer, round(thicks[i]*1000, 1))
            fh.write('{}{}\t\t\t\t\t!- Layer {}\n'.format(lname, sep, i))
        fh.write('\n')
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
    fh.write('    HTML;                    !- Column Separator\n')
    fh.write('\n')
    fh.write('Output:Table:SummaryReports,\n')
    fh.write('    AllSummary;              !- Report 1 Name\n')
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

if __name__ == '__main__':
    pass
    """
    version - x
    timesptep - x
    building - x
    global geometry rules - x
    run period - x 
    zone - x
    building surface: detailed - x
    material - x
    construction - x
    material no mass - x 

    output variables - x


    sizing period design day heating
    sizing period design day cooling
    heat balance algo
    surface convection algo inside
    surface convection algo outside
    simulation control
    site:location

    construction window data file THIS SHOULD BE OPTIONAL
    site ground temperature building surface
    schedule type limits
    

    fenestration surface detailed
    """
