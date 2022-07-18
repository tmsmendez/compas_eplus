"""
********************************************************************************
compas_eplus
********************************************************************************

.. currentmodule:: compas_eplus


.. toctree::
    :maxdepth: 1


"""

from __future__ import print_function

import os


__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

# Weather files - - -
root = os.path.join(HERE, '../../')
SEATTLE = os.path.abspath(os.path.join(root, 'data', 'weather_files', 'USA_WA_Seattle-Tacoma.Intl.AP.727930_TMY3.epw'))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]
