from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import json


class Material(object):
    """
    Datastructure containing a Material for Energy+ analysis

    Parameters
    ----------
    __type__: str, 
        Material type
    name: str, optional
        The name for the construction instance
    roughness: str
        Material roughness
    conductivity: float
        Material conductivity (W/m-K)
    density:cfloat
        Material density (kg/m3)
    specific_heat: float
        Material specific heat (J/kg-K)
    thermal_absorptance: float
        Material thermal absorptance (%)
    solar_absorptance: float
        Material solar absorptance (%)
    visible_absorptance: float
        Material visible absorptance (%)
    
        """
    def __init__(self):
        self.__type__                   = 'Material'
        self.name                       = 'Material'
        self.roughness                  = None
        self.conductivity               = None
        self.density                    = None
        self.specific_heat              = None
        self.thermal_absorptance        = None
        self.solar_absorptance          = None
        self.visible_absorptance        = None
    

    def to_json(self, filepath):
        """
        Serialize the data representation of the material to a JSON file

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

    @property
    def data(self):
        data = {'__type__':             self.__type__,
                'name':                 self.name,
                'roughness':            self.roughness,
                'conductivity':         self.conductivity,
                'density':              self.density,
                'specific_heat':        self.specific_heat,
                'thermal_absorptance':  self.thermal_absorptance,
                'solar_absorptance':    self.solar_absorptance,
                'visible_absorptance':  self.visible_absorptance,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.__type__            = data.get('__type__') or {}
        self.name                = data.get('name') or {}
        self.roughness           = data.get('roughness') or {}
        self.conductivity        = data.get('conductivity') or {}
        self.density             = data.get('density') or {}
        self.specific_heat       = data.get('specific_heat') or {}
        self.thermal_absorptance = data.get('thermal_absorptance') or {}
        self.solar_absorptance   = data.get('solar_absorptance') or {}
        self.visible_absorptance = data.get('visible_absorptance') or {}

    @classmethod
    def from_data(cls, data):
        """
        Create a new instance of the material datastructure from a data dictionary

        Parameters
        ----------
        data: dict
            Data dictionary
        
        Returns
        -------
            Material
                The instance of the material datastructure
        
        """
        material = cls()
        material.data = data
        return material

    @classmethod
    def from_json(cls, filepath):
        """
        Create a new instance of the material datastructure from a JSON file

        Parameters
        ----------
        filepath: str
            Path to the JSON file
        
        Returns
        -------
            Material
                The instance of the material datastructure
        
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        material = cls()
        material.data = data
        return material


class MaterialNoMass(object):
    """
    Datastructure containing a MaterialNoMass for Energy+ analysis

    Parameters
    ----------
    __type__: str
        Material __type__
    name: str
        Material name
    roughness: str
        Material roughness
    thermal_resistance: float
        Material thermal_resistance (m2-K/W)
    thermal_absorptance: float
        Material thermal_absorptance (%)
    solar_absorptance : float
        Material solar_absorptance (%)
    visible_absorptance: float
        Material visible_absorptance (%)

    """
    def __init__(self):
        self.__type__                   = 'MaterialNoMass'
        self.name                       = 'MaterialNoMass'
        self.roughness                  = None
        self.thermal_resistance         = None
        self.thermal_absorptance        = None
        self.solar_absorptance          = None
        self.visible_absorptance        = None
    

    def to_json(self, filepath):
        """
        Serialize the data representation of the material to a JSON file

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

    @property
    def data(self):
        data = {'__type__'              : self.__type__,
                'name'                  : self.name,
                'roughness'             : self.roughness,
                'thermal_resistance'    : self.thermal_resistance,
                'thermal_absorptance'   : self.thermal_absorptance,
                'thermal_absorptance'   : self.thermal_absorptance,
                'solar_absorptance'     : self.solar_absorptance,
                'visible_absorptance'   : self.visible_absorptance,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.__type__            = data.get('__type__') or {}
        self.name                = data.get('name') or {}
        self.roughness           = data.get('roughness') or {}
        self.thermal_resistance  = data.get('thermal_resistance') or {}
        self.thermal_absorptance = data.get('thermal_absorptance') or {}
        self.thermal_absorptance = data.get('thermal_absorptance') or {}
        self.solar_absorptance   = data.get('solar_absorptance') or {}
        self.visible_absorptance = data.get('visible_absorptance') or {}

    @classmethod
    def from_data(cls, data):
        """
        Create a new instance of the material datastructure from a data dictionary

        Parameters
        ----------
        data: dict
            Data dictionary
        
        Returns
        -------
            Material
                The instance of the material datastructure
        
        """
        material = cls()
        material.data = data
        return material

    @classmethod
    def from_json(cls, filepath):
        """
        Create a new instance of the material datastructure from a JSON file

        Parameters
        ----------
        filepath: str
            Path to the JSON file
        
        Returns
        -------
            Material
                The instance of the material datastructure
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        material = cls()
        material.data = data
        return material


