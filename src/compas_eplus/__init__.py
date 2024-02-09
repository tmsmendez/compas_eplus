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
import subprocess


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
ATLANTA = os.path.abspath(os.path.join(root, 'data', 'weather_files', 'USA_GA_Atlanta-Hartsfield-Jackson.Intl.AP.722190_TMY3.epw'))
MILWAUKEE = os.path.abspath(os.path.join(root, 'data', 'weather_files', 'USA_WI_Milwaukee-Mitchell.Intl.AP.726400_TMY3.epw'))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]


def run_idf(idf, name, weather_file, output_path, exe=None, delete=True):
    from compas_eplus.read_write import read_error_file
    from compas_eplus.read_write import read_results_file
    from compas_eplus.building import Building
    if not exe:
        exe = 'energyplus'
    out = os.path.join(output_path, '{}_eplus_out'.format(name))

    if delete:
        try:
            shutil.rmtree(out)
        except:
            pass

    print(exe, '-w', weather_file,'--output-directory', out, idf)
    subprocess.call([exe, '-w', weather_file,'--output-directory', out, idf])


    filepath = os.path.join(out, 'eplusout.eso')
    error_filepath = os.path.join(out, 'eplusout.err')
    read_error_file(error_filepath, print_error=True)
    for i in range(5): print('')

    path = os.path.dirname(idf)
    building = Building(path, weather_file, name=name)
    read_results_file(building, filepath)

    tko = list(building.results.keys())[0]
    zones = building.results[tko].keys()
    print(zones)

    # zones = [self.zones[zk].name for zk in self.zones]
    # totals = {'heating': 0, 'cooling':0, 'lighting': 0}
    # for zone in zones:
    #     heat = [self.results[tk][zone]['heating'] for tk in self.results]
    #     heat = sum(heat)
    #     totals['heating'] += heat

    #     cool = [self.results[tk][zone]['cooling'] for tk in self.results]
    #     cool = sum(cool)
    #     totals['cooling'] += cool

    #     light = [self.results[tk][zone]['lighting'] for tk in self.results]
    #     light = sum(light)
    #     totals['lighting'] += light
        
    #     self.totals[zone] = {'heating': heat,
    #                             'cooling': cool,
    #                             'lighting': light
    #                         }
    # totals['total'] = totals['heating'] + totals['cooling'] + totals['lighting']
    # self.totals['totals'] = totals
