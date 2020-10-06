
from pathlib import Path
import numpy as np
from numpy.lib import recfunctions as rfn

from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.certify import certify


def saveradii(mesh, fptr, args):
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


def savevert2(ftag, data, fptr, args):
    """
    SAVEVERT2: save the POINT data structure to *.msh file.

    """
    fptr.write(ftag + "=" + str(data.size) + "\n")

    rmax = 2 ** 19; next = 0

    while (next < data.size):

        nrow = min(rmax, data.size - next)
        nend = next + nrow

        sfmt = "%%.%ug" % args.prec

        sfmt = ";".join([sfmt] * 2) + ";%d\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(
            rfn.structured_to_unstructured(
                data[next:nend], dtype=np.float64).ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def savevert3(ftag, data, fptr, args):
    """
    SAVEVERT3: save the POINT data structure to *.msh file.

    """
    fptr.write(ftag + "=" + str(data.size) + "\n")

    rmax = 2 ** 19; next = 0

    while (next < data.size):

        nrow = min(rmax, data.size - next)
        nend = next + nrow

        sfmt = "%%.%ug" % args.prec

        sfmt = ";".join([sfmt] * 3) + ";%d\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(
            rfn.structured_to_unstructured(
                data[next:nend], dtype=np.float64).ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def savevalue(ftag, data, fptr, args):
    """
    SAVEVALUE: save the ARRAY data structure to *.msh file.

    """
    if (np.ndim(data) == +1):
        data = np.reshape(data, (data.size, +1))

    npos = np.size(data, 0)
    nval = np.size(data, 1)

    fptr.write(
        ftag + "=" + str(npos) + ";" + str(nval) + "\n")

    rmax = 2 ** 19; next = 0

    while (next < data.shape[0]):

        nrow = min(rmax, data.shape[0] - next)
        nend = next + nrow

        sfmt = "%%.%ug" % args.prec

        sfmt = ";".join([sfmt] * nval) + "\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(data[next:nend:, :].ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def saveedge2(data, fptr, args):
    """
    SAVEEDGE2: save the EDGE2 data structure to *.msh file.

    """
    fptr.write("EDGE2=" + str(data.size) + "\n")

    rmax = 2 ** 19; next = 0

    while (next < data.size):

        nrow = min(rmax, data.size - next)
        nend = next + nrow

        sfmt = ";".join(["%d"] * 2) + ";%d\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(
            rfn.structured_to_unstructured(
                data[next:nend], dtype=np.int32).ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def savetria3(data, fptr, args):
    """
    SAVETRIA3: save the TRIA3 data structure to *.msh file.

    """
    fptr.write("TRIA3=" + str(data.size) + "\n")

    rmax = 2 ** 19; next = 0

    while (next < data.size):

        nrow = min(rmax, data.size - next)
        nend = next + nrow

        sfmt = ";".join(["%d"] * 3) + ";%d\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(
            rfn.structured_to_unstructured(
                data[next:nend], dtype=np.int32).ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def savequad4(data, fptr, args):
    """
    SAVEQUAD4: save the QUAD4 data structure to *.msh file.

    """
    fptr.write("QUAD4=" + str(data.size) + "\n")

    rmax = 2 ** 19; next = 0

    while (next < data.size):

        nrow = min(rmax, data.size - next)
        nend = next + nrow

        sfmt = ";".join(["%d"] * 4) + ";%d\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(
            rfn.structured_to_unstructured(
                data[next:nend], dtype=np.int32).ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def savetria4(data, fptr, args):
    """
    SAVETRIA4: save the TRIA4 data structure to *.msh file.

    """
    fptr.write("TRIA4=" + str(data.size) + "\n")

    rmax = 2 ** 19; next = 0

    while (next < data.size):

        nrow = min(rmax, data.size - next)
        nend = next + nrow

        sfmt = ";".join(["%d"] * 4) + ";%d\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(
            rfn.structured_to_unstructured(
                data[next:nend], dtype=np.int32).ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def savehexa8(data, fptr, args):
    """
    SAVEHEXA8: save the HEXA8 data structure to *.msh file.

    """
    fptr.write("HEXA8=" + str(data.size) + "\n")

    rmax = 2 ** 19; next = 0

    while (next < data.size):

        nrow = min(rmax, data.size - next)
        nend = next + nrow

        sfmt = ";".join(["%d"] * 8) + ";%d\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(
            rfn.structured_to_unstructured(
                data[next:nend], dtype=np.int32).ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def savewedg6(data, fptr, args):
    """
    SAVEWEDG6: save the WEDG6 data structure to *.msh file.

    """
    fptr.write("WEDG6=" + str(data.size) + "\n")

    rmax = 2 ** 19; next = 0

    while (next < data.size):

        nrow = min(rmax, data.size - next)
        nend = next + nrow

        sfmt = ";".join(["%d"] * 6) + ";%d\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(
            rfn.structured_to_unstructured(
                data[next:nend], dtype=np.int32).ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def savepyra5(data, fptr, args):
    """
    SAVEPYRA5: save the PYRA5 data structure to *.msh file.

    """
    fptr.write("PYRA5=" + str(data.size) + "\n")

    rmax = 2 ** 19; next = 0

    while (next < data.size):

        nrow = min(rmax, data.size - next)
        nend = next + nrow

        sfmt = ";".join(["%d"] * 5) + ";%d\n"
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(
            rfn.structured_to_unstructured(
                data[next:nend], dtype=np.int32).ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def savebound(data, fptr, args):
    """
    SAVEBOUND: save the BOUND data structure to *.msh file.

    """
    fptr.write("BOUND=" + str(data.size) + "\n")

    rmax = 2 ** 19; next = 0

    while (next < data.size):

        nrow = min(rmax, data.size - next)
        nend = next + nrow

        sfmt = "%d;%d;%d\n" * nrow

        fdat = sfmt % tuple(
            rfn.structured_to_unstructured(
                data[next:nend], dtype=np.int32).ravel())

        fptr.write(fdat)

        next = next + nrow

    return


def savecoord(data, fptr, args, inum):
    """
    SAVECOORD: save the COORD data structure to *.msh file.

    """
    nnum = np.prod(data.shape)

    fptr.write(
        "COORD=" + str(inum) + ";" + str(nnum) + "\n")

    rmax = 2 ** 19; next = 0

    while (next < data.shape[0]):

        nrow = min(rmax, data.shape[0] - next)

        sfmt = "%%.%ug\n" % args.prec
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(data[next:next+nrow].ravel())
        fptr.write(fdat)

        next = next + nrow

    return


def savendmat(ftag, data, fptr, args):
    """
    SAVENDMAT: save the VALUE data structure to *.msh file.

    """
    nnum = np.prod(data.shape)

    fptr.write(
        ftag + "=" + str(nnum) + "; 1" + "\n")

    dptr = data.reshape(-1, order="F")

    rmax = 2 ** 19; next = 0

    while (next < dptr.shape[0]):

        nrow = min(rmax, dptr.shape[0] - next)

        sfmt = "%%.%ug\n" % args.prec
        sfmt = sfmt * nrow

        fdat = sfmt % tuple(dptr[next:next+nrow].ravel())
        fptr.write(fdat)

        next = next + nrow

    return


def save_mesh_file(mesh, fptr, args, kind):

    fptr.write("MSHID=" + str(args.nver) + ";" + kind + "\n")

    if (mesh.vert2 is not None and
            mesh.vert2.size != +0):

    #----------------------------------- write NDIMS struct.
        fptr.write("NDIMS=2\n")

    if (mesh.vert3 is not None and
            mesh.vert3.size != +0):

    #----------------------------------- write NDIMS struct.
        fptr.write("NDIMS=3\n")

    if (mesh.radii is not None and
            mesh.radii.size != +0):

    #----------------------------------- write RADII struct.
        saveradii(mesh, fptr, args)

    if (mesh.vert2 is not None and
            mesh.vert2.size != +0):

    #----------------------------------- write VERT2 struct.
        savevert2("POINT",
                  mesh.point, fptr, args)

    if (mesh.vert3 is not None and
            mesh.vert3.size != +0):

    #----------------------------------- write VERT3 struct.
        savevert3("POINT",
                  mesh.point, fptr, args)

    if (mesh.seed2 is not None and
            mesh.seed2.size != +0):

    #----------------------------------- write VERT2 struct.
        savevert2("SEEDS",
                  mesh.seeds, fptr, args)

    if (mesh.seed3 is not None and
            mesh.seed3.size != +0):

    #----------------------------------- write VERT3 struct.
        savevert3("SEEDS",
                  mesh.seeds, fptr, args)

    if (mesh.power is not None and
            mesh.power.size != +0):

    #----------------------------------- write POWER struct.
        savevalue("POWER",
                  mesh.power, fptr, args)

    if (mesh.value is not None and
            mesh.value.size != +0):

    #----------------------------------- write VALUE struct.
        savevalue("VALUE",
                  mesh.value, fptr, args)

    if (mesh.slope is not None and
            mesh.slope.size != +0):

    #----------------------------------- write SLOPE struct.
        savevalue("SLOPE",
                  mesh.slope, fptr, args)

    if (mesh.edge2 is not None and
            mesh.edge2.size != +0):

    #----------------------------------- write EDGE2 struct.
        saveedge2(mesh.edge2, fptr, args)

    if (mesh.tria3 is not None and
            mesh.tria3.size != +0):

    #----------------------------------- write TRIA3 struct.
        savetria3(mesh.tria3, fptr, args)

    if (mesh.quad4 is not None and
            mesh.quad4.size != +0):

    #----------------------------------- write QUAD4 struct.
        savequad4(mesh.quad4, fptr, args)

    if (mesh.tria4 is not None and
            mesh.tria4.size != +0):

    #----------------------------------- write TRIA4 struct.
        savetria4(mesh.tria4, fptr, args)

    if (mesh.hexa8 is not None and
            mesh.hexa8.size != +0):

    #----------------------------------- write HEXA8 struct.
        savehexa8(mesh.hexa8, fptr, args)

    if (mesh.wedg6 is not None and
            mesh.wedg6.size != +0):

    #----------------------------------- write WEDG6 struct.
        savewedg6(mesh.wedg6, fptr, args)

    if (mesh.pyra5 is not None and
            mesh.pyra5.size != +0):

    #----------------------------------- write PYRA5 struct.
        savepyra5(mesh.pyra5, fptr, args)

    if (mesh.bound is not None and
            mesh.bound.size != +0):

    #----------------------------------- write BOUND struct.
        savebound(mesh.bound, fptr, args)

    return


def save_grid_file(mesh, fptr, args, kind):

    fptr.write("MSHID=" + str(args.nver) + ";" + kind + "\n")

    if (mesh.radii is not None and
            mesh.radii.size != +0):

    #----------------------------------- write RADII struct.
        saveradii(mesh, fptr, args)

    #----------------------------------- calc. NDIMS struct.
    ndim = +0
    if (mesh.xgrid is not None and
            mesh.xgrid.size != +0):
        ndim += +1

    if (mesh.ygrid is not None and
            mesh.ygrid.size != +0):
        ndim += +1

    if (mesh.zgrid is not None and
            mesh.zgrid.size != +0):
        ndim += +1

    if (ndim >= +1):
    #----------------------------------- write NDIMS struct.
        fptr.write("NDIMS="
                   + str(ndim) + "\n")

    if (mesh.xgrid is not None and
            mesh.xgrid.size != +0):

    #----------------------------------- write XGRID struct.
        savecoord(mesh.xgrid, fptr, args, +1)

    if (mesh.ygrid is not None and
            mesh.ygrid.size != +0):

    #----------------------------------- write YGRID struct.
        savecoord(mesh.ygrid, fptr, args, +2)

    if (mesh.zgrid is not None and
            mesh.zgrid.size != +0):

    #----------------------------------- write ZGRID struct.
        savecoord(mesh.zgrid, fptr, args, +3)

    if (mesh.value is not None and
            mesh.value.size != +0):

    #----------------------------------- write VALUE struct.
        savendmat("VALUE",
                  mesh.value, fptr, args)

    if (mesh.slope is not None and
            mesh.slope.size != +0):

    #----------------------------------- write SLOPE struct.
        savendmat("SLOPE",
                  mesh.slope, fptr, args)

    return


def savemsh(name, mesh, tags=None):
    """
    SAVEMSH: save a JIGSAW MSH object to file.

    SAVEMSH(NAME, MESH)

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

    class stub(object): pass

    args = stub()                           ## savmsh params
    args.kind = "ascii"
    args.nver = + 3
    args.prec = + 17
    args.real = "f64"
    args.ints = "i32"

    fext = Path(name).suffix

    if (fext.strip() != ".msh"): name += ".msh"

    kind = mesh.mshID.lower()

    if (tags is not None):
    #----------------------------------- parse savmsh params
        stag = tags.lower().split(";")
        for this in stag:
            if "precision" in this:
                args.prec = this.split("=")[1]
                args.prec = int(args.prec)

            if "real:type" in this:
                args.real = this.split("=")[1]

            if "ints:type" in this:
                args.ints = this.split("=")[1]

            if "binary" in this:
                args.kind = "binary"

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

    return
