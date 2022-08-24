from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


__all__ = ['read_mean_zone_temperatures',
           'read_error_file',
          ]

def read_mean_zone_temperatures(building, filepath):
    """
    Reads mean zone air temperatures from an Energy+ result file. 

    Parameters
    ----------
    building: object
        The building object where results will be stored
    filepath: str
        Path to the energy+ result file
    
    Return
    ------
    dict
        The resulting air temperatures per time key and zone
    list, 
        A list of times for each temperature measurement. Each item is a list
        with the structure: of hour, day, month 
    
    """
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()
    temps = {}
    times = []
    num_zones = len(building.zones)
    num_intro = 9 + num_zones
    del lines[:num_intro]
    del lines[-2:]
    counter = 0
    for i in range(0, len(lines), num_zones + 1):
        temps[counter] = {}
        line = lines[i]
        time = line.split(',')
        for j in range(num_zones):
            line = lines[i + j + 1]
            _, temp = line.split(',')
            temps[counter][j] = float(temp)
        
        month = int(time[2])
        day = int(time[3])
        hour = int(time[5]) - 1
        times.append([hour, day, month])
        counter += 1
    mean_air_temperatures = temps
    result_times = times
    return mean_air_temperatures, result_times

def read_error_file(filepath, print_error=True):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()
    if print_error:
        print('#'*100)
        print('#'*100)
        print('Energy plus returned the following error(s) or warning(s)')
        print('#'*100)
        print('#'*100)
        print('')
        print('')
        for line in lines:
            print(line)
            # print('')
    return lines