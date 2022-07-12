import compas_eplus

from compas_eplus.viewers import BuildingViewer

from compas_eplus.building import Building

for i in range(50): print('')

path = compas_eplus.TEMP
wea = compas_eplus.SEATTLE

quad = [[0,0,0],
        [30,0,0],
        [30,10,0],
        [0,10,0],
        ]
zone_depth = [3., 6, 3, 6]
b = Building.from_quad(path, wea, quad, zone_depth, height=3)

v = BuildingViewer(b)
v.show()
