
import warnings
from pathlib import Path

from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.certify import certify


def savepoint(data, fptr, ndim):
    """
    SAVEPOINT: save the POINT data structure to *.obj file.

    """
    rmax = 2 ** 19; next = 0

    while (next < data.shape[0]):

        nrow = min(rmax, data.shape[0] - next)
        nend = next + nrow

        sfmt = "v " + " ".join(["%.17g"] * ndim)
        if (ndim < 3): sfmt = sfmt + " 0"

        sfmt = sfmt + "\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(data[next:nend, :].ravel())

        fptr.write(fdat)

        next = next + nrow


def savecells(data, fptr, nnod):
    """
    SAVECELLS: save the CELLS data structure to *.obj file.

    """
    rmax = 2 ** 19; next = 0

    while (next < data.shape[0]):

        nrow = min(rmax, data.shape[0] - next)
        nend = next + nrow

        sfmt = " ".join(["%d"] * nnod) + "\n"
        sfmt = "f " + sfmt
        sfmt = sfmt * nrow

        c = data[next:nend,:] + 1
        fdat = sfmt % tuple(c.ravel())

        fptr.write(fdat)

        next = next + nrow


def save_mesh_file(mesh, fptr):
    """
    SAVE-MESH-FILE: save a JIGSAW mesh object to *.obj file.

    """
    fptr.write(
        "# " + Path(fptr.name).name +
        "; created by JIGSAW's Python interface \n")

    if (mesh.vert3 is not None):
        savepoint(
            mesh.vert3["coord"], fptr, +3)

    if (mesh.tria3 is not None):
        savecells(
            mesh.tria3["index"], fptr, +3)


def saveobj(name, mesh):
    """
    SAVEOBJ: save a JIGSAW MSH object to file.

    SAVEOBJ(NAME, MESH)

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

    if (fext.strip() != ".obj"): name += ".obj"

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
