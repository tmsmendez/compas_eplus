import os
import compas_eplus
from compas_eplus.building import Building
from compas_eplus.viewers import BuildingViewer
from compas_eplus.viewers import ResultsViewer

for i in range(50): print('')

file = 'in.idf'
filepath = os.path.join(compas_eplus.DATA, 'idf_examples', file)
path = compas_eplus.TEMP
wea = compas_eplus.SEATTLE
b = Building.from_idf(filepath, path, wea)

# v = BuildingViewer(b)
# v.show()


b.write_idf()
b.analyze(exe='/Applications/EnergyPlus/energyplus')
b.load_results()

v = ResultsViewer(b)
v.show('lighting')