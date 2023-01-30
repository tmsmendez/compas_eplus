from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

# import json
# from ast import literal_eval


class ZoneControlThermostat(object):
    """
    Datastructure containing an ZoneControlThermostat object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
    """
    def __init__(self):
        self.__type__                           = 'ZoneControlThermostat'
        self.name                               = None
        self.zone_name                          = None
        self.schedule_name                      = None
        self.control1_object_type               = None
        self.control1_object_name               = None
        self.control2_object_type               = None
        self.control2_object_name               = None
        self.control3_object_type               = None
        self.control3_object_name               = None
        self.control4_object_type               = None
        self.control4_object_name               = None
        self.temperature_difference             = None

    

    @classmethod
    def from_data(cls, data):
        zct = cls()
        zct.__type__               = 'ZoneControlThermostat'
        zct.name                   = data['name']
        zct.zone_name              = data['zone_name']
        zct.schedule_name          = data['schedule_name']
        zct.control1_object_type   = data['control1_object_type']
        zct.control1_object_name   = data['control1_object_name']
        zct.control2_object_type   = data['control2_object_type']
        zct.control2_object_name   = data['control2_object_name']
        zct.control3_object_type   = data['control3_object_type']
        zct.control3_object_name   = data['control3_object_name']
        zct.control4_object_type   = data['control4_object_type']
        zct.control4_object_name   = data['control4_object_name']
        zct.temperature_difference = data['temperature_difference']
        return zct














