
import numpy as np

from jigsawpy.parse.utility import (
    CELL_TYPES, GRID_KINDS, MESH_KINDS, netcdf_dataset, shape_grid,
)
from jigsawpy.msh_t import jigsaw_msh_t


def _array(nc, name, dtype):
    variable = nc.variables[name]
    variable.set_auto_maskandscale(False)
    data = np.asarray(variable[:])
    target = np.dtype(dtype)
    if data.dtype.kind not in "iuf":
        raise TypeError(
            "Invalid NetCDF " + name + " data type")
    if target.kind == "i":
        limits = np.iinfo(target)
        if (not np.isfinite(data).all() or
                np.any(data < limits.min) or 
                np.any(data > limits.max) ):
            raise ValueError(
                "Out-of-range NetCDF " + name + " data")
    elif target.itemsize < data.dtype.itemsize:
        limits = np.finfo(target)
        if np.any(np.isfinite(data) & (np.abs(data) > limits.max)):
            raise ValueError(
                "Out-of-range NetCDF " + name + " data")
    return data.astype(target, copy=False)


def _header(nc):
    if "MSHID" not in nc.ncattrs():
        raise ValueError("Missing NetCDF MSHID attribute")
    kind = nc.getncattr("MSHID")
    if isinstance(kind, bytes):
        kind = kind.decode("ascii")
    if not isinstance(kind, str):
        raise ValueError("Invalid NetCDF MSHID attribute")
    kind = kind.strip(" \x00").lower()
    if kind not in MESH_KINDS + GRID_KINDS:
        raise ValueError("Unsupported NetCDF MSHID: " + kind)

    if "NDIMS" in nc.ncattrs():
        value = np.asarray(nc.getncattr("NDIMS"))
        if value.size != 1 or value.dtype.kind not in "iu":
            raise ValueError("Invalid NetCDF NDIMS attribute")
        ndim = int(value.reshape(-1)[0])
    else:
        ndim = 0
        for name, dim in (("xgrid_val", 1), ("ygrid_val", 2),
                          ("zgrid_val", 3), ("vert2_pos", 2),
                          ("seed2_pos", 2), ("vert3_pos", 3),
                          ("seed3_pos", 3)):
            if name in nc.variables: ndim = dim
    if ndim not in (1, 2, 3):
        raise ValueError("Missing or invalid NetCDF NDIMS")
    return kind, ndim


def _records(nc, name, dtype, width, field):
    if   field == "coord":
        data_name = name + "_pos"
        itag_name = name + "_tag"
    elif field == "index":
        data_name = name + "_idx"
        itag_name = name + "_tag"
    else:
        raise ValueError("Invalid NetCDF variable")

    if (data_name not in nc.variables and
        itag_name not in nc.variables):
        return None

    if (data_name not in nc.variables or
        itag_name not in nc.variables):
        raise ValueError(
            "NetCDF requires both " + data_name + " and " 
                                    + itag_name)
    if   field == "coord":
        data = _array(nc, data_name, np.float64)
        tags = _array(nc, itag_name, np.int32)
    elif field == "index":
        data = _array(nc, data_name, np.int32)
        tags = _array(nc, itag_name, np.int32)
    else:
        raise ValueError("Invalid NetCDF variable")

    if data.ndim != 2 or data.shape[1] != width:
        raise ValueError(
            "Invalid NetCDF " + data_name + " dimensions")
    if tags.shape not in ((data.shape[0],), 
                          (data.shape[0], 1)):
        raise ValueError(
            "Invalid NetCDF " + itag_name + " dimensions")

    records = np.empty(data.shape [0], dtype=dtype)
    records[ field ] = data
    records["IDtag"] = tags.reshape(-1)
    return records


def _values(nc, name, mesh, dtype):
    if name not in nc.variables: return None
    data = _array(nc, name, dtype)
    if data.ndim <= 0 or (
       data.ndim == 2 and data.shape[1] == 0):
        raise ValueError(
            "Invalid NetCDF " + name + " dimensions")
    if name == "power_val" and data.ndim > 2:
        raise ValueError(
            "Invalid NetCDF power_val dimensions")

    if mesh.mshID in GRID_KINDS and \
           name != "power_val":
        return shape_grid(data.reshape(-1, order="C"), 
                          mesh, name)
    if data.ndim >= 3:
        return data.reshape(-1, 1, order="C")
    if data.ndim == 1:
        return data.reshape(-1, 1)
    return data


def loadradii(nc, mesh):
    if "RADII" in nc.ncattrs():
        radii = np.asarray(
            nc.getncattr("RADII"), dtype=np.float64)
        if radii.shape != (3,):
            raise ValueError("Invalid NetCDF RADII variable")
        mesh.radii = radii.copy()


def loadpoint(nc, mesh):
    for prefix in ("vert", "seed"):
        name = prefix + str(mesh.ndims)
        if   mesh.ndims == 2:
            dtype = mesh.VERT2_t
        elif mesh.ndims == 3:
            dtype = mesh.VERT3_t
        else:
            raise ValueError("Invalid NetCDF " + name + 
                             " dimensions")
        data = _records(nc, name, dtype, mesh.ndims, "coord")
        if data is not None: setattr(mesh, name, data)


def loadcoord(nc, mesh):
    for axis, index in (("xgrid", 1), ("ygrid", 2), 
                        ("zgrid", 3)):
        name = axis + "_val"
        if name in nc.variables:
            data = _array(nc, name, np.float64)
            if index > mesh.ndims:
                raise ValueError(
                    "Invalid NetCDF " + name + " dimensions")
            if data.ndim not in (1, 2):
                raise ValueError(
                    "Invalid NetCDF " + name + " dimensions")
            if data.ndim == 2 and data.shape[1] != 1:
                raise ValueError(
                    "Invalid NetCDF " + name + " dimensions")
            setattr(mesh, axis, data.reshape(-1))


def loadbound(nc, mesh):
    if "bound_idx" in nc.variables:
        data = _array(nc, "bound_idx", np.int32)
        if data.ndim != 2 or data.shape[1] != 3:
            raise ValueError(
                "Incorrect NetCDF bound_idx dimension")
        mesh.bound = np.empty(
            data.shape[0], dtype=mesh.BOUND_t)
        mesh.bound["IDtag"] = data[:, 0]
        mesh.bound["index"] = data[:, 1]
        mesh.bound["cells"] = data[:, 2]


def loadvalue(nc, mesh):
    for field, key, dtype in (
            ("power", "power_val", np.float64),
            ("value", "value_mat", np.float32),
            ("slope", "slope_mat", np.float32)):
        data = _values(nc, key, mesh, dtype)
        if data is not None: setattr(mesh, field, data)


def load_nc(name, mesh):
    dataset = netcdf_dataset()
    with dataset(name, "r") as nc:
        kind, ndim = _header(nc)
        mesh.mshID, mesh.ndims = kind, ndim
        
        if kind in ["ellipsoid-mesh", "ellipsoid-grid"]:
            loadradii(nc, mesh)

        if ndim >= 2:
            loadpoint(nc, mesh)

        if kind in ["ellipsoid-grid", "euclidean-grid"]:
            loadcoord(nc, mesh)

        for cell, width, dtype in CELL_TYPES:
            data = _records(
                nc, cell, dtype, width, "index")
            if data is not None: setattr(mesh, cell, data)

        loadbound(nc, mesh)

        loadvalue(nc, mesh)
