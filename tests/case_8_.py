"""
* DEMO-8 --- re-mesh geometry generated using marching-cubes 
* reconstruction.
*
* These examples call to JIGSAW via its api.-lib. interface.
*
* Writes "case_8x.vtk" files on output for vis. in PARAVIEW.
*
"""

from pathlib import Path
import numpy as np

import jigsawpy

def case_8_(src_path,dst_path):

    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()

#------------------------------------ make mesh using JIGSAW

    print("Call libJIGSAW: case 8a.")

    geomfile = \
        str(Path(src_path)/"eight.msh")

    jigsawpy.loadmsh(geomfile,geom)

    opts.hfun_hmax = 0.04               # set HFUN limits
    
    opts.mesh_kern = "delfront"         # DELFRONT kernel
    opts.mesh_dims = +3
    
    jigsawpy.lib.jigsaw (opts,geom,mesh)

    print("Saving case_8a.vtk file.")

    jigsawpy.savevtk("case_8a.vtk",geom)

    print("Saving case_8b.vtk file.")

    jigsawpy.savevtk("case_8b.vtk",mesh)

    return



