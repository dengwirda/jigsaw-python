"""
* DEMO-2 --- Build planar meshes for the "lakes" geometry.
% Compare performance of "delaunay" + "delfront" algorithms.
*
* These examples call to JIGSAW via its cmd.-line interface.
*
* Writes "case_2x.vtk" files on output for vis. in PARAVIEW.
*
"""

import os

import jigsawpy


def case_2_(src_path, dst_path):

    opts = jigsawpy.jigsaw_jig_t()

    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        os.path.join(src_path, "lakes.msh")

    opts.jcfg_file = \
        os.path.join(dst_path, "lakes.jig")

    opts.mesh_file = \
        os.path.join(dst_path, "lakes.msh")

#------------------------------------ make mesh using JIGSAW

    opts.mesh_kern = "delaunay"         # DELAUNAY kernel
    opts.mesh_dims = +2

    opts.mesh_top1 = True               # mesh sharp feat.
    opts.geom_feat = True

    opts.optm_iter = +0

    opts.hfun_hmax = 0.02

    jigsawpy.cmd.jigsaw(opts, mesh)

    print("Saving case_2a.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_2a.vtk"), mesh)

#------------------------------------ make mesh using JIGSAW

    opts.mesh_kern = "delfront"         # DELFRONT kernel
    opts.mesh_dims = +2

    opts.mesh_top1 = True               # mesh sharp feat.
    opts.geom_feat = True

    opts.optm_iter = +0

    opts.hfun_hmax = 0.02

    jigsawpy.cmd.jigsaw(opts, mesh)

    print("Saving case_2b.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_2b.vtk"), mesh)

    return
