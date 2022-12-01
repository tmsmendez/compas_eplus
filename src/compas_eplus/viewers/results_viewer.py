from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd



class ResultsViewer(object):
    def __init__(self, building, building2=None):
        self.plot_type = 'line'
        self.timeframe = 'daily'
        self.building = building
        self.building2 = building2

    def show(self, result_type):
        data = {zk:{} for zk in self.building.zones}
        zones = [self.building.zones[zk].name for zk in self.building.zones] 
        counter = 0

        if self.timeframe == 'daily':
            results = {}
            # day = 0
            for key in self.building.results:
                _, h, d, m = key.split('_')
                tkey = '0_0_{}_{}'.format(d, m)
                if tkey not in results:
                    results[tkey] = {}
                for zone in self.building.results[key]:
                    if zone not in results[tkey]:
                        results[tkey][zone] = {'mean_air_temperature':0, 'heating': 0, 'cooling':0, 'lighting': 0}

                    results[tkey][zone]['heating'] += self.building.results[key][zone]['heating']
                    results[tkey][zone]['cooling'] += self.building.results[key][zone]['cooling']
                    results[tkey][zone]['lighting'] += self.building.results[key][zone]['lighting']
        else:
            results = self.building.results

        for key in results:
            _, h, d, m = key.split('_')
            time = datetime(2022, int(m), int(d), int(h))
            for zone in zones:
                data[counter] = {'zone': zone,
                                'mean_air_temperature': results[key][zone]['mean_air_temperature'],
                                'heating': results[key][zone]['heating'],
                                'cooling': results[key][zone]['cooling'],
                                'lighting': results[key][zone]['lighting'],
                                'time': time,
                                'day': d,
                                'hour': h,
                                'month': m,
                                }
                counter += 1

        df = pd.DataFrame.from_dict(data, orient='index')
        
        if self.plot_type == 'scatter':
            if len(self.building.zones) > 1:
                color_by = 'zone'
            else:
                color_by = result_type
            fig = px.scatter(df, x='time', y=result_type, hover_data={"time": "|%B %d, %H, %Y"}, color=color_by, size=None)
        elif self.plot_type == 'line':
            fig = px.line(df, x='time', y=result_type, hover_data={"time": "|%B %d, %H, %Y"}, color='zone')
        fig.update_xaxes(dtick="M1",tickformat="%b", ticklabelmode="period")
        fig.show()

    def compare(self, result_type):
        buildings = [self.building, self.building2]
        data = {}
        counter = 0
        for i, b in enumerate(buildings):
            zones = [self.building.zones[zk].name for zk in self.building.zones] 
            if self.timeframe == 'daily':
                results = {}
                # day = 0
                for key in b.results:
                    _, h, d, m = key.split('_')
                    tkey = '0_0_{}_{}'.format(d, m)
                    if tkey not in results:
                        results[tkey] = {}
                    for zone in b.results[key]:
                        if zone not in results[tkey]:
                            results[tkey][zone] = {'mean_air_temperature':0, 'heating': 0, 'cooling':0, 'lighting': 0}

                        results[tkey][zone]['heating'] += b.results[key][zone]['heating']
                        results[tkey][zone]['cooling'] += b.results[key][zone]['cooling']
                        results[tkey][zone]['lighting'] += b.results[key][zone]['lighting']
            else:
                results = b.results

            for key in results:
                _, h, d, m = key.split('_')
                time = datetime(2022, int(m), int(d), int(h))
                for zone in zones:
                    data[counter] = {'zone': '{}_{}_{}'.format(zone, b.name, i),
                                    'mean_air_temperature': results[key][zone]['mean_air_temperature'],
                                    'heating': results[key][zone]['heating'],
                                    'cooling': results[key][zone]['cooling'],
                                    'lighting': results[key][zone]['lighting'],
                                    'time': time,
                                    'day': d,
                                    'hour': h,
                                    'month': m,
                                    }
                    counter += 1

        df = pd.DataFrame.from_dict(data, orient='index')
        
        if self.plot_type == 'scatter':
            if len(self.building.zones) > 1:
                color_by = 'zone'
            else:
                color_by = result_type
            fig = px.scatter(df, x='time', y=result_type, hover_data={"time": "|%B %d, %H, %Y"}, color=color_by, size=None)
        elif self.plot_type == 'line':
            fig = px.line(df, x='time', y=result_type, hover_data={"time": "|%B %d, %H, %Y"}, color='zone')
        fig.update_xaxes(dtick="M1",tickformat="%b", ticklabelmode="period")
        fig.show()



if __name__ == '__main__':

    import os
    import compas_eplus
    from compas_eplus.read_write import read_results_file
    from compas_eplus.building import Building

    for i in range(50): print('')

    path = compas_eplus.TEMP
    wea = compas_eplus.SEATTLE
    b1 = Building.from_idf(os.path.join(compas_eplus.DATA, 'idf_examples', 'teresa_example.idf'), path, wea)
    filepath = os.path.join(compas_eplus.DATA, 'results', 'teresa.eso')
    read_results_file(b1, filepath)

    b2 = Building.from_idf(os.path.join(compas_eplus.DATA, 'idf_examples', 'teresa_example.idf'), path, wea)
    filepath = os.path.join(compas_eplus.DATA, 'results', 'counter_teresa.eso')
    read_results_file(b2, filepath)

    v = ResultsViewer(b1, b2)
    v.compare('cooling')