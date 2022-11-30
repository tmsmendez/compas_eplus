import os
import compas_eplus
from compas_eplus.read_write import read_results_file
from compas_eplus.building import Building


for i in range(50): print('')

path = compas_eplus.TEMP
wea = compas_eplus.SEATTLE
b1 = Building(path, wea)
filepath = ''
results1 = read_results_file(b1, filepath)