
import numpy as np
from pathlib import Path
from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.certify import certify

def saveradii(mesh,fptr):
    """
    SAVERADII: save the RADII data structure to file.
    
    """
    if   (mesh.radii.size == +3):
        fptr.write("RADII="\
            f"{mesh.radii[0]:.18G};" \
            f"{mesh.radii[1]:.18G};" \
            f"{mesh.radii[2]:.18G}\n"\
            )

    elif (mesh.radii.size == +1):
        fptr.write("RADII="\
            f"{mesh.radii[0]:.18G};" \
            f"{mesh.radii[0]:.18G};" \
            f"{mesh.radii[0]:.18G}\n"\
            )

    return


def savevert2(mesh,fptr):
    """
    SAVEVERT2: save the POINT data structure to file.
    
    """
    fptr.write("POINT=" \
        + str(mesh.vert2.size) + "\n")

    xpts = mesh.vert2["coord"]
    itag = mesh.vert2["IDtag"]

    for ipos in range(mesh.vert2.size):
        fptr.write( \
            f"{xpts[ipos,0]:.18G};"  \
            f"{xpts[ipos,1]:.18G};"  \
            f"{itag[ipos  ]}\n"  \
            )

    return


def savevert3(mesh,fptr):
    """
    SAVEVERT3: save the POINT data structure to file.
    
    """
    fptr.write("POINT=" \
        + str(mesh.vert3.size) + "\n")

    xpts = mesh.vert3["coord"]
    itag = mesh.vert3["IDtag"]

    for ipos in range(mesh.vert3.size):
        fptr.write(
            f"{xpts[ipos,0]:.18G};"  \
            f"{xpts[ipos,1]:.18G};"  \
            f"{xpts[ipos,2]:.18G};"  \
            f"{itag[ipos  ]}\n" \
            )

    return


def savevalue(ftag,data,fptr):
    """
    SAVEVALUE: save the ARRAY data structure to file.
    
    """
    if (np.ndim(data) == +1):
        data = \
    np.reshape(data, (data.size, +1))

    npos = np.size(data,0)
    nval = np.size(data,1)

    fptr.write ( ftag + "=" + \
        str(npos) + ";" + str(nval) + "\n")

    nval = nval - 1

    for ipos in range(npos):
        fstr = ""
        for ival in range(nval):
            fstr = fstr + \
            f"{data[ipos,ival]:.18G};"
        fstr = fstr + \
            f"{data[ipos,nval]:.18G}\n"

        fptr.write(fstr)

    return


def saveedge2(mesh,fptr):
    """
    SAVEEDGE2: save the EDGE2 data structure to file.
    
    """
    fptr.write("EDGE2=" \
        + str(mesh.edge2.size) + "\n")

    cell = mesh.edge2["index"]
    itag = mesh.edge2["IDtag"]

    for ipos in range(mesh.edge2.size):
        fptr.write( \
            f"{cell[ipos,0]};"  \
            f"{cell[ipos,1]};"  \
            f"{itag[ipos  ]}\n" \
            )

    return


def savetria3(mesh,fptr):
    """
    SAVETRIA3: save the TRIA3 data structure to file.
    
    """
    fptr.write("TRIA3=" \
        + str(mesh.tria3.size) + "\n")

    cell = mesh.tria3["index"]
    itag = mesh.tria3["IDtag"]

    for ipos in range(mesh.tria3.size):
        fptr.write( \
            f"{cell[ipos,0]};"  \
            f"{cell[ipos,1]};"  \
            f"{cell[ipos,2]};"  \
            f"{itag[ipos  ]}\n" \
            )

    return


def savequad4(mesh,fptr):
    """
    SAVEQUAD4: save the QUAD4 data structure to file.
    
    """
    fptr.write("QUAD4=" \
        + str(mesh.quad4.size) + "\n")

    cell = mesh.quad4["index"]
    itag = mesh.quad4["IDtag"]

    for ipos in range(mesh.quad4.size):
        fptr.write( \
            f"{cell[ipos,0]};"  \
            f"{cell[ipos,1]};"  \
            f"{cell[ipos,2]};"  \
            f"{cell[ipos,3]};"  \
            f"{itag[ipos  ]}\n" \
            )

    return


def savetria4(mesh,fptr):
    """
    SAVETRIA4: save the TRIA4 data structure to file.
    
    """
    fptr.write("TRIA4=" \
        + str(mesh.tria4.size) + "\n")

    cell = mesh.tria4["index"]
    itag = mesh.tria4["IDtag"]

    for ipos in range(mesh.tria4.size):
        fptr.write( \
            f"{cell[ipos,0]};"  \
            f"{cell[ipos,1]};"  \
            f"{cell[ipos,2]};"  \
            f"{cell[ipos,3]};"  \
            f"{itag[ipos  ]}\n" \
            )

    return


