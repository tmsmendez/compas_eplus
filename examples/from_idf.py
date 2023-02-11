import os
import compas_eplus
from compas_eplus.building import Building
from compas_eplus.viewers import BuildingViewer
from compas_eplus.viewers import ResultsViewer

for i in range(50): print('')

file = 'teresa_example_apt.idf'
filepath = os.path.join(compas_eplus.DATA, 'idf_examples', file)
path = compas_eplus.TEMP
wea = compas_eplus.SEATTLE
b = Building.from_idf(filepath, path, wea)

b.write_idf()
b.analyze(exe='/Applications/EnergyPlus/energyplus')
b.load_results()
# v = BuildingViewer(b)
# v.show()

v = ResultsViewer(b)
v.show('total')