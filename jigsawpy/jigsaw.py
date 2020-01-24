
import subprocess
import os,inspect
import shutil
import copy
import numpy as np

from pathlib import Path

from jigsawpy.tools.scorecard import trideg2, trideg3

from jigsawpy.bisect import bisect

from jigsawpy.jig_t import jigsaw_jig_t
from jigsawpy.msh_t import jigsaw_msh_t

from jigsawpy.loadmsh import loadmsh
from jigsawpy.savemsh import savemsh
from jigsawpy.savejig import savejig

def jigsaw(opts, mesh=None):
    """
    JIGSAW cmd-line interface to JIGSAW.

    JIGSAW(OPTS, MESH=None)

    Call the JIGSAW mesh generator using the config. options
    specified in the OPTS structure.

    OPTS is a user-defined set of meshing options. See JIG_t
    for details.

    """
    jexename = Path()

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (mesh is not None and \
        not isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    savejig(opts.jcfg_file, opts)

    if (jexename == Path()):
#---------------------------- set-up path for "local" binary

    #   stackoverflow.com/questions/2632199/
    #       how-do-i-get-the-
    #       path-of-the-current-executed-file-in-python
        filename = \
            inspect.getsourcefile(lambda:0)

        filepath = \
            Path(filename).resolve().parent

        if   (os.name ==    "nt"):
            jexename  = \
                filepath/"_bin"/"jigsaw.exe"

        elif (os.name == "posix"):
            jexename  = \
                filepath/"_bin"/"jigsaw"

        else:
            jexename  = Path ()

        if (not jexename.is_file()):
            jexename  = Path ()

    if (jexename == Path()):
#---------------------------- search machine path for binary
        jexescan = shutil.which("jigsaw")        

        if (jexescan is not None):        
            jexename  = Path ( jexescan )

    if (jexename != Path()):
#---------------------------- call JIGSAW and capture output
        subprocess.run( \
            [str(jexename), opts.jcfg_file], check = True)

        if mesh is not None: loadmsh(opts.mesh_file, mesh)

    else:

        raise Exception("JIGSAW's executable not found!!")

    return


def tripod(opts, tria=None):
    """
    TRIPOD cmd-line interface to TRIPOD.

    TRIPOD(OPTS, TRIA=None)

    Call the TRIPOD tessellation util. using the config. opt
    specified in the OPTS structure.

    OPTS is a user-defined set of meshing options. See JIG_t
    for details.

    """
    jexename = Path()

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (tria is not None and \
        not isinstance(tria, jigsaw_msh_t)):
        raise Exception("Incorrect type: TRIA.")

    savejig(opts.jcfg_file, opts)

    if (jexename == Path()):
#---------------------------- set-up path for "local" binary
        
    #   stackoverflow.com/questions/2632199/
    #       how-do-i-get-the-
    #       path-of-the-current-executed-file-in-python
        filename = \
            inspect.getsourcefile(lambda:0)

        filepath = \
            Path(filename).resolve().parent

        if   (os.name ==    "nt"):
            jexename  = \
                filepath/"_bin"/"tripod.exe"

        elif (os.name == "posix"):
            jexename  = \
                filepath/"_bin"/"tripod"

        else:
            jexename  = Path ()

        if (not jexename.is_file()):
            jexename  = Path ()

    if (jexename == Path()):
#---------------------------- search machine path for binary
        jexescan = shutil.which("tripod")        

        if (jexescan is not None):        
            jexename  = Path ( jexescan )

    if (jexename != Path()):
#---------------------------- call JIGSAW and capture output
        subprocess.run( \
            [str(jexename), opts.jcfg_file], check = True)

        if tria is not None: loadmsh(opts.mesh_file, tria)

    else:

        raise Exception("JIGSAW's executable not found!!")

    return


def marche(opts, ffun=None):
    """
    MARCHE cmd-line interface to MARCHE.

    MARCHE(OPTS, FFUN=None)

    Call the "fast-marching" solver MARCHE using the config. 
    options specified in the OPTS structure. MARCHE solves
    the Eikonal equations
 
    MAX(||dh/dx||, g) = g, 
 
    where g = g(x) is a gradient threshold applied to h. See 
    the SAVEMSH/LOADMSH functions for a description of the 
    HFUN output structure.

    OPTS is a user-defined set of meshing options. See JIG_t
    for details.

    """
    jexename = Path()

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (ffun is not None and \
        not isinstance(ffun, jigsaw_msh_t)):
        raise Exception("Incorrect type: FFUN.")

    savejig(opts.jcfg_file, opts)

    if (jexename == Path()):
#---------------------------- set-up path for "local" binary
        
    #   stackoverflow.com/questions/2632199/
    #       how-do-i-get-the-
    #       path-of-the-current-executed-file-in-python
        filename = \
            inspect.getsourcefile(lambda:0)

        filepath = \
            Path(filename).resolve().parent

        if   (os.name ==    "nt"):
            jexename  = \
                filepath/"_bin"/"marche.exe"

        elif (os.name == "posix"):
            jexename  = \
                filepath/"_bin"/"marche"

        else:
            jexename  = Path ()

        if (not jexename.is_file()):
            jexename  = Path ()

    if (jexename == Path()):
#---------------------------- search machine path for binary
        jexescan = shutil.which("marche")        

        if (jexescan is not None):        
            jexename  = Path ( jexescan )

    if (jexename != Path()):
#---------------------------- call JIGSAW and capture output
        subprocess.run( \
            [str(jexename), opts.jcfg_file], check = True)

        if ffun is not None: loadmsh(opts.hfun_file, ffun)

    else:

        raise Exception("JIGSAW's executable not found!!")

    return


def jitter(opts, imax, ibad, mesh=None):
    """
    JITTER call JIGSAW iteratively; try to improve topology.

    """

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (mesh is not None and \
        not isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    if (mesh is None):mesh = jigsaw_msh_t()

#--------- call JIGSAW iteratively; try to improve topology.
    OPTS = copy.copy (opts)

    for iter in range(imax):

        if (mesh.point is not None and
                mesh.point.size != +0):

            nvrt = mesh.point.size

            keep = np.full(
                (nvrt), True, dtype=bool)

    #------------------------------ setup initial conditions
            path = Path(opts.mesh_file).parent
            name = Path(opts.mesh_file).stem
            fext = Path(opts.mesh_file).suffix

            name = str(name)
            fext = str(fext)
            name = name + "-INIT" + fext

            OPTS.init_file = str(path / name)

            if (mesh.tria3 is not None and 
                    mesh.tria3.size != +0):

    #------------------------------ mark any irregular nodes
                vdeg = trideg2(
                    mesh.point["coord"], 
                        mesh.tria3["index"])

                ierr = np.abs(vdeg - 6) # err. in topo. deg. 

                M = np.sum(ierr[
                mesh.tria3["index"]], axis=1) >= ibad
    

                keep[mesh.tria3["index"][M,:]] = False

            if (mesh.edge2 is not None and 
                    mesh.edge2.size != +0):

                keep[mesh.edge2["index"][:,:]] = True

    #------------------------------ don't delete everything!
            if (np.count_nonzero(keep) <= +8):

                keep = np.full(
                    (nvrt), True, dtype=bool)

    #------------------------------ keep nodes far from seam
            init = jigsaw_msh_t()            
            init.point = mesh.point[keep]

            savemsh(OPTS.init_file, init)

    #------------------------------ call JIGSAW with new ICs
        jigsaw (OPTS, mesh)

    return


def attach(mesh):
    """
    ATTACH mark points attached to the underlying geom. rep.

    """

    if (mesh.tria4 is not None and
            mesh.tria4.size != +0):

        mesh.point["IDtag"][mesh.tria4["index"]] = 3

    if (mesh.tria3 is not None and
            mesh.tria3.size != +0):

        mesh.point["IDtag"][mesh.tria3["index"]] = 2

    if (mesh.edge2 is not None and
            mesh.edge2.size != +0):

        mesh.point["IDtag"][mesh.edge2["index"]] = 1

    return


def tetris(opts, nlev, mesh=None):
    """
    TETRIS generate a mesh using an inc. bisection strategy.

    """

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (mesh is not None and \
        not isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

#---------------------------- call JIGSAW via inc. bisection
    SCAL = +2. ** nlev

    OPTS = copy.copy (opts)

    while (nlev >= +0):
    
        if (opts.optm_qlim is not None):
    
    #------------------------ create/write current QLIM data
            FACT = max(0.50, 1.00 
                - np.sqrt(nlev) * 0.10)

            OPTS.optm_qlim = \
                opts.optm_qlim * FACT

        else:               # no QLIM specified => defaults!
   
            FACT = max(0.50, 1.00 
                - np.sqrt(nlev) * 0.10)
            
            OPTS.optm_qlim = \
                    +9.375E-01 * FACT

        if (opts.optm_qtol is not None):

    #------------------------ create/write current QTOL data

            OPTS.optm_qtol = \
                opts.optm_qtol*(nlev+1)

        else:               # no QTOL specified => defaults!

            OPTS.optm_qtol = \
                    +1.00E-004*(nlev+1)

        if (opts.optm_dual is not None):
        
    #------------------------ create/write current DUAL data
            OPTS.optm_dual = nlev == 0

        if (opts.hfun_hmax is not None):
        
    #------------------------ create/write current HMAX data
            OPTS.hfun_hmax = \
                opts.hfun_hmax * SCAL
        
        if (opts.hfun_hmin is not None):
        
    #------------------------ create/write current HMIN data
            OPTS.hfun_hmin = \
                opts.hfun_hmin * SCAL

        if (opts.hfun_file is not None):

    #------------------------ create/write current HFUN data
            path = Path(opts.hfun_file).parent
            name = Path(opts.hfun_file).stem
            fext = Path(opts.hfun_file).suffix

            name = str(name)
            fext = str(fext)
            
            OPTS.hfun_file = str(
            path / name + "-ITER" + fext)

            HFUN = jigsaw_msh_t()

            loadmsh(opts.hfun_file, HFUN)
        
            HFUN.value = HFUN.value*SCAL

            savemsh(OPTS.hfun_file, HFUN)

    #------------------------ call JIGSAW kernel at this lev
        if (nlev >= +1):

            jitter(OPTS, 2**(nlev+1), 1, mesh)

        else:

            jitter(OPTS, 2**(nlev+1), 1, mesh)

        nlev = nlev - 1
        SCAL = SCAL / 2.

        if (nlev < +0): done = True; break

        if (opts.init_file is not None):

    #------------------------ create/write current INIT data
            path = Path(opts.init_file).parent
            name = Path(opts.init_file).stem
            fext = Path(opts.init_file).suffix

            name = str(name)
            fext = str(fext)
            
            OPTS.init_file = str(
            path / name + "-ITER" + fext)

            bisect(mesh)
            attach(mesh)
        
            savemsh(OPTS.init_file, mesh)

        else:

    #------------------------ create/write current INIT data
            path = Path(opts.mesh_file).parent
            name = Path(opts.mesh_file).stem
            fext = Path(opts.mesh_file).suffix

            name = str(name)
            fext = str(fext)
            
            OPTS.init_file = str(
            path / name + "-ITER" + fext)

            bisect(mesh)
            attach(mesh)
        
            savemsh(OPTS.init_file, mesh)

    return 