def savehexa8(mesh,fptr):
    """
    SAVEHEXA8: save the HEXA8 data structure to file.
    
    """
    fptr.write("HEXA8=" \
        + str(mesh.hexa8.size) + "\n")

    cell = mesh.hexa8["index"]
    itag = mesh.hexa8["IDtag"]

    for ipos in range(mesh.hexa8.size):
        fptr.write( \
            f"{cell[ipos,0]};"  \
            f"{cell[ipos,1]};"  \
            f"{cell[ipos,2]};"  \
            f"{cell[ipos,3]};"  \
            f"{cell[ipos,4]};"  \
            f"{cell[ipos,5]};"  \
            f"{cell[ipos,6]};"  \
            f"{cell[ipos,7]};"  \
            f"{itag[ipos  ]}\n" \
            )

    return


def savewedg6(mesh,fptr):
    """
    SAVEWEDG6: save the WEDG6 data structure to file.
    
    """
    fptr.write("WEDG6=" \
        + str(mesh.wedg6.size) + "\n")

    cell = mesh.wedg6["index"]
    itag = mesh.wedg6["IDtag"]

    for ipos in range(mesh.wedg6.size):
        fptr.write( \
            f"{cell[ipos,0]};"  \
            f"{cell[ipos,1]};"  \
            f"{cell[ipos,2]};"  \
            f"{cell[ipos,3]};"  \
            f"{cell[ipos,4]};"  \
            f"{cell[ipos,5]};"  \
            f"{itag[ipos  ]}\n" \
            )

    return


def savepyra5(mesh,fptr):
    """
    SAVEPYRA5: save the PYRA5 data structure to file.
    
    """
    fptr.write("PYRA5=" \
        + str(mesh.pyra5.size) + "\n")

    cell = mesh.pyra5["index"]
    itag = mesh.pyra5["IDtag"]

    for ipos in range(mesh.pyra5.size):
        fptr.write( \
            f"{cell[ipos,0]};"  \
            f"{cell[ipos,1]};"  \
            f"{cell[ipos,2]};"  \
            f"{cell[ipos,3]};"  \
            f"{cell[ipos,4]};"  \
            f"{itag[ipos  ]}\n" \
            )

    return


def savebound(mesh,fptr):
    """
    SAVEBOUND: save the BOUND data structure to file.
    
    """
    fptr.write("BOUND=" \
        + str(mesh.bound.size) + "\n")

    itag = mesh.bound["IDtag"]
    indx = mesh.bound["index"]
    kind = mesh.bound["cells"]

    for ipos in range(mesh.bound.size):
        fptr.write( \
            f"{itag[ipos  ]};"  \
            f"{indx[ipos  ]};"  \
            f"{kind[ipos  ]}\n" \
            )

    return


def savecoord(data,fptr,inum):
    """
    SAVECOORD: save the COORD data structure to file.
    
    """
    fptr.write("COORD=" \
        + str(inum) + ";" + str(data.size) + "\n")

    for iptr in np.nditer(data,order="F"):
        fptr.write(f"{iptr:.18G}\n")

    return


def savendmat(ftag,data,fptr):
    """
    SAVENDMAT: save the VALUE data structure to file.
    
    """
    fptr.write(ftag+"=" \
        + str(np.prod(data.shape)) + ";1"  + "\n")

    for iptr in np.nditer(data,order="F"):
        fptr.write(f"{iptr:.18G}\n")

    return


