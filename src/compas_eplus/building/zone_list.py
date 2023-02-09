from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

# import json
# from ast import literal_eval


class ZoneList(object):
    """
    Datastructure containing an ZoneList object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
    """
    def __init__(self):
        self.__type__         = 'ZoneList'
        self.name             = None
        self.zones            = None


    @classmethod
    def from_data(cls, data):
        zlst = cls()
        zlst.__type__         = 'ZoneList'
        zlst.name             = data['name']
        zlst.zones            = data['zones']
        return zlst