"""
* DEMO-7 --- Build surface meshes for the "wheel" geometry;
* defined as a collection of open surfaces.
*
* These examples call to JIGSAW via its api.-lib. interface.
*
* Writes "case_7x.vtk" files on output for vis. in PARAVIEW.
*
"""

import os

import jigsawpy


def case_7_(src_path, dst_path):

    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ make mesh using JIGSAW

    print("Call libJIGSAW: case 7a.")

    jigsawpy.loadmsh(os.path.join(
        src_path, "wheel.msh"), geom)

    opts.hfun_hmax = 0.03               # set HFUN limits

    opts.mesh_kern = "delfront"         # DELFRONT kernel
    opts.mesh_dims = +2

    opts.geom_feat = True
    opts.mesh_top1 = True
    opts.mesh_top2 = True

    jigsawpy.lib.jigsaw(opts, geom, mesh)

    print("Saving case_7a.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_7a.vtk"), geom)

    print("Saving case_7b.vtk file.")

    jigsawpy.savevtk(os.path.join(
        dst_path, "case_7b.vtk"), mesh)

    print("Saving case_7b.obj file.")
    jigsawpy.saveobj(os.path.join(
        dst_path, "case_7b.obj"), mesh)

    return
