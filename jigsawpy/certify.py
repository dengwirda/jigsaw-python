
import numpy as np
from jigsawpy.msh_t import jigsaw_msh_t

def certifyarray(data,stag):

    if (data is not None):
        if (isinstance(data,np.ndarray)):

            return data.size >= +1

        raise Exception("Invalid "+stag+" type.")

    return False


def certifyradii(data,stag):

    if (data.size != +3):
        raise Exception("Invalid "+stag+" size.")
    
    if (data.ndim != +1):
        raise Exception("Invalid "+stag+" size.")

    if (data.dtype != jigsaw_msh_t.REALS_t):
        raise Exception("Invalid "+stag+" type.")

    if (not np.isfinite(data).all()):
        raise Exception("Invalid "+stag+" data.")

    if (np.any(data <= 0.)):
        raise Exception("Invalid "+stag+" data.")

    return


def certifypoint(data,stag,KIND):

    if (data.ndim != +1):
        raise Exception("Invalid "+stag+" size.")

    if (data.dtype != KIND):
        raise Exception("Invalid "+stag+" type.")

    if (not np.isfinite(data["coord"]).all()):
        raise Exception("Invalid "+stag+" data.")

    if (not np.isfinite(data["IDtag"]).all()):
        raise Exception("Invalid "+stag+" data.")

    return


def certifyvalue(vals,stag):

   #if (vals.ndim != +2):
   #    raise Exception("Invalid "+stag+" size.")

    if (vals.dtype != jigsaw_msh_t.REALS_t):
        raise Exception("Invalid "+stag+" type.")

    if (not np.isfinite(vals).all()):
        raise Exception("Invalid "+stag+" data.")

    return


def certifycells(cell,stag,KIND):

    if (cell.ndim != +1):
        raise Exception("Invalid "+stag+" size.")

    if (cell.dtype != KIND):
        raise Exception("Invalid "+stag+" type.")

    if (not np.isfinite(cell["index"]).all()):
        raise Exception("Invalid "+stag+" data.")

    if (np.any(cell["index"] < +0)):
        raise Exception("Invalid "+stag+" data.")

    if (not np.isfinite(cell["IDtag"]).all()):
        raise Exception("Invalid "+stag+" data.")

    return


def certifyindex(data,stag,KIND):

    if (data.ndim != +1):
        raise Exception("Invalid "+stag+" size.")

    if (data.dtype != KIND):
        raise Exception("Invalid "+stag+" type.")

    if (not np.isfinite(data["IDtag"]).all()):
        raise Exception("Invalid "+stag+" data.")

    if (not np.isfinite(data["index"]).all()):
        raise Exception("Invalid "+stag+" data.")

    if (np.any(data["index"] < +0)):
        raise Exception("Invalid "+stag+" data.")

    if (not np.isfinite(data["cells"]).all()):
        raise Exception("Invalid "+stag+" data.")

    if (np.any(data["cells"] < +0)):
        raise Exception("Invalid "+stag+" data.")

    return


