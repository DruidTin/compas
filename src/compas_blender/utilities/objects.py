import bpy
from typing import List, Iterable, Text

# from compas.datastructures import Mesh


__all__ = [
    "delete_object",
    "delete_objects",
    "delete_all_objects",
    "delete_object_by_name",
    "delete_objects_by_names",
    "get_object_by_name",
    "get_objects_by_names",
    # "get_objects",
    # "get_object_name",
    # "get_objects_names",
    # "get_objects_layers",
    # "get_objects_types",
    # "get_objects_coordinates",
    # "get_object_property",
    # "get_objects_property",
    # "get_points",
    # "get_curves",
    # "get_meshes",
    # "get_points_coordinates",
    # "get_curves_coordinates",
    # "select_object",
    # "select_objects",
    # "select_point",
    # "select_points",
    # "select_curve",
    # "select_curves",
    # "select_mesh",
    # "select_meshes",
    # "set_select",
    # "set_deselect",
    # "set_objects_layer",
    # "set_objects_coordinates",
    # "set_objects_rotations",
    # "set_objects_scales",
    # "set_objects_show_names",
    # "set_objects_visible",
    # "set_object_property",
    # "set_objects_property",
    # "mesh_from_bmesh",
]


# ==============================================================================
# Delete
# ==============================================================================


def delete_all_objects():
    """Delete all mesh and curve scene objects, and the attached mesh and curve data blocks."""
    for obj in bpy.data.objects:
        # if obj.type == 'MESH':
        #     bpy.data.objects.remove(obj)
        # elif obj.type == 'CURVE':
        #     bpy.data.objects.remove(obj)
        bpy.data.objects.remove(obj)
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for curve in bpy.data.curves:
        bpy.data.curves.remove(curve)


def delete_object(obj: bpy.types.Object):
    """Delete a scene object.

    If the scene object is of type "MESH" or "CURVE",
    the attached data blocks are also removed.
    """
    if obj.type == 'MESH':
        mesh = obj.data
        bpy.data.objects.remove(obj)
        if mesh:
            bpy.data.meshes.remove(mesh)
    elif obj.type == 'CURVE':
        curve = obj.data
        bpy.data.objects.remove(obj)
        if curve:
            bpy.data.curves.remove(curve)
    else:
        bpy.data.objects.remove(obj)


def delete_objects(objects: Iterable[bpy.types.Object]):
    """Delete multiple scene objects."""
    for obj in objects:
        delete_object(obj)


def delete_object_by_name(name: str):
    """Delete the scene object corresponding to the given name."""
    obj = get_object_by_name(name)
    delete_object(obj)


def delete_objects_by_names(names: Iterable[Text]):
    """Delete the scene objects corresponding to the list of names."""
    objects = get_objects_by_names(names)
    delete_objects(objects)


# ==============================================================================
# Get
# ==============================================================================


def get_object_by_name(name: str) -> bpy.types.Object:
    """Get the object with the given name."""
    return bpy.data.objects[name]


def get_objects_by_names(names: Iterable[str]) -> List[bpy.types.Object]:
    """Get the objects corresponding to the given names."""
    return [bpy.data.objects[name] for name in names]


# def get_objects(names=None, color=None, layer=None, type=None):
#     if names:
#         objects = get_objects_by_names(names)
#     elif color:
#         raise NotImplementedError
#     elif layer:
#         objects = list(bpy.data.collections[layer].objects)
#     elif type:
#         objects = [obj for obj in bpy.data.objects if obj.type == type.upper()]
#     else:
#         objects = list(bpy.data.objects)
#     return objects


# def get_object_name(obj):
#     return obj.name


# def get_objects_names(objects):
#     return [get_object_name(obj) for obj in objects]


# def get_objects_layers(objects):
#     return [obj.users_collection for obj in objects]


# def get_objects_types(objects):
#     return [obj.type for obj in objects]


# def get_objects_coordinates(objects):
#     return [list(obj.location) for obj in objects]


# def get_object_property(obj, property_name):
#     return obj.get(property_name)


# def get_objects_property(objects, property_name):
#     return [get_object_property(obj, property_name) for obj in objects]


# def select_object(message="Select an object."):
#     raise NotImplementedError


# def select_objects(message="Select objects."):
#     raise NotImplementedError


# ==============================================================================
# Points
# ==============================================================================


# def get_points(layer=None):
#     return [obj for obj in get_objects(layer=layer) if obj.type == "EMPTY"]


# def get_points_coordinates(objects=None):
#     if objects is None:
#         objects = get_points()
#     return [list(obj.location) for obj in objects if obj.type == "EMPTY"]


# def select_point(message="Select a point."):
#     raise NotImplementedError


# def select_points(message="Select points."):
#     raise NotImplementedError


# ==============================================================================
# Curves
# ==============================================================================


# def select_curve(message="Select curve."):
#     raise NotImplementedError


# def select_curves(message="Select curves."):
#     raise NotImplementedError


# def get_curves(layer=None):
#     return [obj for obj in get_objects(layer=layer) if obj.type == "CURVE"]


# def get_curves_coordinates(objects):
#     raise NotImplementedError


# ==============================================================================
# Meshes
# ==============================================================================


# def select_mesh(message="Select a mesh."):
#     raise NotImplementedError


# def select_meshes(message="Select meshes."):
#     raise NotImplementedError


# def get_meshes(layer=None):
#     return [obj for obj in get_objects(layer=layer) if obj.type == "MESH"]


# def mesh_from_bmesh(bmesh):
#     vertices = [list(vertex.co) for vertex in bmesh.data.vertices]
#     faces = [list(face.vertices) for face in bmesh.data.polygons]
#     return Mesh.from_vertices_and_faces(vertices=vertices, faces=faces)


# ==============================================================================
# Surfaces
# ==============================================================================


# ==============================================================================
# Set
# ==============================================================================

# def set_select(objects=None):
#     if objects:
#         for obj in objects:
#             obj.select_set(state=True)
#     else:
#         bpy.ops.object.select_all(action="SELECT")


# def set_deselect(objects=None):
#     if objects:
#         for obj in objects:
#             obj.select_set(state=False)
#     else:
#         bpy.ops.object.select_all(action="DESELECT")


# def set_objects_layer(objects, layer):
#     collection_new = bpy.data.collections.get(layer) or bpy.data.collections.new(layer)
#     for obj in objects:
#         for collection_old in obj.users_collection:
#             collection_old.objects.unlink(obj)
#         collection_new.objects.link(obj)


# def set_objects_coordinates(objects, coords):
#     for obj, xyz in zip(objects, coords):
#         obj.location = xyz


# def set_objects_rotations(objects, rotations):
#     for obj, r in zip(objects, rotations):
#         obj.rotation_euler = r


# def set_objects_scales(objects, scales):
#     for obj, s in zip(objects, scales):
#         obj.scale = s


# def set_objects_show_names(objects, show=True):
#     for obj in objects:
#         obj.show_name = show


# def set_objects_visible(objects, visible=True):
#     for obj in objects:
#         obj.hide_viewport = not visible


# def set_object_property(obj, property_name, property_value):
#     obj[property_name] = property_value


# def set_objects_property(objects, property_name, property_value):
#     for obj in objects:
#         obj[property_name] = property_value


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
