from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

# import json
# from ast import literal_eval


class IdealAirLoad(object):
    """
    Datastructure containing an IdealAirLoad object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
    """
    def __init__(self):
        self.__type__                               = 'IdealAirLoad'
        self.name                                   = None
        self.availability_schedule_name             = None
        self.zone_supply_air_node_name              = None    
        self.zone_exhaust_air_node_name             = None
        self.system_inlet_air_node_name             = None
        self.max_heating_supply_temperature         = None
        self.min_cooling_supply_temperature         = None
        self.max_heating_supply_humidity_ratio      = None
        self.min_cooling_supply_humidity_ratio      = None
        self.heating_limit                          = None
        self.max_heating_air_flow_rate              = None    
        self.max_sensible_heating_capacity          = None
        self.cooling_limit                          = None    
        self.maximum_cooling_air_flow_rate          = None    
        self.maximum_total_cooling_capacity         = None
        self.heating_availability_schedule_name     = None    
        self.cooling_availability_schedule_name     = None    
        self.dehimidification_control_type          = None    
        self.cooling_sensible_heat_ratio            = None        
        self.humidification_control_type            = None    
        self.desing_specification_outdoor_air_name  = None        
        self.outdoor_inlet_node_name                = None    
        self.demand_controlled_ventilation_type     = None        
        self.outdoor_air_economizer_type            = None    
        self.heat_recovery_type                     = None    
        self.sensible_heat_recovery_effectiveness   = None        
        self.latent_heat_revovery_effectiveness     = None    


    

    @classmethod
    def from_data(cls, data):
        inr = cls()
        inr.__type__                                = 'IdealAirLoad'
        inr.name                                    = data['name']
        inr.availability_schedule_name              = data['availability_schedule_name']
        inr.zone_supply_air_node_name               = data['zone_supply_air_node_name']
        inr.zone_exhaust_air_node_name              = data['zone_exhaust_air_node_name']
        inr.system_inlet_air_node_name              = data['system_inlet_air_node_name']
        inr.max_heating_supply_temperature          = data['max_heating_supply_temperature']    
        inr.min_cooling_supply_temperature          = data['min_cooling_supply_temperature']    
        inr.max_heating_supply_humidity_ratio       = data['max_heating_supply_humidity_ratio']    
        inr.min_cooling_supply_humidity_ratio       = data['min_cooling_supply_humidity_ratio']    
        inr.heating_limit                           = data['heating_limit']    
        inr.max_heating_air_flow_rate               = data['max_heating_air_flow_rate']    
        inr.max_sensible_heating_capacity           = data['max_sensible_heating_capacity']    
        inr.cooling_limit                           = data['cooling_limit']
        inr.maximum_cooling_air_flow_rate           = data['maximum_cooling_air_flow_rate']    
        inr.maximum_total_cooling_capacity          = data['maximum_total_cooling_capacity']    
        inr.heating_availability_schedule_name      = data['heating_availability_schedule_name']    
        inr.cooling_availability_schedule_name      = data['cooling_availability_schedule_name']        
        inr.dehimidification_control_type           = data['dehimidification_control_type']    
        inr.cooling_sensible_heat_ratio             = data['cooling_sensible_heat_ratio']    
        inr.humidification_control_type             = data['humidification_control_type']    
        inr.desing_specification_outdoor_air_name   = data['desing_specification_outdoor_air_name']        
        inr.outdoor_inlet_node_name                 = data['outdoor_inlet_node_name']    
        inr.demand_controlled_ventilation_type      = data['demand_controlled_ventilation_type']        
        inr.outdoor_air_economizer_type             = data['outdoor_air_economizer_type']    
        inr.heat_recovery_type                      = data['heat_recovery_type']        
        inr.sensible_heat_recovery_effectiveness    = data['sensible_heat_recovery_effectiveness']        
        inr.latent_heat_revovery_effectiveness      = data['latent_heat_revovery_effectiveness']        
        return inr














