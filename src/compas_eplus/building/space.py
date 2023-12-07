from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

# import json
# from ast import literal_eval


class Space(object):
    """
    Datastructure containing an Space object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
    """
    def __init__(self):
        self.__type__           = 'Space'
        self.name               = None
        self.zone_name          = None
        self.height             = None
        self.volume             = None
        self.floor_area         = None
        self.space_type         = None    

    @classmethod
    def from_data(cls, data):
        sp = cls()
        sp.__type__            = 'Space'
        sp.name                = data['name']
        sp.zone_name           = data['zone_name']
        sp.height              = data['height']
        sp.volume              = data['volume']
        sp.floor_area          = data['floor_area']
        sp.space_type          = data['space_type']
        return sp


class SpaceList(object):
    """
    Datastructure containing an ZoneList object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
    """
    def __init__(self):
        self.__type__         = 'SpaceList'
        self.name             = None
        self.spaces            = None


    @classmethod
    def from_data(cls, data):
        slst = cls()
        slst.__type__         = 'SpaceList'
        slst.name             = data['name']
        slst.spaces           = data['spaces']
        return slst













