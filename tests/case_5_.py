"""
* DEMO-5 --- Build planar meshes for the "airfoil" problem. 
* Impose non-uniform mesh-spacing constraints.
*
* These examples call to JIGSAW via its cmd.-line interface.
*
* Writes "case_5x.vtk" files on output for vis. in PARAVIEW.
*
"""

from pathlib import Path
import numpy as np

import jigsawpy

def case_5_(src_path,dst_path):

    opts = jigsawpy.jigsaw_jig_t()

    geom = jigsawpy.jigsaw_msh_t()
    mesh = jigsawpy.jigsaw_msh_t()
    hmat = jigsawpy.jigsaw_msh_t()

#------------------------------------ setup files for JIGSAW

    opts.geom_file = \
        str(Path(src_path)/"airfoil.msh") # GEOM file
        
    opts.jcfg_file = \
        str(Path(dst_path)/"airfoil.jig") # JCFG file
    
    opts.mesh_file = \
        str(Path(dst_path)/"airfoil.msh") # MESH file

    opts.hfun_file = \
        str(Path(dst_path)/"spacing.msh") # HFUN file
    
#------------------------------------ compute HFUN over GEOM 

    jigsawpy.loadmsh(opts.geom_file,geom)

    xgeo = geom.vert2["coord"][:,0]
    ygeo = geom.vert2["coord"][:,1]

    xpos = np.linspace( 
        xgeo.min(), xgeo.max(), 80)
                    
    ypos = np.linspace(
        ygeo.min(), ygeo.max(), 40)

    xmat, ymat = np.meshgrid(xpos, ypos)

    fun1 = +0.1*(xmat-.40)**2 + \
           +2.0*(ymat-.55)**2
   
    fun2 = +0.7*(xmat-.75)**2 + \
           +0.7*(ymat-.45)**2

    hfun = np.minimum(fun1,fun2)
    
    hmin = 0.01 ; hmax = 0.10 ;

    hfun = 0.4 * \
    np.maximum(np.minimum(hfun,hmax),hmin)
    
    hmat.mshID = "euclidean-grid"
    hmat.ndims = +2
    hmat.xgrid = np.array(xpos,
    dtype=jigsawpy.jigsaw_msh_t.REALS_t)
    hmat.ygrid = np.array(ypos,
    dtype=jigsawpy.jigsaw_msh_t.REALS_t)
    hmat.value = np.array(hfun,
    dtype=jigsawpy.jigsaw_msh_t.REALS_t)
    
    jigsawpy.savemsh(opts.hfun_file,hmat)

#------------------------------------ make mesh using JIGSAW

    opts.hfun_scal = "absolute"
    opts.hfun_hmax = float("inf")       # null HFUN limits
    opts.hfun_hmin = float(+0.00)

    opts.mesh_kern = "delfront"         # DELFRONT kernel
    opts.mesh_dims = +2

    opts.geom_feat = True
    opts.mesh_top1 = True
    
    jigsawpy.cmd.jigsaw(opts, mesh)

    print("Saving case_5a.vtk file.")

    jigsawpy.savevtk("case_5a.vtk",hmat)

    print("Saving case_5b.vtk file.")
    
    jigsawpy.savevtk("case_5b.vtk",mesh)

    return



