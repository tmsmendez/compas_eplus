from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import plotly
import plotly.graph_objects as go
import plotly.express as px

from compas.datastructures import Mesh


class BuildingViewer(object):
    """
    Viewer object for Building objects. Can show zone geometries, windows, 
    shading devicesconstruction layers.

    Parameters
    ----------
    building: object
        The building object to be displayed
    data: list
        Plotly data containing plot objects (i.e. Meshes)
    layout: dict
        PLotly layout data

    """
    def __init__(self, building):
        self.building = building
        self.data = []
        self.layout = None

    def make_layout(self):
        """
        Adds the layout data to the viewer object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        name = self.building.name
        title = '{0}'.format(name)
        layout = go.Layout(title=title,
                          scene=dict(aspectmode='data',
                                    xaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    yaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    zaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)')
                                    ),
                          showlegend=True,
                            )
        self.layout = layout

    def show(self):
        """
        Displays the buiilding in a browser window.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        self.make_layout()
        self.add_zones()
        self.add_windows()
        self.add_shadings()

        fig = go.Figure(data=self.data, layout=self.layout)
        fig.show()

    def add_zones(self):
        """
        Adds zone meshes data to the viewer object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        for zk in self.building.zones:
                self.add_zone_mesh(zk)

    def add_windows(self):
        """
        Adds window data to the viewer object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        for wk in self.building.windows:
            self.add_window_mesh(wk)

    def add_shadings(self):
        """
        Adds shading data to the viewer object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """
        for sk in self.building.shadings:
            self.add_shading_mesh(sk)

    def add_shading_mesh(self, key):
        """
        Adds shading mesh data to the viewer object.

        Parameters
        ----------
        key: int
            The shading key to be added

        Returns
        -------
        None
        
        """
        mesh = self.building.shadings[key].mesh
        vertices, faces = mesh.to_vertices_and_faces()
        edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
        line_marker = dict(color='rgb(0,0,0)', width=1.5)
        lines = []
        x, y, z = [], [],  []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        sname = self.building.shadings[key].name
        lines = [go.Scatter3d(name=f'{sname}',
                              x=x,
                              y=y,
                              z=z,
                              mode='lines',
                              line=line_marker,
                              legendgroup=f'{sname}',
                              )]
        triangles = []
        for face in faces:
            triangles.append(face[:3])
            if len(face) == 4:
                triangles.append([face[2], face[3], face[0]])
        
        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]

        text = []
        intensity = []

        faces = [go.Mesh3d(name='Zone',
                           x=x,
                           y=y,
                           z=z,
                           i=i,
                           j=j,
                           k=k,
                           color= 'rgb(255,255,255)',
                           opacity=.8,
                        #    colorbar_title='is_rad',
                        #    colorbar_thickness=10,
                        #    text=text,
                        #    hoverinfo='text',
                           legendgroup=f'{sname}',
                           lighting={'ambient':1.},
                        #    intensitymode='cell',
                        #    intensity=intensity,
                        #    showscale=False,
                        #    colorscale='gnbu',

                )]
        self.data.extend(lines)
        self.data.extend(faces)

    def add_window_mesh(self, key):
        """
        Adds window mesh data to the viewer object.

        Parameters
        ----------
        key: int
            The window key to be added

        Returns
        -------
        None
        
        """
        vertices = self.building.windows[key].nodes
        faces = [[0, 1, 2, 3]]
        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        vertices, faces = mesh.to_vertices_and_faces()
        edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
        line_marker = dict(color='rgb(0,0,0)', width=1.5)
        lines = []
        x, y, z = [], [],  []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        wname = self.building.windows[key].name
        lines = [go.Scatter3d(name=f'{wname}',
                              x=x,
                              y=y,
                              z=z,
                              mode='lines',
                              line=line_marker,
                              legendgroup=f'{wname}',
                              )]
        triangles = []
        for face in faces:
            triangles.append(face[:3])
            if len(face) == 4:
                triangles.append([face[2], face[3], face[0]])
        
        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]


        text = []
        intensity = []
        for fk in mesh.faces():
            ck = self.building.windows[key].construction
            if ck in self.building.construction_key_dict:
                con = self.building.constructions[self.building.construction_key_dict[ck]]
                layers = [con.layers[lk]['name'] for lk in con.layers] 
                # thick = con.layers[lk]['thickness']
                # layers = ['{} {}mm'.format(lay, round(thick*1000, 1)) for lay in layers]
            else:
                layers = []

            string = 'name: {}<br>'.format(wname)
            string += 'construction: {}<br>'.format(ck)
            for lk, layer in enumerate(layers):
                string += 'layer {}: {}<br>'.format(lk, layer)
            text.append(string)
            intensity.append(float(key))
            if len(mesh.face_vertices(fk)) == 4:
                intensity.append(float(key))
                text.append(string)



        faces = [go.Mesh3d(name='Zone',
                           x=x,
                           y=y,
                           z=z,
                           i=i,
                           j=j,
                           k=k,
                           opacity=.8,
                           colorbar_title='is_rad',
                           colorbar_thickness=10,
                           text=text,
                           hoverinfo='text',
                           legendgroup=f'{wname}',
                           lighting={'ambient':1.},
                           intensitymode='cell',
                           intensity=intensity,
                           showscale=False,
                           colorscale='gnbu',

                )]
        self.data.extend(lines)
        self.data.extend(faces)

    def add_zone_mesh(self, key):
        """
        Adds zone mesh data to the viewer object.

        Parameters
        ----------
        key: int
            The zone key to be added

        Returns
        -------
        None
        
        """
        mesh = self.building.zones[key].surfaces
        vertices, faces = mesh.to_vertices_and_faces()
        edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
        line_marker = dict(color='rgb(0,0,0)', width=1.5)
        lines = []
        x, y, z = [], [],  []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        zname = self.building.zones[key].name
        lines = [go.Scatter3d(name=f'{zname}',
                              x=x,
                              y=y,
                              z=z,
                              mode='lines',
                              line=line_marker,
                              legendgroup=f'{zname}',
                              )]
        triangles = []
        for face in faces:
            triangles.append(face[:3])
            if len(face) == 4:
                triangles.append([face[2], face[3], face[0]])
        
        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]

        # colorscales = ['sunset', 'viridis', 'amp']

        colorscales = dir(plotly.colors.sequential)[::2]
        attrs = ['name', 'surface_type', 'outside_boundary_condition', 'construction']
        text = []
        intensity = []
        for fk in mesh.faces():
            faceatts = mesh.face_attributes(fk)
            ck = mesh.face_attribute(fk, 'construction')
            if ck:
                con = self.building.constructions[self.building.construction_key_dict[ck]]
                layers = [con.layers[lk]['name'] for lk in con.layers] 
                thick = [con.layers[lk]['thickness'] for lk in con.layers]
                layers = ['{} {}mm'.format(lay, round(thick[tk]*1000, 1)) for tk, lay in enumerate(layers)]
            else:
                layers = []
            string = 'zone: {}<br>'.format(zname)
            for att in attrs:
                string += '{}: {}<br>'.format(att, faceatts[att])
            for lk, layer in enumerate(layers):
                string += 'layer {}: {}<br>'.format(lk, layer)
            text.append(string)
            intensity.append(float(key))
            if len(mesh.face_vertices(fk)) == 4:
                intensity.append(float(key))
                text.append(string)


        faces = [go.Mesh3d(name='Zone',
                           x=x,
                           y=y,
                           z=z,
                           i=i,
                           j=j,
                           k=k,
                           opacity=.8,
                           colorbar_title='is_rad',
                           colorbar_thickness=10,
                           text = text,
                           hoverinfo='text',
                           legendgroup=f'{zname}',
                           lighting={'ambient':1.0},
                           intensitymode='cell',
                           intensity=intensity,
                           showscale=False,
                           colorscale=colorscales[int(key)],
                )]
        self.data.extend(lines)
        self.data.extend(faces)

if __name__ == '__main__':
    import os
    import compas_eplus
    from compas_eplus.building import Building

    pass