
from pathlib import Path
import numpy as np
from numpy.lib import recfunctions as rfn

from jigsawpy.msh_t import jigsaw_msh_t


def loadmshid(mesh, fptr, ltag):
    """
    LOADMSHID: load the MSHID data segment from file.

    """
    data = ltag[1].split(";")

    if (len(data) > 1):
        mesh.mshID = data[1].strip().lower()

    return


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
        raise Exception("Invalid RADII: " + ltag)

    return


def loadvert2(fptr, ltag):
    """
    LOADVERT2: load the 2-dim. vertex pos. from file.

    """
    lnum = int(ltag[1]); vnum = 3

    data = []
    for line in range(lnum):
        data.append(fptr.readline())

    data = " ".join(data).replace("\n", ";")

    vert = np.fromstring(
        data, dtype=np.float64, sep=";")

    vert = np.reshape(
        vert, (lnum, vnum, ), order="C")

    vert = rfn.unstructured_to_structured(
        vert, dtype=jigsaw_msh_t.VERT2_t, align=True)

    return vert


def loadvert3(fptr, ltag):
    """
    LOADVERT3: load the 3-dim. vertex pos. from file.

    """
    lnum = int(ltag[1]); vnum = 4

    data = []
    for line in range(lnum):
        data.append(fptr.readline())

    data = " ".join(data).replace("\n", ";")

    vert = np.fromstring(
        data, dtype=np.float64, sep=";")

    vert = np.reshape(
        vert, (lnum, vnum, ), order="C")

    vert = rfn.unstructured_to_structured(
        vert, dtype=jigsaw_msh_t.VERT3_t, align=True)

    return vert


def loadpoint(mesh, fptr, ltag):
    """
    LOADPOINT: load the POINT data segment from file.

    """
    if   (mesh.ndims == +2):
        mesh.vert2 = loadvert2(fptr, ltag)

    elif (mesh.ndims == +3):
        mesh.vert3 = loadvert3(fptr, ltag)

    else:
        raise Exception("Invalid NDIMS: " + ltag)

    return


def loadseeds(mesh, fptr, ltag):
    """
    LOADSEEDS: load the SEEDS data segment from file.

    """
    if   (mesh.ndims == +2):
        mesh.seed2 = loadvert2(fptr, ltag)

    elif (mesh.ndims == +3):
        mesh.seed3 = loadvert3(fptr, ltag)

    else:
        raise Exception("Invalid NDIMS: " + ltag)

    return


def loadarray(fptr, ltag, kind):
    """
    LOADARRAY: load the ARRAY data segment from file.

    """
    vtag = ltag[1].split(";")

    lnum = int(vtag[0])
    vnum = int(vtag[1])

    data = []
    for line in range(lnum):
        data.append(fptr.readline())

    data = " ".join(data).replace("\n", ";")

    vals = np.fromstring(
        data, dtype=kind, sep=";")

    vals = np.reshape(
        vals, (lnum, vnum, ), order="F")

    return vals


def loadpower(mesh, fptr, ltag):
    """
    LOADPOWER: load the POWER data segment from file.

    """
    mesh.power = loadarray(fptr, ltag, mesh.REALS_t)

    return


def loadvalue(mesh, fptr, ltag):
    """
    LOADVALUE: load the VALUE data segment from file.

    """
    mesh.value = loadarray(fptr, ltag, mesh.FLT32_t)

    return


def loadslope(mesh, fptr, ltag):
    """
    LOADSLOPE: load the SLOPE data segment from file.

    """
    mesh.slope = loadarray(fptr, ltag, mesh.FLT32_t)

    return


def loadedge2(mesh, fptr, ltag):
    """
    LOADEDGE2: load the EDGE2 data segment from file.

    """
    lnum = int(ltag[1]); vnum = 3

    data = []
    for line in range(lnum):
        data.append(fptr.readline())

    data = " ".join(data).replace("\n", ";")

    cell = np.fromstring(
        data, dtype=np.int32, sep=";")

    cell = np.reshape(
        cell, (lnum, vnum), order="C")

    cell = rfn.unstructured_to_structured(
        cell, dtype=jigsaw_msh_t.EDGE2_t, align=True)

    mesh.edge2 = cell

    return


def loadtria3(mesh, fptr, ltag):
    """
    LOADTRIA3: load the TRIA3 data segment from file.

    """
    lnum = int(ltag[1]); vnum = 4

    data = []
    for line in range(lnum):
        data.append(fptr.readline())

    data = " ".join(data).replace("\n", ";")

    cell = np.fromstring(
        data, dtype=np.int32, sep=";")

    cell = np.reshape(
        cell, (lnum, vnum), order="C")

    cell = rfn.unstructured_to_structured(
        cell, dtype=jigsaw_msh_t.TRIA3_t, align=True)

    mesh.tria3 = cell

    return


