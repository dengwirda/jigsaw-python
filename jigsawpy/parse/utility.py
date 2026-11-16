
import numpy as np

from jigsawpy.msh_t import jigsaw_msh_t


MESH_KINDS = ("euclidean-mesh", "ellipsoid-mesh")
GRID_KINDS = ("euclidean-grid", "ellipsoid-grid")
CELL_TYPES = (
    ("edge2", 2, jigsaw_msh_t.EDGE2_t),
    ("tria3", 3, jigsaw_msh_t.TRIA3_t),
    ("quad4", 4, jigsaw_msh_t.QUAD4_t),
    ("tria4", 4, jigsaw_msh_t.TRIA4_t),
    ("hexa8", 8, jigsaw_msh_t.HEXA8_t),
    ("wedg6", 6, jigsaw_msh_t.WEDG6_t),
    ("pyra5", 5, jigsaw_msh_t.PYRA5_t),
)


def netcdf_dataset():
    try:
        from netCDF4 import Dataset
    except ModuleNotFoundError as error:
        if error.name != "netCDF4":
            raise
        raise ImportError(
            "NetCDF mesh I/O requires netCDF4; "
            "install jigsawpy[netcdf].") from error
    return Dataset


def present(data):
    return data is not None and data.size > 0


def grid_shape(mesh, ndim=None):
    axes = [data.size if present(data) else 0
            for data in (mesh.xgrid, mesh.ygrid, 
                         mesh.zgrid)]
    ndim = mesh.ndims if ndim is None else ndim
    if ndim == 1 and axes[0]:
        return (axes[0],)
    if ndim == 2 and axes[0] and axes[1]:
        return (axes[1], axes[0])
    if ndim == 3 and all(axes):
        return (axes[1], axes[0], axes[2])
    raise ValueError(
        "Incorrect NetCDF grid coordinates for NDIMS")


def shape_grid(data, mesh, name, squeeze=False):
    shape = grid_shape(mesh)
    if data.size == 1: return data.reshape((1, 1))

    count = int(np.prod(shape))
    if data.size % count:
        if name is None:
            raise ValueError("Invalid grid data size")
        raise ValueError(
            "Invalid NetCDF " + name + " size")

    nvalues = data.size // count
    if squeeze:
        return np.squeeze(
            data.reshape(shape + (nvalues,), order="F")
        )
    if nvalues == 1:
        return data.reshape(shape, order="F")
    return  data.reshape(shape + (nvalues,), order="F")
