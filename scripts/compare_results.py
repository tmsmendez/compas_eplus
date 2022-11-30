import os
import compas_eplus
from compas_eplus.read_write import read_results_file
from compas_eplus.building import Building


for i in range(50): print('')

path = compas_eplus.TEMP
wea = compas_eplus.SEATTLE
b1 = Building.from_idf(os.path.join(compas_eplus.DATA, 'idf_examples', 'teresa_example.idf'), path, wea)
filepath = os.path.join(compas_eplus.DATA, 'results', 'teresa.eso')
results1 = read_results_file(b1, filepath)

b2 = Building.from_idf(os.path.join(compas_eplus.DATA, 'idf_examples', 'teresa_example.idf'), path, wea)
filepath = os.path.join(compas_eplus.DATA, 'results', 'counter_teresa.eso')
results1 = read_results_file(b2, filepath)

item = 'cooling'
b1.plot_results(item, plot_type='line', timeframe='daily')
b2.plot_results(item, plot_type='line', timeframe='daily')