def loadquad4(mesh, fptr, ltag):
    """
    LOADUAD4: load the QUAD4 data segment from file.

    """
    lnum = int(ltag[1]); vnum = 5

    data = []
    for line in range(lnum):
        data.append(fptr.readline())

    data = " ".join(data).replace("\n", ";")

    cell = np.fromstring(
        data, dtype=np.int32, sep=";")

    cell = np.reshape(
        cell, (lnum, vnum), order="C")

    cell = rfn.unstructured_to_structured(
        cell, dtype=jigsaw_msh_t.QUAD4_t, align=True)

    mesh.quad4 = cell

    return


def loadtria4(mesh, fptr, ltag):
    """
    LOADTRIA4: load the TRIA4 data segment from file.

    """
    lnum = int(ltag[1]); vnum = 5

    data = []
    for line in range(lnum):
        data.append(fptr.readline())

    data = " ".join(data).replace("\n", ";")

    cell = np.fromstring(
        data, dtype=np.int32, sep=";")

    cell = np.reshape(
        cell, (lnum, vnum), order="C")

    cell = rfn.unstructured_to_structured(
        cell, dtype=jigsaw_msh_t.TRIA4_t, align=True)

    mesh.tria4 = cell

    return


def loadhexa8(mesh, fptr, ltag):
    """
    LOADHEXA8: load the HEXA8 data segment from file.

    """
    lnum = int(ltag[1]); vnum = 9

    data = []
    for line in range(lnum):
        data.append(fptr.readline())

    data = " ".join(data).replace("\n", ";")

    cell = np.fromstring(
        data, dtype=np.int32, sep=";")

    cell = np.reshape(
        cell, (lnum, vnum), order="C")

    cell = rfn.unstructured_to_structured(
        cell, dtype=jigsaw_msh_t.HEXA8_t, align=True)

    mesh.hexa8 = cell

    return


def loadpyra5(mesh, fptr, ltag):
    """
    LOADPYRA5: load the PYRA5 data segment from file.

    """
    lnum = int(ltag[1]); vnum = 6

    data = []
    for line in range(lnum):
        data.append(fptr.readline())

    data = " ".join(data).replace("\n", ";")

    cell = np.fromstring(
        data, dtype=np.int32, sep=";")

    cell = np.reshape(
        cell, (lnum, vnum), order="C")

    cell = rfn.unstructured_to_structured(
        cell, dtype=jigsaw_msh_t.PYRA5_t, align=True)

    mesh.pyra5 = cell

    return


def loadwedg6(mesh, fptr, ltag):
    """
    LOADWEDG6: load the WEDG6 data segment from file.

    """
    lnum = int(ltag[1]); vnum = 7

    data = []
    for line in range(lnum):
        data.append(fptr.readline())

    data = " ".join(data).replace("\n", ";")

    cell = np.fromstring(
        data, dtype=np.int32, sep=";")

    cell = np.reshape(
        cell, (lnum, vnum), order="C")

    cell = rfn.unstructured_to_structured(
        cell, dtype=jigsaw_msh_t.WEDG6_t, align=True)

    mesh.wedg6 = cell

    return


def loadbound(mesh, fptr, ltag):
    """
    LOADBOUND: load the BOUND data segment from file.

    """
    lnum = int(ltag[1]); vnum = 3

    data = []
    for line in range(lnum):
        data.append(fptr.readline())

    data = " ".join(data).replace("\n", ";")

    bnds = np.fromstring(
        data, dtype=np.int32, sep=";")

    bnds = np.reshape(
        bnds, (lnum, vnum), order="C")

    bnds = rfn.unstructured_to_structured(
        bnds, dtype=jigsaw_msh_t.BOUND_t, align=True)

    mesh.bound = bnds

    return


def loadcoord(mesh, fptr, ltag):
    """
    LOADCOORD: load the COORD data segment from file.

    """
    ctag = ltag[1].split(";")

    idim = int(ctag[0])
    lnum = int(ctag[1])

    mesh.ndims = max(mesh.ndims, idim)

    data = []
    for line in range(lnum):
        data.append(fptr.readline())

    data = " ".join(data).replace("\n", ";")

    vals = np.fromstring(
        data, dtype=np.float64, sep=";")

    if   (idim == +1):
        mesh.xgrid = np.reshape(
            vals, (lnum, ), order="C")

    elif (idim == +2):
        mesh.ygrid = np.reshape(
            vals, (lnum, ), order="C")

    elif (idim == +3):
        mesh.zgrid = np.reshape(
            vals, (lnum, ), order="C")

    return


