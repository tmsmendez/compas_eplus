from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import json
import compas_eplus
import subprocess
import shutil

from ast import literal_eval

from math import sin

from compas_eplus.building.construction import Construction

from compas_eplus.building.material import Material
from compas_eplus.building.material import MaterialNoMass
from compas_eplus.building.material import WindowMaterialGas
from compas_eplus.building.material import WindowMaterialGlazing
from compas_eplus.building.material import WindowMaterialGlazingSimple

from compas_eplus.building.shading import Shading

from compas_eplus.building.window import Window

from compas_eplus.building.zone import Zone
from compas_eplus.building.zone import ZoneSurfaces

from compas_eplus.building.schedule import Schedule
from compas_eplus.building.light import Light
from compas_eplus.building.people import People
from compas_eplus.building.electric_eq import ElectricEquipment
from compas_eplus.building.zone_control_thermostat import ZoneControlThermostat
from compas_eplus.building.setpoint import DualSetpoint
from compas_eplus.building.ideal_air_load import IdealAirLoad
from compas_eplus.building.infiltration import Infiltration
from compas_eplus.building.equipment import EquipmentList
from compas_eplus.building.equipment import EquipmentConnection
from compas_eplus.building.zone_list import ZoneList
from compas_eplus.building.node_list import NodeList

# from compas_eplus.building.schedule import OfficeOccupancySchedule
# from compas_eplus.building.schedule import OfficeLightsSchedule
# from compas_eplus.building.schedule import OfficeEquipmentSchedule
# from compas_eplus.building.schedule import OfficeActivitySchedule
# from compas_eplus.building.schedule import OfficeControlTypeSchedule
# from compas_eplus.building.schedule import OfficeHeatingSchedule
# from compas_eplus.building.schedule import OfficeCoolingSchedule

from compas_eplus.read_write import write_idf_from_building
from compas_eplus.read_write import read_results_file
from compas_eplus.read_write import read_error_file
from compas_eplus.read_write import get_idf_data

from compas_eplus.utilities import make_box_from_quad

from compas.geometry import subtract_vectors
from compas.geometry import cross_vectors
from compas.geometry import intersection_line_line_xy
from compas.geometry import add_vectors
from compas.geometry import normalize_vector
from compas.geometry import scale_vector
from compas.geometry import midpoint_point_point

from compas.utilities import geometric_key

from compas.datastructures import Mesh



