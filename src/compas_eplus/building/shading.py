from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


import json
from compas.datastructures import Mesh
from compas.geometry import subtract_vectors
from compas.geometry import cross_vectors
from compas.geometry import scale_vector
from compas.geometry import normalize_vector
from compas.geometry import add_vectors


class Shading(object):
    """
    Shading device object.

    Parameters
    ----------
    name: str, optional
        The name of the shading device
    mesh: object
        compas Mesh object representing the surfaces making up the shading device

    """
    def __init__(self):
        self.name =  'Shading'
        self.mesh = None

    def to_json(self, filepath):
        """
        Serialize the data representation of the shading device to a JSON file

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
        data = {'name'              : self.name,
                'mesh'              : self.mesh.to_data(),
                }
        return data
    
    @data.setter
    def data(self, data):
        mesh           = data.get('mesh') or {}
        self.name      = data.get('name') or {}
        self.mesh      = Mesh.from_data(mesh)


    def add_mesh(self, mesh):
        """
        Adds a mesh to the shading device.

        Parameters
        ----------
        mesh: object
            The compas mesh object to add

        Returns
        -------
        None

        """
        self.mesh = mesh

    @classmethod
    def from_data(cls, data):
        """
        Create a new instance of the shading device datastructure from a data dictionary

        Parameters
        ----------
        data: dict
            Data dictionary
        
        Returns
        -------
            Shading
                The instance of the shading datastructure
        
        """
        zone = cls()
        zone.data = data
        return zone

    @classmethod
    def from_json(cls, filepath):
        """
        Create a new instance of the shading datastructure from a JSON file

        Parameters
        ----------
        filepath: str
            Path to the JSON file
        
        Returns
        -------
            Shading
                The instance of the shading datastructure
        
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        zone = cls()
        zone.data = data
        return zone

    @classmethod
    def from_window(cls, window, top=None, left=None, right=None):
        """
        Create a new instance of the shading from a window object. The shading device will
        be made up of a top, left and right rectangular surfaces surrounding the given
        window. 

        Parameters
        ----------
        window: object
            Window object to be used for the creation of the shading device
        top: float, optional
            Length of the top of the shading device (m)
        left: float, optional
            Length of the left of the shading device (m)
        right: float, optional
            Length of the right of the shading device (m)
        
        Returns
        -------
            Shading
                The instance of the shading device datastructure
        
        """
        vertices = list(window.nodes)
        v1 = subtract_vectors(vertices[3], vertices[2])
        v2 = subtract_vectors(vertices[3], vertices[0])
        n = normalize_vector(cross_vectors(v2, v1))
        faces = []
        if top:
            ntop = scale_vector(n, top)
            vertices.append(add_vectors(vertices[0], ntop))
            vertices.append(add_vectors(vertices[1], ntop))
            num = len(vertices) - 1
            faces.append([1, 0, num - 1, num])
        if left:
            nleft = scale_vector(n, left)
            vertices.append(add_vectors(vertices[1], nleft))
            vertices.append(add_vectors(vertices[2], nleft))
            num = len(vertices) - 1
            faces.append([2, 1, num - 1, num])
        if right:
            nright = scale_vector(n, right)
            vertices.append(add_vectors(vertices[0], nright))
            vertices.append(add_vectors(vertices[3], nright))
            num = len(vertices) - 1
            faces.append([3, 0, num - 1, num])


        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        shading = cls()
        shading.name = f'sh_win{window.name}'
        shading.mesh = mesh
        return shading


