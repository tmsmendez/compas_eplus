from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

# import json
# from ast import literal_eval


class Infiltration(object):
    """
    Datastructure containing an Infiltration object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
    """
    def __init__(self):
        self.__type__                               = 'Infiltration'
        self.name                                   = None
        self.zone_name                              = None
        self.schedule_name                          = None
        self.design_flow_rate_calculation_method    = None
        self.design_flow_rate                       = None
        self.flow_per_zone_floor_area               = None    
        self.flow_per_exterior_area                 = None    
        self.air_changes_per_hour                   = None    
        self.constant_term_coefficient              = None        
        self.temperature_term_coefficient           = None    
        self.velocity_term_coefficient              = None    
        self.velocity_squared_term_coefficient      = None        

    

    @classmethod
    def from_data(cls, data):
        infiltration = cls()
        infiltration.__type__                                = 'Infiltration'
        infiltration.name                                    = data['name']
        infiltration.zone_name                               = data['zone_name']    
        infiltration.schedule_name                           = data['schedule_name']
        infiltration.design_flow_rate_calculation_method     = data['design_flow_rate_calculation_method']    
        infiltration.design_flow_rate                        = data['design_flow_rate']    
        infiltration.flow_per_zone_floor_area                = data['flow_per_zone_floor_area']    
        infiltration.flow_per_exterior_area                  = data['flow_per_exterior_area']
        infiltration.air_changes_per_hour                    = data['air_changes_per_hour']    
        infiltration.constant_term_coefficient               = data['constant_term_coefficient']    
        infiltration.temperature_term_coefficient            = data['temperature_term_coefficient']    
        infiltration.velocity_term_coefficient               = data['velocity_term_coefficient']    
        infiltration.velocity_squared_term_coefficient       = data['velocity_squared_term_coefficient']    
        return infiltration














