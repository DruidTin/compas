from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    basestring
except NameError:
    basestring = str

import compas_rhino
# from compas.utilities import iterable_like
from compas_rhino.artists._primitiveartist import PrimitiveArtist


__all__ = ['FrameArtist']


class FrameArtist(PrimitiveArtist):
    """Artist for drawing frames.

    Parameters
    ----------
    frame : compas.geometry.Frame
        A COMPAS frame.

    Other Parameters
    ----------------
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    Attributes
    ----------
    scale : float
    color_origin : tuple of 3 int between 0 abd 255
    color_xaxis : tuple of 3 int between 0 abd 255
    color_yaxis : tuple of 3 int between 0 abd 255
    color_zaxis : tuple of 3 int between 0 abd 255

    Examples
    --------
    >>>

    """

    def __init__(self, frame, layer=None, name=None, scale=1.0):
        super(FrameArtist, self).__init__(frame, layer=layer, name=name)
        self.scale = scale
        self.color_origin = (0, 0, 0)
        self.color_xaxis = (255, 0, 0)
        self.color_yaxis = (0, 255, 0)
        self.color_zaxis = (0, 0, 255)

    def draw(self):
        """Draw the frame.

        Returns
        -------
        guids: list
            The GUIDs of the created Rhino objects.
        """
        points = []
        lines = []
        origin = list(self.primitive.point)
        x = list(self.primitive.point + self.primitive.xaxis.scaled(self.scale))
        y = list(self.primitive.point + self.primitive.yaxis.scaled(self.scale))
        z = list(self.primitive.point + self.primitive.zaxis.scaled(self.scale))
        points = [{'pos': origin, 'color': self.color_origin}]
        lines = [
            {'start': origin, 'end': x, 'color': self.color_xaxis, 'arrow': 'end'},
            {'start': origin, 'end': y, 'color': self.color_yaxis, 'arrow': 'end'},
            {'start': origin, 'end': z, 'color': self.color_zaxis, 'arrow': 'end'}]
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guids = guids
        return guids

    @staticmethod
    def draw_collection(collection, names=None, colors=None, layer=None, clear=False, add_to_group=False, group_name=None):
        """Draw a collection of circles.

        Parameters
        ----------
        collection : list of :class:`compas.geometry.Frame`
            A collection of frames.
        names : list of str, optional
            Individual names for the frames.
        colors : color or list of color, optional
            A color specification for the frames as a single color or a list of individual colors.
        layer : str, optional
            A layer path.
        clear : bool, optional
            Clear the layer before drawing.
        add_to_group : bool, optional
            Add the frames to a group.
        group_name : str, optional
            Name of the group.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
