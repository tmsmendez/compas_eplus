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
import pickle

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
from compas_eplus.building.light import DaylightingReferencePoint
from compas_eplus.building.light import DaylightingControls
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
from compas_eplus.building.outdoor_air import OutdoorAir
from compas_eplus.building.space import Space
from compas_eplus.building.space import SpaceList

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


#TODO: update to/from JSON eventually, or give a OBJ pickle option



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
    def __init__(self, path, weather, name='Building', program='residential'):
        
        self.name = name
        self.path = path
        self.idf_filepath = os.path.join(path, '{}.idf'.format(self.name))
        self.weather = weather
        self.program = program

        self.ep_version = '22.2.0'
        self.num_timesteps = 1
        self.terrain = 'City'
        self.solar_distribution = 'FullExteriorWithReflections'

        self.daylighting_controls_height = .8

        self.zones                        = {}
        self.windows                      = {}
        self.materials                    = {}
        self.constructions                = {}
        self.shadings                     = {}
        self.layers                       = {}
        self.schedules                    = {}
        self.lights                       = {}
        self.daylighting_reference_points = {}
        self.daylighting_controls         = {}
        self.peoples                      = {}
        self.electric_equipments          = {}
        self.zone_control_thermostats     = {}
        self.setpoints                    = {}
        self.ideal_air_loads              = {}
        self.infiltrations                = {}
        self.equipment_lists              = {}
        self.equipment_connections        = {}
        self.zone_lists                   = {}
        self.node_lists                   = {}
        self.outdoor_airs                 = {}
        self.set_schedules                = set()
        self.construction_key_dict        = {}
        self.srf_cpt_dict                 = {}
        self.material_key_dict            = {}
        self.results                      = {}
        self.spaces                       = {}
        self.space_lists                  = {}
        self.totals                       = {}

    @property
    def area(self):
        area = 0
        for zk in self.zones:
            area += self.zones[zk].area
        return area

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

        results = {}
        for timek in self.results:
            results[timek] = {}
            for zk in self.results[timek]:
                results[timek][zk] = {}
                for rk in self.results[timek][zk]:
                    results[timek][zk][rk] = self.results[timek][zk][rk]


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
                'results' : results,
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
        results                    = data.get('results') or {}
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
                    'WindowMaterialGlazingSimple': WindowMaterialGlazingSimple,
                    'WindowMaterialGas': WindowMaterialGas, 
                    }

        for mk in materials:
            mat = mat_dict[materials[mk]['__type__']]
            self.materials[literal_eval(mk)] = mat.from_data(materials[mk])

        for ck in constructions:
            # print(ck, type(ck))
            self.constructions[literal_eval(ck)] = Construction.from_data(constructions[ck])

        for sk in shadings:
            self.shadings[literal_eval(sk)] = Shading.from_data(shadings[sk])

        for timek in results:
            self.results[literal_eval(timek)] = {}
            for zk in results[timek]:
                self.results[literal_eval(timek)][literal_eval(zk)] = {}
                for rk in results[timek][zk]:
                    self.results[literal_eval(timek)][literal_eval(zk)][literal_eval(rk)] = results[timek][zk][rk]

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
    def from_quad_1zone(cls, path, wea, quad, height):
        building = cls(path, wea)
        mesh = make_box_from_quad(quad, height)
        z = Zone.from_mesh(mesh, 'zone_0')
        building.add_zone(z)
        return building

    @classmethod
    def from_idf(cls, filepath, path, wea):
        data = get_idf_data(filepath)
        building = cls(path, wea)
        building.add_data_from_idf(data)
        return building

    @staticmethod
    def from_obj(filename, output=True):

        """ Imports a Building object from an .obj file through Pickle.

        Parameters
        ----------
        filename : str
            Path to load the Building .obj from.
        output : bool
            Print terminal output.

        Returns
        -------
        obj
            Imported Building object.

        """

        with open(filename, 'rb') as f:
            building = pickle.load(f)

        if output:
            print('***** Building loaded from: {0} *****'.format(filename))

        return building

    def to_obj(self, output=True, path=None, name=None):

        """ Exports the Building object to an .obj file through Pickle.

        Parameters
        ----------
        output : bool
            Print terminal output.

        Returns
        -------
        None

        """
        if not path:
            path = self.path
        if not name:
            name = self.name
        filename = os.path.join(path, name + '.obj')

        with open(filename, 'wb') as f:
            pickle.dump(self, f, protocol=2)

        if output:
            print('***** Building saved to: {0} *****\n'.format(filename))

    def add_data_from_idf(self, data):
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
            z.height = zones[zone]['height']
            z.volume = zones[zone]['volume']
            z.origin = zones[zone]['origin']

            for i, srf in enumerate(surfaces):
                srf = zones[zone]['surfaces'][srf]
                # print(srf['name'])
                z.surfaces.face_attribute(i, 'name', srf['name'])
                z.surfaces.face_attribute(i, 'construction', srf['construction'])
                z.surfaces.face_attribute(i, 'surface_type', srf['surface_type'])
                z.surfaces.face_attribute(i, 'outside_boundary_condition', srf['outside_condition'])
                # print(srf['outside_condition'])
            self.add_zone(z)
        
        windows = data['windows']
        for win in windows:
            w = Window()
            w.name = windows[win]['name']
            w.nodes = windows[win]['nodes']
            w.building_surface = windows[win]['building_surface']
            w.construction =  windows[win]['construction']
            self.add_window(w)

        materials = data['materials']
        self.add_materials_from_json_dict(None, materials)

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
            self.add_construction(c)
        self.make_layers_dict()

        schedules = data['schedules']
        for sk in schedules:
            s = Schedule.from_idf_data(schedules[sk])
            self.add_schedule(s, sk)
        
        lights = data['lights']
        for lk in lights:
            l = Light.from_data(lights[lk])
            self.add_light(l, lk)

        peoples = data['people']
        for pk in peoples:
            p = People.from_data(peoples[pk])
            self.add_people(p, pk)

        eeq = data['electric_equipment']
        for ek in eeq:
            e = ElectricEquipment.from_data(eeq[ek])
            self.add_electric_equipment(e, ek)

        zct = data['zone_control_thermostat']
        for zk in zct:
            z = ZoneControlThermostat.from_data(zct[zk])
            self.add_zone_control_thermostat(z, zk)

        spt = data['setpoint']
        for sk in spt:
            s = DualSetpoint.from_data(spt[sk])
            self.add_setpoint(s, sk)

        ial = data['ideal_air_load']
        for ik in ial:
            i = IdealAirLoad.from_data(ial[ik])
            self.add_ideal_air_load(i, ik)

        infiltration = data['infiltration']
        for ik in infiltration:
            i = Infiltration.from_data(infiltration[ik])
            self.add_infiltration(i, ik)

        el = data['equipment_list']
        for ek in el:
            e = EquipmentList.from_data(el[ek])
            self.add_equipment_list(e, ek)

        ec = data['equipment_connection']
        for ek in ec:
            e = EquipmentConnection.from_data(ec[ek])
            self.add_equipment_connection(e, ek)

        zl = data['zone_lists']
        for zlk in zl:
            zl_ = ZoneList.from_data(zl[zlk])
            self.add_zone_list(zl_, zlk)

        nl = data['node_lists']
        for nlk in nl:
            nl_ = NodeList.from_data(nl[nlk])
            self.add_node_list(nl_, nlk)

        oa = data['outdoor_air']
        for oak in oa:
            oa_ = OutdoorAir.from_data(oa[oak])
            self.add_outdoor_air(oa_, oak)

        dp = data['daylighting:referencepoint']
        for ptk in dp:
            pt = DaylightingReferencePoint.from_data(dp[ptk])
            self.add_daylighting_reference_point(pt, ptk)

        dc = data['daylighting_controls']
        for dck in dc:
            d = DaylightingControls.from_data(dc[dck])
            self.add_daylighting_controls(d, dck)

        sp = data['spaces']
        for spk in sp:
            s = Space.from_data(sp[spk])
            self.add_space(s, spk)

        sl = data['space_lists']
        for slk in sl:
            sl_ = SpaceList.from_data(sl[slk])
            self.add_space_list(sl_, slk)

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

    def add_zone(self, zone, floor_cond='Ground', roof_cond='Outdoors', wall_cond='Outdoors'):
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
        out_dict = {'Wall': wall_cond, 'Roof': roof_cond, 'Floor': floor_cond}

        zk =  len(self.zones)
        self.zones[zk] = zone
        mesh = self.zones[zk].surfaces
        for fk in mesh.faces():
            cpt =mesh.face_centroid(fk)
            gk = geometric_key(cpt)
            out_cond = mesh.face_attribute(fk, 'outside_boundary_condition')
            srft = mesh.face_attribute(fk, 'surface_type')
            fn = mesh.face_attribute(fk, 'name')
            
            if out_cond == None or out_cond == 'Surface':
                out_cond = 'Surface'
                if gk in self.srf_cpt_dict:
                    
                    zk_ = self.srf_cpt_dict[gk]['zone']
                    fk_ = self.srf_cpt_dict[gk]['surface']
                    fn_ = self.zones[zk_].surfaces.face_attribute(fk_, 'name')
                    mesh.face_attribute(fk, 'outside_boundary_condition', out_cond)
                    self.zones[zk_].surfaces.face_attribute(fk_,'outside_boundary_condition', out_cond)  

                    mesh.face_attribute(fk, 'outside_boundary_condition_object', fn_)
                    self.zones[zk_].surfaces.face_attribute(fk_,'outside_boundary_condition_object', fn)
                else:
                    mesh.face_attribute(fk, 'outside_boundary_condition', out_dict[srft])
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
        wk = len(self.windows)
        window.name = '{}_{}'.format(window.name, wk)
        self.windows[wk] = window

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

        # layers = {}
        # count = 0
        # for lk in construction.layers:
        #     th = construction.layers[lk]['thickness']
        #     if th:
        #         layers[count] = construction.layers[lk]
        #         count += 1
        # construction.layers = layers
        ck = construction.name
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

    def add_daylighting_reference_point(self, drpt, ptk):
        """
        Adds a daylight reference point object to the building datastructure.

        Parameters
        ----------
        drpt: object
            The daylight reference point object to be added
        
        Returns
        -------
        None
        
        """
        self.daylighting_reference_points[ptk] = drpt

    def add_daylighting_controls(self, dc, dck):
        """
        Adds a daylight controls object to the building datastructure.

        Parameters
        ----------
        drpt: object
            The daylight controls point object to be added
        
        Returns
        -------
        None
        
        """
        self.daylighting_controls[dck] = dc

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

    def add_space(self, space, sk):
        """
        Adds a space object to the building datastructure.

        Parameters
        ----------
        space: object
            The space object to be added
        
        Returns
        -------
        None
        
        """
        self.spaces[sk] = space

    def add_space_list(self, space_list, slk):
        """
        Adds a space list object to the building datastructure.

        Parameters
        ----------
        space_list: object
            The space list object to be added
        
        Returns
        -------
        None
        
        """
        self.space_lists[slk] = space_list

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

    def add_outdoor_air(self, outdoor_air, nlk):
        """
        Adds an outdoor_air object to the building datastructure.

        Parameters
        ----------
        zone_list: object
            The outdoor_air object to be added
        
        Returns
        -------
        None
        
        """
        self.outdoor_airs[nlk] = outdoor_air

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
        out = os.path.join(self.path, '{}_eplus_out'.format(self.name))

        if delete:
            try:
                self.delete_result_files(out)
            except:
                pass

        print(exe, '-w', self.weather,'--output-directory', out, idf)
        subprocess.call([exe, '-w', self.weather,'--output-directory', out, idf])

    def load_results(self, print_error=True):
        """
        Loads Energy+ results from result text files

        
        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        filepath = os.path.join(self.path, '{}_eplus_out'.format(self.name), 'eplusout.eso')
        error_filepath = os.path.join(self.path, '{}_eplus_out'.format(self.name), 'eplusout.err')
        read_error_file(error_filepath, print_error=print_error)
        for i in range(5): print('')
        read_results_file(self, filepath)
        zones = [self.zones[zk].name for zk in self.zones]
        totals = {'heating': 0, 'cooling':0, 'lighting': 0}
        for zone in zones:
            heat = [self.results[tk][zone]['heating'] for tk in self.results]
            heat = sum(heat)
            totals['heating'] += heat

            cool = [self.results[tk][zone]['cooling'] for tk in self.results]
            cool = sum(cool)
            totals['cooling'] += cool

            light = [self.results[tk][zone]['lighting'] for tk in self.results]
            light = sum(light)
            totals['lighting'] += light
            
            self.totals[zone] = {'heating': heat,
                                 'cooling': cool,
                                 'lighting': light
                                }
        totals['total'] = totals['heating'] + totals['cooling'] + totals['lighting']
        self.totals['totals'] = totals

    def assign_constructions_from_rules(self, rules):
        """
        """
        for zk in self.zones:
            mesh = self.zones[zk].surfaces
            sks = mesh.faces()
            for sk in sks:
                name = mesh.face_attribute(sk, 'surface_type')
                # print(name)
                # print(rules[name])
                mesh.face_attribute(sk, 'construction', rules[name])

        for wk in self.windows:
            self.windows[wk].construction = rules['Window']
        
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

    def set_zone_systems(self):

        from copy import deepcopy

        eqc_key = list(self.equipment_connections.keys())[0]
        eql_key = list(self.equipment_lists.keys())[0]
        inl_key = list(self.node_lists.keys())[0]
        enl_key = list(self.node_lists.keys())[1]
        ial_key = list(self.ideal_air_loads.keys())[0]
        dlc_key = list(self.daylighting_controls.keys())[0]
        dlr_key = list(self.daylighting_reference_points.keys())[0]

        eqc = self.equipment_connections[eqc_key]
        eql = self.equipment_lists[eql_key]
        inl = self.node_lists[inl_key]
        enl = self.node_lists[enl_key]
        ial = self.ideal_air_loads[ial_key]
        dlc = self.daylighting_controls[dlc_key]
        # dlr = self.daylighting_reference_points[dlr_key]

        for zk in self.zones:
            zname = self.zones[zk].name

            self.node_lists[zk] = NodeList.from_data(deepcopy(inl.data))
            inlname = '{}_{}'.format(self.node_lists[zk].name, zname)
            self.node_lists[zk].name = inlname
            self.node_lists[zk].nodes['0'] = 'inlet_node_{}'.format(zname)

            self.node_lists[zname] = NodeList.from_data(deepcopy(enl.data))
            enlname = '{}_{}'.format(self.node_lists[zname].name, zname)
            self.node_lists[zname].name = enlname
            self.node_lists[zname].nodes['0'] = 'exhaust_node_{}'.format(zname)

            self.ideal_air_loads[zk] = IdealAirLoad.from_data(deepcopy(ial.data))
            ialname = '{} {}'.format(zname, self.ideal_air_loads[zk].name)
            self.ideal_air_loads[zk].name = ialname
            self.ideal_air_loads[zk].zone_supply_air_node_name = inlname
            self.ideal_air_loads[zk].zone_exhaust_air_node_name = enlname

            self.equipment_lists[zk] = EquipmentList.from_data(eql.data)
            elname =  '{}_{}'.format(self.equipment_lists[zk].name, zname)
            self.equipment_lists[zk].name = elname
            self.equipment_lists[zk].zone_equipment_name1 = ialname

            self.equipment_connections[zk] = EquipmentConnection.from_data(eqc.data)
            self.equipment_connections[zk].name = zname
            self.equipment_connections[zk].zone_conditioning_equipment_list = elname
            self.equipment_connections[zk].zone_air_inlet_node = inlname
            self.equipment_connections[zk].zone_air_exhaust_node = enlname
            self.equipment_connections[zk].zone_air_node += '_{}'.format(zname)

            self.daylighting_controls[zk] = DaylightingControls.from_data(deepcopy(dlc.data))
            dc_name = 'daylighting_controls_{}'.format(zname)
            dc_ref_pt_name = 'daylighting_ref_pt_{}'.format(zname)
            x, y, _ = self.zones[zk].centroid_xy
            self.daylighting_controls[zk].name = dc_name
            self.daylighting_controls[zk].zone_name = zname
            self.daylighting_controls[zk].glare_reference_point = dc_ref_pt_name
            self.daylighting_controls[zk].reference_points = {0: self.daylighting_controls[zk].reference_points[0]}
            self.daylighting_controls[zk].reference_points[0]['ref_pt_name'] = dc_ref_pt_name
            dl_rpt = DaylightingReferencePoint.from_data({'name': dc_ref_pt_name,
                                                                 'zone_name': zname,
                                                                 'x': x,
                                                                 'y': y,
                                                                 'z': self.daylighting_controls_height,
                                                                 })
            self.daylighting_reference_points[dc_ref_pt_name] = dl_rpt


        del self.equipment_connections[eqc_key]
        del self.equipment_lists[eql_key]
        del self.node_lists[inl_key]
        del self.node_lists[enl_key]
        del self.ideal_air_loads[ial_key]
        del self.daylighting_controls[dlc_key]
        del self.daylighting_reference_points[dlr_key]


if __name__ == '__main__':

    for i in range(50): print('')