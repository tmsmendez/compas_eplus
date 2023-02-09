from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

# import json
# from ast import literal_eval


class OutdoorAir(object):
    """
    Datastructure containing an OutdoorAir object for Energy+ analysis

    Parameters
    ----------
    name: str, 
    outdoor_air_method                   
    outdoor_air_flow_per_person          
    outdoor_air_flow_zone_area           
    outdoor_air_zone                     
    outdoor_air_flow_air_changes_per_hour
    """
    def __init__(self):
        self.__type__                               = 'OutdoorAir'
        self.name                                   = None
        self.outdoor_air_method                     = None
        self.outdoor_air_flow_per_person            = None         
        self.outdoor_air_flow_zone_area             = None
        self.outdoor_air_zone                       = None
        self.outdoor_air_flow_air_changes_per_hour  = None

    @classmethod
    def from_data(cls, data):
        oa = cls()
        oa.__type__                              = 'OutdoorAir'
        oa.name                                  = data['name']
        oa.outdoor_air_method                    = data['outdoor_air_method']
        oa.outdoor_air_flow_per_person           = data['outdoor_air_flow_per_person']
        oa.outdoor_air_flow_zone_area            = data['outdoor_air_flow_zone_area']
        oa.outdoor_air_zone                      = data['outdoor_air_zone']
        oa.outdoor_air_flow_air_changes_per_hour = data['outdoor_air_flow_air_changes_per_hour']
        return oa