class WindowMaterialGas(object):
    """
    Datastructure containing a WindowMaterialGass for Energy+ analysis

    Parameters
    ----------
    __type__ : str
        Material __type__ 
    name     : str
        Material name     
    gas_type : str
        Material gas_type 

    """
    def __init__(self):
        self.__type__          = 'WindowMaterialGas'
        self.name              = 'WindowMaterialGas'                   
        self.gas_type          = None
    

    def to_json(self, filepath):
        """
        Serialize the data representation of the material to a JSON file

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

    @property
    def data(self):
        data = {'__type__'     : self.__type__,
                'name'         : self.name,
                'gas_type'     : self.gas_type,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.__type__       = data.get('__type__') or {}
        self.name           = data.get('name') or {}
        self.gas_type       = data.get('gas_type') or {}

    @classmethod
    def from_data(cls, data):
        """
        Create a new instance of the material datastructure from a data dictionary

        Parameters
        ----------
        data: dict
            Data dictionary
        
        Returns
        -------
            Material
                The instance of the material datastructure
        
        """
        material = cls()
        material.data = data
        return material

    @classmethod
    def from_json(cls, filepath):
        """
        Create a new instance of the material datastructure from a JSON file

        Parameters
        ----------
        filepath: str
            Path to the JSON file
        
        Returns
        -------
            Material
                The instance of the material datastructure
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        material = cls()
        material.data = data
        return material


class WindowMaterialGlazing(object):
    """
    Datastructure containing a MaterialNoMass for Energy+ analysis

    Parameters
    ----------
    __type__: str
        Material __type__                               
    name: str, optional
        Material name                                   
    optical_data_type: str
        Material optical_data_type                      
    win_glass_spectral_data_name: str
        Material win_glass_spectral_data_name           
    thickness: float (m)
        Material thickness                              
    solar_transmittance: float
        Material solar_transmittance (%)
    front_solar_reflectance: float
        Material front_solar_reflectance (%)
    back_solar_reflectance: float
        Material back_solar_reflectance (%)
    visible_transmittance : float
        Material visible_transmittance (%)
    front_visible_reflectance: float
        Material front_visible_reflectance (%)
    back_visible_reflectance: float
        Material back_visible_reflectance (%)
    infrared_transmittance: float
        Material infrared_transmittance (%)
    front_infrared_hemispherical_emissivity: float
        Material front_infrared_hemispherical_emissivity (%)
    back_infrared_hemispherical_emissivity: float
        Material back_infrared_hemispherical_emissivity (%)
    conductivity: float
        Material conductivity (W/m-K)
    dirt_correction_factor: float
        Material dirt_correction_factor (%)
    solar_diffusing: float
        Material solar_diffusing (%)

    """
    def __init__(self):
        self.__type__                                   = 'WindowMaterialGlazing'
        self.name                                       = 'WindowMaterialGlazing'
        self.optical_data_type                          = None
        self.win_glass_spectral_data_name               = None
        self.solar_transmittance                        = None
        self.front_solar_reflectance                    = None
        self.back_solar_reflectance                     = None
        self.visible_transmittance                      = None
        self.front_visible_reflectance                  = None
        self.back_visible_reflectance                   = None
        self.infrared_transmittance                     = None
        self.front_infrared_hemispherical_emissivity    = None
        self.back_infrared_hemispherical_emissivity     = None
        self.conductivity                               = None
        self.dirt_correction_factor                     = None
        self.solar_diffusing                            = None


    def to_json(self, filepath):
        """
        Serialize the data representation of the material to a JSON file

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

    @property
    def data(self):
        data = {'__type__'                                  : self.__type__,
                'name'                                      : self.name,                                   
                'optical_data_type'                         : self.optical_data_type,                     
                'win_glass_spectral_data_name'              : self.win_glass_spectral_data_name,
                'solar_transmittance'                       : self.solar_transmittance,                  
                'front_solar_reflectance'                   : self.front_solar_reflectance,                
                'back_solar_reflectance'                    : self.back_solar_reflectance,                 
                'visible_transmittance'                     : self.visible_transmittance,                  
                'front_visible_reflectance'                 : self.front_visible_reflectance,              
                'back_visible_reflectance'                  : self.back_visible_reflectance,               
                'infrared_transmittance'                    : self.infrared_transmittance,                 
                'front_infrared_hemispherical_emissivity'   : self.front_infrared_hemispherical_emissivity,
                'back_infrared_hemispherical_emissivity'    : self.back_infrared_hemispherical_emissivity, 
                'conductivity'                              : self.conductivity, 
                'dirt_correction_factor'                    : self.dirt_correction_factor,                 
                'solar_diffusing'                           : self.solar_diffusing,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.__type__                                = data.get('__type__') or {}
        self.name                                    = data.get('name') or {}
        self.optical_data_type                       = data.get('optical_data_type') or {}
        self.win_glass_spectral_data_name            = data.get('win_glass_spectral_data_name') or ''
        self.solar_transmittance                     = data.get('solar_transmittance') or {}
        self.front_solar_reflectance                 = data.get('front_solar_reflectance') or {}
        self.back_solar_reflectance                  = data.get('back_solar_reflectance') or {}
        self.visible_transmittance                   = data.get('visible_transmittance') or {}
        self.front_visible_reflectance               = data.get('front_visible_reflectance') or {}
        self.back_visible_reflectance                = data.get('back_visible_reflectance') or {}
        self.infrared_transmittance                  = data.get('infrared_transmittance') or ''
        self.front_infrared_hemispherical_emissivity = data.get('front_infrared_hemispherical_emissivity') or {}
        self.back_infrared_hemispherical_emissivity  = data.get('back_infrared_hemispherical_emissivity') or {}
        self.conductivity                            = data.get('conductivity') or {}
        self.dirt_correction_factor                  = data.get('dirt_correction_factor') or {}
        self.solar_diffusing                         = data.get('solar_diffusing') or {}

    @classmethod
    def from_data(cls, data):
        """
        Create a new instance of the material datastructure from a data dictionary

        Parameters
        ----------
        data: dict
            Data dictionary
        
        Returns
        -------
            Material
                The instance of the material datastructure
        
        """
        material = cls()
        material.data = data
        return material

    @classmethod
    def from_json(cls, filepath):
        """
        Create a new instance of the material datastructure from a JSON file

        Parameters
        ----------
        filepath: str
            Path to the JSON file
        
        Returns
        -------
            Material
                The instance of the material datastructure
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        material = cls()
        material.data = data
        return material


