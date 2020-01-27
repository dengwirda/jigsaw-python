
""" MSH_T: Container struct. for JIGSAW's mesh data.

    .IF. MESH.MSHID == 'EUCLIDEAN-MESH':
    -----------------------------------

    MESH.VERT2 - [V2x 1] array of 2dim. point coordinates,
        VERT2 is a JIGSAW_MSH_t.VERT2_t structure, where:
        VERT2["COORD"] is an array of coordinate values,
        VERT2["IDTAG"] is an ID tag assigned at each vertex.

    MESH.VERT3 - [V3x 1] array of 3dim. point coordinates,
        VERT3 is a JIGSAW_MSH_t.VERT3_t structure, where:
        VERT3["COORD"] is an array of coordinate values,
        VERT3["IDTAG"] is an ID tag assigned at each vertex.

    MESH.POWER - [NVx 1] array of vertex "weights"
        associated with the dual "power" tessellation.

    MESH.EDGE2 - [E2x 1] array of EDGE-2 cell definitions,
        EDGE2 is a JIGSAW_MSH_t.EDGE2_t structure, where:
        EDGE2["INDEX"] is an array of cell indexing,
        EDGE2["IDTAG"] is an ID tag assigned at each cell.

    MESH.TRIA3 - [T3x 1] array of TRIA-3 cell definitions,
        TRIA3 is a JIGSAW_MSH_t.TRIA3_t structure, where:
        TRIA3["INDEX"] is an array of cell indexing,
        TRIA3["IDTAG"] is an ID tag assigned at each cell.

    MESH.QUAD4 - [Q4x 1] array of QUAD-4 cell definitions,
        QUAD4 is a JIGSAW_MSH_t.QUAD4_t structure, where:
        QUAD4["INDEX"] is an array of cell indexing,
        QUAD4["IDTAG"] is an ID tag assigned at each cell.

    MESH.TRIA4 - [T4x 1] array of TRIA-4 cell definitions,
        TRIA4 is a JIGSAW_MSH_t.QUAD4_t structure, where:
        TRIA4["INDEX"] is an array of cell indexing,
        TRIA4["IDTAG"] is an ID tag assigned at each cell.

    MESH.HEXA8 - [H8x 1] array of HEXA-8 cell definitions,
        HEXA8 is a JIGSAW_MSH_t.HEXA8_t structure, where:
        HEXA8["INDEX"] is an array of cell indexing,
        HEXA8["IDTAG"] is an ID tag assigned at each cell.

    MESH.WEDG6 - [W6x 1] array of WEDG-6 cell definitions,
        WEDG6 is a JIGSAW_MSH_t.WEDG6_t structure, where:
        WEDG6["INDEX"] is an array of cell indexing,
        WEDG6["IDTAG"] is an ID tag assigned at each cell.

    MESH.PYRA5 - [P5x 1] array of PYRA-5 cell definitions,
        PYRA5 is a JIGSAW_MSH_t.PYRA5_t structure, where:
        PYRA5["INDEX"] is an array of cell indexing,
        PYRA5["IDTAG"] is an ID tag assigned at each cell.

    MESH.BOUND - [NBx 1] array of "boundary" indexing,
        BOUND is a JIGSAW_MSH_t.BOUND_t structure, defining
        how elements in the geometry are associated with
        enclosed areas/volumes, herein known as "parts":
        BOUND["INDEX"] is an array of cell indexing,
        BOUND["CELLS"] is an array of cell tags, defining
        which element "kind" is indexed via BOUND["INDEX"]
        BOUND["IDTAG"] is an ID tag assigned to each part.

        In the default case, where BOUND is not specified,
        all elements in the geometry are assumed to define
        the boundaries of enclosed "parts".

    MESH.VALUE - [NPxNV] array of "values" associated with
        the vertices of the mesh.

    .IF. MESH.MSHID == 'ELLIPSOID-MESH':
    -----------------------------------

    MESH.RADII - [ 3x 1] array of principal ellipsoid radii.

    Additionally, entities described in the 'EUCLIDEAN-MESH'
    specification may be optionally defined.

    .IF. MESH.MSHID == 'EUCLIDEAN-GRID':
    .OR. MESH.MSHID == 'ELLIPSOID-GRID':
    -----------------------------------

    MESH.XGRID - [NXx 1] array of "x-axis" grid coordinates.
        Values must increase or decrease monotonically.

    MESH.YGRID - [NYx 1] array of "y-axis" grid coordinates.
        Values must increase or decrease monotonically.

    MESH.ZGRID - [NZx 1] array of "z-axis" grid coordinates.
        Values must increase or decrease monotonically.

    MESH.VALUE - [NMxNV] array of "values" associated with
        vertices in the grid, where NM is the product of
        the dimensions of the grid. NV values are associated
        with each vertex.

    MESH.SLOPE - [NMx 1] array of "slopes" associated with
        vertices in the grid, where NM is the product of
        the dimensions of the grid. Slope values define the
        gradient-limits ||dh/dx|| used by the Eikonal solver
        MARCHE.

    See also JIG_t


    --------------------------------------------------------
    """

