from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

# import json
# from ast import literal_eval


class NodeList(object):
    """
    Datastructure containing an NodeList object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
    """
    def __init__(self):
        self.__type__         = 'NodeList'
        self.name             = None
        self.nodes            = None


    @classmethod
    def from_data(cls, data):
        zlst = cls()
        zlst.__type__         = 'NodeList'
        zlst.name             = data['name']
        zlst.nodes            = data['nodes']
        return zlst

    @property
    def data(self):
        data = {}
        data['__type__'] = self.__type__
        data['name']     = self.name    
        data['nodes']    = self.nodes   
        return data
