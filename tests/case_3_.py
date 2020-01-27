"""
* DEMO-3 --- Build surface meshes for the "bunny" geometry.
% Compare performance of "delaunay" + "delfront" algorithms.
*
* These examples call to JIGSAW via its cmd.-line interface.
*
* Writes "case_3x.vtk" files on output for vis. in PARAVIEW.
*
"""

import os

import jigsawpy


def case_3_(src_path, dst_path):

    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        os.path.join(src_path, "bunny.msh")

    opts.jcfg_file = \
        os.path.join(dst_path, "bunny.jig")

    opts.mesh_file = \
        os.path.join(dst_path, "bunny.msh")

#------------------------------------ make mesh using JIGSAW

    jigsawpy.loadmsh(
        opts.geom_file, geom)

    print("Saving case_3a.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_3a.vtk"), geom)

    opts.mesh_kern = "delaunay"         # DELAUNAY kernel
    opts.mesh_dims = +2

    opts.optm_iter = +0

    opts.hfun_hmax = 0.03

    jigsawpy.cmd.jigsaw(opts, mesh)

    scr2 = jigsawpy.triscr2(            # "quality" metric
        mesh.point["coord"],
        mesh.tria3["index"])

    print("Saving case_3b.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_3b.vtk"), mesh)

#------------------------------------ make mesh using JIGSAW

    opts.mesh_kern = "delfront"         # DELFRONT kernel
    opts.mesh_dims = +2

    opts.optm_iter = +0

    opts.hfun_hmax = 0.03

    jigsawpy.cmd.jigsaw(opts, mesh)

    scr2 = jigsawpy.triscr2(            # "quality" metric
        mesh.point["coord"],
        mesh.tria3["index"])

    print("Saving case_3c.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_3c.vtk"), mesh)

    return



