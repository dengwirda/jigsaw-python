
import numpy as np
from jigsawpy.tools.predicate import istri_1, istri_2, istri_3, \
    trivol2, trivol3, normal1, normal2, orient1, orient2


def triscr2(ppos, tri2):
    """
    TRISCR2 calc. area-len. ratios for cells in a 2-simplex
    triangulation.

    SCR2 = TRISCR2(VERT,TRIA) returns the area-len. ratios
    where SCR2 is a T-by-1 vector, VERT is a V-by-D array of
    XYZ coordinates, and TRIA is a T-by-3 array of
    vertex indexing, where each row defines a triangle, such
    that VERT[TRIA[II,0],:], VERT[TRIA[II,1],:] and
    VERT[TRIA[II,2],:] are the coord. of the II-TH triangle.

    """

    okay = istri_2(ppos, tri2)

#--------------------------- compute signed area-len. ratios

    scal = 4.0 * np.sqrt(3.0) / 3.0

    area = trivol2(ppos, tri2)

    pos1 = ppos[tri2[:, 0], :]
    pos2 = ppos[tri2[:, 1], :]
    pos3 = ppos[tri2[:, 2], :]

    lrms = \
        np.sum((pos2 - pos1)**2, axis=1) + \
        np.sum((pos3 - pos2)**2, axis=1) + \
        np.sum((pos1 - pos3)**2, axis=1)

    lrms = (lrms / 3.0) ** 1.0

    return (scal * area / lrms)


def triscr3(ppos, tri3):
    """
    TRISCR3 calc. vol.-len. ratios for cells in a 3-simplex
    triangulation.

    SCR3 = TRISCR3(VERT,TRIA) returns the vol.-len. ratios
    where SCR3 is a T-by-1 vector, VERT is a V-by-D array of
    XYZ coordinates, and TRIA is a T-by-4 array of
    vertex indexing, where each row defines a tetrahedron,
    such that VERT[TRIA[II,0],:], VERT[TRIA[II,1],:],
    VERT[TRIA[II,2],:] and VERT[TRIA[II,3],:] are the coord.
    of the II-TH triangle.

    """

    okay = istri_3(ppos, tri3)

#--------------------------- compute signed vol.-len. ratios

    scal = 6.0 * np.sqrt(2.0) / 1.0

    vol3 = trivol3(ppos, tri3)

    pos1 = ppos[tri3[:, 0], :]
    pos2 = ppos[tri3[:, 1], :]
    pos3 = ppos[tri3[:, 2], :]
    pos4 = ppos[tri3[:, 3], :]

    lrms = \
        np.sum((pos2 - pos1)**2, axis=1) + \
        np.sum((pos3 - pos2)**2, axis=1) + \
        np.sum((pos1 - pos3)**2, axis=1) + \
        np.sum((pos4 - pos1)**2, axis=1) + \
        np.sum((pos4 - pos2)**2, axis=1) + \
        np.sum((pos4 - pos3)**2, axis=1)

    lrms = (lrms / 6.0) ** 1.5

    return (scal * vol3 / lrms)


def trideg2(ppos, tri2):
    """
    TRIDEG2 calc. topological vertex degrees for a 2-simplex
    triangulation.

    VDEG = TRIDEG2(VERT,TRIA) returns the no. of triangles
    incident to each vertex. VDEG is a V-by-1 array of
    vertex degrees, VERT is a V-by-D array of XYZ coord. and
    TRIA is a T-by-3 array of vertex indexes, where each row
    defines a triangle, such that VERT[TRIA[II,0],:],
    VERT[TRIA[II,1],:] and VERT[TRIA[II,2],:] are the coord.
    of the II-TH triangle.

    """

    okay = istri_2(ppos, tri2)

#------------------------------------- compute vertex degree

    return np.bincount(
        np.reshape(tri2, (tri2.size)))


def trideg3(ppos, tri3):
    """
    TRIDEG3 calc. topological vertex degrees for a 3-simplex
    triangulation.

    VDEG = TRIDEG3(VERT,TRIA) returns the no. of tetrahedra
    incident to each vertex. VDEG is a V-by-1 array of
    vertex degrees, VERT is a V-by-D array of XYZ coord. and
    TRIA is a T-by-4 array of vertex indexes, where each row
    defines a tetrahedron, such that VERT[TRIA[II,0],:],
    VERT[TRIA[II,1],:], VERT[TRIA[II,2],:] and
    VERT[TRIA[II,3],:] are the coord. of the II-TH triangle.

    """

    okay = istri_3(ppos, tri3)

#------------------------------------- compute vertex degree

    return np.bincount(
        np.reshape(tri3, (tri3.size)))


def triang2(ppos, tri2):
    """
    TRIANG2 compute enclosed angles assoc. with a 2-simplex
    triangulation embedded in euclidean space.

    ADEG = TRIANG2(VERT,TRIA) returns the enclosed angles
    associated with each triangle, where ADEG is a T-by-3
    array of the angles subtended at each vertex, VERT is a
    V-by-D array of XYZ coordinates, and TRIA is a T-by-3
    array of vertex indexing, where each row defines a cell
    such that VERT[TRIA[II,0],:], VERT[TRIA[II,1],:] and
    VERT[TRIA[II,2],:] are the coord. of the II-TH triangle.

    Angles are returned in degrees.

    """

    okay = istri_2(ppos, tri2)

