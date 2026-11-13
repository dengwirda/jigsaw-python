
import ctypes as ct
import ctypes.util
import numpy as np
import inspect
import platform

from pathlib import Path

from jigsawpy.def_t import indx_t, real_t, fp32_t

from jigsawpy.msh_l import libsaw_VERT2_t, libsaw_VERT3_t, \
    libsaw_EDGE2_t, libsaw_TRIA3_t, \
    libsaw_QUAD4_t, libsaw_TRIA4_t, \
    libsaw_HEXA8_t, libsaw_WEDG6_t, \
    libsaw_PYRA5_t, libsaw_BOUND_t

from jigsawpy.msh_l import libsaw_msh_t
from jigsawpy.jig_l import libsaw_jig_t

from jigsawpy.certify import certify

from jigsawpy.def_t import jigsaw_def_t as defs
from jigsawpy.jig_t import jigsaw_jig_t
from jigsawpy.msh_t import jigsaw_msh_t


_LIB_NAMES = {
    "Windows": "jigsaw.dll",
    "Linux"  : "libjigsaw.so",
    "Darwin" : "libjigsaw.dylib",
}

_LIBRARY = _LIB_NAMES.get(platform.system())
if _LIBRARY is None:
    raise ValueError(
        "Unsupported platform: " + platform.system())

JLIBNAME = Path(
    inspect.getsourcefile(lambda: 0)).resolve().parent
JLIBNAME = JLIBNAME / "_lib" / _LIBRARY
if not JLIBNAME.is_file():
    JLIBNAME = Path(
        ctypes.util.find_library(_LIBRARY) or _LIBRARY)
JLIB = ct.cdll.LoadLibrary(str(JLIBNAME))


_KERNELS = {
    "hfun_scal": {
        "absolute": defs.JIGSAW_HFUN_ABSOLUTE,
        "relative": defs.JIGSAW_HFUN_RELATIVE,
    },
    "bnds_kern": {
        "triacell": defs.JIGSAW_BNDS_TRIACELL,
        "dualcell": defs.JIGSAW_BNDS_DUALCELL,
    },
    "mesh_kern": {
        "delfront": defs.JIGSAW_KERN_DELFRONT,
        "delaunay": defs.JIGSAW_KERN_DELAUNAY,
        "bisector": defs.JIGSAW_KERN_BISECTOR,
    },
    "optm_kern": {
        "odt+dqdx": defs.JIGSAW_KERN_ODT_DQDX,
        "cvt+dqdx": defs.JIGSAW_KERN_CVT_DQDX,
        "h95+dqdx": defs.JIGSAW_KERN_H95_DQDX,
    },
    "optm_cost": {
        "area-len": defs.JIGSAW_KERN_AREA_LEN,
        "skew-cos": defs.JIGSAW_KERN_SKEW_COS,
    },
}

_INTEGER_OPTS = frozenset(
    "verbosity numthread geom_seed mesh_dims mesh_iter "
    "mesh_rule optm_iter".split())
_BOOLEAN_OPTS = frozenset(
    "geom_feat mesh_orph mesh_lock mesh_top1 mesh_top2 "
    "optm_tria optm_dual optm_zip_ optm_div_".split())

_MESH_FLAGS = {
    "euclidean-mesh": defs.JIGSAW_EUCLIDEAN_MESH,
    "euclidean-grid": defs.JIGSAW_EUCLIDEAN_GRID,
    "ellipsoid-mesh": defs.JIGSAW_ELLIPSOID_MESH,
    "ellipsoid-grid": defs.JIGSAW_ELLIPSOID_GRID,
}

