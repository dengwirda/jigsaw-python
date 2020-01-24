
import numpy as np

def istri_1(ppos, tri1):
    """
    ISTRI-1 TRUE if (PPOS, TRIA) is 1-simplex triangulation.

    """

    okay = True

#--------------------------------------- some simple checks!
    if (not isinstance(ppos, np.ndarray)):
        raise Exception("Invalid type: PPOS.")

    if (not isinstance(tri1, np.ndarray)):
        raise Exception("Invalid type: TRIA.")

    if (ppos.ndim != +2):
        raise Exception("Invalid PPOS ndims.")
    
    if (ppos.shape[1] < +2):
        raise Exception("Invalid PPOS shape.")
    
    nump = ppos.shape[0]

    if (tri1.ndim != +2):
        raise Exception("Invalid TRIA ndims.")

    if (tri1.shape[1] < +2):
        raise Exception("Invalid TRIA shape.")

    if (np.min(tri1[:,0:1]) < +0 or 
            np.max(tri1[:,0:1]) >= nump):
        raise Exception("Invalid TRIA index.")

    return okay


def istri_2(ppos, tri2):
    """
    ISTRI-2 TRUE if (PPOS, TRIA) is 2-simplex triangulation.

    """

    okay = True

#--------------------------------------- some simple checks!
    if (not isinstance(ppos, np.ndarray)):
        raise Exception("Invalid type: PPOS.")

    if (not isinstance(tri2, np.ndarray)):
        raise Exception("Invalid type: TRIA.")

    if (ppos.ndim != +2):
        raise Exception("Invalid PPOS ndims.")
    
    if (ppos.shape[1] < +2):
        raise Exception("Invalid PPOS shape.")
    
    nump = ppos.shape[0]

    if (tri2.ndim != +2):
        raise Exception("Invalid TRIA ndims.")

    if (tri2.shape[1] < +3):
        raise Exception("Invalid TRIA shape.")

    if (np.min(tri2[:,0:2]) < +0 or 
            np.max(tri2[:,0:2]) >= nump):
        raise Exception("Invalid TRIA index.")

    return okay


def istri_3(ppos, tri3):
    """
    ISTRI-3 TRUE if (PPOS, TRIA) is 3-simplex triangulation.

    """

    okay = True

#--------------------------------------- some simple checks!
    if (not isinstance(ppos, np.ndarray)):
        raise Exception("Invalid type: PPOS.")

    if (not isinstance(tri3, np.ndarray)):
        raise Exception("Invalid type: TRIA.")

    if (ppos.ndim != +2):
        raise Exception("Invalid PPOS ndims.")
    
    if (ppos.shape[1] < +3):
        raise Exception("Invalid PPOS shape.")
    
    nump = ppos.shape[0]

    if (tri3.ndim != +2):
        raise Exception("Invalid TRIA ndims.")

    if (tri3.shape[1] < +4):
        raise Exception("Invalid TRIA shape.")

    if (np.min(tri3[:,0:3]) < +0 or 
            np.max(tri3[:,0:3]) >= nump):
        raise Exception("Invalid TRIA index.")

    return okay


def trivol2(ppos, tri2):
    """
    TRIVOL2 calc. triangle area for 2-simplex triangulation. 
    embedded in euclidean space.

    """

    okay = istri_2(ppos, tri2)

#--------------------------------------- compute signed area

    ee12 = ppos[tri2[:,1],:]-ppos[tri2[:,0],:]
    ee13 = ppos[tri2[:,2],:]-ppos[tri2[:,0],:]

    if   (ppos.shape[1] == +2):

        vol2 = ee12[:,0] * ee13[:,1] \
             - ee12[:,1] * ee13[:,0]

        vol2 = 0.5 * vol2

    elif (ppos.shape[1] == +3):

        avec = np.cross (ee12, ee13)
        vol2 = np.sqrt(
            np.sum(avec**2, axis=1))
        
        vol2 = 0.5 * vol2

    else:
        raise Exception("Invalid dimension!!")

    return vol2


def trivol3(ppos, tri3):
    """
    TRIVOL3 calc. cell volumes for a 3-simplex triangulation 
    embedded in euclidean space.

    """

    okay = istri_3(ppos, tri3)