#----------------------------------- compute enclosed angles
    dcos = np.empty(
        (tri2.shape[0], 3), dtype=ppos.dtype)

    ee11 = normal1(ppos, tri2[:, (0, 1)])
    ee22 = normal1(ppos, tri2[:, (1, 2)])
    ee33 = normal1(ppos, tri2[:, (2, 0)])

    ll11 = np.sqrt(np.sum(
        ee11 ** 2, axis=1, keepdims=True))
    ll22 = np.sqrt(np.sum(
        ee22 ** 2, axis=1, keepdims=True))
    ll33 = np.sqrt(np.sum(
        ee33 ** 2, axis=1, keepdims=True))

    ee11 = ee11 / ll11
    ee22 = ee22 / ll22
    ee33 = ee33 / ll33

#--------------------------------- about each of the 3 nodes
    dcos[:, 0] = \
        np.sum(-ee11 * ee22, axis=1)
    dcos[:, 1] = \
        np.sum(-ee22 * ee33, axis=1)
    dcos[:, 2] = \
        np.sum(-ee33 * ee11, axis=1)

    dcos[:, 0] = \
        np.maximum(-1.0, dcos[:, 0])
    dcos[:, 0] = \
        np.minimum(+1.0, dcos[:, 0])
    dcos[:, 1] = \
        np.maximum(-1.0, dcos[:, 1])
    dcos[:, 1] = \
        np.minimum(+1.0, dcos[:, 1])
    dcos[:, 2] = \
        np.maximum(-1.0, dcos[:, 2])
    dcos[:, 2] = \
        np.minimum(+1.0, dcos[:, 2])

    return np.arccos(dcos) * 180. / np.pi


def triang3(ppos, tri3):
    """
    TRIANG3 compute enclosed angles assoc. with a 3-simplex
    triangulation embedded in euclidean space.

    ADEG = TRIANG3(VERT,TRIA) returns the enclosed angles
    associated with each tetrahedra, where ADEG is a T-by-6
    array of the angles subtended at each edge, VERT is a
    V-by-D array of XYZ coordinates, and TRIA is a T-by-4
    array of vertex indexing, where each row defines a cell
    such that VERT[TRIA[II,0],:], VERT[TRIA[II,1],:],
    VERT[TRIA[II,2],:] and VERT[TRIA[II,3],:] are the coord
    of the II-TH triangle.

    Angles are returned in degrees.

    """

    okay = istri_3(ppos, tri3)

#----------------------------------- compute enclosed angles
    dcos = np.empty(
        (tri3.shape[0], 6), dtype=ppos.dtype)

    ff11 = \
        normal2(ppos, tri3[:, (0, 1, 2)])
    ff22 = \
        normal2(ppos, tri3[:, (0, 1, 3)])
    ff33 = \
        normal2(ppos, tri3[:, (1, 2, 3)])
    ff44 = \
        normal2(ppos, tri3[:, (2, 0, 3)])

    ll11 = np.sqrt(np.sum(
        ff11 ** 2, axis=1, keepdims=True))
    ll22 = np.sqrt(np.sum(
        ff22 ** 2, axis=1, keepdims=True))
    ll33 = np.sqrt(np.sum(
        ff33 ** 2, axis=1, keepdims=True))
    ll44 = np.sqrt(np.sum(
        ff44 ** 2, axis=1, keepdims=True))

    ff11 = ff11 / ll11
    ff22 = ff22 / ll22
    ff33 = ff33 / ll33
    ff44 = ff44 / ll44

#--------------------------------- about each of the 6 edges
    #   11, 22: (1, 2)
    #   11, 33: (2, 3)
    #   11, 44: (3, 1)
    #   44, 22: (1, 4)
    #   22, 33: (2, 4)
    #   33, 44: (3, 4)

    dcos[:, 0] = \
        np.sum(+ff11 * ff22, axis=1)
    dcos[:, 1] = \
        np.sum(+ff11 * ff33, axis=1)
    dcos[:, 2] = \
        np.sum(+ff11 * ff44, axis=1)
    dcos[:, 3] = \
        np.sum(-ff44 * ff22, axis=1)
    dcos[:, 4] = \
        np.sum(-ff22 * ff33, axis=1)
    dcos[:, 5] = \
        np.sum(-ff33 * ff44, axis=1)

    dcos[:, 0] = \
        np.maximum(-1.0, dcos[:, 0])
    dcos[:, 0] = \
        np.minimum(+1.0, dcos[:, 0])
    dcos[:, 1] = \
        np.maximum(-1.0, dcos[:, 1])
    dcos[:, 1] = \
        np.minimum(+1.0, dcos[:, 1])
    dcos[:, 2] = \
        np.maximum(-1.0, dcos[:, 2])
    dcos[:, 2] = \
        np.minimum(+1.0, dcos[:, 2])
    dcos[:, 3] = \
        np.maximum(-1.0, dcos[:, 3])
    dcos[:, 3] = \
        np.minimum(+1.0, dcos[:, 3])
    dcos[:, 4] = \
        np.maximum(-1.0, dcos[:, 4])
    dcos[:, 4] = \
        np.minimum(+1.0, dcos[:, 4])
    dcos[:, 5] = \
        np.maximum(-1.0, dcos[:, 5])
    dcos[:, 5] = \
        np.minimum(+1.0, dcos[:, 5])

    return np.arccos(dcos) * 180. / np.pi
