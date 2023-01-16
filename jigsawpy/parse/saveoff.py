
import warnings
from pathlib import Path

from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.certify import certify


def savepoint(data, fptr, ndim):
    """
    SAVEPOINT: save the POINT data structure to *.off file.

    """
    rmax = 2 ** 19; next = 0

    while (next < data.shape[0]):

        nrow = min(rmax, data.shape[0] - next)
        nend = next + nrow

        sfmt = " ".join(["%.17g"] * ndim)

        if (ndim < 3): sfmt = sfmt + " 0"

        sfmt = sfmt + "\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(data[next:nend, :].ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def savecells(data, fptr, nnod):
    """
    SAVECELLS: save the CELLS data structure to *.off file.

    """
    rmax = 2 ** 19; next = 0

    while (next < data.shape[0]):

        nrow = min(rmax, data.shape[0] - next)
        nend = next + nrow

        sfmt = " ".join(["%d"] * nnod) + "\n"
        sfmt = str(nnod) + " " + sfmt
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(data[next:nend, :].ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def save_mesh_file(mesh, fptr):
    """
    SAVE-MESH-FILE: save a JIGSAW mesh object to *.OFF file.

    """
    nnum = {
        "PT": 0, "E2": 0, "T3": 0,
        "Q4": 0, "T4": 0, "H8": 0,
        "W6": 0, "P5": 0}

    if (mesh.vert2 is not None):
        nnum["PT"] += mesh.vert2.size
    if (mesh.vert3 is not None):
        nnum["PT"] += mesh.vert3.size

    if (mesh.edge2 is not None):
        nnum["E2"] += mesh.edge2.size

    if (mesh.tria3 is not None):
        nnum["T3"] += mesh.tria3.size
    if (mesh.quad4 is not None):
        nnum["Q4"] += mesh.quad4.size

    if (mesh.tria4 is not None):
        nnum["T4"] += mesh.tria4.size
    if (mesh.hexa8 is not None):
        nnum["H8"] += mesh.hexa8.size
    if (mesh.wedg6 is not None):
        nnum["W6"] += mesh.wedg6.size
    if (mesh.pyra5 is not None):
        nnum["P5"] += mesh.pyra5.size

    fptr.write("OFF \n")
    fptr.write(
        "# " + Path(fptr.name).name +
        "; created by JIGSAW's Python interface \n")

    nnode = nnum["PT"]
    nedge = +0
    nface = nnum["T3"] + nnum["Q4"]

    fptr.write(str(nnode) + " " +
               str(nface) + " " + str(nedge) + "\n")

    if (mesh.vert2 is not None):
        savepoint(
            mesh.vert2["coord"], fptr, +2)

    if (mesh.vert3 is not None):
        savepoint(
            mesh.vert3["coord"], fptr, +3)

    if (mesh.edge2 is not None and
            mesh.edge2.size != +0):
        warnings.warn(
            "EDGE2 elements not supported", Warning)

    if (mesh.tria3 is not None):
        savecells(
            mesh.tria3["index"], fptr, +3)

    if (mesh.quad4 is not None):
        savecells(
            mesh.quad4["index"], fptr, +4)

    if (mesh.tria4 is not None and
            mesh.tria4.size != +0):
        warnings.warn(
            "TRIA4 elements not supported", Warning)

    if (mesh.hexa8 is not None and
            mesh.hexa8.size != +0):
        warnings.warn(
            "HEXA8 elements not supported", Warning)

    if (mesh.wedg6 is not None and
            mesh.wedg6.size != +0):
        warnings.warn(
            "WEDG6 elements not supported", Warning)

    if (mesh.pyra5 is not None and
            mesh.pyra5.size != +0):
        warnings.warn(
            "PYRA5 elements not supported", Warning)

    return


def saveoff(name, mesh):
    """
    SAVEOFF: save a JIGSAW MSH object to file.

    SAVEOFF(NAME, MESH)

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

    fext = Path(name).suffix

    if (fext.strip() != ".off"): name += ".off"

    kind = mesh.mshID.lower()

    with Path(name).open("w") as fptr:
    #----------------------------------- write JIGSAW object
        if   (kind == "euclidean-mesh"):

            save_mesh_file(mesh, fptr)

        elif (kind == "ellipsoid-mesh"):

            save_mesh_file(mesh, fptr)

        else:
            raise ValueError(
                "MESH.mshID is not supported!!")

    return