import numpy as np


class jigsaw_msh_t:
    #------------------------------------------ MESH typedef
    REALS_t = np.float64
    INDEX_t = np.int32

    T = True

    VERT2_t = np.dtype([("coord", REALS_t, 2),
                        ("IDtag", INDEX_t)], align=T)

    VERT3_t = np.dtype([("coord", REALS_t, 3),
                        ("IDtag", INDEX_t)], align=T)

    EDGE2_t = np.dtype([("index", INDEX_t, 2),
                        ("IDtag", INDEX_t)], align=T)

    TRIA3_t = np.dtype([("index", INDEX_t, 3),
                        ("IDtag", INDEX_t)], align=T)

    QUAD4_t = np.dtype([("index", INDEX_t, 4),
                        ("IDtag", INDEX_t)], align=T)

    TRIA4_t = np.dtype([("index", INDEX_t, 4),
                        ("IDtag", INDEX_t)], align=T)

    HEXA8_t = np.dtype([("index", INDEX_t, 8),
                        ("IDtag", INDEX_t)], align=T)

    WEDG6_t = np.dtype([("index", INDEX_t, 6),
                        ("IDtag", INDEX_t)], align=T)

    PYRA5_t = np.dtype([("index", INDEX_t, 5),
                        ("IDtag", INDEX_t)], align=T)

    BOUND_t = np.dtype([("IDtag", INDEX_t),
                        ("index", INDEX_t),
                        ("cells", INDEX_t)], align=T)

    def __init__(self):
    #------------------------------------------ MESH struct.
        self.mshID = "euclidean-mesh"
        self.ndims = +0

        DIM1 = (0); DIM2 = (0, 0)

        self.radii = np.empty(
            DIM1, dtype=jigsaw_msh_t.REALS_t)

        self.vert2 = np.empty(
            DIM1, dtype=jigsaw_msh_t.VERT2_t)
        self.vert3 = np.empty(
            DIM1, dtype=jigsaw_msh_t.VERT3_t)

        self.power = np.empty(
            DIM2, dtype=jigsaw_msh_t.REALS_t)

        self.edge2 = np.empty(
            DIM1, dtype=jigsaw_msh_t.EDGE2_t)
        self.tria3 = np.empty(
            DIM1, dtype=jigsaw_msh_t.TRIA3_t)
        self.quad4 = np.empty(
            DIM1, dtype=jigsaw_msh_t.QUAD4_t)
        self.tria4 = np.empty(
            DIM1, dtype=jigsaw_msh_t.TRIA4_t)
        self.hexa8 = np.empty(
            DIM1, dtype=jigsaw_msh_t.HEXA8_t)
        self.pyra5 = np.empty(
            DIM1, dtype=jigsaw_msh_t.PYRA5_t)
        self.wedg6 = np.empty(
            DIM1, dtype=jigsaw_msh_t.WEDG6_t)

        self.bound = np.empty(
            DIM1, dtype=jigsaw_msh_t.BOUND_t)

        self.xgrid = np.empty(
            DIM1, dtype=jigsaw_msh_t.REALS_t)
        self.ygrid = np.empty(
            DIM1, dtype=jigsaw_msh_t.REALS_t)
        self.zgrid = np.empty(
            DIM1, dtype=jigsaw_msh_t.REALS_t)

        self.value = np.empty(
            DIM2, dtype=jigsaw_msh_t.REALS_t)

        self.slope = np.empty(
            DIM2, dtype=jigsaw_msh_t.REALS_t)

    @property
    def point(self):
    #------------------------------------------ POINT helper
        verts = self.vert2
        if (verts is not None and verts.size):
            return verts

        verts = self.vert3
        if (verts is not None and verts.size):
            return verts

        return None

    @point.setter
    def point(self, verts):
    #------------------------------------------ POINT helper
        if (isinstance(verts, np.ndarray) and
                verts.dtype == self.VERT2_t):

            self.vert2 = verts; return

        if (isinstance(verts, np.ndarray) and
                verts.dtype == self.VERT3_t):

            self.vert3 = verts; return

        raise Exception("Invalid POINT type")



