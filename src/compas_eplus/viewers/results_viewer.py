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
    def __init__(self, building, building2=None, eui_units='kWh'):
        self.plot_type = 'line'
        self.timeframe = 'daily'
        self.building = building
        self.building2 = building2
        self.eui_units = eui_units  # 'kWh', 'kBtu', 'J'
        self.area_units = 'm2'
        self.multiplier = {'Btu': 0.000947817, 'J': 1, 'kWh': 2.77778e-7, 'kBtu': 9.47817e-7}
        self.area_normalize = True
        self.df = None

    def show(self, result_type):
        data = {zk:{} for zk in self.building.zones}
        zks = [zk for zk in self.building.zones] 
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
            for i, zone in enumerate(zones):
                heat = results[key][zone]['heating'] * self.multiplier[self.eui_units]
                cool = results[key][zone]['cooling'] * self.multiplier[self.eui_units]
                light = results[key][zone]['lighting'] * self.multiplier[self.eui_units]

                if self.area_normalize:
                    heat /= self.building.zones[zks[i]].area
                    cool /= self.building.zones[zks[i]].area
                    light /= self.building.zones[zks[i]].area

                data[counter] = {'zone': zone,
                                'mean_air_temperature': results[key][zone]['mean_air_temperature'],
                                'heating': heat,
                                'cooling': cool,
                                'lighting':light,
                                'total': heat + cool + light,
                                'time': time,
                                'day': d,
                                'hour': h,
                                'month': m,
                                }
                counter += 1

        self.df = pd.DataFrame.from_dict(data, orient='index')
        self.plot(result_type)
        
    def compare(self, result_type):
        buildings = [self.building, self.building2]
        data = {}
        counter = 0
        for i, b in enumerate(buildings):
            zks = [zk for zk in b.zones] 
            zones = [b.zones[zk].name for zk in b.zones] 
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
                for j, zone in enumerate(zones):
                    heat = results[key][zone]['heating'] * self.multiplier[self.eui_units]
                    cool = results[key][zone]['cooling'] * self.multiplier[self.eui_units]
                    light = results[key][zone]['lighting'] * self.multiplier[self.eui_units]
                    if self.area_normalize:
                        heat /= b.zones[zks[j]].area
                        cool /= b.zones[zks[j]].area
                        light /= b.zones[zks[j]].area

                    data[counter] = {'zone': '{}_{}_{}'.format(zone, b.name, i),
                                     'mean_air_temperature': results[key][zone]['mean_air_temperature'],
                                     'heating': heat,
                                     'cooling': cool,
                                     'lighting':light,
                                     'total': heat + cool + light,
                                     'time': time,
                                     'day': d,
                                     'hour': h,
                                     'month': m,
                                     }
                    counter += 1

        self.df = pd.DataFrame.from_dict(data, orient='index')
        self.plot(result_type)
        
    def plot(self, result_type):
        if self.plot_type == 'scatter':
            if len(self.building.zones) > 1:
                color_by = 'zone'
            else:
                color_by = result_type
            fig = px.scatter(self.df, x='time', y=result_type, hover_data={"time": "|%B %d, %H, %Y"}, color=color_by, size=None)
        elif self.plot_type == 'line':
            fig = px.line(self.df, x='time', y=result_type, hover_data={"time": "|%B %d, %H, %Y"}, color='zone')
        fig.update_xaxes(dtick="M1",tickformat="%b", ticklabelmode="period")
        if self.area_normalize:
            fig.update_yaxes(title='{} EUI ({}/{})'.format(result_type, self.eui_units, self.area_units))
        else:
            fig.update_yaxes(title='{} EUI ({})'.format(result_type, self.eui_units))
        fig.show()

class HeatMapResultsViewer(object):
    def __init__(self, building):
        self.building = building

    def plot(self):

        import plotly.graph_objects as go
        import datetime
        import numpy as np
        np.random.seed(1)

        programmers = ['Alex','Nicole','Sara','Etienne','Chelsea','Jody','Marianne']

        base = datetime.datetime.today()
        dates = base - np.arange(180) * datetime.timedelta(days=1)
        z = np.random.poisson(size=(len(programmers), len(dates)))

        fig = go.Figure(data=go.Heatmap(
                z=z,
                x=dates,
                y=programmers,
                colorscale='Viridis'))

        fig.update_layout(
            title='GitHub commits per day',
            xaxis_nticks=36)

        fig.show()




if __name__ == '__main__':

    import os
    import compas_eplus
    from compas_eplus.read_write import read_results_file
    from compas_eplus.building import Building
    from compas_eplus.viewers import BuildingViewer

    for i in range(50): print('')

    # file = 'doe_midrise_apt.idf'
    file = 'teresa_example.idf'
    filepath = os.path.join(compas_eplus.DATA, 'idf_examples', file)
    path = compas_eplus.TEMP
    wea = compas_eplus.SEATTLE
    b = Building.from_idf(filepath, path, wea)


    v = BuildingViewer(b)
    v.show()

    b.write_idf()
    b.analyze(exe='/Applications/EnergyPlus/energyplus')
    b.load_results()

    v = ResultsViewer(b)
    v.show('total')