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
        self.type                   = None
        self.type_limits            = ''
        self.weekday                = {}
        self.weekend                = {}
        self.alldays                = {}
        self.summer_design_day      = {}
        self.winter_design_day      = {}

    @classmethod
    def from_idf_data(cls, data):
        name = data['name']
        schedule = cls(name)
        schedule.type = data['__type__']

        if schedule.type == 'compact':
            schedule.type_limits = data['schedule_type_limits']
            schedule.through = data['through']
            schedule.for_ = data['for']
            schedule.until = data['until']
            schedule.value = data['value']

        elif schedule.type == 'day_interval':
            schedule.type_limits = data['schedule_type_limits']
            schedule.interpolate_timestep =  data['interpolate_timestep']
            schedule.time_values = data['time_values']

        elif schedule.type == 'week_daily':
            schedule.sunday             = data['sunday']      
            schedule.monday             = data['monday']      
            schedule.tuesday            = data['tuesday']      
            schedule.wednesday          = data['wednesday']      
            schedule.thursday           = data['thursday']      
            schedule.friday             = data['friday']  
            schedule.saturday           = data['saturday']      
            schedule.holiday            = data['holiday']          
            schedule.summer_design_day  = data['summer_design_day']          
            schedule.winter_design_day  = data['winter_design_day']          
            schedule.custom_day1        = data['custom_day1']              
            schedule.custom_day2        = data['custom_day2']              

        elif schedule.type == 'year':
            schedule.type_limits = data['schedule_type_limits']
            schedule.schedule_week_name1 = data['schedule_week_name1']
            schedule.start_month_1 = data['start_month_1']
            schedule.start_day1 = data['start_day1']
            schedule.end_month1 = data['end_month1']
            schedule.end_day1 = data['end_dat1']

        elif schedule.type == 'schedule_type_limits':
            schedule.lower_limit = data['lower_limit']
            schedule.upper_limit = data['upper_limit']
            schedule.numeric_type = data['numeric_type']
            schedule.unit_type = data['unit_type']
        else:
            print('The {} schedule type has not been implemented'.format(data['__type__']))

        return schedule


class OfficeOccupancySchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type = 'compact'
        self.type_limits =  'Fraction'
        self.weekdays =  {8: 0., 11:1., 12: .8, 13: .4, 14: .8, 18: 1., 19: .5, 24: 0.}
        self.weekends = {24: .3}


class OfficeLightsSchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type = 'compact'
        self.type_limits =  'Fraction'
        self.weekdays =  {8: 0., 11:1., 12: .8, 13: .4, 14: .8, 18: 1., 19: .5, 24: 0.}
        self.weekends = {24: .3}


class OfficeEquipmentSchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type = 'compact'
        self.type_limits =  'Fraction'
        self.weekdays =  {8: 0., 11:1., 12: .8, 13: .4, 14: .8, 18: 1., 19: .5, 24: 0.}
        self.weekends = {24: .3}


class OfficeActivitySchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type = 'compact'
        self.type_limits =  'Any number'
        self.alldays = {24: 120}


class OfficeControlTypeSchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type = 'compact'
        self.type_limits =  'Control Type'
        self.alldays = {24: 4}


class OfficeHeatingSchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type = 'compact'
        self.type_limits =  'Temperature'
        self.weekdays = {6: 16.7, 20: 22.2, 24: 16.7}
        self.weekends = {24: 16.7}
        self.alldays = {24: 16.7}
        self.summer_design_day = {24: 16.7}
        self.winter_design_day = {24: 22.2}


class OfficeCoolingSchedule(Schedule):
    def __init__(self, name):
        Schedule.__init__(self, name=name)
        self.type = 'compact'
        self.type_limits =  'Temperature'
        self.weekdays = {6: 29.4, 20: 23.9, 24: 29.4}
        self.weekends = {24: 29.4}
        self.alldays = {24: 29.4}
        self.summer_design_day = {24: 23.9}
        self.winter_design_day = {24: 29.4}