# field, dtype, ctypes pointer target, and native deallocator
_MESH_ARRAYS = (
    ("vert2", jigsaw_msh_t.VERT2_t, libsaw_VERT2_t, "vert2"),
    ("vert3", jigsaw_msh_t.VERT3_t, libsaw_VERT3_t, "vert3"),
    ("power", real_t, real_t, "reals"),
    ("edge2", jigsaw_msh_t.EDGE2_t, libsaw_EDGE2_t, "edge2"),
    ("tria3", jigsaw_msh_t.TRIA3_t, libsaw_TRIA3_t, "tria3"),
    ("quad4", jigsaw_msh_t.QUAD4_t, libsaw_QUAD4_t, "quad4"),
    ("tria4", jigsaw_msh_t.TRIA4_t, libsaw_TRIA4_t, "tria4"),
    ("hexa8", jigsaw_msh_t.HEXA8_t, libsaw_HEXA8_t, "hexa8"),
    ("wedg6", jigsaw_msh_t.WEDG6_t, libsaw_WEDG6_t, "wedg6"),
    ("pyra5", jigsaw_msh_t.PYRA5_t, libsaw_PYRA5_t, "pyra5"),
    ("bound", jigsaw_msh_t.BOUND_t, libsaw_BOUND_t, "bound"),
    ("seed2", jigsaw_msh_t.VERT2_t, libsaw_VERT2_t, "vert2"),
    ("seed3", jigsaw_msh_t.VERT3_t, libsaw_VERT3_t, "vert3"),
    ("radii", real_t, real_t, "reals"),
    ("xgrid", real_t, real_t, "reals"),
    ("ygrid", real_t, real_t, "reals"),
    ("zgrid", real_t, real_t, "reals"),
    ("value", fp32_t, fp32_t, "flt32"),
    ("slope", fp32_t, fp32_t, "flt32"),
)


def is_type_t(data, kind):
    return isinstance(
        getattr(data, "tolist", lambda: data)(), kind)


def put_jig_t(jigt, jigl):
    if jigt is None:
        return
    if not isinstance(jigt, jigsaw_jig_t):
        raise TypeError("OPTS not JIG_t")

    for name, options in _KERNELS.items():
        value = getattr(jigt, name)
        if value is None:
            continue
        if isinstance(value, str):
            code = options.get(value.lower())
            if code is None:
                raise ValueError(
                    "Invalid " +
                    name.upper().replace("_", "-") + " value")
            setattr(jigl, name, indx_t(code))
        else:
            raise TypeError(
                name.upper().replace("_", "-") + " type")

    for name, ctype in libsaw_jig_t._fields_:
        if name in _KERNELS:
            continue
        value = getattr(jigt, name)
        if value is None:
            continue

        kind = (int if name in _INTEGER_OPTS else
                bool if name in _BOOLEAN_OPTS else float)
        if not is_type_t(value, kind):
            raise TypeError(
                name.upper().replace("_", "-") + " type")
        setattr(jigl, name, ctype(value))


def put_ptr_t(data, kind):
    return data.ctypes.data_as(ct.POINTER(kind))


def put_msh_t(msht, mshl):
    if msht is None: return

    certify(msht)

    try:
        mshl.flags = _MESH_FLAGS[msht.mshID.lower()]
    except KeyError as error:
        raise ValueError(
            "Invalid MESH.MSHID tag.") from error

    owners = []
    for name, dtype, pointer_type, _ in _MESH_ARRAYS:
        data = getattr(msht, name)
        if data is None or data.size == 0:
            continue

        if name in ("power", "radii",
                    "xgrid", "ygrid", "zgrid",
                    "value", "slope"):
            data = np.asfortranarray(data, dtype=dtype)
        else:
            data = np.ascontiguousarray(data)

        owners.append(data)
        c_array = getattr(mshl, name)
        c_array.size = data.size
        c_array.data = put_ptr_t(data, pointer_type)

        if name in ("power", "value", "slope"):
            setattr(msht, name, data)

    mshl._keepalive = owners


def _copy_and_free(c_array, dtype, free_type):
    try:
        view = np.ctypeslib.as_array(
            c_array.data, shape=(c_array.size,))
        return view.view(dtype).copy()
    finally:
        getattr(JLIB, "jigsaw_free_" + free_type)(
            ct.byref(c_array))


