"""
* DEMO-7 --- Build surface meshes for the "wheel" geometry;
* defined as a collection of open surfaces.
*
* These examples call to JIGSAW via its api.-lib. interface.
*
* Writes "case_7x.vtk" files on output for vis. in PARAVIEW.
*
"""

from pathlib import Path
import numpy as np

import jigsawpy

def case_7_(src_path,dst_path):

    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ make mesh using JIGSAW

    print("Call libJIGSAW: case 7a.")

    geomfile = \
        str(Path(src_path)/"wheel.msh")

    jigsawpy.loadmsh(geomfile,geom)

    opts.hfun_hmax = 0.03               # set HFUN limits
    
    opts.mesh_kern = "delfront"         # DELFRONT kernel
    opts.mesh_dims = +2

    opts.geom_feat = True
    opts.mesh_top1 = True
    opts.mesh_top2 = True
    
    jigsawpy.lib.jigsaw (opts,geom,mesh)

    print("Saving case_7a.vtk file.")

    jigsawpy.savevtk("case_7a.vtk",geom)

    print("Saving case_7b.vtk file.")

    jigsawpy.savevtk("case_7b.vtk",mesh)

    return



