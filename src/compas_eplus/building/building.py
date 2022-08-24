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
from compas_eplus.building.shading import Shading
from compas_eplus.building.window import Window
from compas_eplus.building.zone import Zone

from compas_eplus.read_write import write_idf_from_building
from compas_eplus.read_write import read_mean_zone_temperatures
from compas_eplus.read_write import read_error_file

from compas_eplus.utilities import make_box_from_quad

from compas.geometry import subtract_vectors
from compas.geometry import cross_vectors
from compas.geometry import intersection_line_line_xy
from compas.geometry import add_vectors
from compas.geometry import normalize_vector
from compas.geometry import scale_vector

from compas.utilities import geometric_key



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
    def __init__(self, path, weather):
        self.name = 'Building'
        self.path = path
        self.idf_filepath = os.path.join(path, f'{self.name}.idf')
        self.weather = weather

        self.ep_version = '9.6'
        self.num_timesteps = 1
        self.terrain = 'City'
        self.solar_distribution = 'FullExteriorWithReflections'
        self.zones = {}
        self.windows = {}
        self.materials = {}
        self.constructions = {}
        self.shadings = {}
        self.layers = {}

        self.mean_air_temperatures = {}
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
    def from_quad(cls, path, wea, quad, zone_depth, height):
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
        write_idf_from_building(self)

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

    def add_materials_from_json(self, filepath):
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

        with open(filepath, 'r') as fp:
            lib = json.load(fp)

        mat_dict = {'Material': Material,
                    'MaterialNoMass': MaterialNoMass,
                    'WindowMaterialGlazing': WindowMaterialGlazing,
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
        try:
            temps, times = read_mean_zone_temperatures(self, filepath)
            self.mean_air_temperatures = temps
            self.result_times = times
        except:
            raise NameError('Energy+ returned the above error message')

    def plot_mean_zone_temperatures(self, plot_type='scatter'):
        """
        Plots mean zone air temperatures per zone

        Parameters
        ----------
        plot_type: str, optional
            The plot type to be used. Options are "scatter" and "line" 

        Returns
        -------
        None
        
        """
        import plotly.express as px
        from datetime import datetime
        import pandas as pd

        times = [datetime(2022, m, d, h) for h, d, m in self.result_times]
        temps = self.mean_air_temperatures
        data = {}
        counter = 0
        for zk in self.zones:
            # print(zk)
            for i in range(len(times)):
                # print(i)
                # print(i, zk, temps[i])
                data[counter] = {'zone': self.zones[zk].name, 
                                 'temp': temps[i][zk],
                                 'time': times[i],
                                 'hour': self.result_times[i][0],
                                 'day': self.result_times[i][1],
                                 'month': self.result_times[i][2],
                        }
                counter += 1

        df = pd.DataFrame.from_dict(data, orient='index')
        
        if plot_type == 'scatter':
            if len(self.zones) > 1:
                color_by = 'zone'
            else:
                color_by = 'temp'
            fig = px.scatter(df, x='time', y='temp', hover_data={"time": "|%B %d, %H, %Y"}, color=color_by, size=None)
        elif plot_type == 'line':
            fig = px.line(df, x='time', y='temp', hover_data={"time": "|%B %d, %H, %Y"}, color='zone')
        fig.update_xaxes(dtick="M1",tickformat="%b", ticklabelmode="period")
        fig.show()

    def assign_constructions_from_rules(self, rules):
        """
        """
        for zk in self.zones:
            mesh = self.zones[zk].surfaces
            sks = mesh.faces()
            for sk in sks:
                name = mesh.face_attribute(sk, 'name')
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


if __name__ == '__main__':

    for i in range(50): print('')
    b = Building.from_json(os.path.join(compas_eplus.DATA, 'buildings', '5_zone.json'))
    
    b.write_idf()
