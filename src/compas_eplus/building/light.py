from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import json
from ast import literal_eval


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
        self.__type__                           = 'Lights'
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
        lights.__type__                           = 'Lights'
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














