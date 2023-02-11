from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

# import json
# from ast import literal_eval


class EquipmentList(object):
    """
    Datastructure containing an ElectricEquipment object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
    load_distribution_scheme
    zone_equipment_object_type1
    zone_equipment_name1
    zone_equipment_cooling_sequence
    zone_equipment_heating_sequence
    zone_equipment_sequenctial_cooling_fraction_schedule
    zone_equipment_sequential_heating_fraction_schedule
    """
    def __init__(self):
        self.__type__                                              = 'EquipmentList'
        self.name                                                  = None
        self.load_distribution_scheme                              = None
        self.zone_equipment_object_type1                           = None
        self.zone_equipment_name1                                  = None
        self.zone_equipment_cooling_sequence                       = None
        self.zone_equipment_heating_sequence                       = None
        self.zone_equipment_sequenctial_cooling_fraction_schedule  = None
        self.zone_equipment_sequential_heating_fraction_schedule   = None

    @classmethod
    def from_data(cls, data):
        eql = cls()
        eql.__type__                                                = 'EquipmentList'
        eql.name                                                    = data['name']
        eql.load_distribution_scheme                                = data['load_distribution_scheme']
        eql.zone_equipment_object_type1                             = data['zone_equipment_object_type1']
        eql.zone_equipment_name1                                    = data['zone_equipment_name1']
        eql.zone_equipment_cooling_sequence                         = data['zone_equipment_cooling_sequence']
        eql.zone_equipment_heating_sequence                         = data['zone_equipment_heating_sequence']
        eql.zone_equipment_sequenctial_cooling_fraction_schedule    = data['zone_equipment_sequenctial_cooling_fraction_schedule']
        eql.zone_equipment_sequential_heating_fraction_schedule     = data['zone_equipment_sequential_heating_fraction_schedule']
        return eql

    @property
    def data(self):
        data = {}
        data['__type__'] = self.__type__                                            
        data['name'] = self.name                                                
        data['load_distribution_scheme'] = self.load_distribution_scheme                            
        data['zone_equipment_object_type1'] = self.zone_equipment_object_type1                         
        data['zone_equipment_name1'] = self.zone_equipment_name1                                
        data['zone_equipment_cooling_sequence'] = self.zone_equipment_cooling_sequence                     
        data['zone_equipment_heating_sequence'] = self.zone_equipment_heating_sequence                     
        data['zone_equipment_sequenctial_cooling_fraction_schedule'] = self.zone_equipment_sequenctial_cooling_fraction_schedule
        data['zone_equipment_sequential_heating_fraction_schedule'] = self.zone_equipment_sequential_heating_fraction_schedule 
        return data

class EquipmentConnection(object):
    """
    Datastructure containing an EquipmentConnection object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
    """
    def __init__(self):
        self.__type__                           = 'EquipmentConnection'
        self.name                               = None
        self.name                               = None
        self.zone_conditioning_equipment_list   = None
        self.zone_air_inlet_node                = None
        self.zone_air_exhaust_node              = None
        self.zone_air_node                      = None

    @classmethod
    def from_data(cls, data):
        eqc = cls()
        eqc.__type__                            = 'EquipmentConnection'
        eqc.name                                = data['name']
        eqc.zone_conditioning_equipment_list    = data['zone_conditioning_equipment_list']
        eqc.zone_air_inlet_node                 = data['zone_air_inlet_node']
        eqc.zone_air_exhaust_node               = data['zone_air_exhaust_node']
        eqc.zone_air_node                       = data['zone_air_node']
        return eqc

    @property
    def data(self):
        data = {}
        data['__type__'] = self.__type__                        
        data['name'] = self.name                            
        data['name'] = self.name                            
        data['zone_conditioning_equipment_list'] = self.zone_conditioning_equipment_list
        data['zone_air_inlet_node'] = self.zone_air_inlet_node             
        data['zone_air_exhaust_node'] = self.zone_air_exhaust_node           
        data['zone_air_node'] = self.zone_air_node                   
        return data



