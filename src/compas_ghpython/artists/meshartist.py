from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino

import compas_ghpython
from compas_ghpython.artists._artist import BaseArtist
from compas.utilities import color_to_colordict


__all__ = ['MeshArtist']


class MeshArtist(BaseArtist):
    """A mesh artist defines functionality for visualising COMPAS meshes in GhPython.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    settings : dict, optional
        A dict with custom visualisation settings.

    Attributes
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The COMPAS mesh associated with the artist.
    settings : dict
        Default settings for color, scale, tolerance, ...

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas_ghpython.artists import MeshArtist

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        artist = MeshArtist(mesh)
        artist.draw_faces(join_faces=True)
        artist.draw_vertices(color={key: '#ff0000' for key in mesh.vertices_on_boundary()})
        artist.draw_edges()

    """

    def __init__(self, mesh):
        self._mesh = None
        self.mesh = mesh
        self.settings = {
            'color.vertices': (255, 255, 255),
            'color.edges': (0, 0, 0),
            'color.faces': (210, 210, 210),
            'show.vertices': True,
            'show.edges': True,
            'show.faces': True,
            'show.vertexlabels': False,
            'show.facelabels': False,
            'show.edgelabels': False,
            'join_faces': True
        }

    @property
    def mesh(self):
        """compas.datastructures.Mesh: The mesh that should be painted."""
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh

    def draw(self):
        """Draws the mesh using the current settings.

        Returns
        -------
        geometry : list

            * geometry[0]: list of :class:`Rhino.Geometry.Point3d` or `None`, if `self.settings['show.nodes']` is False.
            * geometry[1]: list of :class:`Rhino.Geometry.TextDot` or `None`, if `self.settings['show.nodelabels']` is False.
            * geometry[2]: list of :class:`Rhino.Geometry.Mesh` or `None`, if `self.settings['show.faces']` is False.
            * geometry[3]: list of :class:`Rhino.Geometry.TextDot` or `None`, if `self.settings['show.facelabels']` is False.
            * geometry[4]: list of :class:`Rhino.Geometry.Line` or `None`, if `self.settings['show.edges']` is False.
            * geometry[5]: list of :class:`Rhino.Geometry.TextDot` or `None`, if `self.settings['show.edgelabels']` is False.

        """
        geometry = [None, None, None, None, None, None]

        if self.settings['show.vertices']:
            geometry[0] = self.draw_nodes()
            if self.settings['show.vertexlabels']:
                geometry[1] = self.draw_nodelabels()

        if self.settings['show.faces']:
            geometry[2] = self.draw_faces(join_faces=self.settings['join_faces'])
            if self.settings['show.facelabels']:
                geometry[3] = self.draw_facelabels()

        if self.settings['show.edges']:
            geometry[4] = self.draw_edges()
            if self.settings['show.edgelabels']:
                geometry[5] = self.draw_edgelabels()

        return geometry

    # ==============================================================================
    # components
    # ==============================================================================

    # def draw_mesh(self, color=None):
    #     """Draw the mesh as a RhinoMesh.

    #     Parameters
    #     ----------
    #     color : 3-tuple, optional
    #         RGB color components in integer format (0-255).

    #     Returns
    #     -------
    #     :class:`Rhino.Geometry.Mesh`

    #     Notes
    #     -----
    #     Faces with more than 4 vertices will be triangulated on-the-fly.

    #     """
    #     key_index = self.mesh.key_index()
    #     vertices = self.mesh.vertices_attributes('xyz')
    #     faces = [[key_index[key] for key in self.mesh.face_vertices(fkey)] for fkey in self.mesh.faces()]
    #     new_faces = []
    #     for face in faces:
    #         f = len(face)
    #         if f == 3:
    #             new_faces.append(face + [face[-1]])
    #         elif f == 4:
    #             new_faces.append(face)
    #         elif f > 4:
    #             centroid = len(vertices)
    #             vertices.append(centroid_polygon(
    #                 [vertices[index] for index in face]))
    #             for a, b in pairwise(face + face[0:1]):
    #                 new_faces.append([centroid, a, b, b])
    #         else:
    #             continue
    #     return compas_ghpython.draw_mesh(vertices, new_faces, color)

    def draw_vertices(self, keys=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        keys : list
            A list of vertex keys identifying which vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : str, tuple, dict
            The color specififcation for the vertices.
            Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
            To apply the same color to all vertices, provide a single color specification.
            Individual colors can be assigned using a dictionary of key-color pairs.
            Missing keys will be assigned the default vertex color (``self.settings['color.vertices']``).
            The default is ``None``, in which case all vertices are assigned the default vertex color.

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`

        """
        vertices = keys or list(self.mesh.vertices())
        colordict = color_to_colordict(color,
                                       vertices,
                                       default=self.settings['color.vertices'],
                                       colorformat='rgb',
                                       normalize=False)
        points = []
        for vertex in vertices:
            points.append({
                'pos': self.mesh.vertex_coordinates(vertex),
                'name': "{}.vertex.{}".format(self.mesh.name, vertex),
                'color': colordict[vertex]
            })
        return compas_ghpython.draw_points(points)

    def draw_faces(self, keys=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        fkeys : list
            A list of face keys identifying which faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : str, tuple, dict
            The color specififcation for the faces.
            Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
            To apply the same color to all faces, provide a single color specification.
            Individual colors can be assigned using a dictionary of key-color pairs.
            Missing keys will be assigned the default face color (``self.settings['color.faces']``).
            The default is ``None``, in which case all faces are assigned the default face color.

        Returns
        -------
        list of :class:`Rhino.Geometry.Mesh`

        """
        keys = keys or list(self.mesh.faces())

        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.settings['color.faces'],
                                       colorformat='rgb',
                                       normalize=False)
        faces = []
        for fkey in keys:
            faces.append({
                'points': self.mesh.face_coordinates(fkey),
                'name': "{}.face.{}".format(self.mesh.name, fkey),
                'color': colordict[fkey]
            })

        meshes = compas_ghpython.draw_faces(faces)
        if not join_faces:
            return meshes

        joined_mesh = Rhino.Geometry.Mesh()
        for mesh in meshes:
            joined_mesh.Append(mesh)
        return [joined_mesh]

    def draw_edges(self, keys=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        keys : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : str, tuple, dict
            The color specififcation for the edges.
            Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
            To apply the same color to all edges, provide a single color specification.
            Individual colors can be assigned using a dictionary of key-color pairs.
            Missing keys will be assigned the default face color (``self.settings['color.edges']``).
            The default is ``None``, in which case all edges are assigned the default edge color.

        Returns
        -------
        list of :class:`Rhino.Geometry.Line`

        """
        edges = keys or list(self.mesh.edges())
        colordict = color_to_colordict(color,
                                       edges,
                                       default=self.settings['color.edges'],
                                       colorformat='rgb',
                                       normalize=False)
        lines = []
        for edge in edges:
            start, end = self.mesh.edge_coordinates(*edge)
            lines.append({
                'start': start,
                'end': end,
                'color': colordict[edge],
                'name': "{}.edge.{}-{}".format(self.mesh.name, *edge)
            })
        return compas_ghpython.draw_lines(lines)

    # ==============================================================================
    # labels
    # ==============================================================================

    def draw_vertexlabels(self, text=None, color=None):
        """Draw labels for a selection vertices.

        Parameters
        ----------
        text : dict
            A dictionary of vertex labels as key-text pairs.
            The default value is ``None``, in which case every vertex will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            If a dictionary of specififcations is provided,
            the keys of the should refer to vertex keys and the values should be color specifications in the form of strings or tuples.
            The default value is ``None``,
            in which case the labels are assigned the default vertex color (``self.settings['color.vertices']``).

        Returns
        -------
        list of :class:`Rhino.Geometry.TextDot`

        """
        if text is None:
            textdict = {key: str(key) for key in self.mesh.vertices()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings['color.vertices'],
                                       colorformat='rgb',
                                       normalize=False)
        labels = []

        for key, text in iter(textdict.items()):
            labels.append({
                'pos': self.mesh.vertex_coordinates(key),
                'name': "{}.vertexlabel.{}".format(self.mesh.name, key),
                'color': colordict[key],
                'text': textdict[key]
            })

        return compas_ghpython.draw_labels(labels)

    def draw_facelabels(self, text=None, color=None):
        """Draw labels for a selection of faces.

        Parameters
        ----------
        text : dict
            A dictionary of face labels as key-text pairs.
            The default value is ``None``, in which case every face will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            If a dictionary of specififcations is provided, the keys of the
            should refer to face keys and the values should be color
            specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned
            the default face color (``self.settings['color.faces']``).

        Returns
        -------
        list of :class:`Rhino.Geometry.TextDot`

        """
        if text is None:
            textdict = {key: str(key) for key in self.mesh.faces()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings['color.faces'],
                                       colorformat='rgb',
                                       normalize=False)

        labels = []
        for key, text in iter(textdict.items()):
            labels.append({
                'pos': self.mesh.face_center(key),
                'name': "{}.facelabel.{}".format(self.mesh.name, key),
                'color': colordict[key],
                'text': textdict[key]
            })
        return compas_ghpython.draw_labels(labels)

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict
            A dictionary of edge labels as key-text pairs.
            The default value is ``None``, in which case every edge will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.settings['color.edges']``).
            The default is ``None``, in which case all edges are assigned the
            default edge color.

        Returns
        -------
        list of :class:`Rhino.Geometry.TextDot`

        """
        if text is None:
            textdict = {(u, v): "{}-{}".format(u, v) for u, v in self.mesh.edges()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings['color.edges'],
                                       colorformat='rgb',
                                       normalize=False)
        labels = []

        for (u, v), text in iter(textdict.items()):
            labels.append({
                'pos': self.mesh.edge_midpoint(u, v),
                'name': "{}.edgelabel.{}-{}".format(self.mesh.name, u, v),
                'color': colordict[(u, v)],
                'text': textdict[(u, v)]
            })

        return compas_ghpython.draw_labels(labels)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
