from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

# import json
# from ast import literal_eval


class People(object):
    """
    Datastructure containing a people object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
    zone_name
    schedule_name
    calculation_method
    number_of_people
    people_per_floor_area
    floor_area_per_person
    fraction_radiant
    sensible_heat_fraction
    activity_level_schedule_name
    """
    def __init__(self):
        self.__type__                           = 'People'
        self.name                               = None
        self.zone_name                          = None
        self.schedule_name                      = None
        self.calculation_method                 = None
        self.number_of_people                   = None
        self.people_per_floor_area              = None
        self.floor_area_per_person              = None
        self.fraction_radiant                   = None
        self.sensible_heat_fraction             = None
        self.activity_level_schedule_name       = None
    

    @classmethod
    def from_data(cls, data):
        people = cls()
        people.__type__                           = 'People'
        people.name                              = data['name']   
        people.zone_name                         = data['zone_name']   
        people.schedule_name                     = data['schedule_name']   
        people.calculation_method                = data['calculation_method']   
        people.number_of_people                  = data['number_of_people']   
        people.people_per_floor_area             = data['people_per_floor_area']   
        people.floor_area_per_person             = data['floor_area_per_person']   
        people.fraction_radiant                  = data['fraction_radiant']   
        people.sensible_heat_fraction            = data['sensible_heat_fraction']   
        people.activity_level_schedule_name      = data['activity_level_schedule_name']   
        return people














