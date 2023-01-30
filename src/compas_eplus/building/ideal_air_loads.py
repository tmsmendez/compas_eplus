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
        self.__type__         = 'IdealAirLoad'


    

    @classmethod
    def from_data(cls, data):
        ial = cls()
        ial.__type__         = 'IdealAirLoad'
        return ial














