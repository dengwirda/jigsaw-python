
import warnings
from pathlib import Path
import numpy as np

from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.certify import certify


def savepoint(data, fptr, ndim, ctag):
    """
    SAVEPOINT: save the POINT data structure to *.obj file.

    """
    rmax = 2 ** 19; next = 0

    while (next < data.shape[0]):

        nrow = min(rmax, data.shape[0] - next)
        nend = next + nrow

        sfmt = " ".join(["%.17g"] * ndim)

        if (ndim < 3): sfmt = sfmt + " 0"

        sfmt = ctag + sfmt
        sfmt = sfmt + "\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(data[next:nend, :].ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def savecells(data, fptr, nnod, ctag):
    """
    SAVECELLS: save the CELLS data structure to *.obj file.

    """
    rmax = 2 ** 19; next = 0

    indx = np.array(data[:, :]) + 1

    while (next < data.shape[0]):

        nrow = min(rmax, data.shape[0] - next)
        nend = next + nrow

        sfmt = " ".join(["%d"] * nnod) + "\n"
        sfmt = ctag + sfmt
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(indx[next:nend, :].ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def save_mesh_file(mesh, fptr):
    """
    SAVE-MESH-FILE: save a JIGSAW mesh object to *.OBJ file.

    """
    fptr.write(
        "# " + Path(fptr.name).name
        + "; created by JIGSAW's Python interface \n")

    if (mesh.vert2 is not None):
        savepoint(
            mesh.vert2["coord"], fptr, 2, "v ")

    if (mesh.vert3 is not None):
        savepoint(
            mesh.vert3["coord"], fptr, 3, "v ")

    if (mesh.edge2 is not None):
        savecells(
            mesh.edge2["index"], fptr, 2, "l ")

    if (mesh.tria3 is not None):
        savecells(
            mesh.tria3["index"], fptr, 3, "f ")

    if (mesh.quad4 is not None):
        savecells(
            mesh.quad4["index"], fptr, 4, "f ")

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


def savewav(name, mesh):
    """
    SAVEWAV: save a JIGSAW MSH object to file.

    SAVEWAV(NAME, MESH)

    MESH is JIGSAW's primary mesh/grid/geom class. See MSH_t
    for details.

    Data in MESH is written as-needed -- any objects defined
    will be saved to file.

    """

    if (not isinstance(name, str)):
        raise Exception("Incorrect type: NAME.")

    if (not isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    certify(mesh)

    fext = Path(name).suffix

    if (fext.strip() != ".obj"): name += ".obj"

    kind = mesh.mshID.lower()

    with Path(name).open("w") as fptr:
    #----------------------------------- write JIGSAW object
        if   (kind == "euclidean-mesh"):

            save_mesh_file(mesh, fptr)

        elif (kind == "ellipsoid-mesh"):

            save_mesh_file(mesh, fptr)

        else:
            raise Exception(
                "MESH.mshID is not supported!!")

    return
