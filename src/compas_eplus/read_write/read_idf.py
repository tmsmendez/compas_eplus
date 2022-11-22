from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


def get_idf_data(filepath):
    data = {}
    find_zones(filepath, data)
    find_sufaces(filepath, data)


    return data


def find_zones(filepath, data):

    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'zone':
            i_lines.append(i)

    data['zones'] = {}    
    for i in i_lines:
        name = lines[i + 1].split(',')[0].strip()
        x = float(lines[i + 2].split(',')[0].strip())
        y = float(lines[i + 3].split(',')[0].strip())
        z = float(lines[i + 4].split(',')[0].strip())
        h = float(lines[i + 8].split(',')[0].strip())
        v = float(lines[i + 9].split(',')[0].strip())
        data['zones'][name] = {'origin': [x, y, z],
                               'height': h,
                               'volume':v,
                               'surfaces': {}}


def find_sufaces(filepath, data):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()

    i_lines = []
    for i, line in enumerate(lines):
        line = line.split(',')
        if line[0].lower() == 'buildingsurface:detailed':
            i_lines.append(i)

    for i in i_lines:
        zone  = lines[i + 4].split(',')[0].strip()
        stype = lines[i + 2].split(',')[0].strip()
        cons  = lines[i + 3].split(',')[0].strip()
        outs = lines[i + 6].split(',')[0].strip()
        pts = []
        for j in range(4):
            xyz = lines[i + j + 12].split(',')[:3]
            xyz = [float(x) for x in xyz]
            pts.append(xyz)


        data['zones'][zone]['surfaces'] = {'surface_type': stype}



# BuildingSurface:Detailed,
#   2_Residential_cc56a40e..Face0,          !- Name
#   Wall,                                   !- Surface Type
#   Typical Insulated Wood Framed Exterior Wall-R16, !- Construction Name
#   2_Residential_cc56a40e,                 !- Zone Name
#   ,                                       !- Space Name
#   Outdoors,                               !- Outside Boundary Condition
#   ,                                       !- Outside Boundary Condition Object
#   SunExposed,                             !- Sun Exposure
#   WindExposed,                            !- Wind Exposure
#   ,                                       !- View Factor to Ground
#   ,                                       !- Number of Vertices
#   12.5890309865003, 7.77933424703412, 3.04999999987174, !- X,Y,Z Vertex 1 {m}
#   12.5890309865003, 7.77933424703412, -1.28257671150322e-10, !- X,Y,Z Vertex 2 {m}
#   12.5890309865003, 13.8793342470341, -1.28257671150322e-10, !- X,Y,Z Vertex 3 {m}
#   12.5890309865003, 13.8793342470341, 3.04999999987174; !- X,Y,Z Vertex 4 {m}


if __name__ == '__main__':
    import os
    import compas_eplus

    for i in range(50): print('')

    file = 'teresa_example.idf'
    path = os.path.join(compas_eplus.DATA, 'idf_examples', file)

    data = get_idf_data(path)
    print(data)