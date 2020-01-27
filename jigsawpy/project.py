
import numpy as np
from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.prj_t import jigsaw_prj_t
from jigsawpy.certify import certify
from jigsawpy.tools.projector import stereo3


def project(mesh, proj, sign):
    """
    PROJECT cartographic projections for JIGSAW MSH objects.

    PROJECT(MESH,PROJ,SIGN) returns the projected mesh
    object MESH resulting from application of the projection
    operator PROJ to the input object MESH. SIGN is a string
    defining the "sense" of the projection, either
    SIGN="FWD" for forward projections or SIGN="INV" for the
    inverse operation.

    The following projection operators are supported:

        PROJ.PRJID = "stereographic"
        PROJ.RADII = # sphere radii.
        PROJ.XBASE = # central XLON.
        PROJ.YBASE = # central YLAT.

    """

    if (not isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    if (not isinstance(proj, jigsaw_prj_t)):
        raise Exception("Incorrect type: PROJ.")

    if (not isinstance(sign, str)):
        raise Exception("Incorrect type: SIGN.")

    certify(mesh)

    kind = mesh.mshID.lower()

    if   (kind == "euclidean-mesh" or
          kind == "ellipsoid-mesh"):

    #------------------------------- proj. from MESH to MESH

        if (mesh.vert2 is not None and
                mesh.vert2.size != +0):

            XPOS = mesh.point["coord"][:, 0]
            YPOS = mesh.point["coord"][:, 1]

    #----------------------------------- proj. geometry parts
            if   (proj.prjID.lower() == "stereographic"):

                XNEW, YNEW, SCAL = stereo3(
                    proj.radii, XPOS, YPOS,
                    proj.xbase, proj.ybase, sign)

                """
            elif (proj.prjID.lower() == "hammer-aitoff"):

                XNEW, YNEW, SCAL = hammer3(
                    proj.radii, XPOS, YPOS,
                    proj.xbase, proj.ybase, sign)
                """

            else:

                raise Exception(
                    "Projection operator not suppoted.")

    #----------------------------------- setup proj.'d object
            if   (sign.lower() == "fwd"):

                mesh.mshID = "euclidean-mesh"

                if (mesh.radii is not None):
                    mesh.radii = None

            elif (sign.lower() == "inv"):

                mesh.mshID = "ellipsoid-mesh"

                mesh.radii = np.full(
                    +3, proj.radii,
                    dtype=jigsaw_msh_t.REALS_t)

            else:

                raise Exception(
                    "Incorrect projection PRJID flags.")

            mesh.point["coord"][:, 0] = XNEW
            mesh.point["coord"][:, 1] = YNEW

    #----------------------------------- setup proj.'d extras
            if (mesh.value is not None and
                    mesh.value.size != +0):

                mesh.value = mesh.value * SCAL

            if (mesh.power is not None and
                    mesh.power.size != +0):

                SPOW = np.sqrt(SCAL)

                mesh.power = mesh.power * SPOW

    elif (kind == "euclidean-grid" or
          kind == "ellipsoid-grid"):

    #------------------------------- proj. from GRID to MESH

        if (mesh.xgrid is not None and
                mesh.xgrid.size != +0 and
            mesh.ygrid is not None and
                mesh.ygrid.size != +0):

            XPOS, YPOS = \
                np.meshgrid(mesh.xgrid, mesh.ygrid)

            XPOS = np.reshape(XPOS, (XPOS.size))
            YPOS = np.reshape(YPOS, (YPOS.size))

    #----------------------------------- proj. geometry parts
            if   (proj.prjID.lower() == "stereographic"):

                XNEW, YNEW, SCAL = stereo3(
                    proj.radii, XPOS, YPOS,
                    proj.xbase, proj.ybase, sign)

                """
            elif (proj.prjID.lower() == "hammer-aitoff"):

                XNEW, YNEW, SCAL = hammer3(
                    proj.radii, XPOS, YPOS,
                    proj.xbase, proj.ybase, sign)
                """

            else:

                raise Exception(
                    "Projection operator not suppoted.")

    #----------------------------------- setup proj.'d object
            mesh.point = np.empty(
                XNEW.size, dtype=jigsaw_msh_t.VERT2_t)

            if   (sign.lower() == "fwd"):

                mesh.mshID = "euclidean-mesh"

                if (mesh.radii is not None):
                    mesh.radii = None

            elif (sign.lower() == "inv"):

                mesh.mshID = "ellipsoid-mesh"

                mesh.radii = np.full(
                    +3, proj.radii,
                    dtype=jigsaw_msh_t.REALS_t)

            else:

                raise Exception(
                    "Incorrect projection PRJID flags.")

            mesh.point["IDtag"] = +0
            mesh.point["coord"][:, 0] = XNEW
            mesh.point["coord"][:, 1] = YNEW

    #----------------------------------- setup proj.'d topol.
            mesh.tria3 = np.empty(
                +0, dtype=jigsaw_msh_t.TRIA3_t)

            dim1 = mesh.xgrid.size
            mesh.xgrid = None

            dim2 = mesh.ygrid.size
            mesh.ygrid = None

            for jpos in range(dim2 - 1):

    #----------------------------------- 1st tria. per column
                triaA = np.empty(
                    (dim1 - 1),
                    dtype=jigsaw_msh_t.TRIA3_t)

                triaA["IDtag"] = 0

                index = triaA["index"]
                index[:, 0] = range(0, dim1 - 1)
                index[:, 0] += (jpos + 0) * dim1

                index[:, 1] = range(1, dim1 - 0)
                index[:, 1] += (jpos + 0) * dim1

                index[:, 2] = range(1, dim1 - 0)
                index[:, 2] += (jpos + 1) * dim1

                mesh.tria3 = np.append(
                    mesh.tria3, triaA, axis=+0)

    #----------------------------------- 2nd tria. per column
                triaB = np.empty(
                    (dim1 - 1),
                    dtype=jigsaw_msh_t.TRIA3_t)

                triaB["IDtag"] = 0

                index = triaB["index"]
                index[:, 0] = range(0, dim1 - 1)
                index[:, 0] += (jpos + 0) * dim1

                index[:, 1] = range(1, dim1 - 0)
                index[:, 1] += (jpos + 1) * dim1

                index[:, 2] = range(0, dim1 - 1)
                index[:, 2] += (jpos + 1) * dim1

                mesh.tria3 = np.append(
                    mesh.tria3, triaB, axis=+0)

    #----------------------------------- setup proj.'d extras
            if (mesh.slope is not None and
                    mesh.slope.size != +0):

                mesh.slope = np.reshape(
                    mesh.slope, mesh.slope.size)

            if (mesh.value is not None and
                    mesh.value.size != +0):

                mesh.value = np.reshape(
                    mesh.value, mesh.value.size)

                mesh.value = mesh.value * SCAL

            if (mesh.power is not None and
                    mesh.power.size != +0):

                mesh.power = np.reshape(
                    mesh.power, mesh.power.size)

                SPOW = np.sqrt(SCAL)

                mesh.power = mesh.power * SPOW

    return