def loadlines(mesh, fptr, line):
    """
    LOADLINES: load the next non-null line from file.

    """

    #------------------------------ skip any 'comment' lines

    line = line.strip()
    if (line[0] != "#"):

    #------------------------------ split about '=' charact.
        ltag = line.split("=")
        kind = ltag[0].upper().strip()

        if   (kind == "MSHID"):

    #----------------------------------- parse MSHID struct.
            loadmshid(mesh, fptr, ltag)

        elif (kind == "NDIMS"):

    #----------------------------------- parse NDIMS struct.
            mesh.ndims = int(ltag[1])

        elif (kind == "RADII"):

    #----------------------------------- parse RADII struct.
            loadradii(mesh, fptr, ltag)

        elif (kind == "POINT"):

    #----------------------------------- parse POINT struct.
            loadpoint(mesh, fptr, ltag)

        elif (kind == "SEEDS"):

    #----------------------------------- parse SEEDS struct.
            loadseeds(mesh, fptr, ltag)

        elif (kind == "POWER"):

    #----------------------------------- parse POWER struct.
            loadpower(mesh, fptr, ltag)

        elif (kind == "VALUE"):

    #----------------------------------- parse VALUE struct.
            loadvalue(mesh, fptr, ltag)

        elif (kind == "SLOPE"):

    #----------------------------------- parse SLOPE struct.
            loadslope(mesh, fptr, ltag)

        elif (kind == "EDGE2"):

    #----------------------------------- parse EDGE2 struct.
            loadedge2(mesh, fptr, ltag)

        elif (kind == "TRIA3"):

    #----------------------------------- parse TRIA3 struct.
            loadtria3(mesh, fptr, ltag)

        elif (kind == "QUAD4"):

    #----------------------------------- parse QUAD4 struct.
            loadquad4(mesh, fptr, ltag)

        elif (kind == "TRIA4"):

    #----------------------------------- parse TRIA4 struct.
            loadtria4(mesh, fptr, ltag)

        elif (kind == "HEXA8"):

    #----------------------------------- parse HEXA8 struct.
            loadhexa8(mesh, fptr, ltag)

        elif (kind == "PYRA5"):

    #----------------------------------- parse PYRA5 struct.
            loadpyra5(mesh, fptr, ltag)

        elif (kind == "WEDG6"):

    #----------------------------------- parse WEDG6 struct.
            loadwedg6(mesh, fptr, ltag)

        elif (kind == "BOUND"):

    #----------------------------------- parse BOUND struct.
            loadbound(mesh, fptr, ltag)

        elif (kind == "COORD"):

    #----------------------------------- parse COORD struct.
            loadcoord(mesh, fptr, ltag)

    return


def sanitise_grid(mesh, data):
    """
    SANITISE-GRID: reshape the "unrolled" array in DATA such
    that the matrix matches the dimensions of the structured
    grid objects.

    """

    F = "F"                    # use fortran matrix ordering

    if (data is not None and data.size > +1):
    #--------------------------- finalise VALUE.shape layout
        if (mesh.ndims == +2):
    #--------------------------- reshape data to 2-dim array
            if (mesh.xgrid is None or
                    mesh.xgrid.size == 0):
                raise Exception("Invalid XGRID")

            if (mesh.ygrid is None or
                    mesh.ygrid.size == 0):
                raise Exception("Invalid YGRID")

            num1 = mesh.ygrid.size
            num2 = mesh.xgrid.size

            nprd = (num1 * num2)

            nval = mesh.value.size // nprd

            size = (num1, num2, nval)

            data = np.squeeze(
                np.reshape(data, size, order=F))

        if (mesh.ndims == +3):
    #--------------------------- reshape data to 3-dim array
            if (mesh.xgrid is None or
                    mesh.xgrid.size == 0):
                raise Exception("Invalid XGRID")

            if (mesh.ygrid is None or
                    mesh.ygrid.size == 0):
                raise Exception("Invalid YGRID")

            if (mesh.zgrid is None or
                    mesh.zgrid.size == 0):
                raise Exception("Invalid ZGRID")

            num1 = mesh.ygrid.size
            num2 = mesh.xgrid.size
            num3 = mesh.zgrid.size

            nprd = (num1 * num2 * num3)

            nval = mesh.value.size // nprd

            size = (num1, num2, num3, nval)

            data = np.squeeze(
                np.reshape(data, size, order=F))

    return data


def loadmsh(name, mesh):
    """
    LOADMSH: load a JIGSAW MSH obj. from file.

    LOADMSH(NAME, MESH)

    MESH is JIGSAW's primary mesh/grid/geom class. See MSH_t
    for details.

    Data in MESH is loaded on-demand -- any objects included
    in the file will be read.

    """

    if (not isinstance(name, str)):
        raise Exception("Incorrect type: NAME.")

    if (not isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    with Path(name).open("r") as fptr:
        while (True):

    #--------------------------- get the next line from file
            line = fptr.readline()

            if (len(line) != +0):

    #--------------------------- parse next non-null section
                loadlines(mesh, fptr, line)

            else:
    #--------------------------- reached end-of-file: done!!
                break

    if (mesh.mshID.lower() in
            ["euclidean-grid", "ellipsoid-grid"]):

        mesh.value = \
            sanitise_grid(mesh, mesh.value)

        mesh.slope = \
            sanitise_grid(mesh, mesh.slope)

    return
