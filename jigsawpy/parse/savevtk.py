
from pathlib import Path
import numpy as np
from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.certify import certify


def save_mesh_file(mesh, fptr):
    """
    SAVE-MESH-FILE: save a JIGSAW mesh object to *.VTK file.

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

    nline = \
        nnum["E2"] * 1 + nnum["T3"] * 1 + \
        nnum["Q4"] * 1 + nnum["T4"] * 1 + \
        nnum["H8"] * 1 + nnum["W6"] * 1 + \
        nnum["P5"] * 1

    nints = \
        nnum["E2"] * 3 + nnum["T3"] * 4 + \
        nnum["Q4"] * 5 + nnum["T4"] * 5 + \
        nnum["H8"] * 9 + nnum["W6"] * 7 + \
        nnum["P5"] * 6

    fptr.write("# vtk DataFile Version 3.0\n")
    fptr.write(Path(fptr.name).name + "\n")
    fptr.write("ASCII\n")
    fptr.write("DATASET UNSTRUCTURED_GRID \n")

    #----------------------------------- write POINT dataset

    ZERO_PT_COORD = +0.E+00

    fptr.write("POINTS " +
               str(nnum["PT"]) + " double \n")

    if (mesh.vert2 is not None):
        xpts = mesh.vert2["coord"]
        for ipos in range(mesh.vert2.size):
            fptr.write(
                f"{xpts[ipos, 0]:.18G} "
                f"{xpts[ipos, 1]:.18G} "
                f"{ZERO_PT_COORD:.18G}\n")

    if (mesh.vert3 is not None):
        xpts = mesh.vert3["coord"]
        for ipos in range(mesh.vert3.size):
            fptr.write(
                f"{xpts[ipos, 0]:.18G} "
                f"{xpts[ipos, 1]:.18G} "
                f"{xpts[ipos, 2]:.18G}\n")

    #----------------------------------- write CELLS dataset

    fptr.write(
        "CELLS " +
        str(nline) + " " + str(nints) + " \n")

    if (mesh.edge2 is not None):
        cell = mesh.edge2["index"]
        for ipos in range(mesh.edge2.size):
            fptr.write(
                "2 "
                f"{cell[ipos, 0]} "
                f"{cell[ipos, 1]}\n")

    if (mesh.tria3 is not None):
        cell = mesh.tria3["index"]
        for ipos in range(mesh.tria3.size):
            fptr.write(
                "3 "
                f"{cell[ipos, 0]} "
                f"{cell[ipos, 1]} "
                f"{cell[ipos, 2]}\n")

    if (mesh.quad4 is not None):
        cell = mesh.quad4["index"]
        for ipos in range(mesh.quad4.size):
            fptr.write(
                "4 "
                f"{cell[ipos, 0]} "
                f"{cell[ipos, 1]} "
                f"{cell[ipos, 2]} "
                f"{cell[ipos, 3]}\n")

    if (mesh.tria4 is not None):
        cell = mesh.tria4["index"]
        for ipos in range(mesh.tria4.size):
            fptr.write(
                "4 "
                f"{cell[ipos, 0]} "
                f"{cell[ipos, 1]} "
                f"{cell[ipos, 2]} "
                f"{cell[ipos, 3]}\n")

    if (mesh.hexa8 is not None):
        cell = mesh.hexa8["index"]
        for ipos in range(mesh.hexa8.size):
            fptr.write(
                "8 "
                f"{cell[ipos, 0]} "
                f"{cell[ipos, 1]} "
                f"{cell[ipos, 2]} "
                f"{cell[ipos, 3]} "
                f"{cell[ipos, 4]} "
                f"{cell[ipos, 5]} "
                f"{cell[ipos, 6]} "
                f"{cell[ipos, 7]}\n")

    if (mesh.wedg6 is not None):
        cell = mesh.wedg6["index"]
        for ipos in range(mesh.wedg6.size):
            fptr.write(
                "6 "
                f"{cell[ipos, 0]} "
                f"{cell[ipos, 1]} "
                f"{cell[ipos, 2]} "
                f"{cell[ipos, 3]} "
                f"{cell[ipos, 4]} "
                f"{cell[ipos, 5]}\n")

    if (mesh.pyra5 is not None):
        cell = mesh.pyra5["index"]
        for ipos in range(mesh.pyra5.size):
            fptr.write(
                "5 "
                f"{cell[ipos, 0]} "
                f"{cell[ipos, 1]} "
                f"{cell[ipos, 2]} "
                f"{cell[ipos, 3]} "
                f"{cell[ipos, 4]}\n")

    #----------------------------------- write TYPES dataset

    fptr.write(
        "CELL_TYPES " + str(nline) + "\n")

    if (mesh.edge2 is not None):
        for ipos in range(mesh.edge2.size):
            fptr.write("3\n")

    if (mesh.tria3 is not None):
        for ipos in range(mesh.tria3.size):
            fptr.write("5\n")

    if (mesh.quad4 is not None):
        for ipos in range(mesh.quad4.size):
            fptr.write("9\n")

    if (mesh.tria4 is not None):
        for ipos in range(mesh.tria4.size):
            fptr.write("10\n")

    if (mesh.hexa8 is not None):
        for ipos in range(mesh.hexa8.size):
            fptr.write("12\n")

    if (mesh.wedg6 is not None):
        for ipos in range(mesh.wedg6.size):
            fptr.write("13\n")

    if (mesh.pyra5 is not None):
        for ipos in range(mesh.pyra5.size):
            fptr.write("14\n")

    if (mesh.value is not None and
            mesh.value.size ==
            mesh.point.size):
    #----------------------------------- write VALUE attrib.
        fptr.write(
            "POINT_DATA " +
            str(mesh.value.size) + "\n")
        fptr.write("SCALARS value float 1\n")
        fptr.write("LOOKUP_TABLE default \n")

        for iptr in np.nditer(mesh.value,
                              order="F"):
            fptr.write(f"{iptr: .8G}\n")

    if (mesh.slope is not None and
            mesh.slope.size ==
            mesh.point.size):
    #----------------------------------- write SLOPE attrib.
        fptr.write(
            "POINT_DATA " +
            str(mesh.slope.size) + "\n")
        fptr.write("SCALARS slope float 1\n")
        fptr.write("LOOKUP_TABLE default \n")

        for iptr in np.nditer(mesh.slope,
                              order="F"):
            fptr.write(f"{iptr: .8G}\n")

    return


def save_grid_file(mesh, fptr):
    """
    SAVE-GRID-FILE: save a JIGSAW grid object to *.VTK

    """
    dims = np.ones(+3, dtype=np.int32)

    if (mesh.xgrid is not None and
            mesh.xgrid.size != +0):
        dims[0] = mesh.xgrid.size
    if (mesh.ygrid is not None and
            mesh.ygrid.size != +0):
        dims[1] = mesh.ygrid.size
    if (mesh.zgrid is not None and
            mesh.zgrid.size != +0):
        dims[2] = mesh.zgrid.size

    fptr.write("# vtk DataFile Version 3.0\n")
    fptr.write(Path(fptr.name).name + "\n")
    fptr.write("ASCII\n")
    fptr.write("DATASET RECTILINEAR_GRID  \n")
    fptr.write("DIMENSIONS"
               + " " + str(dims[0])
               + " " + str(dims[1])
               + " " + str(dims[2])
               + " \n")

    #----------------------------------- write COORD dataset

    if (mesh.xgrid is not None and
            mesh.xgrid.size != +0):
        fptr.write(
            "X_COORDINATES "
            + str(dims[0]) + " double\n")
        coord = mesh.xgrid[:]
        for ipos in range(mesh.xgrid.size):
            fptr.write(
                f"{coord [ipos]:.18G}\n")
    else:
        fptr.write(
            "X_COORDINATES "
            + str(dims[0]) + " double\n")
        fptr.write(f"{0.000E+00:.18G}\n")

    if (mesh.ygrid is not None and
            mesh.ygrid.size != +0):
        fptr.write(
            "Y_COORDINATES "
            + str(dims[1]) + " double\n")
        coord = mesh.ygrid[:]
        for ipos in range(mesh.ygrid.size):
            fptr.write(
                f"{coord [ipos]:.18G}\n")
    else:
        fptr.write(
            "Y_COORDINATES "
            + str(dims[1]) + " double\n")
        fptr.write(f"{0.000E+00:.18G}\n")

    if (mesh.zgrid is not None and
            mesh.zgrid.size != +0):
        fptr.write(
            "Z_COORDINATES "
            + str(dims[2]) + " double\n")
        coord = mesh.zgrid[:]
        for ipos in range(mesh.zgrid.size):
            fptr.write(
                f"{coord [ipos]:.18G}\n")
    else:
        fptr.write(
            "Z_COORDINATES "
            + str(dims[2]) + " double\n")
        fptr.write(f"{0.000E+00:.18G}\n")

    if (mesh.value is not None and
            mesh.value.size != +0 and
            mesh.value.size == np.prod(dims)):
    #----------------------------------- write VALUE attrib.
        fptr.write(
            "POINT_DATA " +
            str(mesh.value.size) + "\n")
        fptr.write("SCALARS value float 1\n")
        fptr.write("LOOKUP_TABLE default \n")

        perm = [1, 0] + list(
            range(+2, mesh.value.ndim))

        data = np.transpose(mesh.value, perm)

        for iptr in np.nditer(data,
                              order="F"):
            fptr.write(f"{iptr: .8G}\n")

    if (mesh.slope is not None and
            mesh.slope.size != +0 and
            mesh.slope.size == np.prod(dims)):
    #----------------------------------- write SLOPE attrib.
        fptr.write(
            "POINT_DATA " +
            str(mesh.slope.size) + "\n")
        fptr.write("SCALARS slope float 1\n")
        fptr.write("LOOKUP_TABLE default \n")

        perm = [1, 0] + list(
            range(+2, mesh.slope.ndim))

        data = np.transpose(mesh.slope, perm)

        for iptr in np.nditer(data,
                              order="F"):
            fptr.write(f"{iptr: .8G}\n")

    return


def savevtk(name, mesh):
    """
    SAVEVTK: save a JIGSAW MSH object to file.

    SAVEVTK(NAME, MESH)

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

    if (fext.strip() != ".vtk"):
        name = name + ".vtk"

    kind = mesh.mshID.lower()

    with Path(name).open("w") as fptr:
    #----------------------------------- write JIGSAW object
        if   (kind == "euclidean-mesh"):

            save_mesh_file(mesh, fptr)

        elif (kind == "ellipsoid-mesh"):

            save_mesh_file(mesh, fptr)

        elif (kind == "euclidean-grid"):

            save_grid_file(mesh, fptr)

        elif (kind == "ellipsoid-grid"):

            save_grid_file(mesh, fptr)

        else:
            raise Exception(
                "MESH.mshID is not supported!!")

    return
