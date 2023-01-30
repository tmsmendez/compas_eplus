from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import json
from ast import literal_eval


class Lights(object):
    """
    Datastructure containing a lights object for Energy+ analysis

    Parameters
    ----------
    name: str, optional
        The name for the lights instance
    
    """
    def __init__(self):
        self.name           = 'Construction'
        self.layers         = {}