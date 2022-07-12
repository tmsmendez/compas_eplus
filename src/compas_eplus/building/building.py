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

from ast import literal_eval

from compas.utilities import geometric_key

from compas_eplus.building.construction import Construction
from compas_eplus.building.material import Material
from compas_eplus.building.material import MaterialNoMass
from compas_eplus.building.material import WindowMaterialGas
from compas_eplus.building.material import WindowMaterialGlazing
from compas_eplus.building.shading import Shading
from compas_eplus.building.window import Window
from compas_eplus.building.zone import Zone

from compas_eplus.read_write import write_idf
from compas_eplus.read_write import read_mean_zone_temperatures

# TODO: Delete previous results

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
    mean_air_temperatures: dict
        Dictionaty containing all MAT results per zone
    construction_key_dict: dict
        Dictionary mapping construction names to construction keys
    srf_cpt_dict: dict
        Dictionary mapping all surface center points geometric keys to zones and surface keys
    
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

        self.mean_air_temperatures = {}
        self.construction_key_dict = {}
        self.srf_cpt_dict = {}

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
                'construction_key_dict': self.construction_key_dict, 
                'mean_air_temperatures' : self.mean_air_temperatures,
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
        self.construction_key_dict = data.get('construction_key_dict') or {}
        self.mean_air_temperatures = data.get('mean_air_temperatures') or {}

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
    def from_quad(cls, path, wea, quad, num_zones=5):
        pass

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
        write_idf(self)

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
                self.zones
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

        self.materials[len(self.materials)] = material

    def add_materials_from_lib(self, lib):
        """
        Adds material objects to the building datastructure from a library dictionary.

        Parameters
        ----------
        lib: dict
            Dictionary containing data for all materials to be added
        
        Returns
        -------
        None
        
        """
        mat_dict = {'Material': Material,
                    'MaterialNoMass': MaterialNoMass,
                    'WindowMaterialGlazing': WindowMaterialGlazing,
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

    def analyze(self, exe=None):
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
        temps, times = read_mean_zone_temperatures(self, filepath)
        self.mean_air_temperatures = temps
        self.result_times = times

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


if __name__ == '__main__':
    for i in range(50): print('')

    path = compas_eplus.TEMP
    wea = compas_eplus.SEATTLE

    quad = [[0,0,0],
            [10,0,0],
            [10,10,0],
            [0,10,0],
            ]
    b = Building.from_quad(path, wea, quad, num_zones=5)