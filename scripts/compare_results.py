import os
import compas_eplus
from compas_eplus.read_write import read_results_file
from compas_eplus.building import Building
from compas_eplus.viewers import ResultsViewer
from compas_eplus.viewers import BuildingViewer

import os
import compas_eplus
from compas_eplus.read_write import read_results_file
from compas_eplus.building import Building

for i in range(50): print('')

path = compas_eplus.TEMP
wea = compas_eplus.SEATTLE
b1 = Building.from_idf(os.path.join(compas_eplus.DATA, 'idf_examples', 'teresa_example_apt.idf'), path, wea)
filepath = os.path.join(compas_eplus.DATA, 'results', 'teresa_apt.eso')
read_results_file(b1, filepath)

b2 = Building.from_idf(os.path.join(compas_eplus.DATA, 'idf_examples', 'teresa_example_apt.idf'), path, wea)
# b2 = Building.from_idf(os.path.join(compas_eplus.TEMP, 'Building.idf'), path, wea)
filepath = os.path.join(compas_eplus.TEMP, 'eplus_output', 'eplusout.eso')
read_results_file(b2, filepath)

v = ResultsViewer(b1, b2)
v.compare('cooling')

# v = BuildingViewer(b1)
# v.show()



"""
Homework
--------

Complex
- Read and apply schedules from IDF
- Make sure set-points are imported from IDF too
- Try to implement model where zones have different programs

Easy
- Make the comparison tool plot the delta between two data sets
- Make EUI map plot

"""