class WindowMaterialGlazingSimple(object):
    """
    Datastructure containing a MaterialNoMass for Energy+ analysis

    Parameters
    ----------
    __type__: str
        Material __type__
    name: str, optional
        Material name
    u_factor: float
        Material U-Factor (W/m2-K)
    solar_heat_gain_coefficient: float
        Material Solar Heat Gain Coefficient (%)
    visible_transmittance : float
        Material visible_transmittance (%)


    """

    def __init__(self):
        self.__type__                                   = 'WindowMaterialGlazingSimple'
        self.name                                       = 'WindowMaterialGlazingSimple'
        self.u_factor                                   = None
        self.solar_heat_gain_coefficient                = None
        self.visible_transmittance                      = None


    def to_json(self, filepath):
        """
        Serialize the data representation of the material to a JSON file

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

    @property
    def data(self):
        data = {'__type__'                          : self.__type__,
                'name'                              : self.name,
                'u_factor'                          : self.u_factor,
                'solar_heat_gain_coefficient'       : self.solar_heat_gain_coefficient,
                'visible_transmittance'             : self.visible_transmittance,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.__type__                               = data.get('__type__') or {}
        self.name                                   = data.get('name') or {}
        self.u_factor                               = data.get('u_factor') or {}
        self.solar_heat_gain_coefficient            = data.get('solar_heat_gain_coefficient') or {}
        self.visible_transmittance                  = data.get('visible_transmittance') or {}

    @classmethod
    def from_data(cls, data):
        """
        Create a new instance of the material datastructure from a data dictionary

        Parameters
        ----------
        data: dict
            Data dictionary
        
        Returns
        -------
            Material
                The instance of the material datastructure
        
        """
        material = cls()
        material.data = data
        return material

    @classmethod
    def from_json(cls, filepath):
        """
        Create a new instance of the material datastructure from a JSON file

        Parameters
        ----------
        filepath: str
            Path to the JSON file
        
        Returns
        -------
            Material
                The instance of the material datastructure
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        material = cls()
        material.data = data
        return material


if __name__ == '__main__':
    pass