def certifymesht(mesh):

    if (certifyarray(mesh.radii,"MESH.RADII")):

        certifyradii(mesh.radii,"MESH.RADII")

    if (certifyarray(mesh.vert2,"MESH.VERT2")):

        certifypoint(mesh.vert2,"MESH.VERT2", \
            jigsaw_msh_t.VERT2_t)

    if (certifyarray(mesh.vert3,"MESH.VERT3")):

        certifypoint(mesh.vert3,"MESH.VERT3", \
            jigsaw_msh_t.VERT3_t)

    if (certifyarray(mesh.power,"MESH.POWER")):

        certifyvalue(mesh.power,"MESH.POWER")

    if (certifyarray(mesh.value,"MESH.VALUE")):

        certifyvalue(mesh.value,"MESH.VALUE")

    if (certifyarray(mesh.slope,"MESH.SLOPE")):

        certifyvalue(mesh.slope,"MESH.SLOPE")

    if (certifyarray(mesh.edge2,"MESH.EDGE2")):

        certifycells(mesh.edge2,"MESH.EDGE2", \
            jigsaw_msh_t.EDGE2_t)

    if (certifyarray(mesh.tria3,"MESH.TRIA3")):

        certifycells(mesh.tria3,"MESH.TRIA3", \
            jigsaw_msh_t.TRIA3_t)

    if (certifyarray(mesh.quad4,"MESH.QUAD4")):

        certifycells(mesh.quad4,"MESH.QUAD4", \
            jigsaw_msh_t.QUAD4_t)

    if (certifyarray(mesh.tria4,"MESH.TRIA4")):

        certifycells(mesh.tria4,"MESH.TRIA4", \
            jigsaw_msh_t.TRIA4_t)

    if (certifyarray(mesh.hexa8,"MESH.HEXA8")):

        certifycells(mesh.hexa8,"MESH.HEXA8", \
            jigsaw_msh_t.HEXA8_t)

    if (certifyarray(mesh.wedg6,"MESH.WEDG6")):

        certifycells(mesh.wedg6,"MESH.WEDG6", \
            jigsaw_msh_t.WEDG6_t)

    if (certifyarray(mesh.pyra5,"MESH.PYRA5")):

        certifycells(mesh.pyra5,"MESH.PYRA5", \
            jigsaw_msh_t.PYRA5_t)

    if (certifyarray(mesh.bound,"MESH.BOUND")):

        certifyindex(mesh.bound,"MESH.BOUND", \
            jigsaw_msh_t.BOUND_t)

    return


def certifycoord(data,stag):

    if (data.ndim != +1):
        raise Exception("Invalid "+stag+" size.")

    if (data.dtype != jigsaw_msh_t.REALS_t):
        raise Exception("Invalid "+stag+" type.")

    if (not np.isfinite(data).all()):
        raise Exception("Invalid "+stag+" data.")

    return


def certifyNDmat(data,stag,dims):

    if (data.ndim != len(dims)):
        raise Exception("Invalid "+stag+" size.")

    if (data.size != np.prod(dims)):
        raise Exception("Invalid "+stag+" size.")

    if (data.dtype != jigsaw_msh_t.REALS_t):
        raise Exception("Invalid "+stag+" type.")

    if (not np.isfinite(data).all()):
        raise Exception("Invalid "+stag+" data.")

    return


def certifygridt(mesh):

    dims = []

    if (certifyarray(mesh.radii,"MESH.RADII")):

        certifyradii(mesh.radii,"MESH.RADII")

    if (certifyarray(mesh.xgrid,"MESH.XGRID")):

        dims +=[mesh.xgrid.size]

        certifycoord(mesh.xgrid,"MESH.XGRID")

    if (certifyarray(mesh.ygrid,"MESH.YGRID")):

        dims +=[mesh.ygrid.size]

        certifycoord(mesh.ygrid,"MESH.YGRID")

    if (certifyarray(mesh.zgrid,"MESH.ZGRID")):

        dims +=[mesh.zgrid.size]

        certifycoord(mesh.zgrid,"MESH.ZGRID")

    if (certifyarray(mesh.value,"MESH.VALUE")):

        certifyNDmat(mesh.value,"MESH.VALUE", \
                     dims)

    if (certifyarray(mesh.slope,"MESH.SLOPE")):

        certifyNDmat(mesh.slope,"MESH.SLOPE", \
                     dims)

    return


def certify(mesh):
    """
    CERTIFY: certify layout for a JIGSAW MSH object.
    
    """

    if (mesh is None): return

    if (not isinstance (mesh,jigsaw_msh_t)):
        raise Exception("Invalid MESH structure.")

    if (not isinstance (mesh.mshID,str)):
        raise Exception("Invalid MESH.MSHID tag.")

    if (mesh.mshID.lower() \
            in ["euclidean-mesh","ellipsoid-mesh"
                    ]   ):
    #---------------------------------- certify MESH struct.
        certifymesht(mesh)
                  
    elif (mesh.mshID.lower() \
            in ["euclidean-grid","ellipsoid-grid"
                    ]   ):
    #---------------------------------- certify GRID struct.
        certifygridt(mesh)

    else:
        raise Exception("Invalid MESH.MSHID tag.")
 
    return



