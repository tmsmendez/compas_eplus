from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import json

from compas.geometry import subtract_vectors
from compas.geometry import scale_vector
from compas.geometry import add_vectors
from compas.geometry import normalize_vector
from compas.geometry import distance_point_point

class Window(object):
    """
    Window datastructure for energy+ analysis. 

    Parameters
    ----------
    name: str, optional
        The name of the window
    nodes: list,
        List of x, y, z corrdinates for the corners of the window
    building_surface: str
        The name of the building surface the window is attached to
    construction: str
        The name of the window construction
    
    """
    def __init__(self):
        self.name = None
        self.nodes = None
        self.building_surface = None
        self.construction = None
    
    @classmethod
    def from_wall_and_wwr(cls, zone, wall_key, wwr, construction=None):
        """
        Creates a window instance from a wall and window-to-wall ratio.

        Parameters
        ----------
        zone: object
            The zone object the window is to be places
        wall_key: int
            The key of the wall the window is to be attached to
        wwr: float
            The window-to-wall ratio for the window
        construction: str
            The window construction name

        Returns
        -------
        Window
            The instance of the created window object
        
        """
        if wwr > .95:
            wwr = .95
        nks = zone.surfaces.face_vertices(wall_key)
        pts = [zone.surfaces.vertex_coordinates(nk) for nk in nks]
        cpt = zone.surfaces.face_centroid(wall_key)
        a = zone.surfaces.face_area(wall_key) * wwr
        lx = distance_point_point(pts[0], pts[1]) - .1
        ly = a / lx
        vx = scale_vector(normalize_vector(subtract_vectors(pts[0], pts[1])), lx / 2.)
        vy = scale_vector(normalize_vector(subtract_vectors(pts[0], pts[-1])), ly / 2.)
        vx_ = scale_vector(normalize_vector(subtract_vectors(pts[0], pts[1])), -lx / 2.)
        vy_ = scale_vector(normalize_vector(subtract_vectors(pts[0], pts[-1])), -ly / 2.)

        p0 = add_vectors(cpt, add_vectors(vx_, vy_))
        p1 = add_vectors(cpt, add_vectors(vx, vy_))
        p2 = add_vectors(cpt, add_vectors(vx, vy))
        p3 = add_vectors(cpt, add_vectors(vx_, vy))

        window = cls()
        window.name = f'win_{zone.name}_{wall_key}'
        window.nodes = [p0, p1, p2, p3]
        window.building_surface = f'{zone.name}_{wall_key}' 
        window.construction = construction
        return window
    

    def to_json(self, filepath):
        """
        Serialize the data representation of the window to a JSON file

        Parameters
        ----------
        filepath: str
            Path for the JSON file to be created
        
        Returns
        -------
        None

        """
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'name'                  : self.name,
                'nodes'                 : self.nodes,
                'building_surface'      : self.building_surface,
                'construction'          : self.construction,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.name               = data.get('name') or {}
        self.nodes              = data.get('nodes') or {}
        self.building_surface   = data.get('building_surface') or {}
        self.construction       = data.get('construction') or {}

    @classmethod
    def from_data(cls, data):
        """
        Create a new instance of the window datastructure from a data dictionary.

        Parameters
        ----------
        data: dict
            Data dictionary
        
        Returns
        -------
        Window
            The instance of the window datastructure
        
        """
        window = cls()
        window.data = data
        return window


    @classmethod
    def from_json(cls, filepath):
        """
        Create a new instance of the window datastructure from a JSON file

        Parameters
        ----------
        filepath: str
            Path to the JSON file
        
        Returns
        -------
        Window
            The instance of the window datastructure
        
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        window = cls()
        window.data = data
        return window