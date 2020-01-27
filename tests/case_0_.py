"""
* DEMO-0 --- a simple example demonstrating the construction
*   of 2-d. geometry and user-defined mesh-size constraints.
*
* These examples call to JIGSAW via its api.-lib. interface.
*
* Writes "case_0x.vtk" files on output for vis. in PARAVIEW.
*
"""

import os
import numpy as np
import jigsawpy


def case_0a(src_path, dst_path):

    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ define JIGSAW geometry

    geom.mshID = "euclidean-mesh"
    geom.ndims = +2
    geom.vert2 = np.array([   # list of xy "node" coordinate
        ((0, 0), 0),          # outer square
        ((9, 0), 0),
        ((9, 9), 0),
        ((0, 9), 0),
        ((4, 4), 0),          # inner square
        ((5, 4), 0),
        ((5, 5), 0),
        ((4, 5), 0)],
        dtype=geom.VERT2_t)

    geom.edge2 = np.array([   # list of "edges" between vert
        ((0, 1), 0),          # outer square
        ((1, 2), 0),
        ((2, 3), 0),
        ((3, 0), 0),
        ((4, 5), 0),          # inner square
        ((5, 6), 0),
        ((6, 7), 0),
        ((7, 4), 0)],
        dtype=geom.EDGE2_t)

#------------------------------------ build mesh via JIGSAW!

    print("Call libJIGSAW: case 0a.")

    opts.hfun_hmax = 0.05               # push HFUN limits

    opts.mesh_dims = +2                 # 2-dim. simplexes

    opts.optm_qlim = +.95

    opts.mesh_top1 = True               # for sharp feat's
    opts.geom_feat = True

    jigsawpy.lib.jigsaw(opts, geom, mesh)

    scr2 = jigsawpy.triscr2(            # "quality" metric
        mesh.point["coord"],
        mesh.tria3["index"])

    print("Saving case_0a.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_0a.vtk"), mesh)

    return


def case_0b(src_path, dst_path):

    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ define JIGSAW geometry

    geom.mshID = "euclidean-mesh"
    geom.ndims = +2
    geom.vert2 = np.array([   # list of xy "node" coordinate
        ((0, 0), 0),            # outer square
        ((9, 0), 0),
        ((9, 9), 0),
        ((0, 9), 0),
        ((2, 2), 0),            # inner square
        ((7, 2), 0),
        ((7, 7), 0),
        ((2, 7), 0),
        ((3, 3), 0),
        ((6, 6), 0)],
        dtype=geom.VERT2_t)

    geom.edge2 = np.array([   # list of "edges" between vert
        ((0, 1), 0),            # outer square
        ((1, 2), 0),
        ((2, 3), 0),
        ((3, 0), 0),
        ((4, 5), 0),            # inner square
        ((5, 6), 0),
        ((6, 7), 0),
        ((7, 4), 0),
        ((8, 9), 0)],
        dtype=geom.EDGE2_t)

    et = jigsawpy.\
        jigsaw_def_t.JIGSAW_EDGE2_TAG

    geom.bound = np.array([
        (1, 0, et),
        (1, 1, et),
        (1, 2, et),
        (1, 3, et),
        (1, 4, et),
        (1, 5, et),
        (1, 6, et),
        (1, 7, et),
        (2, 4, et),
        (2, 5, et),
        (2, 6, et),
        (2, 7, et)],
        dtype=geom.BOUND_t)

#------------------------------------ build mesh via JIGSAW!

    print("Call libJIGSAW: case 0b.")

    opts.hfun_hmax = 0.05               # push HFUN limits

    opts.mesh_dims = +2                 # 2-dim. simplexes

    opts.optm_qlim = +.95

    opts.mesh_top1 = True               # for sharp feat's
    opts.geom_feat = True

    jigsawpy.lib.jigsaw(opts, geom, mesh)

    print("Saving case_0b.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_0b.vtk"), mesh)

    return


def case_0c(src_path, dst_path):

    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    hmat = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ define JIGSAW geometry

    geom.mshID = "euclidean-mesh"
    geom.ndims = +2
    geom.vert2 = np.array([   # list of xy "node" coordinate
        ((0, 0), 0),          # outer square
        ((9, 0), 0),
        ((9, 9), 0),
        ((0, 9), 0),
        ((4, 4), 0),          # inner square
        ((5, 4), 0),
        ((5, 5), 0),
        ((4, 5), 0)],
        dtype=geom.VERT2_t)

    geom.edge2 = np.array([   # list of "edges" between vert
        ((0, 1), 0),          # outer square
        ((1, 2), 0),
        ((2, 3), 0),
        ((3, 0), 0),
        ((4, 5), 0),          # inner square
        ((5, 6), 0),
        ((6, 7), 0),
        ((7, 4), 0)],
        dtype=geom.EDGE2_t)

#------------------------------------ compute HFUN over GEOM

    xgeo = geom.vert2["coord"][:, 0]
    ygeo = geom.vert2["coord"][:, 1]

    xpos = np.linspace(
        xgeo.min(), xgeo.max(), 32)

    ypos = np.linspace(
        ygeo.min(), ygeo.max(), 16)

    xmat, ymat = np.meshgrid(xpos, ypos)

    hfun = -0.4 * np.exp(-(
        0.1 * (xmat - 4.5) ** 2 +
        0.1 * (ymat - 4.5) ** 2)) + 0.6

    hmat.mshID = "euclidean-grid"
    hmat.ndims = +2
    hmat.xgrid = np.array(
        xpos, dtype=hmat.REALS_t)
    hmat.ygrid = np.array(
        ypos, dtype=hmat.REALS_t)
    hmat.value = np.array(
        hfun, dtype=hmat.REALS_t)

#------------------------------------ build mesh via JIGSAW!

    print("Call libJIGSAW: case 0c.")

    opts.hfun_scal = "absolute"
    opts.hfun_hmax = float("inf")       # null HFUN limits
    opts.hfun_hmin = float(+0.00)

    opts.mesh_dims = +2                 # 2-dim. simplexes

    opts.optm_qlim = +.95

    opts.mesh_top1 = True               # for sharp feat's
    opts.geom_feat = True

    jigsawpy.lib.jigsaw(opts, geom, mesh,
                        None, hmat)

    print("Saving case_0c.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_0c.vtk"), mesh)

    return


def case_0_(src_path, dst_path):

#------------------------------------ build various examples

    case_0a(src_path, dst_path)
    case_0b(src_path, dst_path)
    case_0c(src_path, dst_path)

    return
