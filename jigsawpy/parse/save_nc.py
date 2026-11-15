
from pathlib import Path

import numpy as np

from jigsawpy.parse.utility import (
    CELL_TYPES, GRID_KINDS, MESH_KINDS,
)
from jigsawpy.parse.utility import (
    netcdf_dataset, present, grid_shape,
)
from jigsawpy.certify import certify
from jigsawpy.msh_t import jigsaw_msh_t


def _write_variable(nc, name, data, dimensions, dtype):
    nc.createVariable(
        name, dtype, dimensions)[:] = data


def _write_verts(nc, name, data, ndim):
    if not present(data): return
    row, col = name + "_row", name + "_col"
    ids = "singleton"
    nc.createDimension(row, data.size)
    nc.createDimension(col, ndim)
    _write_variable(
        nc, name + "_pos", data["coord"], (row, col), "f8")
    _write_variable(
        nc, name + "_tag", data["IDtag"], (row, ids), "i4")


def _write_cells(nc, name, data, width):
    if not present(data): return
    row, col = name + "_row", name + "_col"
    ids = "singleton"
    nc.createDimension(row, data.size)
    nc.createDimension(col, width)
    _write_variable(
        nc, name + "_idx", data["index"], (row, col), "i4")
    _write_variable(
        nc, name + "_tag", data["IDtag"], (row, ids), "i4")


def _write_values(nc, name, data, mesh, ndim, grid):
    if not present(data): return
    if grid:
        shape = grid_shape(mesh, ndim)
        if data.size == 1 and np.prod(shape) != 1:
            data = data.reshape(1)
            dim = ("singleton",)
        else:
            if   ndim == 1:
                dim = ("xgrid_row",)
            elif ndim == 2:
                dim = ("xgrid_row", "ygrid_row")
            else:
                dim = ("zgrid_row", "xgrid_row", 
                       "ygrid_row",)
            data = np.asarray(data).reshape(-1, order="F")
            data = data.reshape(
                tuple(len(nc.dimensions[d]) for d in dim))

        dtype = "f8" if name == "power_val" else "f4"

        _write_variable(nc, name, data, dim, dtype)
    else:
        vert = "vert" + str(ndim) + "_row"
        if data.size == 1:
            row = "singleton"
        elif vert in nc.dimensions and \
                data.shape[0] == len(nc.dimensions[vert]):
            row = vert
        else:
            raise ValueError(
                "Incorrect NetCDF "
                    + name + " size for vert" + str(ndim))

        dim = (row, "singleton")

        dtype = "f8" if name == "power_val" else "f4"

        _write_variable(nc, name, data, tuple(dim), dtype)


def _write_coord(nc, mesh):
    for axis in ("xgrid", "ygrid", "zgrid"):
        values = getattr(mesh, axis)
        name_val = axis + "_val"
        name_dim = axis + "_row"
        if present(values):
            nc.createDimension(name_dim, values.size)
            _write_variable(
                nc, name_val, values, (name_dim,), "f8")


def _write_bound(nc, mesh):
    if present(mesh.bound):
        nc.createDimension("bound_row", mesh.bound.size)
        nc.createDimension("bound_col", 3)
        bound = np.column_stack((mesh.bound["IDtag"],
                                 mesh.bound["index"],
                                 mesh.bound["cells"]))
        _write_variable(
            nc, "bound_idx", bound, ("bound_row", 
                                     "bound_col"), "i4")


def save_nc(name, mesh):
    certify(mesh)
    dataset = netcdf_dataset()

    kind = mesh.mshID.lower()
    ndim = 0
    if present(getattr(mesh, "xgrid")): ndim = 1
    if present(getattr(mesh, "ygrid")): ndim = 2
    if present(getattr(mesh, "zgrid")): ndim = 3

    if present(getattr(mesh, "vert2")): ndim = 2
    if present(getattr(mesh, "vert3")): ndim = 3

    if present(getattr(mesh, "seed2")): ndim = 2
    if present(getattr(mesh, "seed3")): ndim = 3

    if (not isinstance(mesh.ndims, (int, np.integer)) or
            isinstance(mesh.ndims, (bool, np.bool_))):
        raise ValueError("Invalid MESH.NDIMS")

    if not ndim:
        ndim = mesh.ndims
        if not ndim and kind == "ellipsoid-mesh" and \
                present(mesh.radii):
            ndim = 3
    elif mesh.ndims not in (0,ndim):
        raise ValueError("Inconsistent MESH.NDIMS")

    if ndim <= 0:
        raise ValueError("Invalid MESH.NDIMS")

    with dataset(name, "w", format="NETCDF4") as nc:
        nc.createDimension("singleton", +1)

        nc.setncattr("MSHID", kind.upper())
        nc.setncattr("NDIMS", np.int32(ndim))

        title = Path(name).name \
                + "; created by JIGSAW's PYTHON interface"
        nc.setncattr("title", title)
        
        if present(mesh.radii):
            nc.setncattr("RADII", mesh.radii)

        if kind in MESH_KINDS and ndim > 1:
            name = "vert" + str(ndim)
            _write_verts(
                nc, name, getattr(mesh, name), ndim)

            name = "seed" + str(ndim)
            _write_verts(
                nc, name, getattr(mesh, name), ndim)

            _write_values(nc, "power_val", mesh.power, 
                          mesh, ndim, kind in GRID_KINDS)

        if kind in MESH_KINDS:
            for cell, width, _ in CELL_TYPES:
                _write_cells(
                    nc, cell, getattr(mesh, cell), width)

            _write_bound(nc, mesh)

            _write_values(nc, "value_mat", mesh.value, 
                          mesh, ndim, kind in GRID_KINDS)
            _write_values(nc, "slope_mat", mesh.slope, 
                          mesh, ndim, kind in GRID_KINDS)

        if kind in GRID_KINDS:
            _write_coord(nc, mesh)

            _write_values(nc, "value_mat", mesh.value, 
                          mesh, ndim, kind in GRID_KINDS)
            _write_values(nc, "slope_mat", mesh.slope, 
                          mesh, ndim, kind in GRID_KINDS)
