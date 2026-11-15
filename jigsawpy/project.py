
import numpy as np
from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.prj_t import jigsaw_prj_t
from jigsawpy.certify import certify
from jigsawpy.tools.projector import stereo3


def _value_scale_shape(data, scal, stag):
    if data.ndim == 0 or data.shape[0] != scal.size:
        raise ValueError("Invalid MESH." + stag + " size")

    return (scal.size,) + (1,) * (data.ndim - 1)


def _scale_values(data, scal, stag):
    data *= scal.reshape(
        _value_scale_shape(data, scal, stag))
    return data


def _scale_flat_values(data, scal, stag):
    if not scal.size or data.size % scal.size:
        raise ValueError("Invalid MESH." + stag + " size")

    data = np.reshape(data, data.size)
    data.reshape((scal.size, -1))[:]*= scal[:, np.newaxis]
    return data


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
        raise TypeError("Incorrect type: MESH.")

    if (not isinstance(proj, jigsaw_prj_t)):
        raise TypeError("Incorrect type: PROJ.")

    if (not isinstance(sign, str)):
        raise TypeError("Incorrect type: SIGN.")

    sign = sign.lower()
    if sign not in ("fwd", "inv"):
        raise ValueError("Incorrect projection PRJID flags.")

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
            else:
                raise ValueError(
                    "Projection operator not suppoted.")

    #----------------------------------- setup proj.'d object
            if   (sign == "fwd"):
                kind = "euclidean-mesh"
                radii = None
            else:
                kind = "ellipsoid-mesh"
                radii = np.full(
                    +3, proj.radii, 
                        dtype=jigsaw_msh_t.REALS_t)

            if mesh.value is not None and mesh.value.size:
                _value_scale_shape(mesh.value, SCAL, "VALUE")

            SPOW = (
                SCAL ** 2 if mesh.power is not None and 
                             mesh.power.size else None
            )
            if mesh.power is not None and mesh.power.size:
                _value_scale_shape(mesh.power, SPOW, "POWER")

            mesh.mshID = kind
            mesh.radii = radii
            mesh.point["coord"][:, 0] = XNEW
            mesh.point["coord"][:, 1] = YNEW

    #----------------------------------- setup proj.'d extras
            if mesh.value is not None and mesh.value.size:
                _scale_values(mesh.value, SCAL, "VALUE")
            if mesh.power is not None and mesh.power.size:
                _scale_values(mesh.power, SPOW, "POWER")

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
            else:
                raise ValueError(
                    "Projection operator not suppoted.")

    #----------------------------------- setup proj.'d object
            if   (sign == "fwd"):
                kind = "euclidean-mesh"
                radii = None
            else:
                kind = "ellipsoid-mesh"
                radii = np.full(
                    +3, proj.radii,
                        dtype=jigsaw_msh_t.REALS_t)

            if mesh.value is not None and mesh.value.size:
                if mesh.value.size % SCAL.size:
                    raise ValueError("Invalid MESH.VALUE size")

            if mesh.power is not None and mesh.power.size:
                if mesh.power.size % SCAL.size:
                    raise ValueError("Invalid MESH.POWER size")

            mesh.mshID = kind
            mesh.radii = radii
            mesh.point = np.empty(
                XNEW.size, dtype=jigsaw_msh_t.VERT2_t)
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
            tset = []
            for jpos in range(dim2 - 1):

    #----------------------------------- 1st tria. per column
                triaA = np.empty(
                    dim1 - 1, dtype=mesh.TRIA3_t)

                triaA["IDtag"] = 0

                index = triaA["index"]
                index[:, 0] = range(0, dim1 - 1)
                index[:, 0] += (jpos + 0) * dim1

                index[:, 1] = range(1, dim1 - 0)
                index[:, 1] += (jpos + 0) * dim1

                index[:, 2] = range(1, dim1 - 0)
                index[:, 2] += (jpos + 1) * dim1

                tset.append(triaA)

    #----------------------------------- 2nd tria. per column
                triaB = np.empty(
                    dim1 - 1, dtype=mesh.TRIA3_t)

                triaB["IDtag"] = 0

                index = triaB["index"]
                index[:, 0] = range(0, dim1 - 1)
                index[:, 0] += (jpos + 0) * dim1

                index[:, 1] = range(1, dim1 - 0)
                index[:, 1] += (jpos + 1) * dim1

                index[:, 2] = range(0, dim1 - 1)
                index[:, 2] += (jpos + 1) * dim1

                tset.append(triaB)

            mesh.tria3 = np.concatenate(tset, axis=0)

    #----------------------------------- setup proj.'d extras
            if mesh.slope is not None and mesh.slope.size:
                mesh.slope = np.reshape(
                    mesh.slope, mesh.slope.size)

            if mesh.value is not None and mesh.value.size:
                mesh.value = _scale_flat_values(
                    mesh.value, SCAL ** 1, "VALUE")

            if mesh.power is not None and mesh.power.size:
                mesh.power = _scale_flat_values(
                    mesh.power, SCAL ** 2, "POWER")

    return
