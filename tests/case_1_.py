"""
* DEMO-1 --- a simple example demonstrating the construction
*   of 3-d. geometry and user-defined mesh-size constraints.
*
* These examples call to JIGSAW via its api.-lib. interface.
*
* Writes "case_1x.vtk" files on output for vis. in PARAVIEW.
*
"""

import os
import numpy as np

import jigsawpy


def case_1a(src_path, dst_path):

    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ define JIGSAW geometry

    geom.mshID = "euclidean-mesh"
    geom.ndims = +3
    geom.vert3 = np.array([  # list of xy "node" coordinates
        ((0, 0, 0), 0),
        ((3, 0, 0), 0),
        ((3, 3, 0), 0),
        ((0, 3, 0), 0),
        ((0, 0, 3), 0),
        ((3, 0, 3), 0),
        ((3, 3, 3), 0),
        ((0, 3, 3), 0)],
        dtype=geom.VERT3_t)

    geom.tria3 = np.array([  # list of "tria" between points
        ((0, 1, 2), 0),
        ((0, 2, 3), 0),
        ((4, 5, 6), 0),
        ((4, 6, 7), 0),
        ((0, 1, 5), 0),
        ((0, 5, 4), 0),
        ((1, 2, 6), 0),
        ((1, 6, 5), 0),
        ((2, 3, 7), 0),
        ((2, 7, 6), 0),
        ((3, 7, 4), 0),
        ((3, 4, 0), 0)],
        dtype=geom.TRIA3_t)

#------------------------------------ build mesh via JIGSAW!

    print("Call libJIGSAW: case 1a.")

    opts.hfun_hmax = 0.08               # push HFUN limits

    opts.mesh_dims = +3                 # 3-dim. simplexes

    opts.mesh_top1 = True               # for sharp feat's
    opts.geom_feat = True

    jigsawpy.lib.jigsaw(opts, geom, mesh)

    scr3 = jigsawpy.triscr3(            # "quality" metric
        mesh.point["coord"],
        mesh.tria4["index"])

    print("Saving case_1a.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_1a.vtk"), mesh)

    return


def case_1b(src_path, dst_path):

    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    hmat = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ define JIGSAW geometry

    geom.mshID = "euclidean-mesh"
    geom.ndims = +3
    geom.vert3 = np.array([  # list of xy "node" coordinates
        ((0, 0, 0), 0),
        ((3, 0, 0), 0),
        ((3, 3, 0), 0),
        ((0, 3, 0), 0),
        ((0, 0, 3), 0),
        ((3, 0, 3), 0),
        ((3, 3, 3), 0),
        ((0, 3, 3), 0)],
        dtype=geom.VERT3_t)

    geom.tria3 = np.array([  # list of "tria" between points
        ((0, 1, 2), 0),
        ((0, 2, 3), 0),
        ((4, 5, 6), 0),
        ((4, 6, 7), 0),
        ((0, 1, 5), 0),
        ((0, 5, 4), 0),
        ((1, 2, 6), 0),
        ((1, 6, 5), 0),
        ((2, 3, 7), 0),
        ((2, 7, 6), 0),
        ((3, 7, 4), 0),
        ((3, 4, 0), 0)],
        dtype=geom.TRIA3_t)

#------------------------------------ compute HFUN over GEOM

    xgeo = geom.vert3["coord"][:, 0]
    ygeo = geom.vert3["coord"][:, 1]
    zgeo = geom.vert3["coord"][:, 2]

    xpos = np.linspace(
        xgeo.min(), xgeo.max(), 32)

    ypos = np.linspace(
        ygeo.min(), ygeo.max(), 16)

    zpos = np.linspace(
        zgeo.min(), zgeo.max(), 64)

    xmat, ymat, zmat = \
        np.meshgrid(xpos, ypos, zpos)

    hfun = 0.4 - 0.3 * np.exp(
        - 2.0 * (xmat - 1.50) ** 2
        - 2.0 * (ymat - 1.50) ** 2
        - 2.0 * (zmat - 1.50) ** 2)

    hmat.mshID = "euclidean-grid"
    hmat.ndims = +3
    hmat.xgrid = np.array(
        xpos, dtype=hmat.REALS_t)
    hmat.ygrid = np.array(
        ypos, dtype=hmat.REALS_t)
    hmat.zgrid = np.array(
        zpos, dtype=hmat.REALS_t)
    hmat.value = np.array(
        hfun, dtype=hmat.REALS_t)

#------------------------------------ build mesh via JIGSAW!

    print("Call libJIGSAW: case 1b.")

    opts.hfun_scal = "absolute"
    opts.hfun_hmax = float("inf")       # null HFUN limits
    opts.hfun_hmin = float(+0.00)

    opts.mesh_dims = +3                 # 3-dim. simplexes

    opts.mesh_top1 = True               # for sharp feat's
    opts.geom_feat = True

    jigsawpy.lib.jigsaw(opts, geom, mesh,
                        None, hmat)

    print("Saving case_1b.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_1b.vtk"), mesh)

    return


def case_1_(src_path, dst_path):

#------------------------------------ build various examples

    case_1a(src_path, dst_path)
    case_1b(src_path, dst_path)

    return