def get_msh_values(data, mesh, stag):
    if data.size == 1:
        return data.reshape((1, 1))

    if mesh.mshID.lower() in ("euclidean-grid", "ellipsoid-grid"):
        x, y, z = mesh.xgrid.size, mesh.ygrid.size, mesh.zgrid.size
        axes = [size for size in (x, y, z) if size]
        if not axes:
            return data

        npos = int(np.prod(axes))
        if data.size % npos:
            raise ValueError("Invalid MESH." + stag + " size")
        nval = data.size // npos

        if len(axes) == 1:
            shape = (axes[0], nval)
        elif x and y and z:
            shape = (y, x, z, nval)
        elif x and y:
            shape = (y, x, nval)
        else:
            shape = tuple(axes) + (nval,)

        data = data.reshape(shape, order="F")
        return data.squeeze(axis=-1) if nval == 1 else data

    point = mesh.point
    if point is not None and point.size:
        if data.size % point.size:
            raise ValueError("Invalid MESH." + stag + " size")
        return data.reshape((point.size, data.size // point.size),
                            order="F")
    return data


def get_msh_t(msht, mshl):
    for name, flag in _MESH_FLAGS.items():
        if mshl.flags == flag:
            msht.mshID = name
            break
    else:
        raise ValueError("Invalid MESH.MSHID flag.")

    for name, dtype, _, free_type in _MESH_ARRAYS:
        c_array = getattr(mshl, name)
        if c_array.size:
            setattr(msht, name, _copy_and_free(
                c_array, dtype, free_type))

    msht.ndims = (
        3 if msht.vert3.size or msht.zgrid.size else
        2 if msht.vert2.size or msht.ygrid.size else
        1 if msht.xgrid.size else 0)

    if msht.power.size and msht.point is not None:
        npoint = msht.point.size
        if msht.power.size % npoint == 0:
            msht.power = msht.power.reshape(
                (npoint, msht.power.size // npoint), order="F")

    msht.value = get_msh_values(msht.value, msht, "VALUE") \
        if msht.value.size else msht.value
    msht.slope = get_msh_values(msht.slope, msht, "SLOPE") \
        if msht.slope.size else msht.slope


def _init_mesh():
    msh = libsaw_msh_t()
    JLIB.jigsaw_init_msh_t(ct.byref(msh))
    return msh


def _init_opts(opts):
    jig = libsaw_jig_t()
    JLIB.jigsaw_init_jig_t(ct.byref(jig))
    put_jig_t(opts, jig)
    return jig


def jigsaw(opts, geom, mesh, init=None, hfun=None):
    """
    JIGSAW API-lib. interface to JIGSAW.

    JIGSAW(OPTS,GEOM,MESH,INIT=None,
                          HFUN=None)

    Call the JIGSAW mesh generator using the config. options
    specified in the OPTS structure.

    OPTS is a user-defined set of meshing options. See JIG_t
    for details.

    """
    jig = _init_opts(opts)
    gmsh, mmsh, imsh, hmsh = (
        _init_mesh(), _init_mesh(), _init_mesh(), _init_mesh())
    put_msh_t (geom, gmsh)
    put_msh_t (init, imsh)
    put_msh_t (hfun, hmsh)

    retv = JLIB.jigsaw(
        ct.byref(jig), ct.byref(gmsh),
        ct.byref(imsh) if init is not None else 0,
        ct.byref(hmsh) if hfun is not None else 0,
        ct.byref(mmsh))
    if retv:
        JLIB.jigsaw_free_msh_t(ct.byref(mmsh))
        raise ValueError("JIGSAW returned code: " + str(retv))
    get_msh_t(mesh, mmsh)


def tripod(opts, init, tria, geom=None):
    """
    TRIPOD API-lib. interface to TRIPOD.

    TRIPOD(OPTS,INIT,TRIA,GEOM=None)

    Call the TRIPOD tessellation util. using the config. opt
    specified in the OPTS structure.

    OPTS is a user-defined set of meshing options. See JIG_t
    for details.

    """
    jig = _init_opts(opts)
    imsh, tmsh, gmsh = _init_mesh(), _init_mesh(), _init_mesh()
    put_msh_t (init, imsh)
    put_msh_t (geom, gmsh)

    retv = JLIB.tripod(
        ct.byref(jig), ct.byref(imsh),
        ct.byref(gmsh) if geom is not None else 0,
        ct.byref(tmsh))
    if retv:
        JLIB.jigsaw_free_msh_t(ct.byref(tmsh))
        raise ValueError("TRIPOD returned code: " + str(retv))
    get_msh_t(tria, tmsh)


def marche(opts, ffun):
    """
    MARCHE API-lib. interface to MARCHE.

    MARCHE(OPTS,FFUN=None)

    Call the "fast-marching" solver MARCHE using the config.
    options specified in the OPTS structure. MARCHE solves
    the Eikonal equations

    MAX(||dh/dx||, g) = g,

    where g = g(x) is a gradient threshold applied to h. See
    the SAVEMSH/LOADMSH functions for a description of the
    HFUN output structure.

    OPTS is a user-defined set of meshing options. See JIG_t
    for details.

    """
    jig = _init_opts(opts)
    fmsh = _init_mesh()
    put_msh_t (ffun, fmsh)

    retv = JLIB.marche(ct.byref(jig), ct.byref(fmsh))
    if retv:
        raise ValueError("MARCHE returned code: " + str(retv))