def save_mesh_file(mesh,fptr,nver,kind):

    fptr.write("MSHID=" + str(nver) + ";" + kind + "\n")

    if (mesh.vert2 is not None and \
        mesh.vert2.size != +0):

    #----------------------------------- write NDIMS struct.
        fptr.write("NDIMS=2\n")

    if (mesh.vert3 is not None and \
        mesh.vert3.size != +0):

    #----------------------------------- write NDIMS struct.
        fptr.write("NDIMS=3\n")

    if (mesh.radii is not None and \
        mesh.radii.size != +0):

    #----------------------------------- write RADII struct.
        saveradii(mesh,fptr)
 
    if (mesh.vert2 is not None and \
        mesh.vert2.size != +0):

    #----------------------------------- write VERT2 struct.
        savevert2(mesh,fptr)

    if (mesh.vert3 is not None and \
        mesh.vert3.size != +0):

    #----------------------------------- write VERT3 struct.
        savevert3(mesh,fptr)

    if (mesh.power is not None and \
        mesh.power.size != +0):

    #----------------------------------- write POWER struct.
        savevalue("POWER",
                  mesh.power,fptr)

    if (mesh.value is not None and \
        mesh.value.size != +0):

    #----------------------------------- write VALUE struct.
        savevalue("VALUE",
                  mesh.value,fptr)

    if (mesh.slope is not None and \
        mesh.slope.size != +0):

    #----------------------------------- write SLOPE struct.
        savevalue("SLOPE",
                  mesh.slope,fptr)

    if (mesh.edge2 is not None and \
        mesh.edge2.size != +0):

    #----------------------------------- write EDGE2 struct.
        saveedge2(mesh,fptr)

    if (mesh.tria3 is not None and \
        mesh.tria3.size != +0):

    #----------------------------------- write TRIA3 struct.
        savetria3(mesh,fptr)

    if (mesh.quad4 is not None and \
        mesh.quad4.size != +0):

    #----------------------------------- write QUAD4 struct.
        savequad4(mesh,fptr)

    if (mesh.tria4 is not None and \
        mesh.tria4.size != +0):

    #----------------------------------- write TRIA4 struct.
        savetria4(mesh,fptr)

    if (mesh.hexa8 is not None and \
        mesh.hexa8.size != +0):

    #----------------------------------- write HEXA8 struct.
        savehexa8(mesh,fptr)

    if (mesh.wedg6 is not None and \
        mesh.wedg6.size != +0):

    #----------------------------------- write WEDG6 struct.
        savewedg6(mesh,fptr)

    if (mesh.pyra5 is not None and \
        mesh.pyra5.size != +0):

    #----------------------------------- write PYRA5 struct.
        savepyra5(mesh,fptr)

    if (mesh.bound is not None and \
        mesh.bound.size != +0):

    #----------------------------------- write BOUND struct.
        savebound(mesh,fptr)
        

    return


def save_grid_file(mesh,fptr,nver,kind):

    fptr.write("MSHID=" + str(nver) + ";" + kind + "\n")

    if (mesh.radii is not None and \
        mesh.radii.size != +0):

    #----------------------------------- write RADII struct.
        saveradii(mesh,fptr)

    #----------------------------------- calc. NDIMS struct.
    ndim =  +0

    if (mesh.xgrid is not None and \
        mesh.xgrid.size != +0):

        ndim += +1

    if (mesh.ygrid is not None and \
        mesh.ygrid.size != +0):

        ndim += +1

    if (mesh.zgrid is not None and \
        mesh.zgrid.size != +0):

        ndim += +1

    if (ndim >= +1):
    #----------------------------------- write NDIMS struct.
        fptr.write(
        "NDIMS=" + str(ndim) + "\n")


    if (mesh.xgrid is not None and \
        mesh.xgrid.size != +0):

    #----------------------------------- write XGRID struct.
        savecoord(mesh.xgrid,fptr,1)

    if (mesh.ygrid is not None and \
        mesh.ygrid.size != +0):

    #----------------------------------- write YGRID struct.
        savecoord(mesh.ygrid,fptr,2)

    if (mesh.zgrid is not None and \
        mesh.zgrid.size != +0):

    #----------------------------------- write ZGRID struct.
        savecoord(mesh.zgrid,fptr,3)

    if (mesh.value is not None and \
        mesh.value.size != +0):

    #----------------------------------- write VALUE struct.
        savendmat("VALUE",
                  mesh.value,fptr)

    if (mesh.slope is not None and \
        mesh.slope.size != +0):

    #----------------------------------- write SLOPE struct.
        savendmat("SLOPE",
                  mesh.slope,fptr)

    return


def savemsh(name,mesh):
    """
    SAVEMSH: save a JIGSAW MSH object to file.

    SAVEMSH(NAME,MESH)

    MESH is JIGSAW's primary mesh/grid/geom class. See MSH_t
    for details.

    Data in MESH is written as-needed -- any objects defined
    will be saved to file.
    
    """

    if (not isinstance(name,str)):
        raise Exception("Incorrect type: NAME.")
        
    if (not isinstance(mesh,jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    nver =  +3

    certify(mesh)

    fext = Path(name).suffix
    
    if (fext.strip() != ".msh"):
        name =   name + ".msh"

    kind = mesh.mshID.lower()

    with Path(name).open("w") as fptr:
    #----------------------------------- write JIGSAW object    
        fptr.write("# " + Path(name).name + \
    "; created by JIGSAW's PYTHON interface \n")
   
        if (kind == "euclidean-mesh"):
            save_mesh_file( \
            mesh,fptr,nver,"euclidean-mesh")

        if (kind == "euclidean-grid"):
            save_grid_file( \
            mesh,fptr,nver,"euclidean-grid")

        if (kind == "ellipsoid-mesh"):
            save_mesh_file( \
            mesh,fptr,nver,"ellipsoid-mesh")

        if (kind == "ellipsoid-grid"):
            save_grid_file( \
            mesh,fptr,nver,"ellipsoid-grid")

    return
    

    
