
import numpy as np
import warnings
from pathlib import Path
from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.certify import certify

def save_mesh_file(mesh,fptr):
    """
    SAVE-MESH-FILE: save a JIGSAW mesh object to *.OBJ     
    
    """
    fptr.write("# " + Path(fptr.name).name 
        + "; created by JIGSAW's Python interface \n")

    if (mesh.vert2 is not None):
        xpts = mesh.vert2["coord"]
        for ipos in range(mesh.vert2.size):
            fptr.write("v " \
                f"{xpts[ipos,0]:.18G} "  \
                f"{xpts[ipos,1]:.18G} "  \
                f"{0.0E+0:.18G}\n"  \
                )

    if (mesh.vert3 is not None):
        xpts = mesh.vert3["coord"]
        for ipos in range(mesh.vert3.size):
            fptr.write("v " \
                f"{xpts[ipos,0]:.18G} "  \
                f"{xpts[ipos,1]:.18G} "  \
                f"{xpts[ipos,2]:.18G}\n" \
                )

    if (mesh.edge2 is not None):
        cell = mesh.edge2["index"]
        for ipos in range(mesh.edge2.size):
            fptr.write("l " \
                f"{cell[ipos,0]+1} "  \
                f"{cell[ipos,1]+1}\n" \
                )

    if (mesh.tria3 is not None):
        cell = mesh.tria3["index"]
        for ipos in range(mesh.tria3.size):
            fptr.write("f " \
                f"{cell[ipos,0]+1} "  \
                f"{cell[ipos,1]+1} "  \
                f"{cell[ipos,2]+1}\n" \
                )

    if (mesh.quad4 is not None):
        cell = mesh.quad4["index"]
        for ipos in range(mesh.quad4.size):
            fptr.write("f " \
                f"{cell[ipos,0]+1} "  \
                f"{cell[ipos,1]+1} "  \
                f"{cell[ipos,2]+1} "  \
                f"{cell[ipos,3]+1}\n" \
                )

    if (mesh.tria4 is not None and \
            mesh.tria4.size != +0):
        warnings.warn(
        "TRIA4 elements not supported!",Warning)

    if (mesh.hexa8 is not None and \
            mesh.hexa8.size != +0):
        warnings.warn(
        "HEXA8 elements not supported!",Warning)

    if (mesh.wedg6 is not None and \
            mesh.wedg6.size != +0):
        warnings.warn(
        "WEDG6 elements not supported!",Warning)

    if (mesh.pyra5 is not None and \
            mesh.pyra5.size != +0):
        warnings.warn(
        "PYRA5 elements not supported!",Warning)

    return


def savewav(name,mesh):
    """
    SAVEWAV: save a JIGSAW MSH object to file.

    SAVEWAV(NAME,MESH)

    MESH is JIGSAW's primary mesh/grid/geom class. See MSH_t
    for details.

    Data in MESH is written as-needed -- any objects defined
    will be saved to file.
    
    """

    if (not isinstance(name,str)):
        raise Exception("Incorrect type: NAME.")
        
    if (not isinstance(mesh,jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    certify(mesh)

    fext = Path(name).suffix
    
    if (fext.strip() != ".obj"):
        name   = name + ".obj"

    kind = mesh.mshID.lower()

    with Path(name).open("w") as fptr:
    #----------------------------------- write JIGSAW object
        if   (kind == "euclidean-mesh"):
    
            save_mesh_file (mesh,fptr)

        elif (kind == "ellipsoid-mesh"):
    
            save_mesh_file (mesh,fptr)

        else:
            raise Exception(
                "MESH.mshID is not supported!!")

    return