#--------------------------------------- compute signed vol.

    vv14 = ppos[tri3[:,3],:]-ppos[tri3[:,0],:]
    vv24 = ppos[tri3[:,3],:]-ppos[tri3[:,1],:]
    vv34 = ppos[tri3[:,3],:]-ppos[tri3[:,2],:]

    if   (ppos.shape[1] == +3):

        vdet = \
            + vv14[:,0] * \
             (vv24[:,1] * vv34[:,2]  \
            - vv24[:,2] * vv34[:,1]) \
            - vv14[:,1] * \
             (vv24[:,0] * vv34[:,2]  \
            - vv24[:,2] * vv34[:,0]) \
            + vv14[:,2] * \
             (vv24[:,0] * vv34[:,1]  \
            - vv24[:,1] * vv34[:,0])

        vol3 = vdet / 6.0

    else:
        raise Exception("Invalid dimension!!")

    return vol3


def normal1(ppos, tri1):
    """
    NORMAL1 normal vec. assoc. with 1-simplex triangulation.

    """

    okay = istri_1(ppos, tri1)

#------------------------------------- compute tria. normals
    
    evec = ppos[tri1[:,1],:]-ppos[tri1[:,0],:]

    nvec = np.empty(
        (np.size(tri1,0),2), dtype=ppos.dtype)

    nvec[:,0] = - evec[:,1]
    nvec[:,1] = + evec[:,0]

    return nvec


def normal2(ppos, tri2):
    """
    NORMAL2 normal vec. assoc. with 2-simplex triangulation.

    """

    okay = istri_2(ppos, tri2)

#------------------------------------- compute tria. normals
    
    ee12 = ppos[tri2[:,1],:]-ppos[tri2[:,0],:]
    ee13 = ppos[tri2[:,2],:]-ppos[tri2[:,0],:]

    nvec = np.empty(
        (np.size(tri2,0),3), dtype=ppos.dtype)

    nvec[:,0] = ee12[:,1] * ee13[:,2] \
              - ee12[:,2] * ee13[:,1]
    nvec[:,1] = ee12[:,2] * ee13[:,0] \
              - ee12[:,0] * ee13[:,2]
    nvec[:,2] = ee12[:,0] * ee13[:,1] \
              - ee12[:,1] * ee13[:,0]

    return nvec


def orient1(ppos, posa, posb):
    """
    ORIENT1 return orientation of PP wrt. the line [PA, PB].
    
    """

#---------------------------------------------- calc. det(S)

    smat = np.empty(
        (2,2,ppos.shape[0]), dtype=ppos.dtype)

    smat[0,0,:] = apos[:,0]-ppos[:,0]
    smat[0,1,:] = apos[:,1]-ppos[:,1]

    smat[1,0,:] = bpos[:,0]-ppos[:,0]
    smat[1,1,:] = bpos[:,1]-ppos[:,1]

    sign =  (
        smat[0,0,:] * smat[1,1,:]
      - smat[0,1,:] * smat[1,0,:]
            )

    return np.reshape(sign, (sign.size))


def orient2(ppos, posa, posb):
    """
    ORIENT2 return orientation of PP wrt. face [PA, PB, PC].
    
    """

#---------------------------------------------- calc. det(S)

    smat = np.empty(
        (3,3,ppos.shape[0]), dtype=ppos.dtype)

    smat[0,0,:] = apos[:,0]-ppos[:,0]
    smat[0,1,:] = apos[:,1]-ppos[:,1]
    smat[0,2,:] = apos[:,2]-ppos[:,2]
    
    smat[1,0,:] = bpos[:,0]-ppos[:,0]
    smat[1,1,:] = bpos[:,1]-ppos[:,1]
    smat[1,2,:] = bpos[:,2]-ppos[:,2]

    smat[2,0,:] = cpos[:,0]-ppos[:,0]
    smat[2,1,:] = cpos[:,1]-ppos[:,1]
    smat[2,2,:] = cpos[:,2]-ppos[:,2]

    sign =  \
        smat[0,0,:] * (
        smat[1,1,:] * smat[2,2,:]
      - smat[1,2,:] * smat[2,1,:]
            ) - \
        smat[0,1,:] * (
        smat[1,0,:] * smat[2,2,:] 
      - smat[1,2,:] * smat[2,0,:]
            ) + \
        smat[0,2,:] * (
        smat[1,0,:] * smat[2,1,:] 
      - smat[1,1,:] * smat[2,0,:]
            )

    return np.reshape(sign, (sign.size))



