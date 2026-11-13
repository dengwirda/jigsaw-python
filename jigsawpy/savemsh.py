
from pathlib import Path
import numpy as np
from numpy.lib import recfunctions as rfn

from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.certify import certify


_CHUNK_ROWS = 2 ** 19
_MESH_RECORDS = (
    ("edge2", "EDGE2", 3),
    ("tria3", "TRIA3", 4),
    ("quad4", "QUAD4", 5),
    ("tria4", "TRIA4", 5),
    ("hexa8", "HEXA8", 9),
    ("wedg6", "WEDG6", 7),
    ("pyra5", "PYRA5", 6),
    ("bound", "BOUND", 3),
)

def _write_rows(fptr, data, nrows, formats, dtype=None):
    row_format = ";".join(formats) + "\n"

    start = 0
    while start < nrows:
        end = min(start + _CHUNK_ROWS, nrows)
        rows = data[start:end]
        if dtype is not None:
            values = rfn.structured_to_unstructured(
                rows, dtype=dtype).ravel()
        else:
            values = rows.ravel()

        text_format = row_format * (end - start)
        fptr.write(text_format % tuple(values))
        start = end


def _write_data(ftag, data, fptr, formats, dtype):
    fptr.write(ftag + "=" + str(data.size) + "\n")
    _write_rows(fptr, data, data.size, formats, dtype)


def _save_cells(data, fptr, ftag, ncols):
    _write_data(ftag, data, fptr, ["%d"] * ncols, np.int32)


def saveradii(mesh, fptr):
    """
    SAVERADII: save the RADII data structure to *.msh file.

    """
    if   (mesh.radii.size == +3):
        fptr.write(
            "RADII="
            f"{mesh.radii[0]:.17g};"
            f"{mesh.radii[1]:.17g};"
            f"{mesh.radii[2]:.17g}\n")

    elif (mesh.radii.size == +1):
        fptr.write(
            "RADII="
            f"{mesh.radii[0]:.17g};"
            f"{mesh.radii[0]:.17g};"
            f"{mesh.radii[0]:.17g}\n")

    return


def savevert2(ftag, data, fptr):
    """
    SAVEVERT2: save the POINT data structure to *.msh file.

    """
    _write_data(ftag, data, fptr,
        ["%.17g", "%.17g", "%d"], np.float64)


def savevert3(ftag, data, fptr):
    """
    SAVEVERT3: save the POINT data structure to *.msh file.

    """
    _write_data(ftag, data, fptr,
        ["%.17g", "%.17g", "%.17g", "%d"], np.float64)


def savevalue(ftag, data, fptr):
    """
    SAVEVALUE: save the ARRAY data structure to *.msh file.

    """
    if data.ndim == 1:
        data = data.reshape((data.size, 1))

    prec = 9 if data.dtype == np.float32 else 17

    nrows, ncols = data.shape
    fptr.write(f"{ftag}={nrows};{ncols}\n")
    _write_rows(fptr, data, nrows,  [f"%.{prec}g"] * ncols)


def savecoord(data, fptr, inum):
    """
    SAVECOORD: save the COORD data structure to *.msh file.

    """
    fptr.write(f"COORD={inum};{data.size}\n")
    _write_rows(fptr, data, data.size, ["%.17g"])


def savendmat(ftag, data, fptr):
    """
    SAVENDMAT: save the VALUE data structure to *.msh file.

    """
    fptr.write(f"{ftag}={data.size}; 1\n")

    prec = 9 if data.dtype == np.float32 else 17

    vals = data.reshape(-1, order="F")
    _write_rows(fptr, vals, vals.size, [f"%.{prec}g"])


def save_mesh_file(mesh, fptr, args, kind):
    fptr.write("MSHID=" + str(args.nver) + ";" + kind + "\n")

    ndim = 0
    if mesh.vert2 is not None and mesh.vert2.size:
       ndim = +2
    if mesh.vert3 is not None and mesh.vert3.size:
       ndim = +3
    if mesh.seed2 is not None and mesh.seed2.size:
       ndim = +2
    if mesh.seed3 is not None and mesh.seed3.size:
       ndim = +3

    if ndim == 2: fptr.write("NDIMS=2\n")
    if ndim == 3: fptr.write("NDIMS=3\n")

    if mesh.radii is not None and mesh.radii.size:
        saveradii(mesh, fptr)

    if mesh.vert2 is not None and mesh.vert2.size:
        savevert2("POINT", mesh.point, fptr)
    if mesh.vert3 is not None and mesh.vert3.size:
        savevert3("POINT", mesh.point, fptr)
    if mesh.seed2 is not None and mesh.seed2.size:
        savevert2("SEEDS", mesh.seeds, fptr)
    if mesh.seed3 is not None and mesh.seed3.size:
        savevert3("SEEDS", mesh.seeds, fptr)

    for name in ("power", "value", "slope"):
        data = getattr(mesh, name)
        if data is not None and data.size:
            savevalue(name.upper(), data, fptr)

    for name, tag, ncols in _MESH_RECORDS:
        data = getattr(mesh, name)
        if data is not None and data.size:
            _save_cells(data, fptr, tag, ncols)


def save_grid_file(mesh, fptr, args, kind):
    fptr.write("MSHID=" + str(args.nver) + ";" + kind + "\n")

    if mesh.radii is not None and mesh.radii.size:
        saveradii(mesh, fptr)

    coordinates = (
        ("xgrid",1), ("ygrid",2), ("zgrid",3))
    present = [
        (getattr(mesh, name), axis)
        for name, axis in coordinates
        if getattr(mesh, name) is not None and
           getattr(mesh, name).size
    ]
    if present:
        fptr.write(f"NDIMS={len(present)}\n")
    for data, axis in present:
        savecoord(data, fptr, axis)

    for name in ("value", "slope"):
        data = getattr(mesh, name)
        if data is not None and data.size:
            savendmat(name.upper(), data, fptr)


def savemsh(name, mesh):
    """
    SAVEMSH: save a JIGSAW MSH object to file.

    SAVEMSH(NAME, MESH)

    MESH is JIGSAW's primary mesh/grid/geom class. See MSH_t
    for details.

    Data in MESH is written as-needed -- any objects defined
    will be saved to file.

    """
    if (not isinstance(name, str)):
        raise TypeError("Incorrect type: NAME.")

    if (not isinstance(mesh, jigsaw_msh_t)):
        raise TypeError("Incorrect type: MESH.")

    certify(mesh)

    class stub(object): pass

    args = stub()                           ## savmsh params
    args.kind = "ascii"
    args.nver = 3

    fext = Path(name).suffix

    if (fext.strip() != ".msh"): name += ".msh"

    kind = mesh.mshID.lower()

    with Path(name).open("w") as fptr:
    #----------------------------------- write JIGSAW object
        fptr.write(
            "# " + Path(name).name +
            "; created by JIGSAW's PYTHON interface \n")

        if (kind == "euclidean-mesh"):
            save_mesh_file(
                mesh, fptr, args, "euclidean-mesh")

        if (kind == "euclidean-grid"):
            save_grid_file(
                mesh, fptr, args, "euclidean-grid")

        if (kind == "ellipsoid-mesh"):
            save_mesh_file(
                mesh, fptr, args, "ellipsoid-mesh")

        if (kind == "ellipsoid-grid"):
            save_grid_file(
                mesh, fptr, args, "ellipsoid-grid")
