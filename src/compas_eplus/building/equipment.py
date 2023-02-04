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



# ZoneHVAC:EquipmentList,
#   2_residential_aa024cf2 Equipment List,          !- Name
#   SequentialLoad,                                 !- Load Distribution Scheme
#   ZoneHVAC:IdealLoadsAirSystem,                   !- Zone Equipment Object Type 1
#   2_residential_aa024cf2 Ideal Loads Air System,  !- Zone Equipment Name 1
#   1,                                              !- Zone Equipment Cooling Sequence 1
#   1,                                              !- Zone Equipment Heating or No-Load Sequence 1
#   ,                                               !- Zone Equipment Sequential Cooling Fraction Schedule Name 1
#   ;                                               !- Zone Equipment Sequential Heating Fraction Schedule Name 1




# ZoneHVAC:EquipmentConnections,
#   2_residential_aa024cf2,                     !- Zone Name
#   2_residential_aa024cf2 Equipment List,      !- Zone Conditioning Equipment List Name
#   2_residential_aa024cf2 Inlet Node List,     !- Zone Air Inlet Node or NodeList Name
#   2_residential_aa024cf2 Exhaust Node List,   !- Zone Air Exhaust Node or NodeList Name
#   Node 2;                                     !- Zone Air Node Name






