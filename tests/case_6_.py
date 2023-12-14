"""
* DEMO-6 --- Build surface meshes for a mechanical bracket.
* Detect and preserve sharp-features in the input geometry.
*
* These examples call to JIGSAW via its cmd.-line interface.
*
* Writes "case_6x.vtk" files on output for vis. in PARAVIEW.
*
"""

import os

import jigsawpy


def case_6_(src_path, dst_path):

    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        os.path.join(src_path, "piece.msh")

    opts.jcfg_file = \
        os.path.join(dst_path, "piece.jig")

    opts.mesh_file = \
        os.path.join(dst_path, "piece.msh")

#------------------------------------ make mesh using JIGSAW

    jigsawpy.loadmsh(
        opts.geom_file, geom)

    print("Saving case_6a.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_6a.vtk"), geom)

    opts.hfun_hmax = 0.03               # set HFUN limits

    opts.mesh_kern = "delfront"         # DELFRONT kernel
    opts.mesh_dims = +2

    jigsawpy.cmd.jigsaw(opts, mesh)

    print("Saving case_6b.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_6b.vtk"), mesh)

#------------------------------------ make mesh using JIGSAW

    opts.hfun_hmax = 0.03               # set HFUN limits

    opts.mesh_kern = "delfront"         # DELFRONT kernel
    opts.mesh_dims = +2

    opts.geom_feat = True
    opts.mesh_top1 = True

    jigsawpy.cmd.jigsaw(opts, mesh)

    print("Saving case_6c.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_6c.vtk"), mesh)

    print("Saving case_6c.obj file.")

    jigsawpy.saveobj(os.path.join(
        dst_path, "case_6c.obj"), mesh)

    return
