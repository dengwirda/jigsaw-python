
import warnings
from pathlib import Path
from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.certify import certify


def save_mesh_file(mesh, fptr):
    """
    SAVE-MESH-FILE: save a JIGSAW mesh object to *.OFF

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
    nface = nnum["T4"] + nnum["Q4"]

    fptr.write(str(nnode) + " " +
               str(nface) + " " + str(nedge) + "\n")

    if (mesh.vert2 is not None):
        xpts = mesh.vert2["coord"]
        for ipos in range(mesh.vert2.size):
            fptr.write(
                f"{xpts[ipos, 0]:.18G} "
                f"{xpts[ipos, 1]:.18G} "
                f"{0.E+0:.18G}\n")

    if (mesh.vert3 is not None):
        xpts = mesh.vert3["coord"]
        for ipos in range(mesh.vert3.size):
            fptr.write(
                f"{xpts[ipos, 0]:.18G} "
                f"{xpts[ipos, 1]:.18G} "
                f"{xpts[ipos, 2]:.18G}\n")

    if (mesh.edge2 is not None and
            mesh.edge2.size != +0):
        warnings.warn(
            "EDGE2 elements not supported", Warning)

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
        raise Exception("Incorrect type: NAME.")

    if (not isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    certify(mesh)

    fext = Path(name).suffix

    if (fext.strip() != ".off"):
        name = name + ".off"

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



