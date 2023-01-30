from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

# import json
# from ast import literal_eval


class ElectricEquipment(object):
    """
    Datastructure containing an ElectricEquipment object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
    """
    def __init__(self):
        self.__type__                           = 'ElectricEquipment'
        self.name                               = None
        self.zone_name                          = None
        self.schedule_name                      = None
        self.calculation_method                 = None
        self.design_level                       = None
        self.watts_per_zone_floor_area          = None    
        self.watts_per_person                   = None
        self.fraction_latent                    = None
        self.fraction_radiant                   = None
        self.fraction_lost                      = None
        self.end_use_subcategory                = None

    

    @classmethod
    def from_data(cls, data):
        eeq = cls()
        eeq.__type__                           = 'ElectricEquipment'
        eeq.name                               = data['name']
        eeq.zone_name                          = data['zone_name']
        eeq.schedule_name                      = data['schedule_name']    
        eeq.calculation_method                 = data['calculation_method']
        eeq.design_level                       = data['design_level']    
        eeq.watts_per_zone_floor_area          = data['watts_per_zone_floor_area']    
        eeq.watts_per_person                   = data['watts_per_person']    
        eeq.fraction_latent                    = data['fraction_latent']    
        eeq.fraction_radiant                   = data['fraction_radiant']    
        eeq.fraction_lost                      = data['fraction_lost']    
        eeq.end_use_subcategory                = data['end_use_subcategory']
        return eeq














