from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import json
from ast import literal_eval


class Construction(object):
    """
    Datastructure containing a construction for Energy+ analysis

    Parameters
    ----------
    name: str, optional
        The name for the construction instance
    layers: dict
        Dicitionary containing a name and thickness for each of the layersthat make up the construction
    
    """
    def __init__(self):
        self.name           = 'Construction'
        self.layers         = {}

    def to_json(self, filepath):
        """
        Serialize the data representation of the construction to a JSON file

        Parameters
        ----------
        filepath: str
            Path for the JSON file to be created
        
        Returns
        -------
        None

        """
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'name'      : self.name,
                'layers'    : self.layers,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.name   = data.get('name') or {}
        layers = data.get('layers') or {}

        for lk in layers:
            self.layers[literal_eval(lk)] = layers[lk]

    @classmethod
    def from_data(cls, data):
        """
        Create a new instance of the construction datastructure from a data dictionary

        Parameters
        ----------
        data: dict
            Data dictionary
        
        Returns
        -------
            Construction
                The instance of the construction datastructure
        
        """
        construction = cls()
        construction.data = data
        return construction

    @classmethod
    def from_json(cls, filepath):
        """
        Create a new instance of the construction datastructure from a JSON file

        Parameters
        ----------
        filepath: str
            Path to the JSON file
        
        Returns
        -------
            Construction
                The instance of the construction datastructure
        
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        construction = cls()
        construction.data = data
        return construction

if __name__ == '__main__':
    import compas_eplus
    import os

    for i in range(50): print('')

    c = Construction()
    name = 'Tomas Double Pane'
    layers = {0: {'name': 'Generic Low-e Glass', 'thickness':.006},
              1: {'name': 'Generic Window Air Gap', 'thickness':.0127},
              2: {'name': 'Generic Clear Glass', 'thickness':.006}}
    c.layers = layers
