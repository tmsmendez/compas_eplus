from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

# import json
# from ast import literal_eval


class Light(object):
    """
    Datastructure containing a lights object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
        The name for the lights instance
        zone_name
        schedule_name
        design_level_calculation_method
        lighting_level
        watts_per_zone_floor_area
        watts_per_person
        return_air_fraction
        fraction_radiant
        fraction_visible
        fraction_replaceable
        end_use_subcategory
    """
    def __init__(self):
        self.__type__                           = 'Light'
        self.name                               = None
        self.zone_name                          = None
        self.schedule_name                      = None
        self.design_level_calculation_method    = None
        self.lighting_level                     = None
        self.watts_per_zone_floor_area          = None
        self.watts_per_person                   = None
        self.return_air_fraction                = None
        self.fraction_radiant                   = None
        self.fraction_visible                   = None
        self.fraction_replaceable               = None
        self.end_use_subcategory                = None

    @classmethod
    def from_data(cls, data):
        lights = cls()
        lights.__type__                           = 'Light'
        lights.name                               = data['name']
        lights.zone_name                          = data['zone_name']
        lights.schedule_name                      = data['schedule_name']
        lights.design_level_calculation_method    = data['design_level_calculation_method']
        lights.lighting_level                     = data['lighting_level']
        lights.watts_per_zone_floor_area          = data['watts_per_zone_floor_area']
        lights.watts_per_person                   = data['watts_per_person']
        lights.return_air_fraction                = data['return_air_fraction']
        lights.fraction_radiant                   = data['fraction_radiant']
        lights.fraction_visible                   = data['fraction_visible']
        lights.fraction_replaceable               = data['fraction_replaceable']
        lights.end_use_subcategory                = data['end_use_subcategory']
        return lights


class DaylightingControls(object):
    """
    Datastructure containing a DaylightingControls object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
        The name for the lights instance
    """
    def __init__(self):
        self.__type__                             = 'DaylightingControls'
        self.name                                 = None
        self.zone_name                            = None
        self.daylighting_method                   = None
        self.availability_schedule                = None
        self.lighting_control_type                = None
        self.min_input_power_fraction             = None
        self.min_light_output_fraction            = None
        self.num_stepped_control_steps            = None
        self.probability_lighting_reset           = None
        self.glare_reference_point                = None
        self.glare_azimut_angle                   = None
        self.max_allowable_discomfort_glare_index = None
        self.delight_gridding_resolution          = None
        self.reference_points                     = None


    @classmethod
    def from_data(cls, data):
        dc = cls()
        dc.__type__        = 'Light'
        dc.name                                 = data['name']
        dc.zone_name                            = data['zone_name']
        dc.daylighting_method                   = data['daylighting_method']
        dc.availability_schedule                = data['availability_schedule']
        dc.lighting_control_type                = data['lighting_control_type']
        dc.min_input_power_fraction             = data['min_input_power_fraction']
        dc.min_light_output_fraction            = data['min_light_output_fraction']
        dc.num_stepped_control_steps            = data['num_stepped_control_steps']
        dc.probability_lighting_reset           = data['probability_lighting_reset']
        dc.glare_reference_point                = data['glare_reference_point']
        dc.glare_azimut_angle                   = data['glare_azimut_angle']
        dc.max_allowable_discomfort_glare_index = data['max_allowable_discomfort_glare_index']
        dc.delight_gridding_resolution          = data['delight_gridding_resolution']
        dc.reference_points                     = data['reference_points']
        return dc


    @property
    def data(self):
        data = {}
        data['__type__']                                = self.__type__                            
        data['name']                                    = self.name                                
        data['zone_name']                               = self.zone_name                           
        data['daylighting_method']                      = self.daylighting_method                  
        data['availability_schedule']                   = self.availability_schedule               
        data['lighting_control_type']                   = self.lighting_control_type               
        data['min_input_power_fraction']                = self.min_input_power_fraction            
        data['min_light_output_fraction']               = self.min_light_output_fraction           
        data['num_stepped_control_steps']               = self.num_stepped_control_steps           
        data['probability_lighting_reset']              = self.probability_lighting_reset          
        data['glare_reference_point']                   = self.glare_reference_point               
        data['glare_azimut_angle']                      = self.glare_azimut_angle                  
        data['max_allowable_discomfort_glare_index']    = self.max_allowable_discomfort_glare_index
        data['delight_gridding_resolution']             = self.delight_gridding_resolution         
        data['reference_points']                        = self.reference_points                    
        return data


class DaylightingReferencePoint(object):
    """
    Datastructure containing a DaylightingReferencePoint object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
        The name for the lights instance
    """
    def __init__(self):
        self.__type__                           = 'DaylightingReferencePoint'
        self.name                               = None
        self.zone_name                          = None
        self.x                                  = None
        self.y                                  = None
        self.z                                  = None


    @classmethod
    def from_data(cls, data):
        drp = cls()
        drp.__type__        = 'Light'
        drp.name            = data['name']
        drp.zone_name       = data['zone_name']
        drp.x               = data['x']
        drp.y               = data['y']
        drp.z               = data['z']
        return drp