class Building(object):
    """
    Base building datastructure for building energy and thermal analysis.

    Parameters
    ----------
    path: str
        The path for the analysis files and results
    weather: str
        The path to the weather file used in the analysis
    name: str
        The name of the datastructure
    ep_version: str
        Version of Energy+ to be used
    num_timesteps: int
        NUmber of timesteps per hour to be used in the analysis
    terrain: str
        Terrain type ("City" by default)
    solar_distribution: str
        Solar distribution type ("FullExteriorWithReflections" by default)
    zones: dict
        Dictionary containing all zone objects
    windows: dict
        Dictionaty containing all window objects
    materials: dict
        Dictionary containing all material objects
    constructions: dict
        Dictionary containing all constriction objects
    shadings: dict
        Dictionary containing all shading vdevice objects
    layers: dict
        Dictionary containing all layers with different materials and thicknesses
    mean_air_temperatures: dict
        Dictionaty containing all MAT results per zone
    construction_key_dict: dict
        Dictionary mapping construction names to construction keys
    srf_cpt_dict: dict
        Dictionary mapping all surface center points geometric keys to zones and surface keys
    material_key_dict: dict
        Dictionary mapping material names to material keys
    """
    def __init__(self, path, weather, name='Building', program='office'):
        
        self.name = name
        self.path = path
        self.idf_filepath = os.path.join(path, '{}.idf'.format(self.name))
        self.weather = weather
        self.program = program

        self.ep_version = '22.2.0'
        self.num_timesteps = 1
        self.terrain = 'City'
        self.solar_distribution = 'FullExteriorWithReflections'

        self.zones                      = {}
        self.windows                    = {}
        self.materials                  = {}
        self.constructions              = {}
        self.shadings                   = {}
        self.layers                     = {}
        self.schedules                  = {}
        self.lights                     = {}
        self.peoples                    = {}
        self.electric_equipments        = {}
        self.zone_control_thermostats   = {}
        self.setpoints                  = {}
        self.ideal_air_loads            = {}
        self.infiltrations              = {}
        self.equipment_lists            = {}
        self.equipment_connections      = {}
        self.zone_lists                 = {}
        self.node_lists                 = {}
        
        self.set_schedules = set()

        self.construction_key_dict = {}
        self.srf_cpt_dict = {}
        self.material_key_dict = {}


    @property
    def data(self):
        zones = {}
        for zk in self.zones:
            zones[zk] = self.zones[zk].data

        windows = {}
        for wk in self.windows:
            windows[wk] = self.windows[wk].data

        materials = {}
        for mk in self.materials:
            materials[mk] = self.materials[mk].data

        constructions = {}
        for ck in self.constructions:
            constructions[ck] = self.constructions[ck].data

        shadings = {}
        for sk in self.shadings:
            shadings[sk] = self.shadings[sk].data


        data = {'idf_filepath' : self.idf_filepath,
                'path'         : self.path,
                'weather': self.weather,
                'name' : self.name,
                'ep_version' : self.ep_version,
                'num_timesteps' : self.num_timesteps,
                'terrain' : self.terrain,
                'solar_distribution' : self.solar_distribution,
                'zones' : zones,
                'windows' : windows,
                'materials' : materials,
                'constructions' : constructions,
                'shadings': shadings,
                'layers': self.layers,
                'construction_key_dict': self.construction_key_dict, 
                'mean_air_temperatures' : self.mean_air_temperatures,
                'material_key_dict': self.material_key_dict,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.filepath              = data.get('filepath') or {}
        self.path                  = data.get('path') or {}
        self.weather               = data.get('weather') or {}
        self.name                  = data.get('name') or {}
        self.ep_version            = data.get('ep_version') or {}
        self.num_timesteps         = data.get('num_timesteps') or {}
        self.terrain               = data.get('terrain') or {}
        self.solar_distribution    = data.get('solar_distribution') or {}
        zones                      = data.get('zones') or {}
        windows                    = data.get('windows') or {}
        materials                  = data.get('materials') or {}
        constructions              = data.get('constructions') or {}
        shadings                   = data.get('shadings') or {}
        self.layers                = data.get('layers') or {}
        self.construction_key_dict = data.get('construction_key_dict') or {}
        self.mean_air_temperatures = data.get('mean_air_temperatures') or {}
        self.material_key_dict     = data.get('material_key_dict') or {}

        for zk in zones:
            self.zones[zk] = Zone.from_data(zones[zk])

        for wk in windows:
            self.windows[wk] = Window.from_data(windows[wk])

        mat_dict = {'Material': Material,
                    'MaterialNoMass': MaterialNoMass,
                    'WindowMaterialGlazing': WindowMaterialGlazing,
                    'WindowMaterialGas': WindowMaterialGas, 
                    }

        for mk in materials:
            mat = mat_dict[materials[mk]['__type__']]
            self.materials[literal_eval(mk)] = mat.from_data(materials[mk])

        for ck in constructions:
            self.constructions[literal_eval(ck)] = Construction.from_data(constructions[ck])

        for sk in shadings:
            self.shadings[literal_eval(sk)] = Shading.from_data(shadings[sk])

    @classmethod
    def from_json(cls, filepath):
        """
        Create a new instance of the building datastructure from a JSON file

        Parameters
        ----------
        filepath: str
            Path to the JSON file
        
        Returns
        -------
            Building
                The instance of the building datastructure
        
        """

        with open(filepath, 'r') as fp:
            data = json.load(fp)

        path = data['path']
        weather = data['weather']

        building = cls(path, weather)
        building.data = data
        return building

    @classmethod
    def from_quad_5zone(cls, path, wea, quad, zone_depth, height):
        b = cls(path, wea)
        
        if type(zone_depth) == list:
            zd = zone_depth
        else:
            zd = [zone_depth, zone_depth, zone_depth, zone_depth]

        quad_ = []
        for i in range(4):
            if i == 3:
                k = 0
            else:
                k = i + 1
            v1 = normalize_vector(subtract_vectors(quad[k], quad[i]))
            v2 = normalize_vector(subtract_vectors(quad[i - 1], quad[i]))
            v1_ = scale_vector(cross_vectors(v1, [0,0,-1]), zd[i])
            v2_ = scale_vector(cross_vectors(v2, [0,0,1]), zd[i-1])
            l1 = [add_vectors(quad[i], v1_), add_vectors(quad[k], v1_)]
            l2 = [add_vectors(quad[i], v2_), add_vectors(quad[i - 1], v2_)]

            xpt = intersection_line_line_xy(l1, l2)
            quad_.append(xpt)

        for i in range(4):
            if i == 3:
                k = 0
            else:
                k = i + 1
            pts = [quad[i], quad[k], quad_[k], quad_[i]]
            mesh = make_box_from_quad(pts, height)
            z = Zone.from_mesh(mesh, 'zone_{}'.format(i))
            b.add_zone(z)

        mesh = make_box_from_quad(quad_, height)
        z = Zone.from_mesh(mesh, 'zone_4')
        b.add_zone(z)
        return b

    @classmethod
    def from_quad_2zone(cls, path, wea, quad, height):
        building = cls(path, wea)

        a, b, c, d = quad
        e = midpoint_point_point(a, b)
        f = midpoint_point_point(d, c)

        quads = [[a, e, f, d], [e, b, c, f]]

        for i, quad in enumerate(quads):
            mesh = make_box_from_quad(quad, height)
            z = Zone.from_mesh(mesh, 'zone_{}'.format(i))
            building.add_zone(z)
        return building

    @classmethod
    def from_idf(cls, filepath, path, wea):
        building = cls(path, wea)

        data = get_idf_data(filepath)
        zones = data['zones']
        for zone in zones:
            zname = zones[zone]['name']
            surfaces = zones[zone]['surfaces']
            vertices = []
            for srf in surfaces:
                srf = zones[zone]['surfaces'][srf]
                face_v = srf['surface_points']
                vertices.extend(face_v)
            faces = [[0,1,2,3],
                     [4,5,6,7],
                     [8,9,10, 11],
                     [12, 13, 14, 15],
                     [16,17,18,19],
                     [20,21,22,23]
                     ]
            mesh = Mesh.from_vertices_and_faces(vertices, faces)
            z = Zone.from_mesh(mesh, zname)

            for i, srf in enumerate(surfaces):
                srf = zones[zone]['surfaces'][srf]
                # print(srf['name'])
                z.surfaces.face_attribute(i, 'name', srf['name'])
                z.surfaces.face_attribute(i, 'construction', srf['construction'])
                z.surfaces.face_attribute(i, 'surface_type', srf['surface_type'])
                z.surfaces.face_attribute(i, 'outside_boundary_condition', srf['outside_condition'])
            building.add_zone(z)
        
        windows = data['windows']
        for win in windows:
            w = Window()
            w.name = windows[win]['name']
            w.nodes = windows[win]['nodes']
            w.building_surface = windows[win]['building_surface']
            w.construction =  windows[win]['construction']
            building.add_window(w)

        materials = data['materials']
        building.add_materials_from_json_dict(None, materials)

        cons = data['constructions']
        for con in cons:
            name = data['constructions'][con]['name']
            layers = data['constructions'][con]['layers']
            layers_ = {}
            for lk in layers:
                lname = layers[lk]
                mname = materials[lname]['name']
                if 'thickness' in materials[lname]:
                    thick = materials[lname]['thickness']
                else:
                    thick = 0
                layers_[lk] = {'name': mname, 'thickness': thick}
            con_ = {'name': name, 'layers': layers_}
            c = Construction.from_data(con_)
            building.add_construction(c)
        building.make_layers_dict()

        schedules = data['schedules']
        for sk in schedules:
            s = Schedule.from_idf_data(schedules[sk])
            building.add_schedule(s, sk)
        
        lights = data['lights']
        for lk in lights:
            l = Light.from_data(lights[lk])
            building.add_light(l, lk)

        peoples = data['people']
        for pk in peoples:
            p = People.from_data(peoples[pk])
            building.add_people(p, pk)

        eeq = data['electric_equipment']
        for ek in eeq:
            e = ElectricEquipment.from_data(eeq[ek])
            building.add_electric_equipment(e, ek)

        zct = data['zone_control_thermostat']
        for zk in zct:
            z = ZoneControlThermostat.from_data(zct[zk])
            building.add_zone_control_thermostat(z, zk)

        spt = data['setpoint']
        for sk in spt:
            s = DualSetpoint.from_data(spt[sk])
            building.add_setpoint(s, sk)

        ial = data['ideal_air_load']
        for ik in ial:
            i = IdealAirLoad.from_data(ial[ik])
            building.add_ideal_air_load(i, ik)

        infiltration = data['infiltration']
        for ik in infiltration:
            i = Infiltration.from_data(infiltration[ik])
            building.add_infiltration(i, ik)

        el = data['equipment_list']
        for ek in el:
            e = EquipmentList.from_data(el[ek])
            building.add_equipment_list(e, ek)

        ec = data['equipment_connection']
        for ek in ec:
            e = EquipmentConnection.from_data(ec[ek])
            building.add_equipment_connection(e, ek)

        zl = data['zone_lists']
        for zlk in zl:
            zl_ = ZoneList.from_data(zl[zlk])
            building.add_zone_list(zl_, zlk)

        nl = data['node_lists']
        for nlk in nl:
            nl_ = NodeList.from_data(nl[nlk])
            building.add_node_list(nl_, nlk)


        return building

    def to_json(self, filepath):
        """
        Serialize the data representation of the building to a JSON file

        Parameters
        ----------
        filepath: str
            Path for the JSON file to be created
        
        Returns
        -------
        None

        """
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    def write_idf(self):
        """
        Writes an IDF file for Energy+ analysis using the data contained in the building
        datastructure.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """

        self.make_layers_dict()
        if not self.schedules:
            self.get_schedules()
        write_idf_from_building(self)

    def get_schedules(self):
        if self.program == 'office':
            self.schedules['occupancy'] = OfficeOccupancySchedule('{}_occupancy'.format(self.name))
            self.schedules['lights'] = OfficeLightsSchedule('{}_lights'.format(self.name))
            self.schedules['equipment'] = OfficeEquipmentSchedule('{}_equipment'.format(self.name))
            self.schedules['activity'] = OfficeActivitySchedule('{}_activity'.format(self.name))
            self.schedules['control_type'] = OfficeControlTypeSchedule('{}_control_type'.format(self.name))
            self.schedules['heating'] = OfficeHeatingSchedule('{}_heating'.format(self.name))
            self.schedules['heating'] = OfficeCoolingSchedule('{}_heating'.format(self.name))
        else:
            raise('This Building program is not yet implemented')

    def add_zone(self, zone):
        """
        Adds a zone object to the building datastructure.

        Parameters
        ----------
        zone: object
            The zone object to be added
        
        Returns
        -------
        None
        
        """
        zk =  len(self.zones)
        self.zones[zk] = zone
        mesh = self.zones[zk].surfaces
        for fk in mesh.faces():
            cpt =mesh.face_centroid(fk)
            gk = geometric_key(cpt)
            if gk in self.srf_cpt_dict:
                mesh.face_attribute(fk, 'outside_boundary_condition', 'Adiabatic')
                zk_ = self.srf_cpt_dict[gk]['zone']
                fk_ = self.srf_cpt_dict[gk]['surface']
                self.zones[zk_].surfaces.face_attribute(fk_,'outside_boundary_condition', 'Adiabatic')  
            else:
                self.srf_cpt_dict[gk] = {'zone': zk, 'surface': fk}

    def add_window(self, window):
        """
        Adds a windows object to the building datastructure.

        Parameters
        ----------
        window: object
            The window object to be added
        
        Returns
        -------
        None
        
        """

        self.windows[len(self.windows)] = window

    def add_material(self, material):
        """
        Adds a material object to the building datastructure.

        Parameters
        ----------
        material: object
            The material object to be added
        
        Returns
        -------
        None
        
        """
        mk = len(self.materials)
        self.materials[mk] = material
        self.material_key_dict[material.name] = mk

    def add_materials_from_json_dict(self, filepath, lib):
        """
        Adds material objects to the building datastructure from a json file.

        Parameters
        ----------
        filepath: string
            Path to the json file  containing data for all materials to be added
        
        Returns
        -------
        None
        
        """
        if filepath:
            with open(filepath, 'r') as fp:
                lib = json.load(fp)

        mat_dict = {'Material': Material,
                    'MaterialNoMass': MaterialNoMass,
                    'WindowMaterialGlazing': WindowMaterialGlazing,
                    'WindowMaterialGlazingSimple': WindowMaterialGlazingSimple, 
                    'WindowMaterialGas': WindowMaterialGas, 
                    }

        for mk in lib:
            t = lib[mk]['__type__']
            mat = mat_dict[t].from_data(lib[mk])
            self.add_material(mat)

    def add_materials_from_csv(self, filepath):
        """
        Adds material objects to the building datastructure from a csv file.

        Parameters
        ----------
        filepath: string
            Path to the csv file  containing data for all materials to be added
        
        Returns
        -------
        None
        
        """
        fh = open(filepath, 'r')
        lines = fh.readlines()[2:]

        data = {}
        for line in lines:
            line = line.split(',')
            name    = line[0]
            type_   = line[1]
            if type_ == 'Material':
                data[name] = {'__type__'              : type_,
                              'name'                  : name,
                              'roughness'             : line[2],
                              'conductivity'          : line[3],
                              'density'               : line[4],
                              'specific_heat'         : line[5],
                              'thermal_absorptance'   : line[6],
                              'solar_absorptance'     : line[7],
                              'visible_absorptance'   : line[8]}

            elif type_ == 'MaterialNoMass':
                data[name] = {'__type__'            : type_,
                              'name'                : name,
                              'roughness'           : line[2],
                              'thermal_resistance'  : line[9],
                              'thermal_absorptance' : line[6],
                              'solar_absorptance'   : line[7],
                              'visible_absorptance' : line[8]}

            elif type_ == 'WindowMaterialGas':

                data[name] = {'__type__'            : type_,
                              'name'                : name,
                              'gas_type'            : line[10]}

            elif type_ == 'WindowMaterialGlazing':
                data[name] = {'__type__'                                : type_,
                              'name'                                    : name,
                              'optical_data_type'                       : line[11],
                              'win_glass_spectral_data_name'            : line[12],
                              'solar_transmittance'                     : line[13],
                              'front_solar_reflectance'                 : line[14],
                              'back_solar_reflectance'                  : line[15],
                              'visible_transmittance'                   : line[16],
                              'front_visible_reflectance'               : line[17],
                              'back_visible_reflectance'                : line[18],
                              'infrared_transmittance'                  : line[19],
                              'front_infrared_hemispherical_emissivity' : line[20],
                              'back_infrared_hemispherical_emissivity'  : line[21],
                              'conductivity'                            : line[3],
                              'dirt_correction_factor'                  : line[22],
                              'solar_diffusing'                         : line[23]}

        mat_dict = {'Material': Material,
                    'MaterialNoMass': MaterialNoMass,
                    'WindowMaterialGlazing': WindowMaterialGlazing,
                    'WindowMaterialGas': WindowMaterialGas, 
                    }

        for mk in data:
            t = data[mk]['__type__']
            mat = mat_dict[t].from_data(data[mk])
            self.add_material(mat)

    def add_constructions_from_lib(self, lib):
        """
        Adds construction objects to the building datastructure from a library dictionary.

        Parameters
        ----------
        lib: dict
            Dictionary containing data for all constructions to be added
        
        Returns
        -------
        None
        
        """
        for ck in lib:
            con = Construction.from_data(lib[ck])
            self.add_construction(con)

    def add_construction(self, construction):
        """
        Adds a construction object to the building datastructure.

        Parameters
        ----------
        construction: object
            The construction object to be added
        
        Returns
        -------
        None
        
        """
        ck = len(self.constructions)
        self.constructions[ck] = construction
        self.construction_key_dict[construction.name] = ck

    def add_schedule(self, schedule, sk):
        """
        Adds a schedule object to the building datastructure.

        Parameters
        ----------
        schedule: object
            The schedule object to be added
        
        Returns
        -------
        None
        
        """
        self.schedules[sk] = schedule

    def add_light(self, light, lk):
        """
        Adds a light object to the building datastructure.

        Parameters
        ----------
        light: object
            The light object to be added
        
        Returns
        -------
        None
        
        """
        self.lights[lk] = light

    def add_people(self, people, pk):
        """
        Adds a people object to the building datastructure.

        Parameters
        ----------
        people: object
            The people object to be added
        
        Returns
        -------
        None
        
        """
        self.peoples[pk] = people

    def add_electric_equipment(self, eeq, ek):
        """
        Adds a electric_equipment object to the building datastructure.

        Parameters
        ----------
        electric_equipment: object
            The electric_equipment object to be added
        
        Returns
        -------
        None
        
        """
        self.electric_equipments[ek] = eeq

    def add_zone_control_thermostat(self, zct, zk):
        """
        Adds a zone_control_thermostat object to the building datastructure.

        Parameters
        ----------
        zone_control_thermostat: object
            The zone_control_thermostat object to be added
        
        Returns
        -------
        None
        
        """
        self.zone_control_thermostats[zk] = zct

    def add_setpoint(self, spt, sk):
        """
        Adds a setpoint object to the building datastructure.

        Parameters
        ----------
        setpoints: object
            The setpoint object to be added
        
        Returns
        -------
        None
        
        """
        self.setpoints[sk] = spt

    def add_ideal_air_load(self, ideal_air_load, ik):
        """
        Adds an ideal_air_load object to the building datastructure.

        Parameters
        ----------
        ideal_air_load: object
            The ideal_air_load object to be added
        
        Returns
        -------
        None
        
        """
        self.ideal_air_loads[ik] = ideal_air_load

    def add_infiltration(self, infiltration, ik):
        """
        Adds an infiltration object to the building datastructure.

        Parameters
        ----------
        infiltration: object
            The infiltration object to be added
        
        Returns
        -------
        None
        
        """
        self.infiltrations[ik] = infiltration

    def add_equipment_list(self, equipment_list, ek):
        """
        Adds an equipment_list object to the building datastructure.

        Parameters
        ----------
        infiltration: object
            The equipment_list object to be added
        
        Returns
        -------
        None
        
        """
        self.equipment_lists[ek] = equipment_list

    def add_equipment_connection(self, equipment_connection, ek):
        """
        Adds an equipment_connection object to the building datastructure.

        Parameters
        ----------
        equipment_connection: object
            The equipment_connection object to be added
        
        Returns
        -------
        None
        
        """
        self.equipment_connections[ek] = equipment_connection

    def add_zone_list(self, zone_list, zlk):
        """
        Adds a zone_list object to the building datastructure.

        Parameters
        ----------
        zone_list: object
            The zone_list object to be added
        
        Returns
        -------
        None
        
        """
        self.zone_lists[zlk] = zone_list

    def add_node_list(self, node_list, nlk):
        """
        Adds an node_list object to the building datastructure.

        Parameters
        ----------
        zone_list: object
            The node_list object to be added
        
        Returns
        -------
        None
        
        """
        self.node_lists[nlk] = node_list

    def add_shading(self, shading):
        """
        Adds a shading object to the building datastructure.

        Parameters
        ----------
        shading: object
            The shading object to be added
        
        Returns
        -------
        None
        
        """
        self.shadings[len(self.shadings)] = shading

    def analyze(self, exe=None, delete=True):
        """
        Runs Energy+ analysis on the .idf file created by the building datastructure.

        Parameters
        ----------
        exe: str, optional
            The path to the Energy+ executable
        
        Returns
        -------
        None
        
        """





        idf = self.idf_filepath
        if not exe:
            exe = 'energyplus'
        out = os.path.join(compas_eplus.TEMP, 'eplus_output')

        if delete:
            try:
                self.delete_result_files(out)
            except:
                pass

        print(exe, '-w', self.weather,'--output-directory', out, idf)
        subprocess.call([exe, '-w', self.weather,'--output-directory', out, idf])

    def load_results(self):
        """
        Loads Energy+ results from result text files

        
        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        filepath = os.path.join(self.path, 'eplus_output', 'eplusout.eso')
        error_filepath = os.path.join(self.path, 'eplus_output', 'eplusout.err')
        read_error_file(error_filepath, print_error=True)
        for i in range(5): print('')
        read_results_file(self, filepath)

    def assign_constructions_from_rules(self, rules):
        """
        """
        for zk in self.zones:
            mesh = self.zones[zk].surfaces
            sks = mesh.faces()
            for sk in sks:
                name = mesh.face_attribute(sk, 'surface_type')
                mesh.face_attribute(sk, 'construction', rules[name])

    def make_layers_dict(self):
        """
        Makes a dictionary containing all unique layers, with names, materials and
        thicknesses.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        for ck in self.constructions:
            lkeys = self.constructions[ck].layers.keys()
            for lk in lkeys:
                name = self.constructions[ck].layers[lk]['name']
                thick = self.constructions[ck].layers[lk]['thickness']
                lname = '{} {}mm'.format(name, round(thick*1000, 1))
                self.layers[lname] = {'layer_name': lname,
                                                 'material_name': name,
                                                 'thickness': thick}

    def delete_result_files(self, out_path):
        """ Deletes energy+ result files.

        Parameters:
            out_path (str): Path to the energy+ output folder.

        Returns:
            None
        """
        shutil.rmtree(out_path)

    def find_set_schedules(self):

        sdict = {'occupancy': self.peoples,
                 'lights': self.lights,
                 'equipment': self.electric_equipments,
                 'activity': self.peoples,
                 'control': self.zone_control_thermostats,
                 'heating': self.setpoints,
                 'cooling': self.setpoints,
                 'any_number': self.infiltrations,
                }

        for k in sdict:
            o = sdict[k]
            oks = o.keys()
            if k == 'heating':
                skeys = [o[ok].heating_setpoint for ok in oks]
            elif k == 'cooling':
                skeys = [o[ok].cooling_setpoint for ok in oks]
            elif k == 'activity':
                skeys = [o[ok].schedule_name for ok in oks]
                skeys_ = [o[ok].activity_level_schedule_name for ok in oks]
                skeys.extend(skeys_)
            else:
                skeys = [o[ok].schedule_name for ok in oks]
            self.set_schedules.update(skeys)

        year_schs =  set()
        for sk in self.set_schedules:
            schedule = self.schedules[sk]
            stype = schedule.type
            if stype == 'year':
                year_schs.add(schedule.schedule_week_name1)
            

        self.set_schedules.update(year_schs)
        for sk in year_schs:
            wks = []
            wks.append(self.schedules[sk].sunday)
            wks.append(self.schedules[sk].monday)           
            wks.append(self.schedules[sk].tuesday)        
            wks.append(self.schedules[sk].wednesday)        
            wks.append(self.schedules[sk].thursday)         
            wks.append(self.schedules[sk].friday)           
            wks.append(self.schedules[sk].saturday)         
            wks.append(self.schedules[sk].holiday)          
            wks.append(self.schedules[sk].summer_design_day)
            wks.append(self.schedules[sk].winter_design_day)
            wks.append(self.schedules[sk].custom_day1)      
            wks.append(self.schedules[sk].custom_day2)
            self.set_schedules.update(wks)

        tls = []
        for sk in self.schedules:
            schedule = self.schedules[sk]
            stype = schedule.type
            if stype == 'schedule_type_limits':
                tls.append(sk)
        self.set_schedules.update(tls)


if __name__ == '__main__':

    from compas_eplus.viewers import BuildingViewer
    from compas_eplus.viewers import ResultsViewer

    for i in range(50): print('')
    
    file = 'teresa_example_apt.idf'
    filepath = os.path.join(compas_eplus.DATA, 'idf_examples', file)
    path = compas_eplus.TEMP
    wea = compas_eplus.SEATTLE
    b = Building.from_idf(filepath, path, wea)
    

    #TODO: Ideal air loads, design specification not using object for now, hard coded
    
    #TODO: Decide to write all schedules or just needed ones. (I vote all for now)
    #TODO: update to/from JSON eventually, or give a OBJ pickle option


    b.write_idf()
    b.analyze(exe='/Applications/EnergyPlus/energyplus')
    b.load_results()
    # v = BuildingViewer(b)
    # v.show()

    v = ResultsViewer(b)
    v.show('total')