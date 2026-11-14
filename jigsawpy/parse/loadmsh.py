
from pathlib import Path
import numpy as np
from numpy.lib import recfunctions as rfn

from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.parse.utility import shape_grid


_CELL_TYPES = {
    "EDGE2": ("edge2", 3, jigsaw_msh_t.EDGE2_t),
    "TRIA3": ("tria3", 4, jigsaw_msh_t.TRIA3_t),
    "QUAD4": ("quad4", 5, jigsaw_msh_t.QUAD4_t),
    "TRIA4": ("tria4", 5, jigsaw_msh_t.TRIA4_t),
    "HEXA8": ("hexa8", 9, jigsaw_msh_t.HEXA8_t),
    "WEDG6": ("wedg6", 7, jigsaw_msh_t.WEDG6_t),
    "PYRA5": ("pyra5", 6, jigsaw_msh_t.PYRA5_t),
    "BOUND": ("bound", 3, jigsaw_msh_t.BOUND_t),
}

def _read_rows(fptr, nrows, ncols, dtype):
    lines = []
    for _ in range(nrows):
        lines.append(fptr.readline())
    text = " ".join(lines).replace("\n", ";")
    data = np.fromstring(text, dtype=dtype, sep=";")
    return data.reshape((nrows, ncols), order="C")


def _read_data(fptr, nrows, ncols, dtype, out_dtype):
    data = _read_rows(fptr, nrows, ncols, dtype)
    return rfn.unstructured_to_structured(
        data, dtype=out_dtype, align=True)


def _load_cell(mesh, fptr, ltag, kind):
    name, ncols, dtype = _CELL_TYPES[kind]
    setattr(mesh, name, _read_data(
        fptr, int(ltag[+1]), ncols, np.int32, dtype))


def _shape_val(mesh, data):
    if data is not None and data.size > 1:
        if mesh.ndims in (2, 3):
            for axis in ("xgrid", "ygrid", 
                         "zgrid")[:mesh.ndims]:
                coords = getattr(mesh, axis)
                if coords is None or coords.size == 0:
                    raise ValueError(
                        "Invalid " + axis.upper())

            data = shape_grid(data, mesh, 
                              None, squeeze=False)
    return  data


def loadmshid(mesh, fptr, ltag):
    """
    LOADMSHID: load the MSHID data segment from file.

    """
    data = ltag[1].split(";")
    if (len(data) > 1):
        mesh.mshID = data[1].strip().lower()


def loadradii(mesh, fptr, ltag):
    """
    LOADRADII: load the RADII data segment from file.

    """
    rtag = ltag[1].split(";")

    mesh.radii = np.empty(
        +3, dtype=jigsaw_msh_t.REALS_t)

    if   (len(rtag) == +1):
        mesh.radii[0] = float(rtag[0])
        mesh.radii[1] = float(rtag[0])
        mesh.radii[2] = float(rtag[0])

    elif (len(rtag) == +3):
        mesh.radii[0] = float(rtag[0])
        mesh.radii[1] = float(rtag[1])
        mesh.radii[2] = float(rtag[2])

    else:
        raise ValueError("Invalid RADII: " + ltag)


def loadvert2(fptr, ltag):
    """
    LOADVERT2: load the 2-dim. vertex pos. from file.

    """
    return _read_data(fptr, int(ltag[1]),
        3, np.float64, jigsaw_msh_t.VERT2_t)


def loadvert3(fptr, ltag):
    """
    LOADVERT3: load the 3-dim. vertex pos. from file.

    """
    return _read_data(fptr, int(ltag[1]),
        4, np.float64, jigsaw_msh_t.VERT3_t)


def loadpoint(mesh, fptr, ltag):
    """
    LOADPOINT: load the POINT data segment from file.

    """
    if   (mesh.ndims == +2):
        mesh.vert2 = loadvert2(fptr, ltag)

    elif (mesh.ndims == +3):
        mesh.vert3 = loadvert3(fptr, ltag)

    else:
        raise ValueError("Invalid NDIMS: " + ltag)


