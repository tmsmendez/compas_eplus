from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import json
from ast import literal_eval

# TODO: To and from json?

class Schedule(object):
    """
    Datastructure containing a schedule for Energy+ analysis

    Parameters
    ----------
    name: str, optional
        The name for the schedule instance

    
    """
    def __init__(self, name):
        self.name                   = name
        self.type_limits            = ''
        self.weekday                = {}
        self.weekend                = {}
        self.alldays                = {}
        self.summer_design_day      = {}
        self.winter_design_day      = {}


class OfficeOccupancySchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type_limits =  'Fraction'
        self.weekdays =  {8: 0., 11:1., 12: .8, 13: .4, 14: .8, 18: 1., 19: .5, 24: 0.}
        self.weekends = {24: .3}


class OfficeLightsSchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type_limits =  'Fraction'
        self.weekdays =  {8: 0., 11:1., 12: .8, 13: .4, 14: .8, 18: 1., 19: .5, 24: 0.}
        self.weekends = {24: .3}


class OfficeEquipmentSchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type_limits =  'Fraction'
        self.weekdays =  {8: 0., 11:1., 12: .8, 13: .4, 14: .8, 18: 1., 19: .5, 24: 0.}
        self.weekends = {24: .3}


class OfficeActivitySchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type_limits =  'Any number'
        self.alldays = {24: 120}


class OfficeControlTypeSchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type_limits =  'Control Type'
        self.alldays = {24: 4}


class OfficeHeatingSchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type_limits =  'Temperature'
        self.weekdays = {6: 16.7, 20: 22.2, 24: 16.7}
        self.weekends = {24: 16.7}
        self.alldays = {24: 16.7}
        self.summer_design_day = {24: 16.7}
        self.winter_design_day = {24: 22.2}


class OfficeCoolingSchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type_limits =  'Temperature'
        self.weekdays = {6: 29.4, 20: 23.9, 24: 29.4}
        self.weekends = {24: 29.4}
        self.alldays = {24: 29.4}
        self.summer_design_day = {24: 23.9}
        self.winter_design_day = {24: 29.4}
