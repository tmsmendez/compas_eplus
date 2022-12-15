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
            zks = [zk for zk in self.building.zones] 
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
                for j, zone in enumerate(zones):
                    heat = results[key][zone]['heating'] * self.multiplier[self.eui_units]
                    cool = results[key][zone]['cooling'] * self.multiplier[self.eui_units]
                    light = results[key][zone]['lighting'] * self.multiplier[self.eui_units]
                    if self.area_normalize:
                        heat /= self.building.zones[zks[j]].area
                        cool /= self.building.zones[zks[j]].area
                        light /= self.building.zones[zks[j]].area

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



# def plot_eui_map(building):
#     x = np.arange(0, 365, 1)
#     y = np.arange(0, 24, 1)
#     num_zones = len(building.eui_kwh_hourly)
    
    
#     plt.rcParams['font.size'] = '8'
#     cmap = plt.get_cmap('bwr')
#     fig, axes = plt.subplots(num_zones, 1)
    
#     zkeys = [building.zones[i] for i in range(len(building.eui_kwh_hourly))]
#     maxcool = [max(building.eui_kwh_hourly[zkey]['cooling']) for zkey in zkeys]
#     maxheat = [max(building.eui_kwh_hourly[zkey]['heating']) for zkey in zkeys]
#     vmax = max(max(maxcool), max(maxheat))

#     for i, zkey in enumerate(zkeys):
#         ax = axes[i]
#         data = building.eui_kwh_hourly[zkey]['heating']
#         z = np.array(data)
#         z = z.reshape(365, 24)

#         data = building.eui_kwh_hourly[zkey]['cooling']
#         z_ = np.array(data)
#         z_ = z_.reshape(365, 24) * -1
#         z += z_
#         z = z.transpose()

#         norm = None
#         im = ax.pcolormesh(x, y, z, cmap=cmap, norm=norm, shading='auto', vmin=vmax * -1, vmax=vmax)
#         ax.set_title('{}'.format(zkey), fontsize='medium')

#     fig.suptitle('{} - {} EUI'.format(building.simulation_name, building.city), fontsize=16)
#     fig.subplots_adjust(right=.86)
#     cbar_ax = fig.add_axes([.9, .01, .01, .9])
#     cbar = fig.colorbar(im, cax=cbar_ax)
#     cbar.set_label('EUI (kWh)', rotation=0)

#     ticks = cbar.get_ticks().tolist()
#     ticks = [abs(t) for t in ticks]
#     ticks[0] = '{} Cooling'.format(str(ticks[0]))
#     ticks[-1] = '{} Heating'.format(str(ticks[-1]))
#     cbar.ax.set_yticklabels(ticks)

#     plt.show()



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

    v = ResultsViewer(b1, b2, eui_units='kWh')
    v.compare('total')