def loadseeds(mesh, fptr, ltag):
    """
    LOADSEEDS: load the SEEDS data segment from file.

    """
    if   (mesh.ndims == +2):
        mesh.seed2 = loadvert2(fptr, ltag)

    elif (mesh.ndims == +3):
        mesh.seed3 = loadvert3(fptr, ltag)

    else:
        raise ValueError("Invalid NDIMS: " + ltag)


def loadarray(fptr, ltag, kind):
    """
    LOADARRAY: load the ARRAY data segment from file.

    """
    nrows, ncols = map(int, ltag[1].split(";")[:2])
    return _read_rows(fptr, nrows, ncols, kind)


def loadpower(mesh, fptr, ltag):
    """
    LOADPOWER: load the POWER data segment from file.

    """
    mesh.power = loadarray(fptr, ltag, mesh.REALS_t)


def loadvalue(mesh, fptr, ltag):
    """
    LOADVALUE: load the VALUE data segment from file.

    """
    mesh.value = loadarray(fptr, ltag, mesh.FLT32_t)


def loadslope(mesh, fptr, ltag):
    """
    LOADSLOPE: load the SLOPE data segment from file.

    """
    mesh.slope = loadarray(fptr, ltag, mesh.FLT32_t)


def loadcoord(mesh, fptr, ltag):
    """
    LOADCOORD: load the COORD data segment from file.

    """
    ndim, nrow = map(int, ltag[1].split(";")[:2])
    mesh.ndims = max(mesh.ndims, ndim)
    values = _read_rows(
        fptr, nrow, 1, np.float64).reshape((nrow,))

    if   ndim == 1:
        mesh.xgrid = values
    elif ndim == 2:
        mesh.ygrid = values
    elif ndim == 3:
        mesh.zgrid = values


def loadlines(mesh, fptr, line):
    """
    LOADLINES: load the next non-null line from file.

    """
    line = line.strip()
    if (not line): return

    if (line[0] != "#"):
        ltag = line.split("=")
        kind = ltag[0].upper().strip()

        if   kind == "MSHID":
            loadmshid(mesh, fptr, ltag)

        elif kind == "NDIMS":
            mesh.ndims = int(ltag[1])

        elif kind == "RADII":
            loadradii(mesh, fptr, ltag)

        elif kind == "POINT":
            loadpoint(mesh, fptr, ltag)

        elif kind == "SEEDS":
            loadseeds(mesh, fptr, ltag)

        elif kind == "POWER":
            loadpower(mesh, fptr, ltag)

        elif kind == "VALUE":
            loadvalue(mesh, fptr, ltag)

        elif kind == "SLOPE":
            loadslope(mesh, fptr, ltag)

        elif kind == "EDGE2":
            _load_cell(mesh, fptr, ltag, "EDGE2")

        elif kind == "TRIA3":
            _load_cell(mesh, fptr, ltag, "TRIA3")

        elif kind == "QUAD4":
            _load_cell(mesh, fptr, ltag, "QUAD4")

        elif kind == "TRIA4":
            _load_cell(mesh, fptr, ltag, "TRIA4")

        elif kind == "HEXA8":
            _load_cell(mesh, fptr, ltag, "HEXA8")

        elif kind == "PYRA5":
            _load_cell(mesh, fptr, ltag, "PYRA5")

        elif kind == "WEDG6":
            _load_cell(mesh, fptr, ltag, "WEDG6")

        elif kind == "BOUND":
            _load_cell(mesh, fptr, ltag, "BOUND")

        elif kind == "COORD":
            loadcoord(mesh, fptr, ltag)


def loadmsh(name, mesh):
    with Path(name).open("r") as fptr:
        while True:
    #--------------------------- get the next line from file
            line = fptr.readline()

            if (len(line) != 0):
    #--------------------------- parse next non-null section
                loadlines(mesh, fptr, line)

            else:
    #--------------------------- reached end-of-file: done!!
                break

    if (mesh.mshID.lower() in ["euclidean-grid", 
                               "ellipsoid-grid"]):
    #--------------------------- from flat to multi-dim data
        mesh.value = _shape_val(mesh, mesh.value)
        mesh.slope = _shape_val(mesh, mesh.slope)
