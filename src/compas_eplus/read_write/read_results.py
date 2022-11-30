from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


__all__ = ['read_mean_zone_temperatures',
           'read_error_file',
           'read_eso_preamble',
           'read_results_file',
          ]


def read_results_file(building, filepath):
    pre_dict = read_eso_preamble(building, filepath)
    building.results = read_eso(building, filepath, pre_dict)


def read_eso(building, filepath, pre_dict):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    zones = [building.zones[zk].name for zk in building.zones] 

    print(zones)
    
    del lines[:9 + pre_dict['len_preamble']]
    del lines[-2:]

    data = {}
    for line in lines:
        line = line.split(',')
        key = line[0]
        if key == '2':
            month = int(line[2])
            day = int(line[3])
            hour = int(line[5]) - 1
            minutes = int(float(line[6]))
            time_key = '{}_{}_{}_{}'.format(minutes, hour, day, month)
            if time_key not in data:
                data[time_key] =  {zk:{} for zk in zones}
        else:
            zone = pre_dict[key]['zone']
            item = pre_dict[key]['item']
            value = float(line[1].strip())
            data[time_key][zone][item] = value
    return data


def read_eso_preamble(building, filepath):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    del lines[:7]
    del lines[-2:]

    data = {}
    len_preamble = 0
    for line in lines:
        line = line.strip()
        if line == 'End of Data Dictionary':
            break
        # print(line)
        len_preamble += 1
        stuff = line.split(',')
        key = stuff[0]
        zone = stuff[2].split(' ')[0].lower()
        item = stuff[3]
        if 'Cooling' in item:
            item = 'cooling'
        elif 'Heating' in item:
            item = 'heating'
        elif 'Lights' in item:
            item = 'lighting'
        elif 'Temperature' in item:
            item = 'mean_air_temperature'
        
        data[key] = {'zone': zone, 'item': item}
    data['len_preamble'] = len_preamble
    return data


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
    num_intro = 9 + (num_zones * 2)
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