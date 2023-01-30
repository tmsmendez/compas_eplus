from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

# import json
# from ast import literal_eval


class DualSetpoint(object):
    """
    Datastructure containing an DualSetpoint object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
    """
    def __init__(self):
        self.__type__         = 'DualSetpoint'
        self.name             = None
        self.heating_setpoint = None
        self.cooling_setpoint = None


    

    @classmethod
    def from_data(cls, data):
        dsp = cls()
        dsp.__type__         = 'DualSetpoint'
        dsp.name             = data['name']
        dsp.heating_setpoint = data['heating_setpoint']
        dsp.cooling_setpoint = data['cooling_setpoint']
        return dsp














