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
    """
    def __init__(self):
        self.__type__                           = 'EquipmentList'

    

    @classmethod
    def from_data(cls, data):
        eeq = cls()
        eeq.__type__                           = 'EquipmentList'
        return eeq









